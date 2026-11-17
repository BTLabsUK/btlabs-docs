/* SequenceFlow: the messages between two parties, top to bottom (the pairing steps).
 *
 * <SequenceFlow
 *   participants={[{id: string, label: string}, {id, label}]}
 *   steps={[{kind: 'message' | 'reply' | 'note', from: id, to: id, text: string,
 *            num?: string, cmd?: string, note?: string}]}
 *   label?="..."
 * />
 *
 * - Data from tools/lepic_mdx.py `parse_sequence()`; tools/gen-lepic-cli.py adds `num` (the step
 *   number written in the text), `cmd` (the command part, shown in mono) and `note` (the rest).
 * - The first participant is the left lane, the second the right one. A message sits on the
 *   sender's side with an arrow to the other lane; a reply's arrow is dashed. A note spans both.
 * - A figure with an ordered list, so it reads as a list of steps without the drawing.
 */
import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

function Body({s}) {
  const cmd = s.cmd ?? s.text;
  return (
    <>
      {s.num && (
        <span className="ldStepNum" aria-hidden="true">
          {s.num}
        </span>
      )}
      <span className={styles.words}>
        <code className={clsx('ldMono', styles.cmd)} translate="no">{cmd}</code>
        {s.note && <span className={styles.note}>{s.note}</span>}
      </span>
    </>
  );
}

export default function SequenceFlow({participants, steps, label = 'Sequence'}) {
  const [left, right] = participants;
  const name = (id) => (participants.find((p) => p.id === id) || {label: id}).label;
  return (
    <figure className={clsx('ldPanel ldBlock', styles.flow)}>
      <figcaption className="ldSr">{label}</figcaption>
      <div className={styles.lanes} aria-hidden="true">
        <span className={clsx('ldLabel', styles.lane)}>{left.label}</span>
        <span className={clsx('ldLabel', styles.lane, styles.laneRight)}>{right.label}</span>
      </div>
      <ol className={styles.steps}>
        {steps.map((s, i) => {
          const step = s.num ? `Step ${s.num}. ` : '';
          if (s.kind === 'note') {
            return (
              <li key={i} className={clsx(styles.step, styles.noteRow)}>
                <span className="ldSr">{`${step}${name(s.from)} and ${name(s.to)}: `}</span>
                <div className={clsx(styles.bubble, styles.span)}>
                  <Body s={s} />
                </div>
              </li>
            );
          }
          const fromLeft = s.from === left.id;
          return (
            <li key={i} className={clsx(styles.step, fromLeft ? styles.ltr : styles.rtl, s.kind === 'reply' && styles.reply)}>
              <span className="ldSr">{`${step}${name(s.from)} to ${name(s.to)}${s.kind === 'reply' ? ', reply' : ''}: `}</span>
              <div className={styles.bubble}>
                <Body s={s} />
              </div>
              <span className={styles.arrow} aria-hidden="true" />
            </li>
          );
        })}
      </ol>
    </figure>
  );
}
