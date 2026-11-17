/* CommandList: rows of a command and what it does (the ten everyday commands, the contact
 * stage tables).
 *
 * <CommandList
 *   items={[{cmd: string, href?: string, text: parts}]}
 *   columns?={1 | 2}
 *   label?="..."
 * />
 *
 * - `cmd` shows in mono as given: no `$`, no copy button. With `href` it links there (the
 *   command's card in the reference).
 * - `text`: inline parts from tools/lepic_mdx.py `inline()` (see ../Inline.js).
 * - `columns={2}` sets the rows in two columns from 997px up. On a phone a row stacks.
 * - `label` is the accessible name of the list.
 */
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Inline from '../Inline';
import styles from './styles.module.css';

export default function CommandList({items, columns = 1, label}) {
  return (
    <ul
      className={clsx('ldPanel ldPanel--flush ldBlock', styles.list, columns === 2 && styles.two)}
      aria-label={label}>
      {items.map((it, i) => (
        <li key={i} className={styles.item}>
          {it.href ? (
            <Link className={clsx('ldLink ldFocus', styles.cmd)} to={it.href}>
              <code className="ldMono" translate="no">{it.cmd}</code>
            </Link>
          ) : (
            <code className={clsx('ldMono', styles.cmd)} translate="no">{it.cmd}</code>
          )}
          <span className={styles.text}>
            <Inline parts={it.text} />
          </span>
        </li>
      ))}
    </ul>
  );
}
