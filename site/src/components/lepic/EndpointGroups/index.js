import React from 'react';
import Link from '@docusaurus/Link';
import {Tag, LdIcon} from '../kit';
import Inline from '../Inline';
import styles from './styles.module.css';

/* "Endpoints by group" of the API guide: one row per group with what it covers and its calls,
 * each call a chip to its operation in the explorer, the group name a link to its tag there.
 * Props from tools/gen-lepic-api.py: groups = [{name, href, covers, calls: [{method, path, href?}]}]. */

function Call({c}) {
  const inner = (
    <>
      <Tag kind={c.method} />
      <span translate="no">{c.path}</span>
    </>
  );
  return c.href ? (
    <Link className={`ldChip ldChip--cmd ${styles.call}`} to={c.href}>
      {inner}
    </Link>
  ) : (
    <span className={`ldChip ldChip--cmd ${styles.call} ${styles.plain}`}>{inner}</span>
  );
}

export default function EndpointGroups({groups}) {
  return (
    <ul className={`ldPanel ldPanel--flush ldBlock ${styles.list}`} aria-label="Endpoints by group">
      {groups.map((g) => (
        <li key={g.name} className={styles.row}>
          <div className={styles.head}>
            {g.href ? (
              <Link className={`ldLink ldFocus ${styles.name}`} to={g.href}>
                {g.name}
                <LdIcon name="chevron" className={styles.chev} />
              </Link>
            ) : (
              <span className={styles.name}>{g.name}</span>
            )}
            <p className={styles.covers}>
              <Inline parts={g.covers} />
            </p>
          </div>
          <ul className={`ldChips ${styles.calls}`} aria-label={`${g.name} calls`}>
            {g.calls.map((c) => (
              <li key={`${c.method} ${c.path}`}>
                <Call c={c} />
              </li>
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
}
