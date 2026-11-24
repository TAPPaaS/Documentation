"""Build the website's Roadmap page from the TAPPaaS roadmap.

The roadmap is the one plan: the open waves, latest first, then the releases, newest first. Until
the self-hosting cut-over it is ROADMAP.md at the TAPPaaS repository root; from then on it lives in
Vikunja and its published copy is generated into this repository, roadmap/ROADMAP.public.md
(TAPPaaS release/roadmap-generate.py --public; BUILD.md, *The roadmap*). The two have the same
layout. This page is a view of it, generated at every site build by scripts/sync-source.py —
never edited by hand:

  - one timeline card per wave and per release, in ROADMAP.md's order;
  - a wave card says what the wave is for and how far along it is; a release card when it
    shipped, its tag, and what it delivered;
  - "+" on a card opens its groups: each group's headline and intent, and its issues — open,
    done (ticked), or done and waiting for the next release.

Issue links: `Roadmap#N` (the published copy's open rows) goes to the public list on the forge,
ROADMAP_PUBLIC_REPO (TAPPAAS_ROADMAP_PUBLIC_REPO, default forgejo.tappaas.org's TAPPaaS/Roadmap);
`#N` (released rows, and every row of ROADMAP.md) to Codeberg's TAPPaaS/TAPPaaS issue, and
`<Repo>#N` to Codeberg's TAPPaaS/<Repo> — ROADMAP_ARCHIVE_ORG (TAPPAAS_ROADMAP_ARCHIVE_ORG,
default codeberg.org/TAPPaaS). Codeberg's issues are read-only history after the cut-over.

The parser reads only what ROADMAP.md's own reading guide promises: `## Wave N — title`,
`### Gx.y title — … · counts` (`####` inside a release), the group's first paragraph, and
issue rows `| (✅ )?(FW )?(<Repo>)?#N | title | … |`. Anything it cannot read fails the build rather than
publishing a half-empty page.
"""

import html
import os
import re

FORGE_REPO = "https://codeberg.org/TAPPaaS/TAPPaaS"
ROADMAP_PUBLIC_REPO = os.environ.get("TAPPAAS_ROADMAP_PUBLIC_REPO", "https://forgejo.tappaas.org/TAPPaaS/Roadmap").rstrip("/")
ROADMAP_ARCHIVE_ORG = os.environ.get("TAPPAAS_ROADMAP_ARCHIVE_ORG", "https://codeberg.org/TAPPaaS").rstrip("/")
PUBLIC_LIST = "Roadmap"            # the repo name a published row cites: Roadmap#N

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

ROW_RE = re.compile(r"^\| (✅ )?(?:FW )?([A-Za-z0-9_.-]+)?#(\d+) \| (.*?) \|")
GROUP_RE = re.compile(r"^#{3,4} (✅ )?(G\d\.\d) (.*)$")
WAVE_RE = re.compile(r"^## Wave (\d) — (.*)$")
RELEASE_RE = re.compile(r"^## Release (\S+) — (.*)$")


def issue_url(repo, num):
    """Where an issue reference points: Roadmap#N the public list, #N and <Repo>#N Codeberg."""
    if repo == PUBLIC_LIST:
        return "{}/issues/{}".format(ROADMAP_PUBLIC_REPO, num)
    return "{}/{}/issues/{}".format(ROADMAP_ARCHIVE_ORG, repo or "TAPPaaS", num)


def issue_link(repo, num):
    return '<a href="{}">{}#{}</a>'.format(html.escape(issue_url(repo, num)), html.escape(repo or ""), num)


# ── Markdown → HTML, just enough for ROADMAP.md's prose and titles ──────────────────────
def inline(md):
    """`code`, **bold**, *italic*, [text](url), #N, Roadmap#N — escaped, everything else as text."""
    out, pos = [], 0
    token = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\*([^*\s][^*]*?)\*|\[([^\]]+)\]\(<?([^)>]+)>?\)"
                       r"|(?<![\w&/#])([A-Z][A-Za-z0-9_.-]*)?#(\d{1,5})(?![\w-])")
    for m in token.finditer(md):
        out.append(html.escape(md[pos:m.start()]))
        code, bold, ital, ltext, lurl, repo, issue = m.groups()
        if code is not None:
            out.append("<code>{}</code>".format(html.escape(code)))
        elif bold is not None:
            out.append("<strong>{}</strong>".format(inline(bold)))
        elif ital is not None:
            out.append("<em>{}</em>".format(inline(ital)))
        elif ltext is not None:
            out.append('<a href="{}">{}</a>'.format(html.escape(link(lurl)), inline(ltext)))
        else:
            out.append(issue_link(repo, issue))
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
            cur["issues"].append({"done": bool(r.group(1)), "repo": r.group(2) or "", "num": r.group(3),
                                  "title": r.group(4)})
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
    return ('<li class="tap-rm__issue tap-rm__issue--{}">{} {}{}</li>'
            .format(cls, issue_link(i.get("repo", ""), i["num"]), inline(i["title"]), tag))


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


def build(text, published=False):
    """The page; published=True for the copy generated from Vikunja (the plan's wording)."""
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
    return PAGE.format(cards="\n".join(cards), repo=FORGE_REPO,
                       source=SOURCE_PUBLISHED if published else SOURCE_FILE.format(repo=FORGE_REPO),
                       plan=PLAN_PUBLISHED.format(public=ROADMAP_PUBLIC_REPO) if published
                       else PLAN_FILE.format(repo=FORGE_REPO),
                       details=DETAILS_PUBLISHED.format(public=ROADMAP_PUBLIC_REPO, archive=ROADMAP_ARCHIVE_ORG)
                       if published else DETAILS_FILE.format(repo=FORGE_REPO))


SOURCE_FILE = "ROADMAP.md in TAPPaaS/TAPPaaS\n  ({repo}/src/branch/main/ROADMAP.md). Change the roadmap there."
SOURCE_PUBLISHED = ("roadmap/ROADMAP.public.md in this repository, the published copy of the roadmap in\n"
                    "  the project's Vikunja (TAPPaaS release/roadmap-generate.py --public). Change the roadmap there.")
PLAN_FILE = ("- **The order comes from one plan**, [ROADMAP.md]({repo}/src/branch/main/ROADMAP.md) in the\n"
             "  source repository: every open issue in a wave and a group, why they come in that order, and what\n"
             "  each release carried. This page is built from it.")
PLAN_PUBLISHED = ("- **The order comes from one plan**, kept in the project's backlog and published here: every open\n"
                  "  item in a wave and a group, and what each release carried. Each open item is an issue in the\n"
                  "  [public roadmap list]({public}/issues); security work is planned too, but not listed.")
DETAILS_FILE = ("- **The details live on Codeberg**: [milestones]({repo}/milestones) and\n"
                "  [issues]({repo}/issues). To influence the direction, see [Contributing](../community/contributing.md).")
DETAILS_PUBLISHED = ("- **The details**: open items link to the [public roadmap list]({public}/issues); released items\n"
                     "  to their issues on [Codeberg]({archive}/TAPPaaS/issues), kept as history. To report something\n"
                     "  or influence the direction, see [Contributing](../community/contributing.md).")


PAGE = """---
title: Roadmap
description: >
  What TAPPaaS is building, in the order we build it, and what each release has delivered.
---

<!--
  GENERATED FROM SOURCE - do not edit here.
  Built at every site build by scripts/roadmap_page.py from {source}
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

{plan}
- **Which version reached which channel, and when**, is in
  [RELEASES.md]({repo}/src/branch/main/RELEASES.md).
- **Decisions are written down first**, as
  [ADRs in the source repository]({repo}/src/branch/main/docs/ADR).
{details}
"""
