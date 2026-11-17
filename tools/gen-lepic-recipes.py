#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generates the lepic recipes page of the site from LEPIC's docs/recipes.md.

    tools/gen-lepic-recipes.py [--lepic <LEPIC checkout>]

--lepic is the LEPIC checkout; default $LEPIC_REPO, else ~/lepic.

It writes site/docs/developers/lepic/recipes.mdx. The text stays markdown. A recipe's `CLI:` and
`API:` blocks become two tabs ("CLI" and "curl") that switch together across the page and are kept
in the address (`?lepic-side=curl`); a recipe with one side shows that side's label over its
block. A row of links to the groups goes under the intro.

It stops, without writing, when the groups are not the ones docs/recipes.md is meant to have, in
their order, or when a `CLI:` or `API:` label is not followed by a bash block.
"""
import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lepic_mdx as M  # noqa: E402

TOOL = 'gen-lepic-recipes'
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'site/docs/developers/lepic/recipes.mdx'
GROUPS = ['Set up', 'Get paid', 'Pay', 'Invoices', 'Contacts', 'In person and links',
          'Run as a service', 'Fix and restore']
SIDES = {'CLI:': ('cli', 'CLI'), 'API:': ('curl', 'curl')}


def die(msg):
    M.die(TOOL, msg)


def slug(text, seen):
    """GitHub's heading slug (github-slugger), which Docusaurus uses too."""
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    s = re.sub(r'[^\w\- ]', '', text.strip().lower()).replace(' ', '-')
    base, n = s, seen.get(s, 0)
    while s in seen:
        n += 1
        s = f'{base}-{n}'
    seen[base] = n
    seen.setdefault(s, 0)
    return s


def headings(body):
    """[(level, text, slug)] outside fenced blocks."""
    seen, out, inside = {}, [], False
    for line in body.split('\n'):
        if M.FENCE.match(line):
            inside = not inside
        elif not inside and (m := re.match(r'^(#{1,6}) +(.+?)\s*$', line)):
            out.append((len(m.group(1)), m.group(2), slug(m.group(2), seen)))
    return out


def side_label(lines):
    """The side label ('CLI:' or 'API:') a text part ends with, and the text before it."""
    rest = list(lines)
    while rest and not rest[-1].strip():
        rest.pop()
    if rest and rest[-1].strip() in SIDES:
        if rest[-1] != rest[-1].strip():
            die(f'docs/recipes.md: an indented label {rest[-1]!r}')
        label = rest.pop().strip()
        return label, rest
    return None, lines


def tabs(sides):
    out = ['<Tabs groupId="lepic-side" queryString>']
    for label, body in sides:
        value, name = SIDES[label]
        out += [f'<TabItem value="{value}" label="{name}">', '', M.fence('bash', body), '', '</TabItem>']
    out.append('</Tabs>')
    return '\n'.join(out)


def single(label, body):
    return '\n'.join([f'<p><span className="ldTag">{SIDES[label][1]}</span></p>', '',
                      M.fence('bash', body)])


def convert(body):
    """The body with every CLI:/API: pair as tabs and every single side labelled."""
    parts = M.blocks(body)
    out, i, n_tabs, n_single = [], 0, 0, 0
    while i < len(parts):
        part = parts[i]
        if part[0] != 'text':
            out.append(M.fence(part[1], part[2], part[3]))
            i += 1
            continue
        label, before = side_label(part[1])
        if not label:
            out.append('\n'.join(part[1]))
            i += 1
            continue
        out.append('\n'.join(before))
        sides = []
        while label:
            if i + 1 >= len(parts) or parts[i + 1][0] != 'code' or parts[i + 1][1] != 'bash' or parts[i + 1][3]:
                die(f'docs/recipes.md: `{label}` is not followed by a bash block')
            sides.append((label, parts[i + 1][2]))
            i += 2
            label = None
            # A second side follows when the next text part holds only its label.
            if len(sides) == 1 and i < len(parts) and parts[i][0] == 'text':
                nxt, nbefore = side_label(parts[i][1])
                if nxt and not any(ln.strip() for ln in nbefore):
                    if nxt == sides[0][0]:
                        die(f'docs/recipes.md: two `{nxt}` blocks in a row')
                    if nxt != 'API:':
                        die('docs/recipes.md: `API:` comes before `CLI:`')
                    label = nxt
        if len(sides) == 2:
            out.append(tabs(sides))
            n_tabs += 1
        else:
            out.append(single(*sides[0]))
            n_single += 1
    text = '\n'.join(out)
    for line in text.split('\n'):
        if line.strip() in SIDES:
            die(f'docs/recipes.md: a `{line.strip()}` label left over')
    return text, n_tabs, n_single


def chips(heads):
    groups, counts, cur = [], {}, None
    for level, text, s in heads:
        if level == 2:
            cur = s
            groups.append((text, s))
            counts[s] = 0
        elif level == 3 and cur:
            counts[cur] += 1
    if [g for g, _ in groups] != GROUPS:
        die(f'docs/recipes.md: the groups are {[g for g, _ in groups]}, expected {GROUPS}')
    lines = ['<nav className="ldBlock" aria-label="Recipe groups">', '<ul className="ldChips">']
    for text, s in groups:
        lines.append(f'<li><Link className="ldChip" to="#{s}">{text}'
                     f'<span className="ldChip-count">{counts[s]}</span><span className="ldSr"> recipes</span></Link></li>')
    lines += ['</ul>', '</nav>']
    return '\n'.join(lines), sum(counts.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--lepic', default=os.environ.get('LEPIC_REPO') or str(Path.home() / 'lepic'),
                    help='the LEPIC checkout (LEPIC_REPO, else ~/lepic)')
    args = ap.parse_args()
    lepic = Path(args.lepic).expanduser().resolve()
    src = lepic / 'docs/recipes.md'
    if not src.is_file():
        die(f'no docs/recipes.md in {lepic}; pass --lepic <LEPIC checkout> or set LEPIC_REPO')

    title, body = M.read_source(TOOL, src, 'docs/recipes.md')
    nav, n_recipes = chips(headings(body))
    lines = body.split('\n')
    first = next((i for i, ln in enumerate(lines) if ln.startswith('## ')), None)
    intro, rest = '\n'.join(lines[:first]).strip('\n'), '\n'.join(lines[first:])
    rest, n_tabs, n_single = convert(rest)
    if any(p[0] == 'code' and p[1] == 'mermaid' for p in M.blocks(rest)):
        die('docs/recipes.md: a mermaid block (the site has no mermaid)')
    rest = re.sub(r'\n{3,}', '\n\n', rest).strip('\n')

    intro_line = next((ln for ln in intro.split('\n') if ln.strip()), '')
    page = '\n\n'.join([
        M.front_matter(title=title, description='Task-by-task examples for lepic, each with the '
                       'command and the matching API call.'),
        "import Tabs from '@theme/Tabs';\nimport TabItem from '@theme/TabItem';\n"
        "import Link from '@docusaurus/Link';",
        M.GENERATED % ('gen-lepic-recipes.py', 'docs/recipes.md'),
        f'# {title}',
        intro,
        nav,
        rest,
    ]) + '\n'
    if not intro_line:
        die('docs/recipes.md: no intro before the first group')

    page = M.with_notice(page)
    if not OUT.exists() or OUT.read_text() != page:
        OUT.write_text(page)
        print(f'wrote {OUT.relative_to(ROOT)}')
    else:
        print(f'unchanged {OUT.relative_to(ROOT)}')
    print(f'{n_recipes} recipes in {len(GROUPS)} groups: {n_tabs} with both sides, {n_single} with one')


if __name__ == '__main__':
    main()
