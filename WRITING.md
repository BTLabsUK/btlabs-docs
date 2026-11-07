# Writing the docs

The Markdown under `site/docs/` is the one source. It is built into the site at
https://docs.btlabs.uk (Docusaurus) and exported to the GitHub wikis of wallet-for-epic, lepic and
lepic-flutter by `tools/wiki-sync.py`. Write it so both work.

## Format

- Plain Markdown in `.md` files. No JSX, no MDX components, no raw HTML.
- Front matter with `title` and `description` (one sentence), then the page's own `# Heading`
  (the same text as `title`).
- Links to other pages are relative paths with the `.md` extension, for example
  `[Tor](../users/tor.md)` or `[Linux](build/linux.md)`, with an optional `#anchor`.
  Never `/users/tor` or a docs.btlabs.uk URL for a page of this site.
- Notes: `:::note`, `:::tip`, `:::warning` or `:::danger` on a line of its own, the text, then
  `:::` on a line of its own. Nothing else of Docusaurus's syntax.
- Images next to the page in an `img/` folder, linked relatively: `![Receive screen](img/receive.png)`.
- Code blocks with a language (`bash`, `powershell`, `rust`, `dart`, `toml`, `yaml`, `text`).
- Tables are fine; keep them narrow enough for a phone (three or four columns).

## Words

- Short, factual and impersonal. No hype, no "simply", no "just", no exclamation marks.
- No durations or time estimates ("takes a few minutes", "about 6 minutes"). Say what happens, not
  how long it takes. Block counts are fine (a block is a fact, a minute is a guess).
- The app's own words for its parts, exactly as the app shows them: Epicbox, Link · HTTP,
  Link · Tor, Direct · File Transfer, Direct · QR Payment, recovery phrase, Recheck balance,
  Export wallet data, Linked devices, Pair, Advanced, Connection mode (Normal, Tor only,
  Node only, Kill switch). Places in the app as `Settings › This wallet › Linked devices`.
- Product names: BT Wallet, one app for Windows, Linux, Android and the macOS and iOS previews
  ("the desktop app" or "the phone app" where the difference matters); LEPIC (the Rust wallet
  core), lepic-flutter (its Flutter binding). "BT LABS" in capitals when the company is named as
  a brand; "BT Labs" in running text is also fine.
- The old names, Epic Cash Desktop and Epic Cash Mobile (up to 26.10.24), only for moving from an
  old install. `tools/check-doc-names.py` fails the build on any other use.
- Epic node and epic-wallet versions: say "the latest release" and link
  [its releases page](https://github.com/EpicCash/epic/releases). Where a pin matters, link the
  file that holds it instead of copying the number.
- No personal names, no private hostnames, IP addresses, home-directory paths or machine names.
  Public service addresses the app itself uses (for example `node.btlabs.uk`,
  `epicbox.epiccash.com`) are fine.
- Never mention internal chat groups, bots, plans, reviews, audits or internal tooling.
- The source lives only on GitHub, github.com/BTLabsUK/<repo>. Link it there, and nowhere else.
- Security reports go to support@btlabs.uk, never to a public issue.
