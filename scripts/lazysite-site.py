#!/usr/bin/env python3
"""Spike: turn the MkDocs source tree into a lazysite site (TAPPaaS docs on lazysite).

Run after scripts/sync-source.py (which fills docs/generated, docs/stacks, the
SUMMARY.md files and the roadmap page). Writes a lazysite content tree to OUT:

  - every docs/**/*.md as a lazysite page at the same path (a/b.md -> /a/b,
    a/index.md -> /a/), front matter reduced to `title:`;
  - the Markdown normalised for Text::MultiMarkdown, lazysite's renderer:
      relative .md links -> the page's clean URL; images -> site-absolute;
      a GitHub-style anchor on every heading; a blank line before a list that
      follows a paragraph; `\\|` in a table cell -> &#124;; task lists -> ☐/☑;
      bare URLs -> <url>; MkDocs admonitions -> `::: note` boxes; Material
      icons and attribute lists removed;
  - assets/tappaas/nav.json (the whole navigation tree, from mkdocs.yml's nav
    and the SUMMARY.md files) and assets/tappaas/search.json (full text);
  - the layout under lazysite/ (copied from lazysite-layout/).

Usage: python3 scripts/lazysite-site.py OUT
"""

import json
import os
import posixpath
import re
import shutil
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
LAYOUT_SRC = os.path.join(ROOT, "lazysite-layout")
SKIP_DIRS = {"includes", "javascripts", "stylesheets"}
ASSET_EXT = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf"}

STATS = {k: 0 for k in ("pages", "links_rewritten", "links_unresolved", "anchors", "list_blank",
                        "pipes", "tasks", "table_blank", "after_table", "bare_urls", "admonitions", "icons", "attr_lists",
                        "kroki_fences", "mermaid_fences")}
UNRESOLVED = []


# ---------------------------------------------------------------- URLs

def page_url(rel):
    """docs-relative .md path -> the URL lazysite serves it at."""
    rel = rel[:-3]
    if rel == "index":
        return "/"
    if rel.endswith("/index"):
        return "/" + rel[: -len("index")]
    return "/" + rel


# ---------------------------------------------------------------- slugs

def slugify(text, seen):
    """GitHub/MkDocs-style heading id: lower case, punctuation dropped, spaces -> '-'."""
    t = re.sub(r"<[^>]+>", "", text)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)   # link text only
    t = t.replace("`", "").lower().strip()
    t = re.sub(r"[^\w\- ]", "", t)
    t = re.sub(r" ", "-", t)
    base, n = t, 1
    while t in seen:
        t = "{}_{}".format(base, n)
        n += 1
    seen.add(t)
    return t


# ---------------------------------------------------------------- normalise

LINK_RE = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*(?:<([^>]+)>|([^)\s]+))((?:\s+\"[^\"]*\")?)\s*\)")
LIST_RE = re.compile(r"^\s{0,3}([-*+]|\d+[.)])\s")
TASK_RE = re.compile(r"^(\s*[-*+]\s)\[([ xX])\]\s")
BARE_URL_RE = re.compile(r"(?<![(<\[\"'=`])\bhttps?://[^\s)<>`\]]+[^\s)<>`\].,;:!?'\"]")
ICON_RE = re.compile(r":(?:material|fontawesome|octicons|simple)-[a-z0-9-]+:(?:\{[^}]*\})?")
ATTR_RE = re.compile(r"\{:?\s*(?:[.#][\w-]+\s*|[\w-]+=\"[^\"]*\"\s*)+\}")
CODE_SPAN_RE = re.compile(r"(`+).+?\1")


def outside_code(line, fn):
    """Apply fn to the parts of a line that are not code spans."""
    out, last = [], 0
    for m in CODE_SPAN_RE.finditer(line):
        out.append(fn(line[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(fn(line[last:]))
    return "".join(out)


def rewrite_link(m, page_rel, pages):
    bang, text, angled, plain, title = m.groups()
    target = angled or plain
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
        return m.group(0)
    path, _, frag = target.partition("#")
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(page_rel), path))
    if bang or os.path.splitext(path)[1].lower() in ASSET_EXT:
        return "{}[{}](/{}{})".format(bang, text, resolved, title)
    if resolved.endswith("/"):
        resolved += "index.md"
    if not resolved.endswith(".md") and resolved + "/index.md" in pages:
        resolved += "/index.md"
    if resolved in pages:
        STATS["links_rewritten"] += 1
        return "[{}]({}{}{})".format(text, page_url(resolved), "#" + frag if frag else "", title)
    STATS["links_unresolved"] += 1
    UNRESOLVED.append((page_rel, target))
    return m.group(0)


def normalise(body, page_rel, pages):
    lines = body.split("\n")
    out, fence, seen, prev = [], None, set(), ""
    i = 0
    while i < len(lines):
        line = lines[i]
        fm = re.match(r"^\s*(```+|~~~+)\s*([\w-]*)", line)
        if fence:
            if fm and fm.group(1)[0] == fence[0] and len(fm.group(1)) >= len(fence):
                fence = None
            out.append(line)
            i += 1
            continue
        if fm:
            fence = fm.group(1)
            lang = fm.group(2)
            if lang == "mermaid":
                STATS["mermaid_fences"] += 1
            elif lang.startswith("kroki") or lang in ("plantuml", "blockdiag", "seqdiag", "graphviz", "dot", "d2", "bpmn", "c4plantuml"):
                STATS["kroki_fences"] += 1
            if prev.strip() and not prev.startswith((" ", "\t")):
                out.append("")
            out.append(line)
            prev = line
            i += 1
            continue

        # MkDocs admonition: !!! type "Title" + 4-space indented body
        am = re.match(r'^(!!!|\?\?\?\+?)\s+(\w+)(?:\s+"([^"]*)")?\s*$', line)
        if am:
            STATS["admonitions"] += 1
            kind, title = am.group(2), am.group(3)
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                block.append(lines[i][4:] if lines[i].startswith("    ") else "")
                i += 1
            while block and not block[-1].strip():
                block.pop()
            out += ["", "::: admonition-" + kind.lower()]
            if title:
                out += ["**{}**".format(title), ""]
            out += [normalise_inline(b, page_rel, pages) for b in block]
            out += [":::", ""]
            prev = ""
            continue

        # headings: GitHub-style anchor
        hm = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if hm:
            slug = slugify(hm.group(2), seen)
            STATS["anchors"] += 1
            text = normalise_inline(hm.group(2), page_rel, pages)
            line = '{} <a id="{}"></a>{}'.format(hm.group(1), slug, text)
            out.append(line)
            prev = line
            i += 1
            continue

        # MultiMarkdown takes the blank line after a table into the table, so what
        # follows a table (a list, above all) needs two
        if prev.lstrip().startswith("|") and not line.lstrip().startswith("|"):
            out += [""] if not line.strip() else ["", ""]
            STATS["after_table"] += 1

        # a list straight after a paragraph line or a table needs a blank line
        if LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev) \
                and not prev.startswith((" ", "\t", "#", "<", ">", ":::")):
            out.append("")
            STATS["list_blank"] += 1

        # a table straight after a paragraph line needs a blank line
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.lstrip().startswith("|") and re.match(r"^\s*\|?\s*:?-{2,}", nxt) \
                and prev.strip() and not prev.lstrip().startswith("|"):
            out.append("")
            STATS["table_blank"] += 1

        tm = TASK_RE.match(line)
        if tm:
            STATS["tasks"] += 1
            line = tm.group(1) + ("☑ " if tm.group(2) in "xX" else "☐ ") + line[tm.end():]

        if line.lstrip().startswith("|") and "\\|" in line:
            STATS["pipes"] += line.count("\\|")
            line = line.replace("\\|", "&#124;")

        line = normalise_inline(line, page_rel, pages)
        out.append(line)
        prev = line
        i += 1
    return "\n".join(out)


def normalise_inline(line, page_rel, pages):
    # links first, on the whole line (their text may hold a code span), but not a
    # link that sits inside a code span
    spans = [m.span() for m in CODE_SPAN_RE.finditer(line)]

    def link(m):
        if any(a <= m.start() < b for a, b in spans):
            return m.group(0)
        return rewrite_link(m, page_rel, pages)
    line = LINK_RE.sub(link, line)

    def fix(seg):
        n = len(ICON_RE.findall(seg))
        if n:
            STATS["icons"] += n
            seg = ICON_RE.sub("", seg)
        n = len(ATTR_RE.findall(seg))
        if n:
            STATS["attr_lists"] += n
            seg = ATTR_RE.sub("", seg)

        def bare(m):
            STATS["bare_urls"] += 1
            return "<{}>".format(m.group(0))
        # bare URLs, but not inside an existing link's target or text
        parts, last = [], 0
        for lm in re.finditer(r"!?\[[^\]]*\]\([^)]*\)|<[^>\n]+>", seg):
            parts.append(BARE_URL_RE.sub(bare, seg[last:lm.start()]))
            parts.append(lm.group(0))
            last = lm.end()
        parts.append(BARE_URL_RE.sub(bare, seg[last:]))
        return "".join(parts)
    return outside_code(line, fix)


# ---------------------------------------------------------------- front matter

def split_front_matter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            meta = yaml.safe_load(text[4:end]) or {}
            return meta, text[end + 4:].lstrip("\n")
    return {}, text


def first_h1(body):
    m = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    return m.group(1) if m else None


# ---------------------------------------------------------------- nav

class Loader(yaml.SafeLoader):
    pass


Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda l, s, n: None)
Loader.add_multi_constructor("!", lambda l, s, n: None)


def summary_tree(dir_rel):
    """A literate-nav SUMMARY.md -> [{label, url?, children}]."""
    path = os.path.join(DOCS, dir_rel, "SUMMARY.md")
    root = []
    stack = [(-1, root)]
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip())
            item = line.strip().lstrip("*-").strip()
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", item)
            node = {"label": m.group(1) if m else item, "children": []}
            if m:
                node["url"] = page_url(posixpath.normpath(posixpath.join(dir_rel, m.group(2))))
            while stack[-1][0] >= indent:
                stack.pop()
            stack[-1][1].append(node)
            stack.append((indent, node["children"]))
    return root


def nav_tree(entries):
    out = []
    for e in entries:
        (label, val), = e.items() if isinstance(e, dict) else (("", e),)
        if isinstance(val, list):
            out.append({"label": label, "children": nav_tree(val)})
        elif isinstance(val, str) and val.endswith("/"):
            out.append({"label": label, "children": summary_tree(val.rstrip("/"))})
        else:
            out.append({"label": label, "url": page_url(val), "children": []})
    return out


# ---------------------------------------------------------------- search

def plain_text(md):
    t = re.sub(r"```.*?```", " ", md, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[#*_`|>:-]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


# ---------------------------------------------------------------- main

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out_dir = os.path.abspath(sys.argv[1])
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    pages = set()
    assets = []
    for root, dirs, files in os.walk(DOCS):
        rel_root = os.path.relpath(root, DOCS)
        if rel_root.split(os.sep)[0] in SKIP_DIRS:
            dirs[:] = []
            continue
        for fn in files:
            rel = os.path.normpath(os.path.join(rel_root, fn)).replace(os.sep, "/")
            if fn.endswith(".md") and fn != "SUMMARY.md":
                pages.add(rel)
            elif os.path.splitext(fn)[1].lower() in ASSET_EXT:
                assets.append(rel)

    search = []
    for rel in sorted(pages):
        with open(os.path.join(DOCS, rel), encoding="utf-8") as fh:
            meta, body = split_front_matter(fh.read())
        title = str(meta.get("title") or first_h1(body) or rel)
        if rel == "index.md":
            body = open(os.path.join(ROOT, "lazysite-layout", "home.md"), encoding="utf-8").read()
        elif not first_h1(body):
            body = "# {}\n\n{}".format(title, body)
        text = normalise(body, rel, pages)
        dest = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write('---\ntitle: "{}"\n---\n\n{}\n'.format(title.replace('"', "'"), text))
        STATS["pages"] += 1
        search.append({"u": page_url(rel), "t": title, "x": plain_text(body)[:20000]})

    for rel in assets:
        dest = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(os.path.join(DOCS, rel), dest)

    with open(os.path.join(ROOT, "mkdocs.yml"), encoding="utf-8") as fh:
        cfg = yaml.load(fh, Loader=Loader)
    adir = os.path.join(out_dir, "assets", "tappaas")
    os.makedirs(adir, exist_ok=True)
    with open(os.path.join(adir, "nav.json"), "w", encoding="utf-8") as fh:
        json.dump(nav_tree(cfg["nav"]), fh, ensure_ascii=False)
    with open(os.path.join(adir, "search.json"), "w", encoding="utf-8") as fh:
        json.dump(search, fh, ensure_ascii=False)

    # the layout and the site's static assets
    shutil.copytree(os.path.join(LAYOUT_SRC, "lazysite"), os.path.join(out_dir, "lazysite"))
    for fn in os.listdir(os.path.join(LAYOUT_SRC, "assets")):
        src = os.path.join(LAYOUT_SRC, "assets", fn)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, os.path.join(adir, fn))

    print(json.dumps(STATS, indent=1))
    if UNRESOLVED:
        print("unresolved relative links (kept as written):")
        for p, t in UNRESOLVED[:40]:
            print("  {} -> {}".format(p, t))


if __name__ == "__main__":
    main()
