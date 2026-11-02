import React from 'react';
import clsx from 'clsx';
import useIsBrowser from '@docusaurus/useIsBrowser';
import {LOOKS, useLook} from '@site/src/components/look';

/**
 * The look switch, in the colour-mode toggle's place: Night, Grid and Day, the BT Wallet landing
 * page's three looks (src/components/look.js). Each look sets the colour mode as well (Night and
 * Grid dark, Day light), so this replaces the old two-state sun/moon toggle without losing it.
 *
 * Three small buttons with aria-pressed, one per look, so every look is one press away and the
 * current one is visible. The marks are drawn in CSS from html[data-look], which is set before the
 * first paint, so the right one is lit before React hydrates. Disabled until then, like upstream.
 */
const MARKS = {
  a: (
    <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M20 14.2A8.2 8.2 0 0 1 9.8 4a8.4 8.4 0 1 0 10.2 10.2z" />
    </svg>
  ),
  b: (
    <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
      <rect x="3.5" y="3.5" width="17" height="17" rx="1.5" />
      <path d="M3.5 9.2h17M3.5 14.8h17M9.2 3.5v17M14.8 3.5v17" />
    </svg>
  ),
  c: (
    <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" aria-hidden="true">
      <circle cx="12" cy="12" r="4.2" />
      <path d="M12 2.4v2.2M12 19.4v2.2M2.4 12h2.2M19.4 12h2.2M5.2 5.2l1.6 1.6M17.2 17.2l1.6 1.6M18.8 5.2l-1.6 1.6M6.8 17.2l-1.6 1.6" />
    </svg>
  ),
};

export default function ColorModeToggle({className}) {
  const isBrowser = useIsBrowser();
  const [look, setLook] = useLook();
  return (
    <div className={clsx('btwLookSwitch', className)} role="group" aria-label="Page look">
      {LOOKS.map((l) => (
        <button
          key={l.id}
          type="button"
          className={clsx('clean-btn', 'btwLookSwitch-btn', `btwLookSwitch-btn--${l.id}`)}
          disabled={!isBrowser}
          aria-pressed={look === l.id}
          title={`${l.name} look`}
          aria-label={`${l.name} look`}
          onClick={() => setLook(l.id)}>
          {MARKS[l.id]}
        </button>
      ))}
    </div>
  );
}
