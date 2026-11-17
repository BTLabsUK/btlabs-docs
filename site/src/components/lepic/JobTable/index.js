/* JobTable: a goal per row, the command (or two, run one after the other) and a link to the
 * section that explains it (Find a command by job).
 *
 * <JobTable rows={[{goal: parts, cmds: [string], more: {label: string, href: string}}]} />
 *
 * - `goal`: inline parts from tools/lepic_mdx.py `inline()`.
 * - `cmds`: one or two commands, each on a command strip with a copy button; "then" between.
 * - `more`: the section link; `href` is `#anchor` or a site path.
 */
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Inline from '../Inline';
import CmdLine from '../cmdline';
import {LdIcon} from '../kit';
import styles from './styles.module.css';

export default function JobTable({rows, label = 'Find a command by job'}) {
  return (
    <ul className={clsx('ldPanel ldPanel--flush ldBlock', styles.list)} aria-label={label}>
      {rows.map((r, i) => (
        <li key={i} className={styles.row}>
          <p className={styles.goal}>
            <Inline parts={r.goal} />
          </p>
          <div className={styles.cmds}>
            {r.cmds.map((c, j) => (
              <React.Fragment key={j}>
                {j > 0 && <span className={styles.then}>then</span>}
                <CmdLine cmd={c} />
              </React.Fragment>
            ))}
          </div>
          <Link className={clsx('ldLink ldFocus', styles.more)} to={r.more.href}>
            <span className="ldSr">More in </span>
            {r.more.label}
            <LdIcon name="chevron" className={styles.chev} />
          </Link>
        </li>
      ))}
    </ul>
  );
}
