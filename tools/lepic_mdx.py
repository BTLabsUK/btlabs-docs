# SPDX-License-Identifier: Apache-2.0
"""Shared by the LEPIC page generators (gen-lepic-cli.py, gen-lepic-recipes.py, gen-lepic-api.py).

LEPIC's markdown is the source: GitHub shows it as written, and the site turns it into MDX pages
whose marked parts are React components (site/src/components/lepic). This module holds what the
generators have in common: reading a file to the contract, link rewriting, table and diagram
parsing, and writing component props.

A generator stops (SystemExit) when a shape it expects is missing, so a change in LEPIC's docs
cannot ship a half-rendered page.
"""
import json
import posixpath
import re
import sys

GITHUB = 'https://github.com/BTLabsUK/lepic'

# LEPIC files that are pages of this site: repository path -> site path.
SITE = {
    'docs/cli.md': '/developers/lepic/cli/',
    'docs/recipes.md': '/developers/lepic/recipes/',
    'docs/api/README.md': '/developers/lepic/api/v1/',
    'docs/api/openapi.json': '/developers/lepic/api/v1/explorer/',
}

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')
POINTER = re.compile(r'^Interactive version: \[[^\]]+\]\(https://docs\.btlabs\.uk/[^)]*\)\.$')
LINK = re.compile(r'(?<!\!)\[((?:[^\]\\]|\\.)*)\]\(([^)\s]+)\)')
ALLOWED_HTML = re.compile(r'^</?(details|summary)>')


def die(tool, msg):
    sys.exit(f'{tool}: {msg}')


# ---------- blocks ----------

def blocks(text):
    """The file as a list of ('code', lang, body, indent) and ('text', lines) parts, in order.

    A fenced block is one part; the prose between two blocks is one part.
    """
    out, prose, lines, i = [], [], text.split('\n'), 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            prose.append(lines[i])
            i += 1
            continue
        indent, ticks, lang = m.group(1), m.group(2), m.group(3).strip()
        j = i + 1
        while j < len(lines) and not (lines[j].strip().startswith(ticks) and lines[j].strip().strip(ticks[0]) == ''):
            j += 1
        if prose:
            out.append(('text', prose))
            prose = []
        body = [ln[len(indent):] if ln.startswith(indent) else ln for ln in lines[i + 1:j]]
        out.append(('code', lang, '\n'.join(body), indent))
        i = j + 1
    if prose:
        out.append(('text', prose))
    return out


def fence(lang, body, indent=''):
    ticks = '```'
    while ticks in body:
        ticks += '`'
    return '\n'.join(indent + ln if ln else ln for ln in [ticks + lang, *body.split('\n'), ticks])


def map_prose(text, fn):
    """`text` with fn applied to each prose line; fenced blocks pass through unchanged."""
    out = []
    for part in blocks(text):
        if part[0] == 'code':
            out.append(fence(part[1], part[2], part[3]))
        else:
            out.append('\n'.join(fn(line) for line in part[1]))
    return '\n'.join(out)


def outside_code(line, fn):
    """fn applied to the pieces of a prose line that are not inside a code span."""
    pieces = re.split(r'(`+[^`]*`+)', line)
    return ''.join(p if p.startswith('`') else fn(p) for p in pieces)


# ---------- reading a LEPIC file ----------

def read_source(tool, path, repo_path):
    """(title, body) of a LEPIC markdown file, checked against the contract and made MDX-safe.

    Drops the `# Title` line and the `Interactive version:` pointer on line 3, rewrites the
    links (see rewrite_links), and stops on a bare `<`, `{` or `}` in prose or an HTML comment.
    """
    text = path.read_text()
    lines = text.split('\n')
    if not lines[0].startswith('# '):
        die(tool, f'{repo_path}: line 1 is not a `# Title`')
    if len(lines) < 3 or lines[1] != '' or not POINTER.match(lines[2]):
        die(tool, f'{repo_path}: line 3 is not the `Interactive version:` pointer')
    title = lines[0][2:].strip()
    body = '\n'.join(lines[3:]).strip('\n') + '\n'
    if '<!--' in body:
        die(tool, f'{repo_path}: an HTML comment (MDX cannot read it)')
    for n, part in enumerate(blocks(body)):
        if part[0] != 'text':
            continue
        for line in part[1]:
            bare = outside_code(line, lambda s: s)
            rest = ''.join(p for p in re.split(r'(`+[^`]*`+)', line) if not p.startswith('`'))
            stripped = rest.strip()
            if ALLOWED_HTML.match(stripped):
                rest = re.sub(r'</?(details|summary)>', '', rest)
            if re.search(r'[<{}]', rest):
                die(tool, f'{repo_path}: a bare <, {{ or }} outside code: {bare.strip()!r}')
    return title, rewrite_links(tool, body, repo_path)


def rewrite_links(tool, text, repo_path):
    """Relative links of a LEPIC file, made to work on the site.

    A link to a file that is a page here (SITE) becomes that page; any other file of the
    repository becomes its GitHub URL; a docs.btlabs.uk URL becomes its site path. Anchors
    within the page and other full URLs stay.
    """
    base = posixpath.dirname(repo_path)

    def one(m):
        label, target = m.group(1), m.group(2)
        if target.startswith('https://docs.btlabs.uk/'):
            # a page of this site: a site path, so the build checks it
            return f"[{label}]({target[len('https://docs.btlabs.uk'):]})"
        if re.match(r'^[a-z][a-z0-9+.-]*:', target) or target.startswith('#') or target.startswith('/'):
            return m.group(0)
        path, _, frag = target.partition('#')
        full = posixpath.normpath(posixpath.join(base, path))
        if full.startswith('..'):
            die(tool, f'{repo_path}: link leaves the repository: {target}')
        frag = '#' + frag if frag else ''
        if full == repo_path:
            return f'[{label}]({frag or SITE[repo_path]})'
        if full in SITE:
            return f'[{label}]({SITE[full]}{frag})'
        kind = 'tree' if path.endswith('/') or '.' not in posixpath.basename(full) else 'blob'
        return f'[{label}]({GITHUB}/{kind}/main/{full}{frag})'

    return map_prose(text, lambda line: outside_code(line, lambda s: LINK.sub(one, s)))


# ---------- sections ----------

def heading_level(line):
    m = re.match(r'^(#{1,6}) +\S', line)
    return len(m.group(1)) if m else 0


def split_section(tool, body, heading):
    """(before, section, after) for the section that starts at the exact heading line `heading`
    (such as '## Find a command by job') and runs to the next heading of the same or a higher
    level. `section` includes its heading line. Headings inside fenced blocks do not count."""
    level = heading_level(heading)
    lines, start, end, inside = body.split('\n'), None, None, False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            inside = not inside
            continue
        if inside:
            continue
        if start is None:
            if line.rstrip() == heading:
                start = i
        elif 0 < heading_level(line) <= level:
            end = i
            break
    if start is None:
        die(tool, f'section not found: {heading!r}')
    end = len(lines) if end is None else end
    return '\n'.join(lines[:start]), '\n'.join(lines[start:end]), '\n'.join(lines[end:])


# ---------- tables ----------

def table_cells(row):
    """Cells of one table row. `\\|` is a literal pipe inside a cell."""
    row = row.strip()
    if not (row.startswith('|') and row.endswith('|')):
        return None
    cells = re.split(r'(?<!\\)\|', row[1:-1])
    return [c.strip().replace('\\|', '|') for c in cells]


def find_table(tool, section, header, where):
    """(lines before, rows, lines after) for the first table of `section` (text) whose header
    row is exactly `header` (a list of cell texts). Rows are lists of cell texts."""
    lines = section.split('\n')
    for i, line in enumerate(lines):
        if table_cells(line) == header:
            if i + 1 >= len(lines) or not re.match(r'^\|[\s:|-]+\|$', lines[i + 1].strip()):
                break
            j, rows = i + 2, []
            while j < len(lines) and table_cells(lines[j]) is not None:
                cells = table_cells(lines[j])
                if len(cells) != len(header):
                    die(tool, f'{where}: a row with {len(cells)} cells, expected {len(header)}: {lines[j]!r}')
                rows.append(cells)
                j += 1
            return '\n'.join(lines[:i]), rows, '\n'.join(lines[j:])
    die(tool, f'{where}: no table with the header | {" | ".join(header)} |')


def code_spans(cell):
    """The code spans of a cell, in order, without their backticks."""
    return [m.group(2) for m in re.finditer(r'(`+)(.+?)\1', cell)]


def inline(text):
    """A cell or sentence as parts the `Inline` component renders:
    {'t': 'text'|'code'|'strong', 'v': ...} or {'t': 'link', 'v': label parts, 'href': ...}."""
    parts, pos = [], 0
    token = re.compile(r'(`+)(.+?)\1|\*\*(.+?)\*\*|(?<!\!)\[((?:[^\]\\]|\\.)*)\]\(([^)\s]+)\)')
    for m in token.finditer(text):
        if m.start() > pos:
            parts.append({'t': 'text', 'v': text[pos:m.start()]})
        if m.group(2) is not None:
            parts.append({'t': 'code', 'v': m.group(2)})
        elif m.group(3) is not None:
            parts.append({'t': 'strong', 'v': m.group(3)})
        else:
            parts.append({'t': 'link', 'v': inline(m.group(4)), 'href': m.group(5)})
        pos = m.end()
    if pos < len(text):
        parts.append({'t': 'text', 'v': text[pos:]})
    return parts


# ---------- diagrams ----------

def parse_sequence(tool, src):
    """A mermaid sequenceDiagram (contract subset) as
    {'participants': [{'id', 'label'}], 'steps': [{'kind': 'message'|'reply'|'note', 'from', 'to', 'text'}]}.
    A note's 'from' and 'to' are the first and last participant it spans."""
    lines = [ln.strip() for ln in src.strip().split('\n') if ln.strip()]
    if not lines or lines[0] != 'sequenceDiagram':
        die(tool, 'the pairing diagram is not a sequenceDiagram')
    people, steps = [], []
    for ln in lines[1:]:
        if m := re.match(r'^participant (\w+)(?: as (.+))?$', ln):
            people.append({'id': m.group(1), 'label': (m.group(2) or m.group(1)).strip()})
        elif m := re.match(r'^(\w+)(-->>|->>)(\w+): (.+)$', ln):
            steps.append({'kind': 'reply' if m.group(2) == '-->>' else 'message',
                          'from': m.group(1), 'to': m.group(3), 'text': m.group(4).strip()})
        elif m := re.match(r'^Note over (\w+)(?:,(\w+))?: (.+)$', ln):
            steps.append({'kind': 'note', 'from': m.group(1), 'to': m.group(2) or m.group(1),
                          'text': m.group(3).strip()})
        else:
            die(tool, f'sequenceDiagram line outside the contract: {ln!r}')
    ids = {p['id'] for p in people}
    for s in steps:
        if s['from'] not in ids or s['to'] not in ids:
            die(tool, f'sequenceDiagram names an undeclared participant: {s}')
    return {'participants': people, 'steps': steps}


def parse_states(tool, src):
    """A mermaid stateDiagram-v2 (contract subset) as
    {'start': [state], 'end': [state], 'transitions': [{'from', 'to', 'label'}]}."""
    lines = [ln.strip() for ln in src.strip().split('\n') if ln.strip()]
    if not lines or lines[0] != 'stateDiagram-v2':
        die(tool, 'the lifecycle diagram is not a stateDiagram-v2')
    start, end, moves = [], [], []
    for ln in lines[1:]:
        m = re.match(r'^(\[\*\]|\w+) --> (\[\*\]|\w+)(?:: (.+))?$', ln)
        if not m:
            die(tool, f'stateDiagram line outside the contract: {ln!r}')
        a, b, label = m.group(1), m.group(2), (m.group(3) or '').strip()
        if a == '[*]':
            start.append(b)
        elif b == '[*]':
            end.append(a)
        else:
            moves.append({'from': a, 'to': b, 'label': label})
    return {'start': start, 'end': end, 'transitions': moves}


# ---------- writing MDX ----------

def prop(value):
    """A value as a JSX attribute expression: `{...}`. JSON is valid JavaScript; `<` is escaped
    so a string can never open a tag in the page source."""
    return '{' + json.dumps(value, ensure_ascii=False).replace('<', '\\u003c') + '}'


def component(name, **props):
    """`<Name a={...} b={...} />` on its own lines, ready to sit between blank lines."""
    attrs = ''.join(f'\n  {k}={prop(v)}' for k, v in props.items())
    return f'<{name}{attrs}\n/>'


def front_matter(**fields):
    lines = ['---']
    for k, v in fields.items():
        lines.append(f'{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, str) else v}')
    return '\n'.join(lines + ['---'])


ALPHA_NOTICE = (
    ':::warning Alpha\n'
    'LEPIC is alpha and not ready for production use. Commands, the API and data formats can '
    'change between versions without a migration path.\n'
    ':::'
)


def with_notice(text):
    """The page with the alpha notice right after its first `# ` heading (outside code blocks)."""
    lines, fenced = text.split('\n'), False
    for i, ln in enumerate(lines):
        if FENCE.match(ln):
            fenced = not fenced
        elif not fenced and ln.startswith('# '):
            return '\n'.join(lines[:i + 1] + ['', ALPHA_NOTICE] + lines[i + 1:])
    die('with_notice', 'no top-level heading in the page')


GENERATED = '{/* Generated by tools/%s from LEPIC %s. Do not edit. */}'
