#!/usr/bin/env python3
"""Spike: crawl a lazysite docs site and check every internal link and anchor.

Usage: python3 scripts/lazysite-check.py BASE_URL   (e.g. http://localhost:8381)
Reports pages, broken links, missing anchors, pages served as Markdown source,
leftover Markdown in the HTML, and the first-render vs cached time per page.
"""
import html.parser
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip("/")


class Parse(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.in_main, self.text = set(), [], False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "main":
            self.in_main = True

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False

    def handle_data(self, d):
        if self.in_main:
            self.text.append(d)


def fetch(path):
    t = time.time()
    try:
        with urllib.request.urlopen(BASE + path, timeout=30) as r:
            body, code, ctype = r.read().decode("utf-8", "replace"), r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        body, code, ctype = "", e.code, ""
    return code, ctype, body, time.time() - t


def nav_urls(nodes):
    for n in nodes:
        if n.get("url"):
            yield n["url"]
        yield from nav_urls(n.get("children", []))


def main():
    nav = json.loads(fetch("/assets/tappaas/nav.json")[2])
    todo = ["/"] + list(dict.fromkeys(nav_urls(nav)))
    seen, pages, links = set(), {}, []
    times = []
    while todo:
        p = todo.pop(0)
        if p in seen:
            continue
        seen.add(p)
        code, ctype, body, t1 = fetch(p)
        _, _, _, t2 = fetch(p)
        times.append((p, t1, t2))
        parser = Parse()
        parser.feed(body)
        pages[p] = (code, ctype, parser.ids, "".join(parser.text))
        for href in parser.links:
            if re.match(r"^[a-z][a-z0-9+.-]*:", href) or href.startswith("//"):
                continue
            u = urllib.parse.urlparse(urllib.parse.urljoin("http://x" + p, href))
            path = u.path or p
            if not href.startswith(("/", "#")):
                links.append((p, path, "", "RELATIVE:" + href))
            links.append((p, path, u.fragment, href))
            if path not in seen and not re.search(r"\.(png|svg|jpg|jpeg|gif|pdf|ico|json|js|css)$", path):
                todo.append(path)

    bad_status = sorted({(src, href) for src, path, frag, href in links if pages.get(path, (fetch(path)[0],))[0] != 200})
    missing_anchor = sorted({(src, href) for src, path, frag, href in links
                             if frag and path in pages and frag not in pages[path][2]})
    source_served = [p for p, v in pages.items() if not v[1].startswith("text/html")]
    leftovers = {}
    pats = {"literal [ ]": r"\[ \]|\[x\]", "list as text": r"\n- [A-Za-z`*]", "raw ** bold": r"\*\*\w",
            "raw link md": r"\]\([^)]*\)", "admonition !!!": r"^!!!", "pipe row": r"^\|.*\|$"}
    for p, v in pages.items():
        for k, rx in pats.items():
            if re.search(rx, v[3], re.M):
                leftovers.setdefault(k, []).append(p)

    first = sorted(t1 for _, t1, _ in times)
    cached = sorted(t2 for _, _, t2 in times)
    q = lambda xs, f: xs[min(len(xs) - 1, int(len(xs) * f))]
    print("pages crawled: {}  links checked: {}".format(len(pages), len(links)))
    print("non-200 pages: {}".format([p for p, v in pages.items() if v[0] != 200]))
    print("links to a non-200 target: {}".format(len(bad_status)))
    for s, h in bad_status[:25]:
        print("   {} -> {}".format(s, h))
    print("links whose #anchor is missing: {}".format(len(missing_anchor)))
    for s, h in missing_anchor[:40]:
        print("   {} -> {}".format(s, h))
    print("pages not served as HTML: {}".format(source_served))
    for k, v in leftovers.items():
        print("leftover '{}': {} pages, e.g. {}".format(k, len(v), v[:5]))
    print("first render: median {:.0f} ms, p90 {:.0f} ms, max {:.0f} ms ({})".format(
        q(first, .5) * 1000, q(first, .9) * 1000, first[-1] * 1000, max(times, key=lambda x: x[1])[0]))
    print("cached:       median {:.0f} ms, p90 {:.0f} ms, max {:.0f} ms".format(
        q(cached, .5) * 1000, q(cached, .9) * 1000, cached[-1] * 1000))


if __name__ == "__main__":
    main()
