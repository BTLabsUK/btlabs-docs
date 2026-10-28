#!/bin/sh
# Strips the " *(available soon)*" marks after links to gitlab.com/bt-labs-group, once wallet-for-epic,
# lepic and lepic-flutter are public on GitLab. Run it, check `git diff`, commit, then rebuild
# and deploy the site (deploy/install.sh) and sync the wikis (tools/wiki-sync.py --push).
set -eu
cd "$(dirname "$0")/.."
grep -rl --include='*.md' ' \*(available soon)\*' site/docs | while read -r f; do
    sed -i 's/ \*(available soon)\*//g' "$f"
    echo "unmarked $f"
done
if grep -rn --include='*.md' 'available soon' site/docs; then
    echo "repos-public: marks left above, remove them by hand" >&2
    exit 1
fi
