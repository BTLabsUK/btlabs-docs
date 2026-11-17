import React, {useState} from 'react';
import Link from '@docusaurus/Link';
import useBrokenLinks from '@docusaurus/useBrokenLinks';
import {Tag, LdIcon} from '../kit';
import Inline from '../Inline';
import styles from './styles.module.css';

/* "Payment lifecycle" of the API guide, from the source's stateDiagram-v2 and its status table.
 *
 *  1. The main path as a rail (horizontal when the panel has room for it, vertical otherwise).
 *     Entry states are marked "starts here"; the last state of the path "ends here".
 *  2. The other endings, one row each with the moves into them; shortcuts and late moves as lists.
 *  3. One row per state: meaning, the calls in `actions` (chips to the explorer), then.
 *
 * Every move of the diagram is drawn once, as an element with data-from, data-to and data-label
 * (`[*]` for the start and the end): moves between states in 1 or 2, starts on the rail's
 * "starts here", ends in the "Then" column of 3.
 * Props from tools/gen-lepic-api.py: states (table order), start, end, moves. */

const rowId = (name) => `lifecycle-${name.replace(/_/g, '-')}`;

/** The longest path of forward moves (in table order) from a start state; ties go to the
 *  earliest target, so the path reads the way the table does. */
function mainPath(order, start, moves) {
  const idx = new Map(order.map((s, i) => [s, i]));
  const best = new Map();
  const walk = (s) => {
    if (best.has(s)) return best.get(s);
    let path = [s];
    const out = moves.filter((m) => m.from === s && idx.get(m.to) > idx.get(s)).sort((a, b) => idx.get(a.to) - idx.get(b.to));
    for (const m of out) {
      const p = [s, ...walk(m.to)];
      if (p.length > path.length) path = p;
    }
    best.set(s, path);
    return path;
  };
  let path = [];
  for (const s of start) {
    const p = walk(s);
    if (p.length > path.length) path = p;
  }
  return path;
}

function St({name}) {
  return (
    <code className={`ldMono ${styles.st}`} translate="no">
      {name}
    </code>
  );
}

function Move({m, children, className}) {
  return (
    <span className={className} data-from={m.from} data-to={m.to} data-label={m.label}>
      {children}
    </span>
  );
}

function StartMark({name, start}) {
  return start.includes(name) ? (
    <Move m={{from: '[*]', to: name, label: ''}} className={styles.mark}>
      starts here
    </Move>
  ) : null;
}

export default function PaymentLifecycle({states, start, end, moves}) {
  const {collectAnchor} = useBrokenLinks();
  const [active, setActive] = useState(null);
  const order = states.map((s) => s.name);
  const path = mainPath(order, start, moves);
  const onPath = new Set(path);
  const rail = new Set(path.slice(1).map((to, i) => `${path[i]}>${to}`));
  const railMove = (from, to) => moves.find((m) => m.from === from && m.to === to);

  const endings = order.filter((s) => !onPath.has(s) && end.includes(s));
  const intoEnding = new Set(endings);
  const shortcuts = moves.filter((m) => onPath.has(m.from) && onPath.has(m.to) && !rail.has(`${m.from}>${m.to}`));
  const late = moves.filter((m) => intoEnding.has(m.from));
  const placed = new Set([...rail, ...shortcuts.map((m) => `${m.from}>${m.to}`), ...late.map((m) => `${m.from}>${m.to}`)]);
  const other = moves.filter((m) => !intoEnding.has(m.to) && !placed.has(`${m.from}>${m.to}`));
  // States off the main path that are not endings still need a place for their start mark (their ends show in their rows).
  const loose = order.filter((s) => !onPath.has(s) && !intoEnding.has(s));

  const hover = (name) => ({
    onMouseEnter: () => setActive(name),
    onMouseLeave: () => setActive(null),
    onFocus: () => setActive(name),
    onBlur: () => setActive(null),
  });

  for (const s of order) collectAnchor(rowId(s));

  return (
    <div className={`ldBlock ${styles.wrap}`}>
      <figure className={`ldPanel ldPanel--ticked ${styles.figure}`}>
        <figcaption className="ldSr">How the status of a payment moves</figcaption>
        <p className="ldLabel">Main path</p>
        <ol className={styles.rail} style={{'--rail-cols': `repeat(${path.length - 1}, auto minmax(max-content, 1fr)) auto`}}>
          {path.map((s, i) => {
            const last = i === path.length - 1;
            const m = last ? null : railMove(s, path[i + 1]);
            return (
              <li key={s} className={styles.railItem}>
                <a href={`#${rowId(s)}`} className={`ldLink ldFocus ${styles.node}`} data-active={active === s || undefined} {...hover(s)}>
                  <St name={s} />
                  <StartMark name={s} start={start} />
                  {last && end.includes(s) && <span className={styles.mark}>ends here</span>}
                </a>
                {m && (
                  <Move m={m} className={styles.edge}>
                    <span className={styles.edgeLabel}>{m.label}</span>
                    <span className={styles.edgeLine} aria-hidden="true" />
                    <span className="ldSr"> to </span>
                  </Move>
                )}
              </li>
            );
          })}
        </ol>

        <div className={styles.lower}>
          <div className={styles.group}>
            <p className="ldLabel">Other endings</p>
            <ul className={styles.endings}>
              {endings.map((e) => {
                const into = moves.filter((m) => m.to === e);
                const labels = [...new Set(into.map((m) => m.label))];
                return (
                  <li key={e} className={styles.ending}>
                    <a href={`#${rowId(e)}`} className={`ldLink ldFocus ${styles.endName}`} data-active={active === e || undefined} {...hover(e)}>
                      <St name={e} />
                      <StartMark name={e} start={start} />
                    </a>
                    <ul className={styles.into}>
                      {labels.map((label) => (
                        <li key={label}>
                          <span className={styles.label}>{label}</span> from{' '}
                          {into
                            .filter((m) => m.label === label)
                            .map((m, k) => (
                              <React.Fragment key={m.from}>
                                {k > 0 && ', '}
                                <Move m={m}>
                                  <St name={m.from} />
                                </Move>
                              </React.Fragment>
                            ))}
                        </li>
                      ))}
                    </ul>
                  </li>
                );
              })}
            </ul>
          </div>
          {[
            ['Shortcuts', shortcuts],
            ['Late moves', late],
            ['Other moves', other],
          ]
            .filter(([, list]) => list.length > 0)
            .map(([title, list]) => (
              <div key={title} className={styles.group}>
                <p className="ldLabel">{title}</p>
                <ul className={styles.moves}>
                  {list.map((m) => (
                    <li key={`${m.from}>${m.to}`}>
                      <Move m={m} className={styles.move}>
                        <St name={m.from} />
                        <LdIcon name="arrowRight" className={styles.arrow} />
                        <span className="ldSr"> to </span>
                        <St name={m.to} />
                        {m.label && <span className={styles.label}>{m.label}</span>}
                      </Move>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          {loose.length > 0 && (
            <div className={styles.group}>
              <p className="ldLabel">Other states</p>
              <ul className={styles.moves}>
                {loose.map((s) => (
                  <li key={s}>
                    <St name={s} /> <StartMark name={s} start={start} />
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </figure>

      <ul className={`ldPanel ldPanel--flush ${styles.states}`} aria-label="Payment states">
        {states.map((s) => {
          const next = moves.filter((m) => m.from === s.name);
          return (
            <li key={s.name} id={rowId(s.name)} className={styles.state} data-active={active === s.name || undefined}>
              <span className={styles.stateName}>
                <St name={s.name} />
              </span>
              <div className={styles.stateBody}>
                <p className={styles.meaning}>
                  <Inline parts={s.meaning} />
                </p>
                <div className={styles.facts}>
                  <div className={styles.fact}>
                    <span className="ldLabel">Calls in actions</span>
                    {s.actions.length > 0 ? (
                      <ul className={styles.calls}>
                        {s.actions.map((a) => (
                          <li key={a.name}>
                            <Link className={`ldChip ldChip--cmd ${styles.call}`} to={a.href}>
                              <Tag kind={a.method} />
                              <span translate="no">{a.path}</span>
                            </Link>
                            {a.note.length > 0 && (
                              <span className={styles.note}>
                                <Inline parts={a.note} />
                              </span>
                            )}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span className={styles.none}>{s.none || 'none'}</span>
                    )}
                  </div>
                  <div className={styles.fact}>
                    <span className="ldLabel">Then</span>
                    <ul className={styles.then}>
                      {next.map((m) => (
                        <li key={m.to}>
                          <St name={m.to} /> <span className={styles.label}>{m.label}</span>
                        </li>
                      ))}
                      {end.includes(s.name) && (
                        <li>
                          <Move m={{from: s.name, to: '[*]', label: ''}} className={styles.label}>
                            {next.length ? 'or ends' : 'ends'}
                          </Move>
                        </li>
                      )}
                    </ul>
                  </div>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
