#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generates the two lepic command-line pages of the site.

    tools/gen-lepic-cli.py --bin <lepic binary> [--lepic <LEPIC checkout>]

--bin (or LEPIC_BIN) is a lepic binary built from LEPIC main (`cargo build --release -p lepic-cli`).
--lepic is the LEPIC checkout whose docs/cli.md and docs/recipes.md are read; default $LEPIC_REPO,
else ~/lepic.

It writes
  site/docs/developers/lepic/cli/index.mdx      from docs/cli.md: the text stays markdown, and the
                                                parts listed in GUIDE_PARTS become components
                                                (site/src/components/lepic).
  site/docs/developers/lepic/cli/reference.mdx  from `lepic <command> --help` for every command, with
                                                the core and repair tags of the cli.md group table
                                                and examples from the bash blocks of cli.md and
                                                recipes.md.
and deletes the .md pages they replace. Both pages are generated: change LEPIC's docs, its help
text or this script, not the pages.

The binary runs with an empty HOME, no LEPIC_* variables, NO_COLOR=1 and COLUMNS=100, so the help
shows the defaults and nothing of the machine it ran on. It stops, without writing, when a part of
cli.md is not the shape it expects or when the help and the group table name different commands.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lepic_mdx as M  # noqa: E402

TOOL = 'gen-lepic-cli'
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / 'site/docs/developers/lepic/cli'
GUIDE = OUT_DIR / 'index.mdx'
REFERENCE = OUT_DIR / 'reference.mdx'
REPLACED = [OUT_DIR / 'index.md', OUT_DIR / 'reference.md']
REF_URL = '/developers/lepic/cli/reference/'
COMPONENTS = '@site/src/components/lepic'

EVERYDAY = ['wallet init', 'wallet info', 'wallet address', 'epicbox listen', 'tx send', 'tx list',
            'tx show', 'invoice issue', 'contact invite', 'serve']
PAIRING_STEPS = 'The pairing steps'


def die(msg):
    M.die(TOOL, msg)


def anchor(path):
    """The reference card id of a command path such as 'tx send': lepic-tx-send."""
    return 'lepic-' + '-'.join(path.split())


def ref_href(path):
    return REF_URL + '#' + anchor(path)


def slug(text, seen):
    """GitHub's heading slug (github-slugger), which Docusaurus uses too."""
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', text)
    s = re.sub(r'[^\w\- ]', '', text.strip().lower()).replace(' ', '-')
    base, n = s, seen.get(s, 0)
    while s in seen:
        n += 1
        s = f'{base}-{n}'
    seen[base] = n
    seen.setdefault(s, 0)
    return s


def heading_slugs(body):
    seen, out, inside = {}, set(), False
    for line in body.split('\n'):
        if M.FENCE.match(line):
            inside = not inside
        elif not inside and (m := re.match(r'^#{1,6} +(.+?)\s*$', line)):
            out.add(slug(m.group(1), seen))
    return out


def join_parts(parts):
    """Text of blocks() parts again, as map_prose writes it."""
    return '\n'.join(M.fence(p[1], p[2], p[3]) if p[0] == 'code' else '\n'.join(p[1]) for p in parts)


def block(name, **props):
    return '\n' + M.component(name, **props) + '\n'


# ---------- the help ----------

def run_help(binary, path, home):
    env = {k: v for k, v in os.environ.items() if not k.startswith('LEPIC_')}
    env.update(HOME=home, USERPROFILE=home, NO_COLOR='1', COLUMNS='100')
    out = subprocess.run([binary, *path, '--help'], capture_output=True, text=True, env=env,
                         timeout=30, check=True)
    return out.stdout.rstrip('\n')


SECTION = re.compile(r'^([A-Z][A-Za-z ]*):$')


def sections(text):
    """{'about': [...], 'usage': [...], 'Options': [...], ..., 'after': [...]} of one help text.
    A section runs from its `Name:` line to the next one; the text after the last indented
    section (clap's after_help) is 'after'."""
    lines = text.split('\n')
    out, name = {'about': []}, 'about'
    for line in lines:
        m = SECTION.match(line)
        if line.startswith('Usage: '):
            name = 'usage'
            out[name] = [line[len('Usage: '):]]
            continue
        if m:
            name = m.group(1)
            out[name] = []
            continue
        if name not in ('about', 'after') and line and not line.startswith(' '):
            name = 'after'
            out.setdefault(name, [])
        out[name].append(line)
    return out


def paragraphs(lines):
    out, cur = [], []
    for ln in lines:
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


ENTRY = re.compile(r'^ {2,6}([-<\[].*)$')


def entries(lines):
    """Option or argument entries of a help section: [{'spec', 'help': [lines]}]."""
    out = []
    for ln in lines:
        m = ENTRY.match(ln)
        if m and not ln.startswith(' ' * 7):
            spec, rest = (re.split(r'\s{2,}', m.group(1).rstrip(), maxsplit=1) + [''])[:2]
            out.append({'spec': spec, 'help': [rest] if rest else []})
        elif out:
            out[-1]['help'].append(ln)
        elif ln.strip():
            die(f'help line outside an entry: {ln!r}')
    return out


META = re.compile(r'\s*\[(default|env|possible values): ([^\]]*)\]')


def first_sentence(text):
    return re.split(r'(?<=\.)\s+(?=[A-Z`])', text, maxsplit=1)[0]


def parse_entry(e, is_arg):
    help_text = '\n'.join(e['help'])
    meta = {}
    for m in META.finditer(help_text):
        meta.setdefault(m.group(1), m.group(2).strip())
    plain = META.sub('', help_text)
    values = []
    pv = re.search(r'Possible values:\n((?:\s*- .*\n?)+)', plain)
    if pv:
        values = [re.match(r'\s*- ([^:]+)', ln).group(1).strip() for ln in pv.group(1).split('\n') if ln.strip()]
        plain = plain[:pv.start()]
    elif 'possible values' in meta:
        values = [v.strip() for v in meta['possible values'].split(',')]
    paras = paragraphs(plain.split('\n'))
    text = first_sentence(' '.join(paras[0])) if paras else ''
    row = {'text': text}
    if is_arg:
        spec = e['spec']
        row['name'] = spec
        row['required'] = spec.startswith('<')
    else:
        m = re.match(r'^((?:-\w, )?--?[\w-]+)(.*)$', e['spec'])
        if not m:
            die(f'option entry not understood: {e["spec"]!r}')
        row['flag'] = m.group(1)
        if m.group(2).strip():
            row['value'] = m.group(2).strip()
    if 'default' in meta:
        row['default'] = meta['default']
    if 'env' in meta:
        row['env'] = meta['env']
    if values:
        row['values'] = values
    return row


def strip_global(text):
    """The help without its `Global options:` block, which every command repeats."""
    lines, out, skip = text.split('\n'), [], False
    for i, ln in enumerate(lines):
        if ln == 'Global options:':
            skip = True
            if out and out[-1] == '':
                out.pop()
            continue
        if skip:
            if ln == '' or ln.startswith(' '):
                continue
            skip = False
            out.append('')
        out.append(ln)
    return '\n'.join(out).rstrip('\n')


def walk(binary, home, path, out):
    text = run_help(binary, path, home)
    sec = sections(text)
    subs = []
    for e in sec.get('Commands', []):
        m = re.match(r'^  (\S+)(?:\s{2,}(.*))?$', e)
        if m and m.group(1) != 'help':
            subs.append((m.group(1), (m.group(2) or '').strip()))
        elif e.strip() and not m:
            # a wrapped summary line
            continue
    about = paragraphs(sec['about'])
    if not about:
        die(f'`lepic {" ".join(path)} --help` has no summary line')
    if 'usage' not in sec:
        die(f'`lepic {" ".join(path)} --help` has no Usage line')
    usage = '\n'.join(ln.strip() for ln in sec['usage'] if ln.strip())
    out.append({
        'path': ' '.join(path),
        'summary': ' '.join(about[0]),
        'usage': usage,
        'args': [parse_entry(e, True) for e in entries(sec.get('Arguments', []))],
        'options': [r for r in (parse_entry(e, False) for e in entries(sec.get('Options', [])))
                    if r['flag'] not in ('-h, --help', '-V, --version')],
        'global': [parse_entry(e, False) for e in entries(sec.get('Global options', []))],
        'exit': [ln for ln in sec.get('Exit codes', []) if ln.strip()],
        'help': strip_global(text),
        'subs': [{'name': n, 'path': ' '.join([*path, n]), 'summary': s} for n, s in subs],
    })
    for name, _ in subs:
        walk(binary, home, [*path, name], out)


def read_help(binary_arg):
    binary = Path(binary_arg).resolve()
    if not binary.is_file():
        die(f'no lepic binary at {binary}')
    with tempfile.TemporaryDirectory() as tmp:
        # clap prints the name it was started under: run it as `lepic`.
        link = Path(tmp) / 'lepic'
        link.symlink_to(binary)
        home = Path(tmp) / 'home'
        home.mkdir()
        version = subprocess.run([str(link), '--version'], capture_output=True, text=True,
                                 check=True).stdout.strip()
        cmds = []
        walk(str(link), str(home), [], cmds)
    return version, cmds


# ---------- docs/cli.md: the parts that become components ----------

def group_table(body):
    _, section, _ = M.split_section(TOOL, body, '### All commands by group')
    before, rows, after = M.find_table(TOOL, section, ['Group', 'Core', 'Other', 'Repair'],
                                       'docs/cli.md, All commands by group')
    groups = []
    for name, *cols in rows:
        runs = []
        for cell in cols:
            spans = M.code_spans(cell)
            if re.sub(r'`[^`]+`', '', cell).replace(',', '').strip():
                die(f'docs/cli.md, All commands by group: a cell that is not code spans: {cell!r}')
            runs.append(spans)
        groups.append({'name': name.strip('`'), 'core': runs[0], 'other': runs[1], 'repair': runs[2]})
    return section, before, groups, after


def start_here(section):
    parts = M.blocks(section)
    heading = parts[0][1][0]
    steps, tail, cur = [], [], None
    for k, part in enumerate(parts):
        if tail:
            tail.append(part)
            continue
        if part[0] == 'code':
            if cur is None or part[1] != 'bash':
                die('docs/cli.md, Start here: a code block that is not a step\'s bash block')
            if 'cmd' in cur:
                die(f'docs/cli.md, Start here: step {len(steps)} has two code blocks')
            cur['cmd'] = part[2].strip('\n')
            continue
        lines = part[1][1:] if k == 0 else part[1]
        for i, ln in enumerate(lines):
            if m := re.match(r'^\d+\. (.*)$', ln):
                cur = {'src': [m.group(1)]}
                steps.append(cur)
            elif ln.startswith('   ') and ln.strip() and cur is not None and 'cmd' not in cur:
                cur['src'].append(ln.strip())
            elif ln.strip() and not ln.startswith(' '):
                if not steps:
                    die('docs/cli.md, Start here: text before the numbered list')
                tail.append(('text', lines[i:]))
                break
    if not steps:
        die('docs/cli.md, Start here: no numbered list')
    out = []
    for n, s in enumerate(steps, 1):
        if 'cmd' not in s:
            die(f'docs/cli.md, Start here: step {n} has no bash block')
        src = ' '.join(s['src'])
        m = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', src)
        lead, text = (m.group(1), m.group(2)) if m else (None, src)
        out.append({'lead': M.inline(lead) if lead else None, 'text': M.inline(text), 'cmd': s['cmd']})
    return heading, out, join_parts(tail)


def job_table(section, slugs):
    before, rows, after = M.find_table(TOOL, section, ['I want to', 'Run', 'More'],
                                       'docs/cli.md, Find a command by job')
    if not 10 <= len(rows) <= 14:
        die(f'docs/cli.md, Find a command by job: {len(rows)} rows, expected 10 to 14')
    out = []
    for goal, run, more in rows:
        cmds = M.code_spans(run)
        if not cmds or ' then '.join(f'`{c}`' for c in cmds) != run or len(cmds) > 2:
            die(f'docs/cli.md, Find a command by job: Run is not one code span or two joined by " then ": {run!r}')
        m = re.fullmatch(M.LINK, more)
        if not m:
            die(f'docs/cli.md, Find a command by job: More is not one link: {more!r}')
        href = m.group(2)
        if href.startswith('#') and href[1:] not in slugs:
            die(f'docs/cli.md, Find a command by job: no heading for {href}')
        out.append({'goal': M.inline(goal), 'cmds': cmds, 'more': {'label': m.group(1), 'href': href}})
    return before, out, after


def command_rows(section, where, leaves, prefix=''):
    """Rows of a `| Command | What it does |` table as CommandList items, each linking to the
    reference card of the longest command path its code span starts with."""
    before, rows, after = M.find_table(TOOL, section, ['Command', 'What it does'], where)
    items = []
    for cmd, text in rows:
        spans = M.code_spans(cmd)
        if len(spans) != 1 or f'`{spans[0]}`' != cmd:
            die(f'{where}: the Command cell is not one code span: {cmd!r}')
        words = spans[0].split()
        if prefix:
            if words[0] != prefix:
                die(f'{where}: a command without `{prefix}`: {cmd!r}')
            words = words[1:]
        path = next((' '.join(words[:n]) for n in range(len(words), 0, -1) if ' '.join(words[:n]) in leaves), None)
        if path is None:
            die(f'{where}: names no command of the group table: {cmd!r}')
        items.append({'cmd': spans[0], 'href': ref_href(path), 'text': M.inline(text), 'path': path})
    return before, items, after


def pairing(section):
    parts = M.blocks(section)
    found = [i for i, p in enumerate(parts) if p[0] == 'code' and p[1] == 'mermaid']
    if len(found) != 1:
        die('docs/cli.md, The pairing steps: expected one mermaid block')
    seq = M.parse_sequence(TOOL, parts[found[0]][2])
    for s in seq['steps']:
        m = re.match(r'^(?:(\d+)\.\s+)?(.*)$', s['text'])
        s['num'] = m.group(1)
        rest = m.group(2)
        cmd, note = rest, ''
        if (p := re.match(r'^(.*?) \((.*)\)$', rest)):
            cmd, note = p.group(1), p.group(2)
        elif ', ' in rest:
            cmd, note = rest.split(', ', 1)
        s['cmd'], s['note'] = cmd, note
    before = join_parts(parts[:found[0]])
    after = join_parts(parts[found[0] + 1:])
    return before + '\n' + block('SequenceFlow', participants=seq['participants'], steps=seq['steps'],
                                 label='The pairing steps') + '\n' + after


def build_guide(lepic, leaves_from_table=None):
    title, body = M.read_source(TOOL, lepic / 'docs/cli.md', 'docs/cli.md')
    slugs = heading_slugs(body)

    section, before, groups, after = group_table(body)
    leaves = [c for g in groups for k in ('core', 'other', 'repair') for c in g[k]]
    if len(set(leaves)) != len(leaves):
        die('docs/cli.md, All commands by group: a command listed twice')
    core = [c for g in groups for c in g['core']]
    if sorted(core) != sorted(EVERYDAY):
        die(f'docs/cli.md, All commands by group: the Core column is not the ten everyday commands: {core}')
    leafset = set(leaves)
    body = body.replace(section, before.rstrip('\n') + '\n' + block('CommandGroups', groups=groups) + after, 1)

    # Start here
    b, section, a = M.split_section(TOOL, body, '## Start here')
    heading, steps, tail = start_here(section)
    for s in steps:
        for part in s['text']:
            if part['t'] == 'link' and part['href'].startswith('#') and part['href'][1:] not in slugs:
                die(f'docs/cli.md, Start here: no heading for {part["href"]}')
    body = '\n'.join([b, heading, block('Steps', steps=steps, label='Start here'), tail, a])

    # Find a command by job
    b, section, a = M.split_section(TOOL, body, '## Find a command by job')
    tb, rows, ta = job_table(section, slugs)
    body = '\n'.join([b, tb.rstrip('\n') + '\n' + block('JobTable', rows=rows) + ta, a])

    # The ten everyday commands
    b, section, a = M.split_section(TOOL, body, '### The ten everyday commands')
    tb, items, ta = command_rows(section, 'docs/cli.md, The ten everyday commands', leafset, prefix='lepic')
    if [i['path'] for i in items] != EVERYDAY:
        die('docs/cli.md, The ten everyday commands: not the ten commands of the contract, in order')
    for i in items:
        i['cmd'] = 'lepic ' + i['cmd'].split(' ', 1)[1]
        del i['path']
    body = '\n'.join([b, tb.rstrip('\n') + '\n' + block('CommandList', items=items, columns=2,
                                                        label='The ten everyday commands') + ta, a])

    # Contacts and pairing: the pairing steps and the stage tables
    b, contacts, a = M.split_section(TOOL, body, '## Contacts and pairing')
    sb, section, sa = M.split_section(TOOL, contacts, '### The pairing steps')
    contacts = '\n'.join([sb, pairing(section), sa])
    # every other ### part of the section that holds a `| Command | What it does |` table is a stage
    stages = [h for h in re.findall(r'^### (.+?)\s*$', contacts, re.M) if h != PAIRING_STEPS]
    stages = [h for h in stages if re.search(
        r'^\| Command \| What it does \|', M.split_section(TOOL, contacts, f'### {h}')[1], re.M)]
    if not stages:
        die('docs/cli.md, Contacts and pairing: no part with a Command table')
    for stage in stages:
        sb, section, sa = M.split_section(TOOL, contacts, f'### {stage}')
        where = f'docs/cli.md, {stage}'
        tb, items, ta = command_rows(section, where, leafset)
        if not re.search(r'\S', tb.split('\n', 1)[1] if '\n' in tb else ''):
            die(f'{where}: no sentence before the table')
        for i in items:
            del i['path']
        contacts = '\n'.join([sb, tb.rstrip('\n') + '\n' + block('CommandList', items=items, label=stage) + ta, sa])
    body = '\n'.join([b, contacts, a])

    if any(p[0] == 'code' and p[1] == 'mermaid' for p in M.blocks(body)):
        die('docs/cli.md: a mermaid block outside The pairing steps (the site has no mermaid)')
    body = re.sub(r'\n{3,}', '\n\n', body).strip('\n')

    imports = '\n'.join(f"import {n} from '{COMPONENTS}/{n}';" for n in
                        ['Steps', 'JobTable', 'CommandList', 'CommandGroups', 'SequenceFlow'])
    page = '\n\n'.join([
        M.front_matter(title=title, description='The lepic command-line wallet: the first commands, a '
                       'command for each job, and how each part works.'),
        imports,
        M.GENERATED % ('gen-lepic-cli.py', 'docs/cli.md'),
        f'# {title}',
        body,
    ]) + '\n'
    return page, groups, leafset


# ---------- examples from the bash blocks ----------

def examples(lepic, leaves, global_values):
    """{path: [{'cmd', 'note'}]}: the `lepic ...` lines of the bash blocks of cli.md, then
    recipes.md, each with its trailing `#` comment or the comment line above it."""
    out = {}
    for rel in ('docs/cli.md', 'docs/recipes.md'):
        for part in M.blocks((lepic / rel).read_text()):
            if part[0] != 'code' or part[1] != 'bash':
                continue
            lines = part[2].split('\n')
            i, above = 0, None
            while i < len(lines):
                ln = lines[i].rstrip()
                if ln.lstrip().startswith('#'):
                    above = ln.lstrip()[1:].strip()
                    i += 1
                    continue
                cmd = [ln]
                while cmd[-1].endswith('\\') and i + 1 < len(lines):
                    i += 1
                    cmd.append(lines[i].rstrip())
                i += 1
                note_above, above = above, None
                text = '\n'.join(cmd)
                if not text.startswith('lepic ') and text != 'lepic':
                    continue
                note = None
                if m := re.match(r'^(.*?)\s{2,}#\s?(.*)$', text, re.S):
                    text, note = m.group(1).rstrip(), m.group(2).strip()
                if re.search(r'&|\||;', text):
                    continue
                note = note or note_above
                if note:
                    note = re.sub(r'^\d+\.\s+', '', note)
                    note = note[0].upper() + note[1:]
                words = text.replace('\\\n', ' ').split()[1:]
                while words and words[0].startswith('-'):
                    flag = words.pop(0)
                    if flag in global_values and '=' not in flag and words:
                        words.pop(0)
                path = next((' '.join(words[:n]) for n in range(len(words), 0, -1)
                             if ' '.join(words[:n]) in leaves), None)
                if path is None:
                    continue
                lst = out.setdefault(path, [])
                key = ' '.join(text.split())
                if len(lst) < 3 and all(' '.join(e['cmd'].split()) != key for e in lst):
                    lst.append({'cmd': text, **({'note': note} if note else {})})
    return out


# ---------- the reference page ----------

def build_reference(version, cmds, groups, leafset, lepic):
    root = cmds[0]
    by_path = {c['path']: c for c in cmds}
    help_leaves = {c['path'] for c in cmds[1:] if not c['subs']}
    missing = sorted(help_leaves - leafset)
    extra = sorted(leafset - help_leaves)
    if missing or extra:
        die('the help and the group table of docs/cli.md disagree.'
            + (f' In the help only: {", ".join(missing)}.' if missing else '')
            + (f' In the table only: {", ".join(extra)}.' if extra else ''))
    top = [s['name'] for s in root['subs']]
    if top != [g['name'] for g in groups]:
        die(f'the groups of the table are not the commands of `lepic --help` in its order: {top}')
    tags = {}
    for g in groups:
        for c in g['core']:
            tags[c] = ['core']
        for c in g['repair']:
            tags[c] = ['repair']
    gvalues = {o['flag'].split(', ')[-1] for o in root['global'] if o.get('value')}
    ex = examples(lepic, leafset, gvalues)

    def card(c):
        props = {'path': c['path'], 'summary': c['summary'], 'usage': c['usage']}
        if c['path'] in tags:
            props['tags'] = tags[c['path']]
        if c['subs']:
            props['subs'] = c['subs']
        else:
            if ex.get(c['path']):
                props['examples'] = ex[c['path']]
            if c['args']:
                props['args'] = c['args']
            if c['options']:
                props['options'] = c['options']
        props['help'] = c['help']
        return M.component('CommandCard', **props)

    index = [{'path': c['path'], 'summary': c['summary'], 'tags': tags.get(c['path'], []),
              'group': bool(c['subs'])} for c in cmds[1:]]
    exits = []
    for ln in root['exit']:
        m = re.match(r'^\s*(\d+)\s{2,}(.*)$', ln)
        if not m:
            die(f'exit code line not understood: {ln!r}')
        kind, _, meaning = m.group(2).partition(': ')
        if not meaning:
            kind, meaning = '', m.group(2)
        exits.append(f'| {m.group(1)} | {"`" + kind + "`" if kind else ""} | {meaning} |')
    if not exits:
        die('`lepic --help` has no Exit codes block')

    out = [
        M.front_matter(title='lepic command reference', toc_max_heading_level=2,
                       description="Every lepic command and option, from the binary's own help."),
        "import CommandCard, {OptionRows} from '%s/CommandCard';\n"
        "import RefFilter, {RefGroup} from '%s/RefFilter';" % (COMPONENTS, COMPONENTS),
        M.GENERATED % ('gen-lepic-cli.py', '`lepic --help`'),
        '# lepic command reference',
        f'Generated from the help of `{version}`. The same text is in `lepic COMMAND --help`. '
        'Task-first examples are on the [command-line wallet](./index.mdx) page.',
        M.component('RefFilter', commands=index).replace('\n/>', '\n>'),
        '<RefGroup>',
        '## Global options',
        'Every command takes these options, before or after the command name. A flag overrides its '
        'environment variable, which overrides the config file.',
        M.component('OptionRows', options=root['global'], label='Global options'),
        '<details>\n<summary>Full help of lepic</summary>\n\n' + M.fence('text', root['help']) + '\n\n</details>',
        '## Exit codes',
        '| Code | Kind | Meaning |\n|---|---|---|\n' + '\n'.join(exits),
        '</RefGroup>',
    ]
    for g in root['subs']:
        paths = [c['path'] for c in cmds[1:] if c['path'] == g['path'] or c['path'].startswith(g['path'] + ' ')]
        out.append(M.component('RefGroup', paths=paths).replace('\n/>', '\n>'))
        out.append(f'## `{g["name"]}`')
        for p in paths:
            out.append(card(by_path[p]))
        out.append('</RefGroup>')
    out.append('</RefFilter>')
    return '\n\n'.join(out) + '\n', len(help_leaves), len(cmds) - 1 - len(help_leaves)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--bin', default=os.environ.get('LEPIC_BIN'), help='the lepic binary (LEPIC_BIN)')
    ap.add_argument('--lepic', default=os.environ.get('LEPIC_REPO') or str(Path.home() / 'lepic'),
                    help='the LEPIC checkout (LEPIC_REPO, else ~/lepic)')
    args = ap.parse_args()
    if not args.bin:
        die('pass --bin <lepic binary> or set LEPIC_BIN')
    lepic = Path(args.lepic).expanduser().resolve()
    if not (lepic / 'docs/cli.md').is_file():
        die(f'no docs/cli.md in {lepic}; pass --lepic <LEPIC checkout> or set LEPIC_REPO')

    guide, groups, leafset = build_guide(lepic)
    version, cmds = read_help(args.bin)
    reference, n_leaves, n_groups = build_reference(version, cmds, groups, leafset, lepic)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in ((GUIDE, M.with_notice(guide)), (REFERENCE, M.with_notice(reference))):
        if not path.exists() or path.read_text() != text:
            path.write_text(text)
            print(f'wrote {path.relative_to(ROOT)}')
        else:
            print(f'unchanged {path.relative_to(ROOT)}')
    for old in REPLACED:
        if old.exists():
            old.unlink()
            print(f'deleted {old.relative_to(ROOT)}')
    n_core = sum(len(g['core']) for g in groups)
    n_repair = sum(len(g['repair']) for g in groups)
    print(f'{version}: {n_leaves} commands and {n_groups} groups, {n_core} core, {n_repair} repair')


if __name__ == '__main__':
    main()
