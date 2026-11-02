import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import {Icon} from '@site/src/components/icons';

/**
 * The landing page, in the BT Wallet landing page's looks (src/css/looks.css): a hero with the two
 * first steps, one panel per audience, every page by group, and the way to support.
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
    <section className="btwCard" aria-labelledby={id}>
      <p className="btwCardHead" id={id}>
        {title}
      </p>
      <p className="btwCardLede">{lede}</p>
      <ul className="btwList">
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
      title="BT Wallet documentation"
      description="Documentation for BT Wallet for Epic Cash, desktop and mobile, and the LEPIC wallet core: install, use, build and review.">
      <main className="btw">
        <header className="btwHero">
          <div className="btwWrap btwHeroIn">
            <div>
              <p className="btwKicker">Documentation</p>
              <h1 className="btwTitle">
                <span>BT Wallet</span> <span className="btwTitle-b">docs.</span>
              </h1>
              <p className="btwLede">
                How to install and use the self-custodial wallet for Epic Cash, and how it is built.
              </p>
              <div className="btwCta">
                <Link className="btwBtn btwBtn--primary" to="/users/">
                  Get started
                </Link>
                <Link className="btwBtn btwBtn--ghost" to="/users/install/">
                  Install
                </Link>
                <Link className="btwBtn btwBtn--ghost" to="/support/">
                  Support
                </Link>
              </div>
            </div>
            <div className="btwPanels">
              <Panel id="btwUsers" title="Use the wallet" lede="Install, first wallet, payments, backups." links={USERS} />
              <Panel id="btwDevs" title="Build and review" lede="The code, the build, the security model." links={DEVELOPERS} />
            </div>
          </div>
        </header>

        <section className="btwSection">
          <div className="btwWrap">
            <h2 className="btwH2">Everything here</h2>
            <div className="btwIndex">
              {GROUPS.map((group) => (
                <nav className="btwGroup" key={group.heading} aria-label={group.heading}>
                  <h3 className="btwGroupLabel">{group.heading}</h3>
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
          </div>
        </section>

        <section className="btwSection">
          <div className="btwWrap">
            <div className="btwHelp">
              <div>
                <h2>Stuck?</h2>
                <p>Ask on Telegram, follow BT LABS on X, or write to support@btlabs.uk.</p>
              </div>
              <div className="btwChips">
                <Link className="btwChip" to="/support/">
                  <Icon name="help" /> Support
                </Link>
                <a className="btwChip" href="https://t.me/BTLABS_EPIC" rel="noopener">
                  <Icon name="telegram" /> Telegram
                </a>
                <a className="btwChip" href="https://x.com/BTLabsUK" rel="noopener">
                  <Icon name="x" /> X
                </a>
                <a className="btwChip" href="mailto:support@btlabs.uk">
                  <Icon name="mail" /> Email
                </a>
              </div>
            </div>
            <p className="btwFootNote">
              The Epic Cash node, reference wallet, Epicbox protocol and APIs are documented on the{' '}
              <a href="https://devdocs.btlabs.uk">Epic Cash Developer Hub</a>.
            </p>
          </div>
        </section>
      </main>
    </Layout>
  );
}
