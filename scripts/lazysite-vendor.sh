#!/usr/bin/env bash
# Spike: fetch the pinned third-party scripts the lazysite layout serves itself (no CDN at runtime).
set -euo pipefail
d="$(dirname "$0")/../lazysite-layout/assets/vendor"; mkdir -p "$d"
curl -sfL -o "$d/mermaid.min.js"   https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js
curl -sfL -o "$d/highlight.min.js" https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/highlight.min.js
curl -sfL -o "$d/hl-light.css"     https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/styles/github.min.css
curl -sfL -o "$d/hl-dark.css"      https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/styles/github-dark.min.css
