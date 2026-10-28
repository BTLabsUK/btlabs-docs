# BT LABS docs

The source of https://docs.btlabs.uk, the documentation of Epic Cash Desktop, Epic Cash Mobile,
LEPIC and lepic-flutter, and of the three repositories' GitLab wikis.

| Path | Contents |
| --- | --- |
| `site/docs/` | The pages: `users/` (the user guide), `developers/`, `security.md`. The one source. |
| `site/` | Docusaurus 3. The look is the Epic Cash Developer Hub's (devdocs.btlabs.uk): `src/css/custom.css`, `index-page.css`, the colour-mode toggle and the contents panel are copied from it unchanged; `src/css/btlabs.css` holds what this site adds. |
| `WRITING.md` | Format and word rules for the pages. Read it before writing. |
| `tools/wiki-sync.py` | Exports pages to the GitLab wikis (GitHub with `--host github`) of wallet-for-epic, lepic and lepic-flutter. |
| `tools/repos-public.sh` | Drops the "available soon" marks once the repositories are public. |
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

## GitLab wikis

The code lives at https://gitlab.com/bt-labs-group (wallet-for-epic, lepic, lepic-flutter).

```bash
tools/wiki-sync.py               # dry run: writes build-wiki/<repo>/, pushes nothing
tools/wiki-sync.py --push        # pushes each wiki to gitlab.com/bt-labs-group/<repo>.wiki.git
```

Which pages go to which wiki is the `WIKIS` table at the top of the script. Each wiki gets
`home.md`, `_sidebar.md` and its pages; GitLab has no footer page, so the footer text is added to
the end of every page. Links to pages a wiki does not carry point to docs.btlabs.uk. The group is
`btlabs`; use `--group <name>` or `GITLAB_GROUP` for another.

`--push` uses the token in `~/.config/btlabs/gitlab-token` (user `oauth2`) if the file exists,
otherwise git's own credentials. An empty wiki is created by the push; the project must exist and
its wiki must be on.

### When the repositories are public

1. In each GitLab project: set Visibility to Public and check that the Wiki feature is on
   (Settings › General › Visibility, project features, permissions).
2. `tools/repos-public.sh`, check `git diff`, commit.
3. `(cd site && npm run build) && deploy/install.sh`
4. `tools/wiki-sync.py --push`

### GitHub

`tools/wiki-sync.py --host github` exports for the GitHub wikis of BTLabs-EPIC (`Home.md`,
`_Sidebar.md`, `_Footer.md`). Before `--push`, each repository needs its wiki switched on
(Settings › Features › Wikis) and a first page created once in the Wiki tab (**Create the first
page**, any text); a GitHub wiki's git repository exists only after that.

## License

The pages are under the Apache License 2.0, like the code they describe.
