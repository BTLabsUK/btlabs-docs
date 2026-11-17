import React, {createContext, useContext, useEffect, useMemo, useRef, useState} from 'react';
import {useLocation} from '@docusaurus/router';
import useBrokenLinks from '@docusaurus/useBrokenLinks';
import {Cmd, LdIcon, Tag} from '@site/src/components/lepic/kit';
import styles from './styles.module.css';

/**
 * A read-only browser for the lepic serve OpenAPI document. No request leaves the page: there is
 * no try-it, and nothing loads from a CDN. The generated explorer.mdx gives one markdown heading
 * per tag inside <ApiTag>, so the table of contents and the #tag-* anchors are the site's own;
 * each operation's id is its operationId (#approvePayment), which the guide links to.
 *
 * Everything renders on the server: every operation with its parameters, request body and the
 * fields of its answers. A named schema inside a field opens on request, below its row.
 */
const METHODS = ['get', 'put', 'post', 'patch', 'delete'];
const Ctx = createContext(null);

export function tagId(name) {
  return 'tag-' + name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

/* ---------- text ---------- */

/** Descriptions use `code`, **bold** and blank-line paragraphs, nothing else. */
function Inline({text}) {
  const parts = String(text || '').split(/(`[^`]*`|\*\*[^*]+\*\*)/g);
  return parts.map((p, i) => {
    if (p.startsWith('`') && p.endsWith('`') && p.length > 1) return <code key={i}>{p.slice(1, -1)}</code>;
    if (p.startsWith('**') && p.endsWith('**') && p.length > 4) return <strong key={i}>{p.slice(2, -2)}</strong>;
    return <React.Fragment key={i}>{p}</React.Fragment>;
  });
}

function Prose({text, className}) {
  if (!text) return null;
  return String(text)
    .trim()
    .split(/\n{2,}/)
    .map((para, i) => (
      <p key={i} className={className}>
        <Inline text={para.replace(/\n/g, ' ')} />
      </p>
    ));
}

/* ---------- spec helpers ---------- */

function lookup(spec, ref) {
  return ref
    .replace(/^#\//, '')
    .split('/')
    .reduce((cur, part) => (cur == null ? cur : cur[part]), spec);
}
const schemaRef = (s) => s && s.$ref && /^#\/components\/schemas\/[^/]+$/.test(s.$ref) ? s.$ref.split('/').pop() : null;
const deref = (spec, s) => (s && s.$ref ? deref(spec, lookup(spec, s.$ref)) : s);

function operations(spec) {
  const out = [];
  for (const [path, item] of Object.entries(spec.paths)) {
    for (const method of METHODS) if (item[method]) out.push({path, method, op: item[method], item});
  }
  return out;
}

function matches(o, q) {
  if (!q) return true;
  const hay = `${o.method} ${o.path} ${o.op.summary || ''} ${o.op.operationId || ''} ${(o.op.tags || []).join(' ')}`.toLowerCase();
  return q.split(/\s+/).every((w) => hay.includes(w));
}

/* ---------- curl ---------- */

function placeholder(path, name, before) {
  if (name !== 'id') return name.toUpperCase();
  const seg = (before || 'item').replace(/s$/, '');
  return `${seg.replace(/[^a-z0-9]+/gi, '_').toUpperCase()}_ID`;
}

function sample(spec, name, s) {
  s = deref(spec, s) || {};
  if (s.enum) return s.enum[0];
  if ('const' in s) return s.const;
  if ('default' in s) return s.default;
  const t = Array.isArray(s.type) ? s.type.find((x) => x !== 'null') : s.type;
  if (t === 'integer' || t === 'number') return s.minimum ?? 1;
  if (t === 'boolean') return true;
  if (t === 'array') return [];
  if (t === 'object') return {};
  return name.toUpperCase();
}

/** The call in the guide's socket form, built from the method, the path and the required body fields. */
export function curlLine(spec, {path, method, op}) {
  const segs = path.split('/');
  const url = segs.map((seg, i) => seg.replace(/^\{(\w+)\}$/, (_, n) => placeholder(path, n, segs[i - 1]))).join('/');
  let line = 'curl --unix-socket ./w.sock';
  if (method !== 'get') line += ` -X ${method.toUpperCase()}`;
  line += ` http://lepic/api/v1${url}`;
  const media = op.requestBody && deref(spec, op.requestBody).content?.['application/json'];
  if (media && media.schema) {
    const s = deref(spec, media.schema);
    const body = {};
    for (const name of s.required || []) body[name] = sample(spec, name, s.properties?.[name]);
    line += ` \\\n  -H 'content-type: application/json' -d '${JSON.stringify(body)}'`;
  }
  return line;
}

/* ---------- types and fields ---------- */

/** A short type label. A named schema is a button that opens its fields under the row. */
function TypeLabel({spec, schema, open, onToggle, seen}) {
  if (!schema) return <span>any</span>;
  const name = schemaRef(schema);
  if (name) {
    if (seen.includes(name) || !onToggle) return <span className={styles.typeName} translate="no">{name}</span>;
    return (
      <button type="button" className={`ldFocus ${styles.refButton}`} aria-expanded={open.includes(name)} onClick={() => onToggle(name)}>
        {name}
        <LdIcon name="chevron" className={styles.refChev} />
      </button>
    );
  }
  if (schema.$ref) return <TypeLabel spec={spec} schema={lookup(spec, schema.$ref)} open={open} onToggle={onToggle} seen={seen} />;
  const sub = (s) => <TypeLabel spec={spec} schema={s} open={open} onToggle={onToggle} seen={seen} />;
  if (schema.enum) {
    return (
      <span>
        one of{' '}
        {schema.enum.map((v, i) => (
          <React.Fragment key={String(v)}>
            {i > 0 && ', '}
            <code>{String(v)}</code>
          </React.Fragment>
        ))}
      </span>
    );
  }
  for (const key of ['oneOf', 'anyOf', 'allOf']) {
    if (schema[key]) {
      return (
        <span>
          {schema[key].map((s, i) => (
            <React.Fragment key={i}>
              {i > 0 && (key === 'allOf' ? ' and ' : ' or ')}
              {sub(s)}
            </React.Fragment>
          ))}
        </span>
      );
    }
  }
  let t = schema.type || 'any';
  if (Array.isArray(t)) t = t.join(' or ');
  if (t === 'array') return <span>array of {sub(schema.items)}</span>;
  if (t === 'object' && schema.additionalProperties && !schema.properties) {
    return <span>map of {typeof schema.additionalProperties === 'object' ? sub(schema.additionalProperties) : 'any'}</span>;
  }
  const extra = [];
  if (schema.format) extra.push(schema.format);
  if ('const' in schema) extra.push(`always ${JSON.stringify(schema.const)}`);
  if (schema.pattern) extra.push(`pattern ${schema.pattern}`);
  if (schema.minimum !== undefined || schema.maximum !== undefined) extra.push(`${schema.minimum ?? ''}..${schema.maximum ?? ''}`);
  if (schema.minLength !== undefined || schema.maxLength !== undefined) extra.push(`length ${schema.minLength ?? 0}..${schema.maxLength ?? ''}`);
  if (schema.maxItems !== undefined || schema.minItems !== undefined) extra.push(`${schema.minItems ?? 0}..${schema.maxItems ?? ''} items`);
  if ('default' in schema) extra.push(`default ${JSON.stringify(schema.default)}`);
  return (
    <span>
      {t}
      {extra.length > 0 && ` (${extra.join(', ')})`}
    </span>
  );
}

/** The named schemas a field's type mentions, so their fields can open under the row. */
function refsOf(spec, s, out = []) {
  if (!s) return out;
  const name = schemaRef(s);
  if (name) {
    if (!out.includes(name)) out.push(name);
    return out;
  }
  if (s.$ref) return refsOf(spec, lookup(spec, s.$ref), out);
  for (const key of ['oneOf', 'anyOf', 'allOf']) (s[key] || []).forEach((x) => refsOf(spec, x, out));
  if (s.items) refsOf(spec, s.items, out);
  if (s.additionalProperties && typeof s.additionalProperties === 'object') refsOf(spec, s.additionalProperties, out);
  return out;
}

/** Field rows of an object schema; an inline object's fields are indented under it. */
function Fields({spec, schema, seen = [], label}) {
  const s = deref(spec, schema) || {};
  const props = Object.entries(s.properties || {});
  if (props.length === 0) {
    return (
      <p className={styles.plainType}>
        <TypeLabel spec={spec} schema={schema} open={[]} seen={seen} />
      </p>
    );
  }
  const req = new Set(s.required || []);
  return (
    <ul className={styles.fields} aria-label={label}>
      {props.map(([name, p]) => (
        <Field key={name} spec={spec} name={name} schema={p} required={req.has(name)} seen={seen} />
      ))}
    </ul>
  );
}

function Field({spec, name, schema, required, seen, where}) {
  const [open, setOpen] = useState([]);
  const toggle = (n) => setOpen((o) => (o.includes(n) ? o.filter((x) => x !== n) : [...o, n]));
  const target = deref(spec, schema) || {};
  const inner = target.type === 'array' ? deref(spec, target.items) || {} : target;
  const inlineObject = !schemaRef(schema) && !schemaRef(target.items || {}) && inner.properties;
  const description = schema.description || target.description || '';
  return (
    <li className={styles.field}>
      <div className={styles.fieldHead}>
        <code className={`ldMono ${styles.fieldName}`} translate="no">{name}</code>
        <span className={styles.fieldType}>
          <TypeLabel spec={spec} schema={schema} open={open} onToggle={toggle} seen={seen} />
        </span>
        {where && <span className={styles.fieldType}>in {where}</span>}
        {required && <span className={styles.req}>required</span>}
      </div>
      {description && (
        <div className={styles.fieldText}>
          <Prose text={description} />
        </div>
      )}
      {inlineObject && <Fields spec={spec} schema={inner} seen={seen} label={`${name} fields`} />}
      {refsOf(spec, schema)
        .filter((n) => open.includes(n))
        .map((n) => (
          <div key={n} className={styles.nested}>
            <p className={styles.nestedTitle}>{n}</p>
            <Fields spec={spec} schema={spec.components.schemas[n]} seen={[...seen, n]} label={`${n} fields`} />
          </div>
        ))}
    </li>
  );
}

/* ---------- one operation ---------- */

function Section({title, children}) {
  return (
    <div className={styles.section}>
      <p className={styles.sectionTitle}>{title}</p>
      {children}
    </div>
  );
}

function Body({spec, schema}) {
  const name = schemaRef(schema);
  const s = deref(spec, schema) || {};
  return (
    <>
      {name && <p className={styles.schemaName}>{name}</p>}
      {s.description && <Prose text={s.description} className={styles.schemaText} />}
      <Fields spec={spec} schema={schema} seen={name ? [name] : []} label={name ? `${name} fields` : 'Fields'} />
    </>
  );
}

function Operation({spec, o}) {
  const {path, method, op, item} = o;
  const id = op.operationId;
  const role = op['x-role'];
  const params = [...(item.parameters || []), ...(op.parameters || [])].map((p) => deref(spec, p));
  const body = op.requestBody && deref(spec, op.requestBody);
  const bodyMedia = body && Object.entries(body.content || {});
  const responses = Object.entries(op.responses || {});
  return (
    <details className={styles.op} id={id}>
      <summary className={styles.opHead}>
        <LdIcon name="chevron" className={styles.opChev} />
        <Tag kind={method} />
        <code className={`ldMono ${styles.path}`} translate="no">{path}</code>
        <span className={styles.opSummary}>
          <Inline text={op.summary} />
        </span>
        {role && (
          <span className={`ldTag ${styles.role}`}>
            <span className="ldSr">Role </span>
            {role}
          </span>
        )}
      </summary>
      <div className={styles.opBody}>
        <p className={styles.meta}>
          <code className={`ldMono ${styles.opId}`} translate="no">{id}</code>
          {role && (
            <span>
              Role <code className="ldMono">{role}</code>
              {op['x-role-note'] ? ' or more' : ''}
            </span>
          )}
          {op['x-socket-only'] && <span>Unix socket only</span>}
          {op.deprecated && <span>Deprecated</span>}
          <a className={`ldLink ldFocus ${styles.selfLink}`} href={`#${id}`}>
            <LdIcon name="link" className={styles.linkIcon} />
            Link to this operation
          </a>
        </p>
        {op['x-role-note'] && (
          <p className={styles.note}>
            <Inline text={op['x-role-note']} />
          </p>
        )}
        <Prose text={op.description} className={styles.desc} />
        <Cmd label="Copy curl command">{curlLine(spec, o)}</Cmd>
        {params.length > 0 && (
          <Section title="Parameters">
            <ul className={styles.fields} aria-label="Parameters">
              {params.map((p) => (
                <Field key={`${p.in} ${p.name}`} spec={spec} name={p.name} schema={{...p.schema, description: p.description}} required={p.required} seen={[]} where={p.in} />
              ))}
            </ul>
          </Section>
        )}
        {bodyMedia &&
          bodyMedia.map(([ctype, media]) => (
            <Section key={ctype} title={`Request body, ${body.required ? 'required' : 'optional'}, ${ctype}`}>
              {media.schema && <Body spec={spec} schema={media.schema} />}
            </Section>
          ))}
        <Section title="Responses">
          <ul className={styles.responses}>
            {responses.map(([code, resp]) => {
              const r = deref(spec, resp) || {};
              const media = Object.entries(r.content || {})[0];
              const shared = Boolean(resp.$ref);
              return (
                <li key={code} className={styles.response}>
                  <div className={styles.responseHead}>
                    <code className={`ldMono ${styles.status}`} data-ok={code.startsWith('2') || undefined}>
                      {code}
                    </code>
                    <span className={styles.responseText}>
                      <Inline text={(r.description || '').replace(/\s*\(\d{3}\)\.?$/, '')} />
                    </span>
                    {media && <span className={styles.ctype}>{media[0]}</span>}
                  </div>
                  {media && media[1].schema && !shared && (
                    <div className={styles.responseBody}>
                      <Body spec={spec} schema={media[1].schema} />
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </Section>
      </div>
    </details>
  );
}

/* ---------- page ---------- */

/** One tag: the markdown heading the page gives it, then its operations. Hidden when the filter
 *  matches none of them. */
export function ApiTag({name, children}) {
  const ctx = useContext(Ctx);
  const {collectAnchor} = useBrokenLinks();
  const ops = ctx.byTag.get(name) || [];
  ops.forEach((o) => collectAnchor(o.op.operationId));
  const shown = ops.filter((o) => matches(o, ctx.q));
  return (
    <section className={styles.tag} hidden={shown.length === 0} aria-labelledby={tagId(name)}>
      {children}
      <div className={styles.ops}>
        {ops.map((o) => (
          <div key={o.op.operationId} hidden={!shown.includes(o)}>
            <Operation spec={ctx.spec} o={o} />
          </div>
        ))}
      </div>
    </section>
  );
}

export default function ApiExplorer({spec, children}) {
  const [query, setQuery] = useState('');
  const [allOpen, setAllOpen] = useState(false);
  const root = useRef(null);
  const location = useLocation();
  const all = useMemo(() => operations(spec), [spec]);
  const byTag = useMemo(() => {
    const m = new Map();
    for (const o of all) for (const t of o.op.tags || ['Other']) m.set(t, [...(m.get(t) || []), o]);
    return m;
  }, [all]);
  const tags = useMemo(() => {
    const names = (spec.tags || []).map((t) => t.name).filter((n) => byTag.has(n));
    return [...names, ...[...byTag.keys()].filter((n) => !names.includes(n))];
  }, [spec, byTag]);

  const q = query.trim().toLowerCase();
  const count = all.filter((o) => matches(o, q)).length;

  // #approvePayment opens that operation and scrolls to it, also when the filter hides it.
  useEffect(() => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const el = document.getElementById(id);
    if (!el) return;
    if (el.closest('[hidden]')) {
      setQuery('');
      return;
    }
    if (el.tagName === 'DETAILS' && !el.open) el.open = true;
    el.scrollIntoView({block: 'start'});
  }, [location.hash, q === '']);

  const toggleAll = () => {
    const next = !allOpen;
    root.current?.querySelectorAll('details[id]').forEach((d) => {
      d.open = next;
    });
    setAllOpen(next);
  };

  return (
    <Ctx.Provider value={{spec, byTag, q}}>
      <div className={styles.explorer} ref={root}>
        <div className={styles.toolbar}>
          <div className={styles.filterRow}>
            <label className="ldFilter">
              <span className="ldSr">Filter by path, name or tag</span>
              <LdIcon name="search" />
              <input
                className="ldFilter-input"
                type="search"
                name="filter"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Filter by path, name or tag…"
                autoComplete="off"
                spellCheck={false}
              />
            </label>
            <button type="button" className={`ldChip ${styles.toggleAll}`} onClick={toggleAll}>
              {allOpen ? 'Collapse all' : 'Expand all'}
            </button>
          </div>
          <p className={styles.count} aria-live="polite">
            {count === all.length ? `${all.length} operations` : `${count} of ${all.length} operations`}
          </p>
          <nav aria-label="Tags">
            <ul className="ldChips">
              {tags.map((t) => {
                const n = (byTag.get(t) || []).filter((o) => matches(o, q)).length;
                return (
                  <li key={t} hidden={n === 0}>
                    <a className="ldChip" href={`#${tagId(t)}`}>
                      {t} <span className="ldChip-count">{n}</span>
                    </a>
                  </li>
                );
              })}
            </ul>
          </nav>
        </div>
        {count === 0 && <p className="ldEmpty">No operation matches “{query}”.</p>}
        {children}
      </div>
    </Ctx.Provider>
  );
}
