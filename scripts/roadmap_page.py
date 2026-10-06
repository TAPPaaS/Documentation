"""Build the website's Roadmap page from TAPPaaS's ROADMAP.md.

ROADMAP.md (TAPPaaS repository root) is the one plan: the open waves, latest first, then the
releases, newest first. This page is a view of it, generated at every site build by
scripts/sync-source.py — never edited by hand:

  - one timeline card per wave and per release, in ROADMAP.md's order;
  - a wave card says what the wave is for and how far along it is; a release card when it
    shipped, its tag, and what it delivered;
  - "+" on a card opens its groups: each group's headline and intent, and its issues linked to
    Codeberg — open, done (ticked), or done and waiting for the next release.

The parser reads only what ROADMAP.md's own reading guide promises: `## Wave N — title`,
`### Gx.y title — … · counts` (`####` inside a release), the group's first paragraph, and
issue rows `| (✅ )?(FW )?#N | title | … |`. Anything it cannot read fails the build rather than
publishing a half-empty page.
"""

import html
import re

FORGE_REPO = "https://codeberg.org/TAPPaaS/TAPPaaS"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

ROW_RE = re.compile(r"^\| (✅ )?(?:FW )?#(\d+) \| (.*?) \|")
GROUP_RE = re.compile(r"^#{3,4} (✅ )?(G\d\.\d) (.*)$")
WAVE_RE = re.compile(r"^## Wave (\d) — (.*)$")
RELEASE_RE = re.compile(r"^## Release (\S+) — (.*)$")


# ── Markdown → HTML, just enough for ROADMAP.md's prose and titles ──────────────────────
def inline(md):
    """`code`, **bold**, *italic*, [text](url), #N — escaped, everything else as text."""
    out, pos = [], 0
    token = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\*([^*\s][^*]*?)\*|\[([^\]]+)\]\(<?([^)>]+)>?\)|(?<![\w&/#])#(\d{1,5})(?![\w-])")
    for m in token.finditer(md):
        out.append(html.escape(md[pos:m.start()]))
        code, bold, ital, ltext, lurl, issue = m.groups()
        if code is not None:
            out.append("<code>{}</code>".format(html.escape(code)))
        elif bold is not None:
            out.append("<strong>{}</strong>".format(inline(bold)))
        elif ital is not None:
            out.append("<em>{}</em>".format(inline(ital)))
        elif ltext is not None:
            out.append('<a href="{}">{}</a>'.format(html.escape(link(lurl)), inline(ltext)))
        else:
            out.append('<a href="{}/issues/{}">#{}</a>'.format(FORGE_REPO, issue, issue))
        pos = m.end()
    out.append(html.escape(md[pos:]))
    return "".join(out)


def link(url):
    """A link in ROADMAP.md is relative to the TAPPaaS repository root; on the site it points
    at the file on Codeberg. Anchors inside ROADMAP.md point at ROADMAP.md itself."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", url):
        return url
    if url.startswith("#"):
        return "{}/src/branch/main/ROADMAP.md{}".format(FORGE_REPO, url)
    return "{}/src/branch/main/{}".format(FORGE_REPO, url)


def first_paragraph(lines):
    """The first block of prose lines (not a heading, table or anchor), joined."""
    para = []
    for l in lines:
        if not l.strip():
            if para:
                break
            continue
        if l.startswith(("|", "#", "<a id=", "---")):
            if para:
                break
            continue
        para.append(l.strip())
    return " ".join(para)


def paragraphs(lines):
    out, para = [], []
    for l in lines + [""]:
        if not l.strip() or l.startswith(("|", "#", "<a id=", "---")):
            if para:
                out.append(" ".join(para))
                para = []
            continue
        para.append(l.strip())
    return out


def date_label(text):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if not m:
        return ""
    y, mo, d = m.groups()
    return "{} {} {}".format(int(d), MONTHS[int(mo) - 1], y)


# ── Parsing ─────────────────────────────────────────────────────────────────────────────
def sections(lines):
    """Top-level `## ` sections as (heading, body lines)."""
    out, cur = [], None
    for l in lines:
        if l.startswith("## "):
            cur = (l, [])
            out.append(cur)
        elif cur is not None:
            cur[1].append(l)
    return out


def groups(body):
    """Groups inside a wave or release body: id, title, scores/counts, intent, issues."""
    out, cur = [], None
    for l in body:
        m = GROUP_RE.match(l)
        if m:
            done, gid, rest = m.groups()
            title, _, meta = rest.partition(" — ")
            if not meta and " · " in title:          # `### G0.4 Merge trust · released in 2.1`
                title, _, meta = title.partition(" · ")
            cur = {"id": gid, "title": title.strip(), "meta": meta.strip(), "done": bool(done),
                   "lines": [], "issues": []}
            out.append(cur)
            continue
        if l.startswith("### ") or l.startswith("## "):   # a release's `### Wave N` heading
            cur = None
            continue
        if cur is None:
            continue
        r = ROW_RE.match(l)
        if r:
            cur["issues"].append({"done": bool(r.group(1)), "num": r.group(2), "title": r.group(3)})
        cur["lines"].append(l)
    for g in out:
        g["intent"] = first_paragraph(g["lines"])
    return out


def parse(text):
    lines = text.split("\n")
    waves, releases = [], []
    for head, body in sections(lines):
        m = WAVE_RE.match(head)
        if m:
            waves.append({"n": int(m.group(1)), "title": m.group(2).strip(),
                          "intent": first_paragraph(body), "groups": groups(body)})
            continue
        m = RELEASE_RE.match(head)
        if m:
            version, when = m.groups()
            gs = groups(body)
            cut = next((i for i, l in enumerate(body) if l.startswith("### ")), len(body))
            prose = paragraphs(body[:cut])
            releases.append({"version": version, "when": when, "groups": gs, "prose": prose})
    if not waves and not releases:
        raise ValueError("ROADMAP.md: no `## Wave N — …` or `## Release X — …` section found")
    for r in releases:
        if not r["groups"] and not r["prose"]:
            raise ValueError("ROADMAP.md: release {} has neither groups nor a summary".format(r["version"]))
    return waves, releases


# ── Rendering ───────────────────────────────────────────────────────────────────────────
def issue_li(i, next_release):
    """One issue: ticked when done; a done row still in a wave ships with the next release."""
    cls = "done" if i["done"] else "open"
    tag = ' <span class="tap-rm__next">{}</span>'.format(next_release) if i.get("pending") else ""
    return ('<li class="tap-rm__issue tap-rm__issue--{}"><a href="{}/issues/{}">#{}</a> {}{}</li>'
            .format(cls, FORGE_REPO, i["num"], i["num"], inline(i["title"]), tag))


def group_html(g, next_release, in_wave):
    for i in g["issues"]:
        i["pending"] = in_wave and i["done"]
    issues = "".join(issue_li(i, next_release) for i in g["issues"])
    intent = '<p class="tap-rm__intent">{}</p>'.format(inline(g["intent"])) if g["intent"] else ""
    return ('<div class="tap-rm__group"><p class="tap-rm__gtitle">{}{} {}</p>{}<ul class="tap-rm__issues">{}</ul></div>'
            .format("✓ " if g["done"] else "", html.escape(g["id"]), inline(g["title"]), intent, issues))


def counts(gs):
    done = pending = open_ = 0
    for g in gs:
        for i in g["issues"]:
            if not i["done"]:
                open_ += 1
            else:
                pending += 1
    return pending, open_


def card(kind, when, title, text, tag_html, more_html, more_label):
    more = ""
    if more_html:
        more = ('<details class="tap-rm__more"><summary><span class="tap-rm__plus" aria-hidden="true"></span>{}</summary>{}</details>'
                .format(html.escape(more_label), more_html))
    return ('<div class="tap-rm tap-rm--{}">\n  <div class="tap-rm__when">{}</div>\n  <div class="tap-rm__card">\n'
            '    <p class="tap-rm__title">{}</p>\n    <p>{}</p>\n    {}\n    {}\n  </div>\n</div>\n'
            .format(kind, when, title, text, tag_html, more))


def build(text):
    waves, releases = parse(text)
    next_release = "next release"
    if releases:
        m = re.match(r"(\d+)\.(\d+)", releases[0]["version"])
        if m:
            next_release = "{}.{}".format(m.group(1), int(m.group(2)) + 1)
    cards = []
    for w in waves:
        pending, open_ = counts(w["groups"])
        kind = "now" if pending else "soon"
        ng = len(w["groups"])
        tags = '<span class="tap-rm__tag">{} group{}</span> <span class="tap-rm__tag">{} open</span>'.format(
            ng, "" if ng == 1 else "s", open_)
        if pending:
            tags += ' <span class="tap-rm__tag">{} done for {}</span>'.format(pending, next_release)
        more = "".join(group_html(g, next_release, True) for g in w["groups"])
        cards.append(card(kind, "Wave {}".format(w["n"]), inline(w["title"][:1].upper() + w["title"][1:]),
                          inline(w["intent"]), tags, more, "Groups and issues"))
    for r in releases:
        version = r["version"]
        tagname = "v" + version
        tag = '<a class="tap-rm__tag" href="{}/releases/tag/{}">{}</a>'.format(FORGE_REPO, tagname, tagname)
        if "production" in r["when"] and not re.search(r"production \d{4}-", r["when"]):
            tag += ' <span class="tap-rm__tag">in staging</span>'
        summary = r["prose"]
        # The card shows one sentence: the first of the first paragraph that is not the tag line.
        body = [p for p in summary if not p.startswith("Tag `")]
        lead = re.sub(r"^What it delivered:\s*", "", body[0]) if body else ""
        lead = re.split(r"(?<=[.;])\s+(?=\*\*|[A-Z])", re.sub(r"^\*\*[^*]+\.\*\*\s*", "", lead), 1)[0]
        more = "".join("<p>{}</p>".format(inline(p)) for p in summary)
        if r["groups"]:
            more += "".join(group_html(g, next_release, False) for g in r["groups"])
        label = "What it carried, by group" if r["groups"] else "What it delivered"
        cards.append(card("release", date_label(r["when"]), "TAPPaaS {}".format(html.escape(version)),
                          inline(lead), tag, more, label))
    return PAGE.format(cards="\n".join(cards), repo=FORGE_REPO)


PAGE = """---
title: Roadmap
description: >
  What TAPPaaS is building, in the order we build it, and what each release has delivered.
---

<!--
  GENERATED FROM SOURCE - do not edit here.
  Built at every site build by scripts/roadmap_page.py from ROADMAP.md in TAPPaaS/TAPPaaS
  ({repo}/src/branch/main/ROADMAP.md). Change the roadmap there.
-->

# Roadmap

What we are building, in the order we build it, and what each release has delivered — the open
work at the top, the releases below it.

**The current plan is security and stability.** It is built in waves: first make upgrades safe,
then make the breaking changes while few sites depend on today's shapes, then harden the network,
then stability, then new capabilities. A filled marker means work in the wave is done and waits
for the next release; a hollow one, nothing in it is done yet. Every two weeks the next version is
cut for staging and reaches production two weeks later. Press **+** on a card for its groups and
their issues.

<div class="tap-roadmap">

{cards}
</div>

## How we plan

- **The order comes from one plan**, [ROADMAP.md]({repo}/src/branch/main/ROADMAP.md) in the
  source repository: every open issue in a wave and a group, why they come in that order, and what
  each release carried. This page is built from it.
- **Which version reached which channel, and when**, is in
  [RELEASES.md]({repo}/src/branch/main/RELEASES.md).
- **Decisions are written down first**, as
  [ADRs in the source repository]({repo}/src/branch/main/docs/ADR).
- **The details live on Codeberg**: [milestones]({repo}/milestones) and
  [issues]({repo}/issues). To influence the direction, see [Contributing](../community/contributing.md).
"""
