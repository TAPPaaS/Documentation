(function () {
  "use strict";
  var here = location.pathname.replace(/\.md$/, "");
  var norm = function (u) { return (u || "").replace(/\/$/, "") || "/"; };
  var hereN = norm(here);

  function contains(node) {
    if (node.url && norm(node.url) === hereN) return true;
    return (node.children || []).some(contains);
  }
  function firstUrl(node) {
    if (node.url) return node.url;
    for (var i = 0; i < (node.children || []).length; i++) { var u = firstUrl(node.children[i]); if (u) return u; }
    return "/";
  }
  function tree(nodes, depth) {
    var ul = document.createElement("ul");
    nodes.forEach(function (n) {
      var li = document.createElement("li");
      if (n.url) {
        var a = document.createElement("a"); a.href = n.url; a.textContent = n.label;
        if (norm(n.url) === hereN) a.className = "on";
        li.appendChild(a);
        if (n.children && n.children.length) li.appendChild(tree(n.children, depth + 1));
      } else if (depth > 0) {
        var d = document.createElement("details"); d.open = contains(n);
        var s = document.createElement("summary"); s.textContent = n.label; d.appendChild(s);
        d.appendChild(tree(n.children || [], depth + 1)); li.appendChild(d);
      } else {
        var sp = document.createElement("span"); sp.textContent = n.label; li.appendChild(sp);
        li.appendChild(tree(n.children || [], depth + 1));
      }
      ul.appendChild(li);
    });
    return ul;
  }

  fetch("/assets/tappaas/nav.json").then(function (r) { return r.json(); }).then(function (nav) {
    var tabs = document.getElementById("tabs"), side = document.getElementById("side"), cur = null;
    nav.forEach(function (sec) {
      var a = document.createElement("a"); a.href = firstUrl(sec); a.textContent = sec.label;
      if (contains(sec)) { a.className = "on"; cur = sec; }
      tabs.appendChild(a);
    });
    if (cur && cur.children && cur.children.length) side.appendChild(tree(cur.children, 1));
    else side.style.visibility = "hidden";
  });

  // on this page
  var toc = document.getElementById("toc"), hs = document.querySelectorAll("#page h2, #page h3");
  if (hs.length > 1) {
    var b = document.createElement("b"); b.textContent = "On this page"; toc.appendChild(b);
    hs.forEach(function (h) {
      var anchor = h.querySelector("a[id]"), id = anchor ? anchor.id : h.id;
      var a = document.createElement("a"); a.href = "#" + id; a.textContent = h.textContent;
      a.className = h.tagName.toLowerCase(); toc.appendChild(a);
    });
  }

  // code: mermaid diagrams and highlighting
  var mm = document.querySelectorAll("pre code.language-mermaid");
  if (mm.length) {
    mm.forEach(function (c) { var d = document.createElement("div"); d.className = "mermaid"; d.textContent = c.textContent; c.parentNode.replaceWith(d); });
    var s = document.createElement("script"); s.src = "/assets/tappaas/vendor/mermaid.min.js";
    s.onload = function () {
      window.mermaid.initialize({ startOnLoad: false, theme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "default" });
      window.mermaid.run({ querySelector: ".mermaid" });
    };
    document.head.appendChild(s);
  }
  window.addEventListener("load", function () { if (window.hljs) document.querySelectorAll("pre code").forEach(function (c) { window.hljs.highlightElement(c); }); });

  // search
  var q = document.getElementById("q"), out = document.getElementById("results"), index = null;
  document.getElementById("search").addEventListener("submit", function (e) { e.preventDefault(); });
  q.addEventListener("input", function () {
    var term = q.value.trim().toLowerCase();
    if (term.length < 2) { out.hidden = true; return; }
    var go = function () {
      var words = term.split(/\s+/), hits = [];
      index.forEach(function (p) {
        var t = p.t.toLowerCase(), x = p.x.toLowerCase(), score = 0;
        if (!words.every(function (w) { return t.indexOf(w) >= 0 || x.indexOf(w) >= 0; })) return;
        words.forEach(function (w) { if (t.indexOf(w) >= 0) score += 10; score += Math.min(5, x.split(w).length - 1); });
        var at = x.indexOf(words[0]); hits.push({ p: p, s: score, at: at });
      });
      hits.sort(function (a, b) { return b.s - a.s; });
      out.innerHTML = "";
      hits.slice(0, 15).forEach(function (h) {
        var a = document.createElement("a"); a.href = h.p.u;
        var bt = document.createElement("b"); bt.textContent = h.p.t; a.appendChild(bt);
        var sm = document.createElement("small"); sm.textContent = h.at >= 0 ? "…" + h.p.x.substr(Math.max(0, h.at - 60), 160) + "…" : ""; a.appendChild(sm);
        out.appendChild(a);
      });
      if (!hits.length) out.textContent = "No results";
      out.hidden = false;
    };
    if (index) go(); else fetch("/assets/tappaas/search.json").then(function (r) { return r.json(); }).then(function (j) { index = j; go(); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".search")) out.hidden = true; });
})();
