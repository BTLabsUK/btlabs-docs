# BT LABS docs

The source of https://docs.btlabs.uk, the documentation of Epic Cash Desktop, Epic Cash Mobile,
LEPIC and lepic-flutter, and of the three repositories' GitHub wikis.

| Path | Contents |
| --- | --- |
| `site/docs/` | The pages: `users/` (the user guide), `developers/`, `security.md`. The one source. |
| `site/` | Docusaurus 3. The look is the Epic Cash Developer Hub's (devdocs.btlabs.uk): `src/css/custom.css`, `index-page.css`, the colour-mode toggle and the contents panel are copied from it unchanged; `src/css/btlabs.css` holds what this site adds. |
| `WRITING.md` | Format and word rules for the pages. Read it before writing. |
| `tools/wiki-sync.py` | Exports pages to the GitHub wikis of wallet-for-epic, lepic and lepic-flutter. |
| `tools/repos-public.sh` | Removes the "available soon" marks once the repositories are public. |
| `deploy/` | Deploys the built site to the web server (nginx site `btlabs-docs`, `/srv/btlabs-docs`). |

## Work on the pages

```bash
cd site
npm ci
npm start            # http://localhost:3002, reloads on save
npm run build        # site/build; broken links fail the build
```

## Deploy

```bash
(cd site && npm ci && npm run build)
deploy/install.sh
```

`deploy/install.sh --check` only runs `nginx -t` on the server. The first deploy also gets the
certificate for docs.btlabs.uk with the server's certbot; renewals run with the server's others.

## GitHub wikis

```bash
tools/wiki-sync.py               # dry run: writes build-wiki/<repo>/, pushes nothing
tools/wiki-sync.py --push        # pushes each wiki to github.com/BTLabs-EPIC/<repo>.wiki.git
```

Which pages go to which wiki is the `WIKIS` table at the top of the script. Each wiki gets
`Home.md`, `_Sidebar.md`, `_Footer.md` and its pages; links to pages a wiki does not carry point
to docs.btlabs.uk.

### When the repositories are public

1. `tools/repos-public.sh`, check `git diff`, commit.
2. `(cd site && npm run build) && deploy/install.sh`
3. In each of the three repositories on GitHub: Settings › Features › Wikis on, then the Wiki tab,
   **Create the first page**, save it (any text: the sync replaces it). A wiki's git repository
   exists only after that first page.
4. `tools/wiki-sync.py --push`

## License

The pages are under the Apache License 2.0, like the code they describe.
