<div align="center">

<img src="site/static/img/bt-wallet-lockup-row-dark.svg" alt="BT Wallet for Epic Cash" width="260">

# btlabs-docs

**The source of docs.btlabs.uk: the documentation of BT Wallet for Epic Cash (desktop and mobile),
LEPIC and lepic-flutter.**

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Docusaurus 3.10](https://img.shields.io/badge/docusaurus-3.10.2-3ECC5F.svg)](site/package.json)

[Read the docs](https://docs.btlabs.uk) · [Writing rules](WRITING.md) · [Security](SECURITY.md)

</div>

One set of Markdown pages, written once, becomes two things: the website
[docs.btlabs.uk](https://docs.btlabs.uk) (Docusaurus) and the wikis of the three code projects on
GitHub ([wallet-for-epic](https://github.com/BTLabsUK/wallet-for-epic),
[lepic](https://github.com/BTLabsUK/lepic),
[lepic-flutter](https://github.com/BTLabsUK/lepic-flutter)). Source:
[github.com/BTLabsUK/btlabs-docs](https://github.com/BTLabsUK/btlabs-docs).

> **Status: live.** The site is published at docs.btlabs.uk.

## Build from source

You need Node.js 20 or newer (tested with 22), npm and Python 3. Nothing else: the site has no
server part.

```bash
git clone https://github.com/BTLabsUK/btlabs-docs && cd btlabs-docs/site
npm ci
npm start            # http://localhost:3002, reloads on save
npm run build        # site/build; a broken link or an old app name fails the build
```

Builds run on your own machine; there is no hosted CI.

## Project structure

| Path | Contents |
| --- | --- |
| `site/docs/` | The pages: `users/` (the user guide), `developers/` (building, architecture, testing, releases), `security.md`. The one source. |
| `site/` | Docusaurus 3: `docusaurus.config.js`, `sidebars.js`, the theme in `src/`: the Epic Cash Developer Hub's base (`src/css/custom.css`), this site's additions (`src/css/btlabs.css`), and the BT Wallet landing page's three looks, Night, Grid and Day (`src/css/looks.css`, `src/components/look.js`; the navbar's switch and the footer's picker). `src/pages/support.js` is the support page. |
| `WRITING.md` | Format and word rules for the pages. Read it before writing. |
| `tools/check-doc-names.py` | Fails on the app's old names outside `tools/doc-names.allow`, and on Epic node or epic-wallet version numbers in the pages. `npm run build` runs it first. |
| `tools/wiki-sync.py` | Exports a chosen set of pages to each code project's GitHub wiki. |
| `deploy/` | Deploys the built site to the web server (an nginx site serving `/srv/btlabs-docs`). |

## Deploy

```bash
(cd site && npm ci && npm run build)
BTLABS_DOCS_HOST=<ssh host of the web server> deploy/install.sh
```

`deploy/install.sh --check` only runs `nginx -t` on the server. The first deploy also gets the
certificate for docs.btlabs.uk with the server's certbot; renewals run with the server's others.

## GitHub wikis

```bash
tools/wiki-sync.py               # dry run: writes build-wiki/<repo>/, pushes nothing
tools/wiki-sync.py --push        # pushes each wiki to github.com/BTLabsUK/<repo>.wiki.git
```

Which pages go to which wiki is the `WIKIS` table at the top of the script. Each wiki gets
`Home.md`, `_Sidebar.md`, `_Footer.md` and its pages. Links to pages a wiki does not carry point to
docs.btlabs.uk. Before `--push`, each repository needs its wiki switched on (Settings › Features ›
Wikis) and a first page created once in the Wiki tab; a GitHub wiki's git repository exists only
after that.

## Contributing

Corrections are welcome: open an issue or a pull request. Follow [WRITING.md](WRITING.md) and
check that `npm run build` passes. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

To report a vulnerability in the wallets or this site, email support@btlabs.uk. [SECURITY.md](SECURITY.md) has the details.

## License

The pages and the site code are under the Apache License 2.0, like the code they describe: see
[LICENSE](LICENSE) and [NOTICE](NOTICE). The Montserrat fonts in `site/static/fonts/` are under
the SIL Open Font License.

<p align="center"><sub>Made by BT Labs</sub></p>
