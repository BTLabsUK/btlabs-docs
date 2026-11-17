/* Steps: a numbered sequence, each step with its command (Start here).
 *
 * <Steps
 *   steps={[{lead: parts | null, text: parts, cmd: string, answer?: string}]}
 *   label?="Start here"
 * />
 *
 * - `lead` and `text` are inline parts from tools/lepic_mdx.py `inline()` (see ../Inline.js).
 *   `lead` shows bold before `text`.
 * - `cmd` goes on a command strip with the `$` prompt and a copy button. A command of several
 *   lines keeps its lines; a trailing `  # comment` shows dim and is not copied.
 * - `answer`, when given, is shown as written (pre-formatted) under the label "Answer", on the
 *   terminal surface in a box of at most 14rem that scrolls inside itself: a focusable region
 *   named "Answer to step N".
 * - `label` is the accessible name of the list.
 */
import React from 'react';
import clsx from 'clsx';
import Inline from '../Inline';
import CmdLine from '../cmdline';
import styles from './styles.module.css';

export default function Steps({steps, label = 'Steps'}) {
  return (
    <ol className={clsx('ldBlock', styles.steps)} aria-label={label}>
      {steps.map((s, i) => (
        <li key={i} className={styles.step}>
          <span className={clsx('ldStepNum', styles.num)} aria-hidden="true">
            {i + 1}
          </span>
          <div className={styles.body}>
            <p className={styles.text}>
              {s.lead && (
                <strong className={styles.lead}>
                  <Inline parts={s.lead} />
                </strong>
              )}
              {s.lead && ' '}
              <Inline parts={s.text} />
            </p>
            {s.cmd && <CmdLine cmd={s.cmd} />}
            {s.answer && (
              <div className={styles.answerWrap}>
                <p className="ldLabel">Answer</p>
                <pre
                  className={clsx('ldTerm ldFocus', styles.answer)}
                  tabIndex={0}
                  role="region"
                  aria-label={`Answer to step ${i + 1}`}>
                  {s.answer}
                </pre>
              </div>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}
