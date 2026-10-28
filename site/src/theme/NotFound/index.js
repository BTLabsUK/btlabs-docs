import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import './../../css/index-page.css';

/**
 * The not-found page, shadowing @theme/NotFound (as on the Developer Hub), so the static 404.html
 * and the client-side catch-all render the same tree. src/pages/404.js re-exports it.
 */

const ROUTES = [
  {
    heading: 'Use the wallet',
    links: [
      ['Install', '/users/install/'],
      ['Your first wallet', '/users/first-wallet/'],
      ['Send and receive', '/users/send-and-receive/'],
      ['Troubleshooting', '/users/troubleshooting/'],
    ],
  },
  {
    heading: 'Build and review',
    links: [
      ['Developer guide', '/developers/'],
      ['Architecture', '/developers/architecture/'],
      ['Build from source', '/developers/build/'],
      ['Security model', '/developers/security-model/'],
    ],
  },
];

export default function NotFound() {
  return (
    <Layout title="Page not found" description="That page does not exist on the Epic Cash wallet documentation.">
      <header className="ixMast">
        <div className="container">
          <p className="ixEyebrow">Error 404</p>
          <h1 className="ixTitle">That page does not exist</h1>
          <p className="ixLede">Search in the navbar covers every page, or start from one of these.</p>
        </div>
      </header>
      <main className="container ixMain">
        <section className="ixSection ixSectionLast">
          <div className="ixIndex">
            {ROUTES.map((group) => (
              <nav className="ixGroup" key={group.heading} aria-label={group.heading}>
                <h3 className="ixGroupLabel">{group.heading}</h3>
                <ul>
                  {group.links.map(([label, to]) => (
                    <li key={to}>
                      <Link to={to}>{label}</Link>
                    </li>
                  ))}
                </ul>
              </nav>
            ))}
          </div>
          <p className="ixFoot">
            <Link to="/">The documentation index</Link> lists every page.
          </p>
        </section>
      </main>
    </Layout>
  );
}
