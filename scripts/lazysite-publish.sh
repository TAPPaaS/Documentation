#!/usr/bin/env bash
# Publish the docs to a lazysite instance by hand, until the Woodpecker pipeline
# (lazysite-layout/woodpecker-lazysite.yml) does it. Builds from a TAPPaaS checkout,
# then pushes the site to the instance's served branch through the mothership.
#
#   scripts/lazysite-publish.sh [--tappaas DIR] [--via HOST] [--repo SSH_URL] [--branch B] [--key FILE]
#
# Defaults: --tappaas ~/src/TAPPaaS, --via cicd-hrossen,
#   --repo ssh://forgejo@forgejo-tappaas.tappaas.internal/websites/lazysite-tappaas.git,
#   --branch live, --key ~/.tappaas/docs-pipeline/key (its public half is in repoPushKeys).
# KROKI_URL renders the Kroki diagrams (e.g. https://kroki.io); without it they stay code.
set -euo pipefail
cd "$(dirname "$0")/.."
TAPPAAS="$HOME/src/TAPPaaS"; VIA=cicd-hrossen; BRANCH=live; KEY="$HOME/.tappaas/docs-pipeline/key"
REPO="ssh://forgejo@forgejo-tappaas.tappaas.internal/websites/lazysite-tappaas.git"
while [[ $# -gt 0 ]]; do case "$1" in
    --tappaas) TAPPAAS="$2"; shift 2 ;; --via) VIA="$2"; shift 2 ;; --repo) REPO="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;; --key) KEY="$2"; shift 2 ;; *) echo "unknown option $1" >&2; exit 2 ;;
esac; done
OUT="$(mktemp -d)"; trap 'rm -rf "$OUT"' EXIT
TAPPAAS_SOURCE_DIR="$TAPPAAS" python3 scripts/sync-source.py | tail -1
[[ -s lazysite-layout/assets/vendor/mermaid.min.js ]] || ./scripts/lazysite-vendor.sh
python3 scripts/lazysite-site.py "$OUT/site" | grep -E '"pages"|unresolved'
REV="$(git -C "$TAPPAAS" rev-parse --short HEAD)"
COPYFILE_DISABLE=1 tar --no-xattrs -C "$OUT/site" -czf "$OUT/site.tgz" .
R="tmp-docs-publish.$$"
ssh -o BatchMode=yes "$VIA" "mkdir -m 700 ~/$R"
scp -q "$OUT/site.tgz" "$VIA:$R/site.tgz"; scp -q "$KEY" "$VIA:$R/key"
ssh -o BatchMode=yes "$VIA" "R=~/$R REPO='$REPO' BRANCH='$BRANCH' REV='$REV' bash -s" <<'EOSH'
set -euo pipefail
trap 'rm -rf "$R"' EXIT
chmod 600 "$R/key"
export GIT_SSH_COMMAND="ssh -i $R/key -o IdentitiesOnly=yes -o IdentityAgent=none -o UserKnownHostsFile=$R/known_hosts -o StrictHostKeyChecking=accept-new -o BatchMode=yes"
git clone -q --depth 1 --branch "$BRANCH" "$REPO" "$R/out" 2>/dev/null || { git init -q -b "$BRANCH" "$R/out"; }
find "$R/out" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
tar -xzf "$R/site.tgz" -C "$R/out" 2>/dev/null
cd "$R/out"; git add -A
if git -c user.email=ci@tappaas.org -c user.name="TAPPaaS docs" commit -qm "Publish from TAPPaaS $REV"; then
    git push -q "$REPO" "HEAD:$BRANCH" 2>&1 | grep -vE 'INF|remote:' || true
    echo "published $(git rev-parse --short HEAD) to $BRANCH; live within a minute"
else
    echo "nothing changed"
fi
EOSH
