import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import './../css/index-page.css';

/**
 * The landing page. It reuses the Developer Hub's masthead and index styles (index-page.css), with
 * two panels instead of the quick start: one per audience, each a short list of first pages.
 */

const USERS = [
  ['Install', '/users/install/'],
  ['Your first wallet', '/users/first-wallet/'],
  ['Send and receive', '/users/send-and-receive/'],
  ['Backups and wallet data', '/users/backups/'],
  ['Troubleshooting', '/users/troubleshooting/'],
];

const DEVELOPERS = [
  ['Architecture', '/developers/architecture/'],
  ['LEPIC crates', '/developers/lepic/'],
  ['Build from source', '/developers/build/'],
  ['Security model', '/developers/security-model/'],
  ['Contributing', '/developers/contributing/'],
];

const GROUPS = [
  {
    heading: 'Using the wallet',
    links: [
      ['What the apps are', '/users/'],
      ['Payment methods', '/users/payment-methods/'],
      ['Recovery phrase', '/users/recovery-phrase/'],
      ['Restore and move a wallet', '/users/restore/'],
      ['Tor', '/users/tor/'],
      ['Privacy', '/users/privacy/'],
      ['FAQ', '/users/faq/'],
      ['Glossary', '/users/glossary/'],
    ],
  },
  {
    heading: 'Contacts and devices',
    links: [
      ['Contacts, pairing and invoices', '/users/pairing/'],
      ['Linked devices', '/users/linked-devices/'],
      ['Nodes and your own node', '/users/nodes/'],
      ['Epicbox', '/users/epicbox/'],
      ['Network modes', '/users/network-modes/'],
      ['Updates', '/users/updates/'],
    ],
  },
  {
    heading: 'Building and reviewing',
    links: [
      ['Developer guide', '/developers/'],
      ['lepic-flutter', '/developers/lepic-flutter/'],
      ['Decisions (ADRs)', '/developers/decisions/'],
      ['LEPIC and upstream', '/developers/upstream/'],
      ['Development environment', '/developers/dev-environment/'],
      ['Testing', '/developers/testing/'],
      ['Releases', '/developers/releases/'],
      ['Report a security issue', '/security/'],
    ],
  },
];

function Panel({id, title, lede, links}) {
  return (
    <section className="ixPanel" aria-labelledby={id}>
      <p className="ixPanelHead" id={id}>
        {title}
      </p>
      <p className="btPanelLede">{lede}</p>
      <ul className="ixPanelList">
        {links.map(([label, to]) => (
          <li key={to}>
            <Link to={to}>{label}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function Home() {
  return (
    <Layout
      title="Epic Cash wallet documentation"
      description="Documentation for Epic Cash Desktop, Epic Cash Mobile and the LEPIC wallet core: install, use, build and review.">
      <header className="ixMast">
        <div className="ixGrid" aria-hidden="true" />
        <div className="container ixMastIn">
          <div className="ixMastGrid">
            <div>
              <p className="ixEyebrow">BT LABS</p>
              <h1 className="ixTitle">Epic Cash wallets</h1>
              <p className="ixLede">
                Epic Cash Desktop, Epic Cash Mobile and LEPIC, the Rust wallet core behind them. How to
                use them, and how they are built.
              </p>
              <div className="ixExplorerStrip">
                <span className="ixPill ixPill--data">Windows · Linux · Android</span>
                <span className="ixPill ixPill--data">macOS · iOS preview</span>
                <span className="ixPill ixPill--data">Apache-2.0</span>
              </div>
            </div>
            <div className="btPanels">
              <Panel
                id="btUsers"
                title="Use the wallet"
                lede="Install, first wallet, payments, backups."
                links={USERS}
              />
              <Panel
                id="btDevs"
                title="Build and review"
                lede="The code, the build, the security model."
                links={DEVELOPERS}
              />
            </div>
          </div>
        </div>
      </header>
      <main className="container ixMain">
        <section className="ixSection ixSectionLast">
          <h2 className="ixKicker">Everything here</h2>
          <div className="ixIndex">
            {GROUPS.map((group) => (
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
            The Epic Cash node, reference wallet, Epicbox protocol and APIs are documented on the{' '}
            <a href="https://devdocs.btlabs.uk">Epic Cash Developer Hub</a>.
          </p>
        </section>
      </main>
    </Layout>
  );
}
