import React from 'react';
import Link from '@docusaurus/Link';

/* Inline text from tools/lepic_mdx.py `inline()`:
 *   parts: [{t: 'text' | 'code' | 'strong', v: string} | {t: 'link', v: parts, href: string}]
 * Renders no wrapper element. Links to a page of the site (`/...`) or an anchor (`#...`) use
 * Docusaurus Link, so the build checks them; other links are plain anchors.
 * `linkClassName` is put on every link (pass 'ldLink ...' for a link that is not prose). */
export default function Inline({parts, linkClassName}) {
  if (!parts) return null;
  return parts.map((p, i) => {
    switch (p.t) {
      case 'code':
        return <code key={i}>{p.v}</code>;
      case 'strong':
        return <strong key={i}>{p.v}</strong>;
      case 'link': {
        const inner = <Inline parts={p.v} />;
        return p.href.startsWith('/') || p.href.startsWith('#') ? (
          <Link key={i} to={p.href} className={linkClassName}>
            {inner}
          </Link>
        ) : (
          <a key={i} href={p.href} className={linkClassName}>
            {inner}
          </a>
        );
      }
      default:
        return <React.Fragment key={i}>{p.v}</React.Fragment>;
    }
  });
}
