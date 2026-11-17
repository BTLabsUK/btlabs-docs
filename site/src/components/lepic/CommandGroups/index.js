/* CommandGroups: every command, one row per group, in three runs (Core, Other, Repair), with a
 * filter (All commands by group).
 *
 * <CommandGroups groups={[{name: string, core: [path], other: [path], repair: [path]}]} />
 *
 * - A path is a full command path without `lepic ` ("contact payload post"). Each command is a
 *   chip linking to its card in the reference (/developers/lepic/cli/reference/#lepic-...).
 * - The filter matches a substring of the path ("lepic " in the query is ignored), hides what
 *   does not match and announces the count. Everything renders without JavaScript.
 */
import React, {useId, useMemo, useState} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import {LdIcon} from '../kit';
import styles from './styles.module.css';

const REF = '/developers/lepic/cli/reference/#lepic-';
const RUNS = [
  ['core', 'Core'],
  ['other', 'Other'],
  ['repair', 'Repair'],
];

export function normalizeQuery(q) {
  return q.trim().toLowerCase().replace(/^lepic(\s+|$)/, '').replace(/\s+/g, ' ');
}

export default function CommandGroups({groups}) {
  const [query, setQuery] = useState('');
  const id = useId();
  const q = normalizeQuery(query);
  const total = useMemo(() => groups.reduce((n, g) => n + g.core.length + g.other.length + g.repair.length, 0), [groups]);
  const match = (p) => !q || p.includes(q);
  const shown = groups.map((g) => ({
    ...g,
    runs: RUNS.map(([k, label]) => ({k, label, cmds: g[k].filter(match)})).filter((r) => r.cmds.length),
  }));
  const count = shown.reduce((n, g) => n + g.runs.reduce((m, r) => m + r.cmds.length, 0), 0);

  return (
    <div className={clsx('ldBlock', styles.wrap)}>
      <div className={styles.bar}>
        <label className={clsx('ldFilter', styles.filter)} htmlFor={id}>
          <span className="ldSr">Find a command</span>
          <LdIcon name="search" />
          <input
            id={id}
            className="ldFilter-input"
            type="search"
            name="command-filter"
            placeholder="Find a command…"
            autoComplete="off"
            spellCheck={false}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <p className={clsx('ldMeta', styles.count)} aria-live="polite">
          {q ? `${count} of ${total} commands` : `${total} commands`}
        </p>
      </div>
      {count === 0 ? (
        <p className="ldEmpty">No command matches “{query.trim()}”.</p>
      ) : (
        <ul className={clsx('ldPanel ldPanel--flush', styles.list)} aria-label="Commands by group">
          {shown.map(
            (g) =>
              g.runs.length > 0 && (
                <li key={g.name} className={styles.group}>
                  <code className={clsx('ldMono', styles.name)} translate="no">{g.name}</code>
                  <div className={styles.runs}>
                    {g.runs.map((r) => (
                      <div key={r.k} className={styles.run}>
                        <span className={clsx('ldLabel', styles.runLabel)} id={`${id}-${g.name}-${r.k}`}>
                          {r.label}
                        </span>
                        <ul className="ldChips" aria-labelledby={`${id}-${g.name}-${r.k}`}>
                          {r.cmds.map((p) => (
                            <li key={p}>
                              <Link
                                className={clsx('ldChip ldChip--cmd', r.k === 'core' && styles.core)}
                                to={REF + p.split(' ').join('-')}>
                                {p.startsWith(g.name + ' ') ? (
                                  <>
                                    <span className="ldSr">{g.name} </span>
                                    {p.slice(g.name.length + 1)}
                                  </>
                                ) : (
                                  p
                                )}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </li>
              ),
          )}
        </ul>
      )}
    </div>
  );
}
