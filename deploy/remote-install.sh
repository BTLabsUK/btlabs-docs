#!/bin/sh
# Runs on the host as root, from ~bt/btlabs-docs-stage (see install.sh). Installs the built site
# under /srv/btlabs-docs (root-owned, read-only, the three newest releases kept), the nginx site
# `btlabs-docs`, and on the first run the Let's Encrypt certificate for docs.btlabs.uk through the
# host's existing certbot (webroot /var/www/html; certbot.timer renews it with the others).
# Touches no other site or service. `nginx -t` runs before every reload, and a failing test puts
# the previous site file back.
set -eu
STAGE=$(cd "$(dirname "$0")/.." && pwd)
NAME=docs.btlabs.uk
SITE=/etc/nginx/sites-available/btlabs-docs
LINK=/etc/nginx/sites-enabled/btlabs-docs
CERT=/etc/letsencrypt/live/$NAME/fullchain.pem

[ -f "$STAGE/build/index.html" ] || { echo "remote-install: no build in $STAGE/build" >&2; exit 1; }
if [ "${1:-}" = "--check" ]; then
    nginx -t
    exit 0
fi

mkdir -p /srv/btlabs-docs/releases
rel=/srv/btlabs-docs/releases/$(date -u +%Y%m%d-%H%M%S)
cp -r "$STAGE/build" "$rel"
chown -R root:root "$rel"
find "$rel" -type d -exec chmod 755 {} +
find "$rel" -type f -exec chmod 644 {} +
ln -sfn "$rel" /srv/btlabs-docs/current.new && mv -T /srv/btlabs-docs/current.new /srv/btlabs-docs/current
ls -1dt /srv/btlabs-docs/releases/* | tail -n +4 | xargs -r rm -rf

# Installs nginx site file $1, tests, reloads; restores the previous file when the test fails.
install_site() {
    if [ -f "$SITE" ] && cmp -s "$1" "$SITE"; then
        ln -sfn "$SITE" "$LINK"
        return 0
    fi
    rm -f "$SITE.prev"
    [ -f "$SITE" ] && cp -p "$SITE" "$SITE.prev"
    install -m 0644 "$1" "$SITE"
    ln -sfn "$SITE" "$LINK"
    if nginx -t; then
        systemctl reload nginx
    else
        echo "remote-install: nginx -t failed; restoring the previous site file" >&2
        if [ -f "$SITE.prev" ]; then cp -p "$SITE.prev" "$SITE"; else rm -f "$LINK" "$SITE"; fi
        nginx -t
        exit 1
    fi
}

if [ ! -f "$CERT" ]; then
    install_site "$STAGE/deploy/nginx/docs.btlabs.uk.bootstrap.conf"
    certbot certonly --non-interactive --webroot -w /var/www/html -d "$NAME" \
        --key-type ecdsa --deploy-hook 'systemctl reload nginx'
fi
install_site "$STAGE/deploy/nginx/docs.btlabs.uk.conf"
echo "remote-install: https://$NAME serves $rel"
