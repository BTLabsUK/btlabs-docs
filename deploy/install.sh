#!/bin/sh
# Deploys the built site to the web server: rsync site/build and deploy/ to a staging folder
# under the deploy user's home, then run deploy/remote-install.sh there with sudo. Build first:
#
#   (cd site && npm ci && npm run build)
#   deploy/install.sh            deploy
#   deploy/install.sh --check    only nginx -t on the host (nothing installed or reloaded)
set -eu
HOST=${BTLABS_DOCS_HOST:?set BTLABS_DOCS_HOST to the ssh host of the web server}
cd "$(dirname "$0")/.."
[ -f site/build/index.html ] || { echo "install: build the site first (cd site && npm run build)" >&2; exit 1; }
ssh "$HOST" "mkdir -p btlabs-docs-stage"
rsync -az --delete -e ssh --exclude '.DS_Store' site/build/ "$HOST:btlabs-docs-stage/build/"
rsync -az --delete -e ssh deploy/ "$HOST:btlabs-docs-stage/deploy/"
ssh "$HOST" "sudo -n sh btlabs-docs-stage/deploy/remote-install.sh ${1:-}"
