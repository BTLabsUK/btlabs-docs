/* CommandCard: one command of the reference.
 *
 * <CommandCard
 *   path="tx send"                 command path without `lepic `; the h3 id is `lepic-tx-send`
 *   summary="..."                  the first line of its help
 *   tags?={['core' | 'repair']}
 *   usage="lepic tx send [OPTIONS] ..."
 *   examples?={[{cmd: string, note?: string}]}       up to three, from LEPIC's docs
 *   args?={[{name: '<AMOUNT>', required: bool, text, default?}]}
 *   options?={[{flag: '-a, --account', value?: '<LABEL>', text, default?, env?, values?: [string]}]}
 *   subs?={[{name, path, summary}]}                  a group command: its subcommands
 *   help="..."                     the full help text, shown folded
 * />
 *
 * OptionRows ({options, label}) is the option list on its own (the global options).
 * Inside RefFilter the card hides itself when the filter does not match it.
 */
import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import {Tag} from '../kit';
import CmdLine from '../cmdline';
import {useRefMatch} from '../RefFilter';
import styles from './styles.module.css';

export const anchor = (path) => 'lepic-' + path.split(' ').join('-');

/** Help text with its `code` spans set as code. */
function Ticks({text}) {
  return text.split(/(`[^`]+`)/).map((t, i) =>
    t.length > 2 && t.startsWith('`') && t.endsWith('`') ? <code key={i}>{t.slice(1, -1)}</code> : t,
  );
}

function Meta({row}) {
  const bits = [];
  if (row.default != null) bits.push(['Default', row.default]);
  if (row.values) bits.push(['Values', row.values.join(', ')]);
  if (row.env) bits.push(['Env', row.env]);
  if (row.required === false) bits.unshift(['Optional', null]);
  if (!bits.length) return null;
  return (
    <span className={clsx('ldMeta', styles.meta)}>
      {bits.map(([k, v]) => (
        <span key={k} className={styles.metaItem}>
          {v == null ? (
            k
          ) : (
            <>
              {k} <code>{v}</code>
            </>
          )}
        </span>
      ))}
    </span>
  );
}

function Rows({rows, label, arg}) {
  return (
    <dl className={styles.rows} aria-label={label}>
      {rows.map((r) => (
        <div key={arg ? r.name : r.flag} className={styles.optRow}>
          <dt className={styles.flag}>
            <code className="ldMono" translate="no">
              {arg ? r.name : r.flag}
              {r.value && <span className={styles.value}> {r.value}</span>}
            </code>
          </dt>
          <dd className={styles.desc}>
            {r.text && (
              <span className={styles.text}>
                <Ticks text={r.text} />
              </span>
            )}
            <Meta row={r} />
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function OptionRows({options, label = 'Options'}) {
  return (
    <div className={clsx('ldPanel ldBlock', styles.solo)}>
      <Rows rows={options} label={label} />
    </div>
  );
}

export default function CommandCard({path, summary, tags = [], usage, examples, args, options, subs, help}) {
  const shown = useRefMatch(path);
  const id = anchor(path);
  return (
    <section className={clsx('ldPanel ldPanel--ticked', styles.card)} aria-labelledby={id} hidden={!shown}>
      <header className={styles.head}>
        <Heading as="h3" id={id} className={styles.title}>
          <code className="ldMono" translate="no">lepic {path}</code>
        </Heading>
        {tags.length > 0 && (
          <span className={styles.tags}>
            {tags.map((t) => (
              <Tag key={t} kind={t} />
            ))}
          </span>
        )}
      </header>
      <p className={styles.summary}>{summary}</p>
      <CmdLine cmd={usage} label="Copy usage" />

      {examples && examples.length > 0 && (
        <div className={styles.part}>
          <p className={clsx('ldLabel', styles.label)}>Examples</p>
          <ul className={styles.examples}>
            {examples.map((e, i) => (
              <li key={i}>
                {e.note && <p className={styles.exNote}># {e.note}</p>}
                <CmdLine cmd={e.cmd} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {subs && subs.length > 0 && (
        <div className={styles.part}>
          <p className={clsx('ldLabel', styles.label)}>Commands</p>
          <ul className={clsx('ldChips', styles.subs)}>
            {subs.map((s) => (
              <li key={s.path}>
                <Link className="ldChip ldChip--cmd" to={'#' + anchor(s.path)} title={s.summary}>
                  <span className="ldSr">lepic {path} </span>
                  {s.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}

      {args && args.length > 0 && (
        <div className={styles.part}>
          <p className={clsx('ldLabel', styles.label)}>Arguments</p>
          <Rows rows={args} label={`Arguments of lepic ${path}`} arg />
        </div>
      )}

      {options && options.length > 0 && (
        <div className={styles.part}>
          <p className={clsx('ldLabel', styles.label)}>Options</p>
          <Rows rows={options} label={`Options of lepic ${path}`} />
        </div>
      )}

      <details className={styles.full}>
        <summary>Full help</summary>
        <pre className={clsx('ldTerm', styles.help)}>{help}</pre>
      </details>
    </section>
  );
}
