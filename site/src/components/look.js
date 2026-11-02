import {useEffect, useState} from 'react';
import {useColorMode} from '@docusaurus/theme-common';

/**
 * The BT Wallet looks: the landing page's three (epiccash.btlabs.uk), on this site too.
 *
 *   a  Night  gold on black, Montserrat            Docusaurus dark mode
 *   b  Grid   graphite, Geist                      Docusaurus dark mode
 *   c  Day    warm paper, Bricolage and Inter      Docusaurus light mode
 *
 * The look lives on html[data-look] and in localStorage 'btw-look', the landing page's key (this
 * origin's own copy). The inline script in docusaurus.config.js sets the attribute before the first
 * paint; a reader whose saved theme was light starts on Day. Picking a look also sets Docusaurus's
 * colour mode, so code blocks, tables and the search follow, and the two can never disagree.
 */
export const LOOKS = [
  {id: 'a', name: 'Night', mode: 'dark'},
  {id: 'b', name: 'Grid', mode: 'dark'},
  {id: 'c', name: 'Day', mode: 'light'},
];

const KEY = 'btw-look';

function current() {
  if (typeof document === 'undefined') return 'a';
  const l = document.documentElement.getAttribute('data-look');
  return l === 'b' || l === 'c' ? l : 'a';
}

export function useLook() {
  const {setColorMode} = useColorMode();
  // 'a' on the server and on the first client render, so hydration matches; the real value right after.
  const [look, setLookState] = useState('a');
  useEffect(() => {
    setLookState(current());
    // Another control on the page (navbar or footer) may change it: follow the attribute.
    const obs = new MutationObserver(() => setLookState(current()));
    obs.observe(document.documentElement, {attributes: true, attributeFilter: ['data-look']});
    return () => obs.disconnect();
  }, []);
  const setLook = (id) => {
    const l = LOOKS.find((x) => x.id === id) || LOOKS[0];
    document.documentElement.setAttribute('data-look', l.id);
    try {
      localStorage.setItem(KEY, l.id);
    } catch (e) {
      // private window: the choice lasts the page view
    }
    setColorMode(l.mode);
  };
  return [look, setLook];
}
