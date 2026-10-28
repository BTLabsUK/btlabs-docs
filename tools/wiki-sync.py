#!/usr/bin/env python3
"""Turns the docs Markdown (site/docs) into GitHub wiki pages for the three repositories.

One source of truth: the pages under site/docs are written once (WRITING.md) and built into
https://docs.btlabs.uk. This script exports a chosen set of them to each repository's wiki:

    wallet-for-epic   the user guide and the app-developer pages
    lepic             the Rust core pages
    lepic-flutter     the binding pages

For each wiki it writes Home.md, _Sidebar.md, _Footer.md and one file per page into
build-wiki/<repo>/, with front matter dropped, admonitions turned into quotes, links between pages
rewritten to wiki page names (or to docs.btlabs.uk for a page that wiki does not carry), and images
copied into images/.

    tools/wiki-sync.py                 dry run: write build-wiki/ and list what would change
    tools/wiki-sync.py --push          the same, then push each wiki to <repo>.wiki.git
    tools/wiki-sync.py --repo lepic    only one wiki (with or without --push)

A wiki's git repository exists only after its first page was saved in the GitHub web interface
(Wiki tab, "Create the first page"); --push says so when the clone fails. Everything in a wiki is
generated: --push replaces the pages there with the export.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'site' / 'docs'
OUT = ROOT / 'build-wiki'
SITE = 'https://docs.btlabs.uk'
ORG = 'https://github.com/BTLabs-EPIC'

# Page names in the wikis, for the pages whose title is too long or too generic for a wiki link.
NAMES = {
    'users/index.md': 'User guide',
    'developers/index.md': 'Developer guide',
    'developers/build/index.md': 'Build from source',
    'security.md': 'Report a security issue',
}

# Each wiki: what its Home says, and its sidebar sections with the pages in order.
WIKIS = {
    'wallet-for-epic': {
        'title': 'Epic Cash Desktop and Epic Cash Mobile',
        'intro': (
            'Epic Cash Desktop (Windows, Linux, macOS preview) and Epic Cash Mobile (Android, iOS '
            'preview): the Flutter app on top of the [LEPIC](' + ORG + '/lepic/wiki) wallet core.'
        ),
        'sections': [
            ('Use the wallet', [
                'users/index.md', 'users/install.md', 'users/first-wallet.md',
                'users/recovery-phrase.md', 'users/send-and-receive.md',
                'users/payment-methods.md', 'users/addresses.md', 'users/cancel.md',
                'users/pairing.md', 'users/linked-devices.md', 'users/nodes.md',
                'users/epicbox.md', 'users/tor.md', 'users/network-modes.md', 'users/privacy.md',
                'users/backups.md', 'users/restore.md', 'users/updates.md', 'users/advanced.md',
                'users/how-it-works.md', 'users/troubleshooting.md', 'users/faq.md',
                'users/glossary.md',
            ]),
            ('Build the app', [
                'developers/index.md', 'developers/architecture.md',
                'developers/build/index.md', 'developers/build/linux.md',
                'developers/build/windows.md', 'developers/build/android.md',
                'developers/build/apple.md', 'developers/build/variants.md',
                'developers/dev-environment.md', 'developers/testing.md',
                'developers/releases.md', 'developers/contributing.md', 'security.md',
            ]),
        ],
    },
    'lepic': {
        'title': 'LEPIC',
        'intro': (
            'LEPIC is the Epic Cash wallet core in Rust behind Epic Cash Desktop and Epic Cash '
            'Mobile: a library that runs inside the app, with its FFI API for the '
            '[Flutter binding](' + ORG + '/lepic-flutter/wiki).'
        ),
        'sections': [
            ('The core', [
                'developers/lepic.md', 'developers/architecture.md',
                'developers/security-model.md', 'developers/decisions.md',
                'developers/upstream.md', 'developers/dependencies.md',
            ]),
            ('Working on it', [
                'developers/dev-environment.md', 'developers/testing.md',
                'developers/contributing.md', 'security.md',
            ]),
        ],
    },
    'lepic-flutter': {
        'title': 'lepic-flutter',
        'intro': (
            'The Flutter binding of [LEPIC](' + ORG + '/lepic/wiki): the Dart API over the Rust '
            'wallet core, and the build hook that bundles its native library. Used by '
            '[Epic Cash Desktop and Epic Cash Mobile](' + ORG + '/wallet-for-epic/wiki).'
        ),
        'sections': [
            ('The binding', [
                'developers/lepic-flutter.md', 'developers/architecture.md',
                'developers/security-model.md',
            ]),
            ('Working on it', [
                'developers/build/index.md', 'developers/dev-environment.md',
                'developers/testing.md', 'developers/contributing.md', 'security.md',
            ]),
        ],
    },
}

FRONT = re.compile(r'\A---\n(.*?)\n---\n', re.S)
LINK = re.compile(r'(!?)\[([^\]]*)\]\(([^)\s]+)\)')
ADMONITION = re.compile(r'^:::(note|tip|info|warning|danger|caution)[^\n]*\n(.*?)^:::[ \t]*$', re.S | re.M)
FENCE = re.compile(r'^(```|~~~)')


def front_matter(text):
    m = FRONT.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"\'')
        text = text[m.end():]
    return meta, text


def page_name(rel, meta):
    return NAMES.get(rel) or meta.get('title') or Path(rel).stem


def wiki_file(name):
    # GitHub turns spaces into hyphens in wiki page names; keep only safe characters.
    return re.sub(r'[^A-Za-z0-9._-]+', '-', name).strip('-')


def site_url(rel, anchor=''):
    path = rel[:-3]
    if path.endswith('/index') or path == 'index':
        path = path[: -len('index')]
    else:
        path += '/'
    return f'{SITE}/{path}{anchor}'


def split_code(text):
    """Yields (is_code, chunk): fenced code blocks are left alone."""
    out, buf, code = [], [], False
    for line in text.splitlines(keepends=True):
        if FENCE.match(line.lstrip()):
            if not code:
                out.append((False, ''.join(buf)))
                buf = [line]
                code = True
            else:
                buf.append(line)
                out.append((True, ''.join(buf)))
                buf = []
                code = False
            continue
        buf.append(line)
    out.append((code, ''.join(buf)))
    return out


def convert(rel, text, pages, images):
    """One page's body, as wiki Markdown. pages maps doc path -> wiki file name for this wiki."""
    _, body = front_matter(text)
    # The wiki shows the page name as its title, so the page's own H1 would repeat it.
    body = re.sub(r'\A\s*# [^\n]*\n+', '', body)
    here = (DOCS / rel).parent

    def admonition(m):
        label = {'danger': 'Danger', 'caution': 'Warning'}.get(m.group(1), m.group(1).capitalize())
        lines = m.group(2).strip('\n').splitlines()
        quoted = '\n'.join('> ' + l if l.strip() else '>' for l in lines)
        return f'> **{label}**\n>\n{quoted}'

    def link(m):
        bang, label, target = m.groups()
        if re.match(r'^[a-z]+:', target) or target.startswith('#'):
            return m.group(0)
        path, _, anchor = target.partition('#')
        anchor = '#' + anchor if anchor else ''
        resolved = (here / path).resolve()
        try:
            doc = resolved.relative_to(DOCS).as_posix()
        except ValueError:
            raise SystemExit(f'{rel}: link outside the docs: {target}')
        if bang:
            if not resolved.is_file():
                raise SystemExit(f'{rel}: missing image {target}')
            name = 'images/' + doc.replace('/', '-')
            images[name] = resolved
            return f'![{label}]({name})'
        if not doc.endswith('.md'):
            raise SystemExit(f'{rel}: link to a non-page: {target}')
        if not resolved.is_file():
            raise SystemExit(f'{rel}: broken link {target}')
        if doc in pages:
            return f'[{label}]({pages[doc]}{anchor})'
        return f'[{label}]({site_url(doc, anchor)})'

    parts = []
    for is_code, chunk in split_code(body):
        if not is_code:
            chunk = ADMONITION.sub(admonition, chunk)
            chunk = LINK.sub(link, chunk)
        parts.append(chunk)
    rest = ''.join(parts).rstrip() + '\n'
    return rest + f'\n---\n\nOn the docs site: [{site_url(rel)}]({site_url(rel)})\n'


def export(repo, spec):
    dest = OUT / repo
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    order = [p for _, ps in spec['sections'] for p in ps]
    metas = {}
    for rel in order:
        if not (DOCS / rel).is_file():
            raise SystemExit(f'{repo}: no page {rel}')
        metas[rel], _ = front_matter((DOCS / rel).read_text())
    pages = {rel: wiki_file(page_name(rel, metas[rel])) for rel in order}
    if len(set(pages.values())) != len(pages):
        raise SystemExit(f'{repo}: two pages share a wiki name: {sorted(pages.values())}')

    images = {}
    for rel in dict.fromkeys(order):
        (dest / f'{pages[rel]}.md').write_text(convert(rel, (DOCS / rel).read_text(), pages, images))
    for name, src in images.items():
        (dest / name).parent.mkdir(exist_ok=True)
        shutil.copyfile(src, dest / name)

    def entry(rel):
        title = page_name(rel, metas[rel])
        return f'- [{title}]({pages[rel]})'

    home = [f'# {spec["title"]}', '', spec['intro'], '',
            f'The full documentation, with search, is at **[docs.btlabs.uk]({SITE})**. '
            'These wiki pages are generated from it.', '']
    for heading, rels in spec['sections']:
        home.append(f'## {heading}')
        home.append('')
        for rel in rels:
            desc = metas[rel].get('description', '')
            home.append(entry(rel) + (f': {desc}' if desc else ''))
        home.append('')
    (dest / 'Home.md').write_text('\n'.join(home))

    side = ['**[Home](Home)**', '']
    for heading, rels in spec['sections']:
        side.append(f'**{heading}**')
        side.append('')
        side.extend(entry(rel) for rel in rels)
        side.append('')
    side.append(f'[docs.btlabs.uk]({SITE})')
    (dest / '_Sidebar.md').write_text('\n'.join(side) + '\n')

    (dest / '_Footer.md').write_text(
        f'Generated from the BT LABS documentation, [docs.btlabs.uk]({SITE}). '
        'Edits made here are replaced at the next sync. '
        'Security issues: support@btlabs.uk.\n')
    return dest


def git(*args, cwd=None, check=True):
    return subprocess.run(['git', *args], cwd=cwd, check=check, text=True, capture_output=True)


def push(repo, dest):
    url = f'{ORG}/{repo}.wiki.git'
    work = OUT / f'.{repo}.wiki'
    if work.exists():
        shutil.rmtree(work)
    r = git('clone', '--quiet', url, str(work), check=False)
    if r.returncode != 0:
        print(f'{repo}: cannot clone {url}. Open {ORG}/{repo}/wiki, create the first page once in '
              f'the web interface, then run this again.\n{r.stderr.strip()}', file=sys.stderr)
        return False
    for f in work.iterdir():
        if f.name != '.git':
            shutil.rmtree(f) if f.is_dir() else f.unlink()
    shutil.copytree(dest, work, dirs_exist_ok=True)
    git('add', '-A', cwd=work)
    if git('status', '--porcelain', cwd=work).stdout.strip() == '':
        print(f'{repo}: wiki already up to date')
        return True
    sha = git('rev-parse', '--short', 'HEAD', cwd=ROOT, check=False).stdout.strip() or 'local'
    git('commit', '--quiet', '-m', f'Sync from the docs ({sha})', cwd=work)
    git('push', '--quiet', 'origin', 'HEAD', cwd=work)
    print(f'{repo}: pushed to {url}')
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--push', action='store_true', help='push each wiki to <repo>.wiki.git')
    ap.add_argument('--repo', choices=sorted(WIKIS), help='only this wiki')
    a = ap.parse_args()
    ok = True
    for repo, spec in WIKIS.items():
        if a.repo and repo != a.repo:
            continue
        dest = export(repo, spec)
        files = sorted(p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file())
        print(f'{repo}: {len(files)} files in {dest.relative_to(ROOT)}/')
        if a.push:
            ok = push(repo, dest) and ok
    if not a.push:
        print('Dry run: nothing pushed. Push with: tools/wiki-sync.py --push')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
