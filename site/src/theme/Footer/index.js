import React from 'react';
import Footer from '@theme-original/Footer';
import {LOOKS, useLook} from '@site/src/components/look';

/**
 * The theme's footer, then the BT Wallet landing page's quiet Look picker under it: three text
 * buttons, Night, Grid and Day (src/components/look.js).
 */
function LookPick() {
  const [look, setLook] = useLook();
  return (
    <nav className="btwLookPick" aria-label="Page look">
      <span>Look</span>
      {LOOKS.map((l) => (
        <button key={l.id} type="button" aria-pressed={look === l.id} onClick={() => setLook(l.id)}>
          {l.name}
        </button>
      ))}
    </nav>
  );
}

export default function FooterWrapper(props) {
  return (
    <>
      <Footer {...props} />
      <LookPick />
    </>
  );
}
