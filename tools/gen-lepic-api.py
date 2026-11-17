#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generates the wallet API pages from LEPIC's docs/api.

    tools/gen-lepic-api.py [--lepic <checkout>]

The checkout is a LEPIC repository (default: $LEPIC_REPO, else ~/lepic). The script writes

  site/docs/developers/lepic/api/v1/index.mdx     the guide, from docs/api/README.md
  site/docs/developers/lepic/api/v1/reference.md  every operation, from docs/api/openapi.json
  site/docs/developers/lepic/api/v1/explorer.mdx  the browsable view of the spec, by tag
  site/static/lepic-openapi.json                  a copy of the spec

The guide stays markdown except for the parts the contract marks (LEPIC's docs/api/README.md):
`## First request` becomes <FirstRequest>, the lifecycle diagram and its table become
<PaymentLifecycle>, the `Rule:` paragraph is set as .ldRule, and the `## Endpoints by group`
table becomes <EndpointGroups>. The components are in site/src/components/lepic. A missing shape
stops the script.

The explorer page renders the copy of the spec with src/components/ApiExplorer: a static,
read-only page (no try-it, no request leaves it, no CDN). Its tag headings are markdown, so the
table of contents lists them; each operation's id is its operationId.

All four are generated: change the LEPIC source or this script, not the output.
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

import lepic_mdx as L

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'site/docs/developers/lepic/api/v1/reference.md'
GUIDE = ROOT / 'site/docs/developers/lepic/api/v1/index.mdx'
OLD_GUIDE = ROOT / 'site/docs/developers/lepic/api/v1/index.md'
EXPLORER = ROOT / 'site/docs/developers/lepic/api/v1/explorer.mdx'
STATIC = ROOT / 'site/static/lepic-openapi.json'
METHODS = ('get', 'put', 'post', 'patch', 'delete')


TOOL = 'gen-lepic-api.py'
README = 'docs/api/README.md'
EXPLORER_URL = L.SITE['docs/api/openapi.json']
GUIDE_DESCRIPTION = ('How to connect to the lepic serve wallet API, its roles and conventions, and how '
                     'payments, events and webhooks work.')


def die(msg):
    L.die('gen-lepic-api', msg)


def default_repo():
    return Path(os.environ.get('LEPIC_REPO', Path.home() / 'lepic'))


def tag_id(name):
    return 'tag-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def operations(spec):
    """[(method, path, op)] in the spec's order."""
    return [(m, p, item[m]) for p, item in spec['paths'].items() for m in METHODS if m in item]


def find_op(spec, call):
    """The operation of a call written `METHOD /path` (path relative to /api/v1), or None."""
    m = re.fullmatch(r'(GET|PUT|POST|PATCH|DELETE) (/\S*)', call.strip())
    if not m:
        return None
    op = spec['paths'].get(m.group(2), {}).get(m.group(1).lower())
    return op


def call_prop(spec, call, where):
    """A call as the components take it: method, path, and the explorer link when it maps."""
    m = re.fullmatch(r'(GET|PUT|POST|PATCH|DELETE) (/\S*)', call.strip())
    if not m:
        die(f'{where}: not a call (`METHOD /path`): {call!r}')
    op = find_op(spec, call)
    out = {'method': m.group(1).lower(), 'path': m.group(2)}
    if op and op.get('operationId'):
        out['href'] = f'{EXPLORER_URL}#{op["operationId"]}'
    return out


# Pages of this site as files, relative to the guide's folder, so Docusaurus checks the links.
# Explorer links keep their site path (the hash is an operation or tag id on that page).
FILES = {
    '/developers/lepic/cli/': '../../cli/index.mdx',
    '/developers/lepic/cli/reference/': '../../cli/reference.mdx',
    '/developers/lepic/recipes/': '../../recipes.mdx',
    '/developers/lepic/api/v1/reference/': 'reference.md',
}
SITE_LINK = re.compile(r'\]\((/developers/lepic/[^)#]*)(#[^)]*)?\)')


def file_links(text):
    """Site paths of the other LEPIC pages (from lepic_mdx.rewrite_links) become file links."""
    def one(m):
        f = FILES.get(m.group(1))
        return f'](' + f + (m.group(2) or '') + ')' if f else m.group(0)
    return L.map_prose(text, lambda line: L.outside_code(line, lambda s: SITE_LINK.sub(one, s)))


def paragraphs(lines):
    """Prose lines as paragraphs (lists of lines), split at blank lines."""
    out, cur = [], []
    for ln in lines:
        if ln.strip():
            cur.append(ln)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def first_request(section):
    """`## First request` -> the intro prose (if any) and the steps for <FirstRequest>."""
    parts = L.blocks(section.split('\n', 1)[1] if '\n' in section else '')
    steps, pending = [], None
    for part in parts:
        if part[0] == 'text':
            paras = paragraphs(part[1])
            if not paras:
                continue
            if len(paras) != 1:
                die(f'{README}: ## First request: each step is one sentence, found {len(paras)} paragraphs: {paras!r}')
            pending = ' '.join(ln.strip() for ln in paras[0])
        elif part[1] == 'bash':
            if pending is None:
                die(f'{README}: ## First request: a bash block without its sentence')
            steps.append({'lead': None, 'text': L.inline(pending), 'cmd': part[2].strip('\n')})
            pending = None
        elif part[1] == 'json':
            if not steps or 'answer' in steps[-1] or pending is not None:
                die(f'{README}: ## First request: a json block that does not follow a step\'s bash block')
            try:
                steps[-1]['answer'] = json.dumps(json.loads(part[2]), indent=2, ensure_ascii=False)
            except json.JSONDecodeError as e:
                die(f'{README}: ## First request: the answer of step {len(steps)} is not JSON: {e}')
        else:
            die(f'{README}: ## First request: a {part[1] or "plain"} block; only bash and json belong here')
    if pending is not None:
        die(f'{README}: ## First request: a sentence without its bash block: {pending!r}')
    if len(steps) != 3:
        die(f'{README}: ## First request has {len(steps)} steps, the contract says three')
    return steps


ACTION_PIECE = re.compile(r'^(?:and |or )?`([a-z_]+)`(.*)$')


def lifecycle(spec, section):
    """`## Payment lifecycle` -> (prose before, component, prose after)."""
    heading, _, rest = section.partition('\n')
    parts = L.blocks(rest)
    idx = [i for i, p in enumerate(parts) if p[0] == 'code' and p[1] == 'mermaid']
    if len(idx) != 1:
        die(f'{README}: ## Payment lifecycle needs exactly one mermaid block, found {len(idx)}')
    i = idx[0]
    if any(p[0] == 'code' for p in parts[:i] + parts[i + 1:]):
        die(f'{README}: ## Payment lifecycle: a fenced block other than the diagram')
    before = '\n'.join('\n'.join(p[1]) for p in parts[:i]).strip('\n')
    after = '\n'.join('\n'.join(p[1]) for p in parts[i + 1:]).strip('\n')
    diagram = L.parse_states(TOOL, parts[i][2])
    between, rows, after = L.find_table(TOOL, after, ['Status', 'Meaning', 'Calls in actions'],
                                        f'{README}: ## Payment lifecycle')
    names = []
    states = []
    for status, meaning, calls in rows:
        spans = L.code_spans(status)
        if len(spans) != 1 or status != f'`{spans[0]}`':
            die(f'{README}: lifecycle table: the status is not one code span: {status!r}')
        name = spans[0]
        names.append(name)
        actions = []
        if calls.strip() and calls.strip() != 'none':
            for piece in re.split(r',\s+(?![^(]*\))', calls.strip()):
                m = ACTION_PIECE.match(piece.strip())
                if not m:
                    die(f'{README}: lifecycle table, {name}: a call that does not start with a code span: {piece!r}')
                action, note = m.group(1), m.group(2).strip()
                call = f'POST /payments/{{id}}/{action}'
                prop = call_prop(spec, call, f'lifecycle table, {name}')
                if 'href' not in prop:
                    die(f'{README}: lifecycle table, {name}: `{action}` has no operation {call} in openapi.json')
                actions.append({'name': action, **prop, 'note': L.inline(note) if note else []})
        states.append({'name': name, 'meaning': L.inline(meaning), 'actions': actions,
                       'none': calls.strip() if not actions else None})
    known = set(names)
    used = set(diagram['start']) | set(diagram['end']) | {s for t in diagram['transitions'] for s in (t['from'], t['to'])}
    if used - known:
        die(f'{README}: the lifecycle diagram names states the table does not: {sorted(used - known)}')
    if known - used:
        die(f'{README}: the lifecycle table names states the diagram does not: {sorted(known - used)}')
    component = L.component('PaymentLifecycle', states=states, start=diagram['start'],
                            end=diagram['end'], moves=diagram['transitions'])
    pre = '\n\n'.join(x for x in (before.strip('\n'), between.strip('\n')) if x.strip())
    return heading, pre, component, after.strip('\n')


def rule(text):
    """The paragraph that starts with `Rule:` set as .ldRule; the rest as it is."""
    lines, out, found, i = text.split('\n'), [], False, 0
    while i < len(lines):
        if lines[i].startswith('Rule:') and (i == 0 or not lines[i - 1].strip()):
            j = i
            while j < len(lines) and lines[j].strip():
                j += 1
            out += ['<div className="ldRule">', '', *lines[i:j], '', '</div>']
            found, i = True, j
            continue
        out.append(lines[i])
        i += 1
    if not found:
        die(f'{README}: ## Payment lifecycle: no paragraph that starts with `Rule:`')
    return '\n'.join(out)


def endpoint_groups(spec, section):
    heading, _, rest = section.partition('\n')
    before, rows, after = L.find_table(TOOL, rest, ['Group', 'Calls', 'What it covers'],
                                       f'{README}: ## Endpoints by group')
    groups = []
    for group, calls, covers in rows:
        props = [call_prop(spec, c, f'endpoints table, {group}') for c in L.code_spans(calls)]
        if not props:
            die(f'{README}: endpoints table, {group}: no calls')
        tags = []
        for c in props:
            op = find_op(spec, f'{c["method"].upper()} {c["path"]}')
            for t in (op or {}).get('tags', []):
                if t not in tags:
                    tags.append(t)
        groups.append({'name': group, 'covers': L.inline(covers), 'calls': props,
                       'href': f'{EXPLORER_URL}#{tag_id(tags[0])}' if tags else None})
    return heading, before.strip('\n'), L.component('EndpointGroups', groups=groups), after.strip('\n')


def guide(spec, readme):
    title, body = L.read_source(TOOL, readme, README)
    body = file_links(body)
    pre, sec, post = L.split_section(TOOL, body, '## First request')
    steps = first_request(sec)
    first = '\n\n'.join(['## First request', L.component('FirstRequest', steps=steps)])
    body = pre.rstrip('\n') + '\n\n' + first + '\n\n' + post.lstrip('\n')

    pre, sec, post = L.split_section(TOOL, body, '## Payment lifecycle')
    head, before, comp, after = lifecycle(spec, sec)
    life = '\n\n'.join(x for x in (head, before, comp, rule(after)) if x.strip())
    body = pre.rstrip('\n') + '\n\n' + life + '\n\n' + post.lstrip('\n')

    pre, sec, post = L.split_section(TOOL, body, '## Endpoints by group')
    head, before, comp, after = endpoint_groups(spec, sec)
    groups = '\n\n'.join(x for x in (head, before, comp, after) if x.strip())
    body = pre.rstrip('\n') + '\n\n' + groups + '\n\n' + post.lstrip('\n')

    if '```mermaid' in body:
        die(f'{README}: a mermaid block outside ## Payment lifecycle (the site does not draw mermaid)')
    return '\n'.join([
        L.front_matter(title=title, description=GUIDE_DESCRIPTION), '',
        L.GENERATED % (TOOL, README), '',
        "import FirstRequest from '@site/src/components/lepic/FirstRequest';",
        "import PaymentLifecycle from '@site/src/components/lepic/PaymentLifecycle';",
        "import EndpointGroups from '@site/src/components/lepic/EndpointGroups';", '',
        f'# {title}', '',
        body.strip('\n'), ''])


def explorer(spec, n_ops):
    """The explorer page: a short intro, the download link, and one markdown heading per tag
    inside the component, so the table of contents and the anchors are the site's own."""
    tags = []
    for _, _, op in operations(spec):
        for t in op.get('tags', ['Other']):
            if t not in tags:
                tags.append(t)
    order = [t['name'] for t in spec.get('tags', []) if t['name'] in tags]
    order += [t for t in tags if t not in order]
    lines = [
        '---',
        'title: Wallet API v1 explorer',
        'description: "Browse the operations of the lepic serve wallet API by tag: paths, roles, parameters, request and response bodies."',
        'toc_max_heading_level: 2',
        '---', '',
        L.GENERATED % (TOOL, 'docs/api/openapi.json'), '',
        "import ApiExplorer, {ApiTag} from '@site/src/components/ApiExplorer';",
        "import spec from '@site/static/lepic-openapi.json';", '',
        '# Wallet API v1 explorer', '',
        f'The {n_ops} operations of the `lepic serve` wallet API, contract version {spec["info"]["version"]}, '
        f'in {len(order)} tags. Open an operation for its role, parameters, request body and responses. '
        'The page is read-only: it sends no request.', '',
        'How to connect, the roles and the conventions are in the [guide](index.mdx); the same content '
        'as one long page is the [reference](reference.md). The OpenAPI 3.1 document is '
        '[lepic-openapi.json](pathname:///lepic-openapi.json); a running serve returns it at '
        '`GET /api/v1/openapi.json`.', '',
        '<ApiExplorer spec={spec}>', '']
    for t in order:
        lines += [f'<ApiTag name={L.prop(t)}>', '', f'## {t} {{/* #{tag_id(t)} */}}', '', '</ApiTag>', '']
    lines += ['</ApiExplorer>', '']
    return '\n'.join(lines)


def esc(text):
    """One-line table-safe text: pipes escaped, angle brackets outside code spans escaped."""
    parts = re.split(r'(`[^`]*`)', ' '.join(str(text).split()))
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 0:
            p = p.replace('<', '&lt;').replace('>', '&gt;')
        out.append(p)
    return ''.join(out).replace('|', '\\|')


def para(text):
    parts = re.split(r'(`[^`]*`)', str(text).strip())
    return ''.join(p if i % 2 else p.replace('<', '&lt;').replace('>', '&gt;')
                   for i, p in enumerate(parts))


def op_anchor(path, method):
    return re.sub(r'[^a-z0-9]+', '-', f'{method} {path}'.lower()).strip('-')


def anchor(name):
    return 'schema-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


class Ctx:
    def __init__(self, spec):
        self.spec = spec
        self.schemas = spec['components']['schemas']
        self.used = set()

    def resolve(self, node):
        while '$ref' in node:
            node = self.lookup(node['$ref'])
        return node

    def lookup(self, ref):
        cur = self.spec
        for part in ref.lstrip('#/').split('/'):
            cur = cur[part]
        return cur

    def type_of(self, s):
        """A short type label; named schemas link to their section."""
        if '$ref' in s:
            name = s['$ref'].rsplit('/', 1)[-1]
            if re.fullmatch(r'#/components/schemas/[^/]+', s['$ref']):
                self.used.add(name)
                return f'[`{name}`](#{anchor(name)})'
            return self.type_of(self.lookup(s['$ref']))
        if 'enum' in s:
            return 'one of ' + ', '.join(f'`{v}`' for v in s['enum'])
        for key in ('oneOf', 'anyOf'):
            if key in s:
                return ' or '.join(self.type_of(x) for x in s[key])
        if 'allOf' in s:
            return ' + '.join(self.type_of(x) for x in s['allOf'])
        t = s.get('type', 'any')
        if t == 'array':
            return 'array of ' + self.type_of(s.get('items', {}))
        if t == 'object' and 'additionalProperties' in s and not s.get('properties'):
            ap = s['additionalProperties']
            return 'map of ' + (self.type_of(ap) if isinstance(ap, dict) else 'any')
        if isinstance(t, list):
            t = ' or '.join(t)
        extra = []
        if s.get('format'):
            extra.append(s['format'])
        if 'const' in s:
            extra.append(f"always {json.dumps(s['const'])}")
        if 'pattern' in s:
            extra.append(f"pattern {s['pattern']}")
        if 'maxLength' in s or 'minLength' in s:
            extra.append(f"length {s.get('minLength', 0)}..{s.get('maxLength', '')}")
        if 'maxItems' in s or 'minItems' in s:
            extra.append(f"{s.get('minItems', 0)}..{s.get('maxItems', '')} items")
        if 'example' in s:
            extra.append(f"example {json.dumps(s['example'])}")
        if 'minimum' in s or 'maximum' in s:
            extra.append(f"{s.get('minimum', '')}..{s.get('maximum', '')}")
        if 'default' in s:
            extra.append(f"default {json.dumps(s['default'])}")
        return f'`{t}`' + (f' ({esc(", ".join(extra))})' if extra else '')

    def fields(self, s):
        """Rows (name, type, required, description) of an object schema, nested ones dotted."""
        rows = []

        def walk(s, prefix):
            s = self.resolve(s) if '$ref' not in s or not s['$ref'].startswith('#/components/schemas/') else s
            props = s.get('properties', {})
            req = set(s.get('required', []))
            for name, p in props.items():
                full = prefix + name
                desc = p.get('description') or self.resolve(p).get('description', '')
                rows.append((full, self.type_of(p), name in req, desc))
                inner = p
                if inner.get('type') == 'array':
                    inner = inner.get('items', {})
                if '$ref' not in inner and inner.get('properties'):
                    walk(inner, full + ('[].' if p.get('type') == 'array' else '.'))
        walk(s, '')
        return rows


def table_fields(ctx, rows):
    out = ['| Field | Type | Required | Description |', '|---|---|---|---|']
    for name, typ, req, desc in rows:
        out.append(f'| `{name}` | {typ} | {"yes" if req else ""} | {esc(desc)} |')
    return out


def render_schema_body(ctx, s):
    """Lines describing a schema: its fields, or its type when it is not an object."""
    s_res = ctx.resolve(s) if '$ref' in s and not s['$ref'].startswith('#/components/schemas/') else s
    lines = []
    if s_res.get('description'):
        lines += [para(s_res['description']), '']
    base = s_res
    rows = ctx.fields(base)
    if rows:
        lines += table_fields(ctx, rows) + ['']
    else:
        lines += [f'Type: {ctx.type_of(base)}', '']
    return lines


def render_op(ctx, path, method, op):
    lines = [f'### `{method.upper()} {path}` {{#{op_anchor(path, method)}}}', '']
    lines += [para(op.get('summary', '')), '']
    role = op.get('x-role')
    meta = []
    if role:
        meta.append(f'Role: at least `{role}`' if op.get('x-role-note') else f'Role: `{role}`')
    if op.get('x-socket-only'):
        meta.append('Unix socket only')
    if op.get('deprecated'):
        meta.append('Deprecated')
    if meta:
        lines += ['. '.join(meta) + '.', '']
    if op.get('x-role-note'):
        lines += [f'**Role depends on the request:** {para(op["x-role-note"])}', '']
    if op.get('description'):
        lines += [para(op['description']), '']
    params = [ctx.resolve(p) for p in op.get('parameters', [])]
    params += [ctx.resolve(p) for p in ctx.spec['paths'][path].get('parameters', [])]
    if params:
        lines += ['| Parameter | In | Type | Description |', '|---|---|---|---|']
        for p in params:
            req = ' (required)' if p.get('required') else ''
            lines.append(f"| `{p['name']}` | {p['in']}{req} | {ctx.type_of(p.get('schema', {}))} | "
                         f"{esc(p.get('description', ''))} |")
        lines.append('')
    body = op.get('requestBody')
    if body:
        body = ctx.resolve(body)
        for ctype, media in body.get('content', {}).items():
            req = 'required' if body.get('required') else 'optional'
            sch = media.get('schema', {})
            lines += [f'**Request body** ({req}, `{ctype}`): {ctx.type_of(sch)}', '']
    lines += ['**Responses**', '', '| Status | Meaning |', '|---|---|']
    for code, resp in op.get('responses', {}).items():
        name = resp['$ref'].rsplit('/', 1)[-1] if '$ref' in resp else None
        r = ctx.resolve(resp)
        desc = re.sub(r'\s*\(\d{3}\)\.?$', '', r.get('description', '').strip()).rstrip('.')
        content = r.get('content', {})
        if content:
            sch = next(iter(content.values())).get('schema', {})
            if sch and not name:
                desc += f': {ctx.type_of(sch)}'
        lines.append(f'| {code} | {esc(desc) if "[" not in desc else desc.replace("|", chr(92) + "|")} |')
    lines.append('')
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lepic', default=str(default_repo()))
    args = ap.parse_args()
    spec_path = Path(args.lepic) / 'docs/api/openapi.json'
    spec = json.loads(spec_path.read_text())
    ctx = Ctx(spec)
    info = spec['info']

    ops = {}
    for path, item in spec['paths'].items():
        for m in METHODS:
            if m in item:
                for tag in item[m].get('tags', ['Other']):
                    ops.setdefault(tag, []).append((path, m, item[m]))
    n_ops = sum(len(v) for v in ops.values())

    lines = [
        '---',
        'title: Wallet API v1 reference',
        f'description: "Every endpoint of the `lepic serve` wallet API: paths, roles, parameters, request and response bodies."',
        '---', '',
        '<!-- Generated by tools/gen-lepic-api.py from LEPIC docs/api/openapi.json. Do not edit. -->', '',
        '# Wallet API v1 reference', '',
        f'The reference of the `lepic serve` wallet API, version {info["version"]} of its contract: '
        f'{n_ops} operations under `/api/v1`. How to connect, the roles and the conventions are in '
        'the [guide](index.mdx). A running serve returns the same document at `GET /api/v1/openapi.json`; '
        'a copy is at [lepic-openapi.json](pathname:///lepic-openapi.json).', '',
        'Every path below is relative to `/api/v1`. `Role` is the least role of an owner TLS client '
        'that may call the operation; the Unix socket always has `full`.', '',
        '## Operations', '',
    ]
    # Contents
    for tag in [t['name'] for t in spec.get('tags', []) if t['name'] in ops]:
        lines.append(f'- **{tag}**: ' + ', '.join(
            f'[`{m.upper()} {p}`](#{op_anchor(p, m)})'
            for p, m, _ in ops[tag]))
    lines.append('')
    for tag in [t['name'] for t in spec.get('tags', []) if t['name'] in ops]:
        lines += [f'## {tag}', '']
        for path, m, op in ops[tag]:
            lines += render_op(ctx, path, m, op)

    # Shared responses and schemas
    lines += ['## Errors', '',
              'Errors are RFC 9457 problem documents (`application/problem+json`), the '
              f'[`Problem`](#{anchor("Problem")}) schema. These shared responses are named in the tables above.', '',
              '| Response | Meaning |', '|---|---|']
    ctx.used.add('Problem')
    for name, r in spec['components'].get('responses', {}).items():
        lines.append(f'| `{name}` | {esc(r.get("description", ""))} |')
    lines.append('')

    lines += ['## Schemas', '']
    done = set()
    # referenced schemas can reference more: iterate to a fixed point
    while True:
        todo = [n for n in ctx.schemas if n in ctx.used and n not in done]
        if not todo:
            break
        for name in todo:
            done.add(name)
            s = ctx.schemas[name]
            lines += [f'### {name} {{#{anchor(name)}}}', '']
            lines += render_schema_body(ctx, s)
    out = '\n'.join(lines).rstrip() + '\n'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out)
    STATIC.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(spec_path, STATIC)
    EXPLORER.write_text(explorer(spec, n_ops))
    GUIDE.write_text(guide(spec, Path(args.lepic) / README))
    if OLD_GUIDE.exists():
        OLD_GUIDE.unlink()
    print(f'wrote {GUIDE.relative_to(ROOT)}, {OUT.relative_to(ROOT)}, {EXPLORER.relative_to(ROOT)} ({n_ops} operations, {len(done)} schemas) and {STATIC.relative_to(ROOT)}')


if __name__ == '__main__':
    sys.exit(main())
