#!/usr/bin/env python3
"""Turns the docs Markdown (site/docs) into wiki pages for the three repositories.

One source of truth: the pages under site/docs are written once (WRITING.md) and built into
https://docs.btlabs.uk. This script exports a chosen set of them to each repository's wiki:

    wallet-for-epic   the user guide and the app-developer pages
    lepic             the Rust core pages
    lepic-flutter     the binding pages

The default host is GitLab.com (group epic-cash-bt, or $GITLAB_GROUP, or --group); --host github exports
for the GitHub wikis of BTLabsUK instead. For each wiki it writes the home page, the sidebar and
one file per page into build-wiki/<repo>/, with front matter dropped, admonitions turned into
quotes, links between pages rewritten to wiki page names (or to docs.btlabs.uk for a page that wiki
does not carry), and images copied into images/.

    GitLab:  home.md, _sidebar.md. GitLab wikis have no footer page, so the footer text is
             appended to every page. Page links are relative slugs without extension
             ([User guide](User-guide)); a page's file name is its slug.
    GitHub:  Home.md, _Sidebar.md, _Footer.md. Page links are the page names.

    tools/wiki-sync.py                 dry run: write build-wiki/ and list what would change
    tools/wiki-sync.py --push          the same, then push each wiki to <repo>.wiki.git
    tools/wiki-sync.py --repo lepic    only one wiki (with or without --push)
    tools/wiki-sync.py --host github   export for GitHub (set up --push as below)

Push credentials on GitLab: if ~/.config/btlabs/gitlab-token exists it is passed to git through a
credential helper on the command line (user oauth2); it is never written anywhere else. A wiki that
is still empty is created by the push itself (the project must exist and its wiki must be on).
On GitHub a wiki's git repository exists only after its first page was saved in the web interface
(Wiki tab, "Create the first page"); --push says so when the clone fails. Everything in a wiki is
generated: --push replaces the pages there with the export.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'site' / 'docs'
OUT = ROOT / 'build-wiki'
SITE = 'https://docs.btlabs.uk'
TOKEN = Path.home() / '.config' / 'btlabs' / 'gitlab-token'

# The GitLab group path lives in one place, the GITLAB_GROUP file at the repository root (the site
# build reads it too). The pages name it as SOURCE_GROUP; another path rewrites their links.
SOURCE_GROUP = 'epic-cash-bt'
IDENTITY = ('blacktyger', '53139520+blacktyger@users.noreply.github.com')
GITLAB_GROUP = (ROOT / 'GITLAB_GROUP').read_text().strip()
GITHUB_ORG = 'BTLabsUK'

HOSTS = {
    'gitlab': {
        'home': 'home', 'sidebar': '_sidebar', 'footer': None,
        'wiki_path': '/-/wikis/home',
    },
    'github': {
        'home': 'Home', 'sidebar': '_Sidebar', 'footer': '_Footer',
        'wiki_path': '/wiki',
    },
}
HOST = {'name': 'gitlab', 'base': 'https://gitlab.com/' + GITLAB_GROUP}


def repo_url(repo):
    return f'{HOST["base"]}/{repo}'


def wiki_url(repo):
    return repo_url(repo) + HOSTS[HOST['name']]['wiki_path']

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
            'preview): the Flutter app on top of the [LEPIC]({wiki:lepic}) wallet core.'
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
            '[Flutter binding]({wiki:lepic-flutter}).'
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
            'The Flutter binding of [LEPIC]({wiki:lepic}): the Dart API over the Rust '
            'wallet core, and the build hook that bundles its native library. Used by '
            '[Epic Cash Desktop and Epic Cash Mobile]({wiki:wallet-for-epic}).'
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

FOOTER = (f'Generated from the BT LABS documentation, [docs.btlabs.uk]({SITE}). '
          'Edits made here are replaced at the next sync. '
          'Security issues: support@btlabs.uk.')

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
    group = HOST['base'].rsplit('/', 1)[-1] if HOST['name'] == 'gitlab' else SOURCE_GROUP
    if group != SOURCE_GROUP:
        text = text.replace(f'gitlab.com/{SOURCE_GROUP}/', f'gitlab.com/{group}/')
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
    names = HOSTS[HOST['name']]
    gitlab = HOST['name'] == 'gitlab'
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
        body = convert(rel, (DOCS / rel).read_text(), pages, images)
        if gitlab:
            body += '\n' + FOOTER + '\n'
        (dest / f'{pages[rel]}.md').write_text(body)
    for name, src in images.items():
        (dest / name).parent.mkdir(exist_ok=True)
        shutil.copyfile(src, dest / name)

    def entry(rel):
        title = page_name(rel, metas[rel])
        return f'- [{title}]({pages[rel]})'

    intro = re.sub(r'\{wiki:([a-z-]+)\}', lambda m: wiki_url(m.group(1)), spec['intro'])
    home = [f'# {spec["title"]}', '', intro, '',
            f'The full documentation, with search, is at **[docs.btlabs.uk]({SITE})**. '
            'These wiki pages are generated from it.', '']
    for heading, rels in spec['sections']:
        home.append(f'## {heading}')
        home.append('')
        for rel in rels:
            desc = metas[rel].get('description', '')
            home.append(entry(rel) + (f': {desc}' if desc else ''))
        home.append('')
    if gitlab:
        home += [FOOTER, '']
    (dest / f'{names["home"]}.md').write_text('\n'.join(home))

    side = [f'**[Home]({names["home"]})**', '']
    for heading, rels in spec['sections']:
        side.append(f'**{heading}**')
        side.append('')
        side.extend(entry(rel) for rel in rels)
        side.append('')
    side.append(f'[docs.btlabs.uk]({SITE})')
    (dest / f'{names["sidebar"]}.md').write_text('\n'.join(side) + '\n')

    if names['footer']:
        (dest / f'{names["footer"]}.md').write_text(FOOTER + '\n')
    return dest


def git(*args, cwd=None, check=True, auth=False):
    cmd = ['git']
    if auth and HOST['name'] == 'gitlab' and TOKEN.is_file():
        # The token is read by the helper at run time; it is not in the arguments or on disk elsewhere.
        helper = ('!f() { echo username=oauth2; echo "password=$(cat ' + str(TOKEN) + ')"; }; f')
        cmd += ['-c', 'credential.helper=', '-c', f'credential.helper={helper}']
    return subprocess.run(cmd + list(args), cwd=cwd, check=check, text=True, capture_output=True,
                          env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'})


def push(repo, dest):
    url = f'{repo_url(repo)}.wiki.git'
    work = OUT / f'.{repo}.wiki'
    if work.exists():
        shutil.rmtree(work)
    gitlab = HOST['name'] == 'gitlab'
    r = git('clone', '--quiet', url, str(work), check=False, auth=True)
    if r.returncode != 0:
        if gitlab:
            # A wiki with no page yet: start a repository and let the push create it.
            work.mkdir(parents=True, exist_ok=True)
            git('init', '--quiet', '-b', 'main', cwd=work)
            git('remote', 'add', 'origin', url, cwd=work)
            probe = git('ls-remote', '--exit-code', 'origin', cwd=work, check=False, auth=True)
            if probe.returncode == 128:
                print(f'{repo}: cannot reach {url}. Check that the project exists, is accessible '
                      f'with the token, and has the wiki feature on.\n{probe.stderr.strip()}',
                      file=sys.stderr)
                return False
        else:
            print(f'{repo}: cannot clone {url}. Open {repo_url(repo)}/wiki, create the first page '
                  f'once in the web interface, then run this again.\n{r.stderr.strip()}',
                  file=sys.stderr)
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
    # Commits in a published wiki carry the project's public identity, never a machine's own.
    git('-c', f'user.name={IDENTITY[0]}', '-c', f'user.email={IDENTITY[1]}',
        'commit', '--quiet', '-m', f'Sync from the docs ({sha})', cwd=work)
    branch = git('rev-parse', '--abbrev-ref', 'HEAD', cwd=work).stdout.strip()
    p = git('push', '--quiet', 'origin', f'HEAD:{branch}', cwd=work, check=False, auth=True)
    if p.returncode != 0:
        print(f'{repo}: push to {url} failed.\n{p.stderr.strip()}', file=sys.stderr)
        return False
    print(f'{repo}: pushed to {url}')
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--push', action='store_true', help='push each wiki to <repo>.wiki.git')
    ap.add_argument('--host', choices=sorted(HOSTS), default='gitlab', help='default: gitlab')
    ap.add_argument('--group', default=os.environ.get('GITLAB_GROUP', GITLAB_GROUP),
                    help='GitLab group (default: $GITLAB_GROUP or %s)' % GITLAB_GROUP)
    ap.add_argument('--repo', choices=sorted(WIKIS), help='only this wiki')
    a = ap.parse_args()
    HOST['name'] = a.host
    HOST['base'] = f'https://gitlab.com/{a.group}' if a.host == 'gitlab' else f'https://github.com/{GITHUB_ORG}'
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
