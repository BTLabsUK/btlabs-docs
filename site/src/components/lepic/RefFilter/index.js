/* RefFilter: the toolbar of the command reference and the filter state its cards read.
 *
 * <RefFilter commands={[{path, summary, tags: ['core' | 'repair'], group: bool}]}>
 *   ...the page: <RefGroup>## Global options ...</RefGroup>,
 *   <RefGroup paths={[path]}>## group heading, <CommandCard .../>...</RefGroup>
 * </RefFilter>
 *
 * - The toolbar: a filter field (matches a substring of the command path or its summary;
 *   "lepic " in the query is ignored) and the toggles All, Core and Repair with their counts.
 *   The count of matching commands is announced.
 * - CommandCard hides itself when it does not match (useRefMatch); RefGroup hides a group with
 *   no match, heading included. Group cards (`lepic tx`) show only while nothing is filtered.
 * - Without JavaScript, and before the reader filters, everything shows.
 */
import React, {createContext, useContext, useId, useMemo, useState} from 'react';
import clsx from 'clsx';
import {LdIcon} from '../kit';
import styles from './styles.module.css';

const Ctx = createContext(null);

const KINDS = [
  ['all', 'All'],
  ['core', 'Core'],
  ['repair', 'Repair'],
];

function normalize(q) {
  return q.trim().toLowerCase().replace(/^lepic(\s+|$)/, '').replace(/\s+/g, ' ');
}

function makeMatch(commands, query, kind) {
  const q = normalize(query);
  const byPath = new Map(commands.map((c) => [c.path, c]));
  return (path) => {
    const c = byPath.get(path);
    if (!c) return true;
    if (c.group) return kind === 'all' && !q;
    if (kind !== 'all' && !c.tags.includes(kind)) return false;
    return !q || c.path.includes(q) || c.summary.toLowerCase().includes(q);
  };
}

/** True when the command `path` shows under the current filter (always true outside RefFilter). */
export function useRefMatch(path) {
  const ctx = useContext(Ctx);
  return ctx ? ctx.match(path) : true;
}

/** A part of the page that shows while one of `paths` matches. Without `paths` (the global
 *  options, the exit codes) it shows while nothing is filtered. */
export function RefGroup({paths, children}) {
  const ctx = useContext(Ctx);
  const shown = !ctx || (paths ? paths.some((p) => ctx.match(p)) : !ctx.filtered);
  return (
    <div className={styles.group} hidden={!shown}>
      {children}
    </div>
  );
}

export default function RefFilter({commands, children}) {
  const [query, setQuery] = useState('');
  const [kind, setKind] = useState('all');
  const id = useId();
  const leaves = useMemo(() => commands.filter((c) => !c.group), [commands]);
  const counts = useMemo(
    () => ({
      all: leaves.length,
      core: leaves.filter((c) => c.tags.includes('core')).length,
      repair: leaves.filter((c) => c.tags.includes('repair')).length,
    }),
    [leaves],
  );
  const match = useMemo(() => makeMatch(commands, query, kind), [commands, query, kind]);
  const shown = leaves.filter((c) => match(c.path)).length;
  const filtered = kind !== 'all' || normalize(query) !== '';

  return (
    <Ctx.Provider value={{match, filtered}}>
      <div className={clsx('ldPanel ldBlock', styles.bar)} role="search" aria-label="Filter commands">
        <label className={clsx('ldFilter', styles.filter)} htmlFor={id}>
          <span className="ldSr">Filter commands</span>
          <LdIcon name="search" />
          <input
            id={id}
            className="ldFilter-input"
            type="search"
            name="command-filter"
            placeholder="Filter by command or summary…"
            autoComplete="off"
            spellCheck={false}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <div className={styles.row}>
          <ul className="ldChips" aria-label="Show">
            {KINDS.map(([k, label]) => (
              <li key={k}>
                <button type="button" className="ldChip" aria-pressed={kind === k} onClick={() => setKind(k)}>
                  {label}
                  <span className="ldChip-count">{counts[k]}</span>
                  <span className="ldSr"> commands</span>
                </button>
              </li>
            ))}
          </ul>
          <p className={clsx('ldMeta', styles.count)} aria-live="polite">
            {filtered ? `${shown} of ${counts.all} commands` : `${counts.all} commands`}
          </p>
        </div>
        {shown === 0 && (
          <p className={clsx('ldEmpty', styles.empty)}>
            No command matches “{query.trim()}”{kind !== 'all' ? ` among the ${kind} commands` : ''}.
          </p>
        )}
      </div>
      {children}
    </Ctx.Provider>
  );
}
