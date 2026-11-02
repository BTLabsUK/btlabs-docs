import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import {Icon} from '@site/src/components/icons';

/**
 * Support: where to send people. The three channels (Telegram, X, email), the in-app problem report,
 * the self-help pages, and the security route. Facts only; no promises about reply times.
 */

const CHANNELS = [
  {
    icon: 'telegram',
    title: 'Telegram',
    handle: 't.me/BTLABS_EPIC',
    href: 'https://t.me/BTLABS_EPIC',
    text: 'The BT Wallet beta group. Questions, feedback and help from the people who build the wallet.',
    go: 'Open Telegram',
  },
  {
    icon: 'x',
    title: 'X',
    handle: '@BTLabsUK',
    href: 'https://x.com/BTLabsUK',
    text: 'News, releases and updates from BT LABS.',
    go: 'Follow on X',
  },
  {
    icon: 'mail',
    title: 'Email',
    handle: 'support@btlabs.uk',
    href: 'mailto:support@btlabs.uk',
    text: 'Bugs, private questions and security reports.',
    go: 'Write an email',
  },
];

const SELF_HELP = [
  ['Troubleshooting', '/users/troubleshooting/'],
  ['FAQ', '/users/faq/'],
  ['Install', '/users/install/'],
  ['Restore and move a wallet', '/users/restore/'],
  ['Updates', '/users/updates/'],
];

export default function Support() {
  return (
    <Layout title="Support" description="Get help with BT Wallet: Telegram, X and support@btlabs.uk, the in-app problem report, and the troubleshooting pages.">
      <main className="btw">
        <header className="btwHero">
          <div className="btwWrap btwHeroIn btwHeroIn--single">
            <div>
              <p className="btwKicker">Support</p>
              <h1 className="btwTitle">
                <span>Get help</span> <span className="btwTitle-b">with BT Wallet.</span>
              </h1>
              <p className="btwLede">Ask the people who build the wallet, report a problem from the app, or find the answer here.</p>
            </div>
          </div>
        </header>

        <section className="btwWrap" aria-label="Contact">
          <div className="btwChannels">
            {CHANNELS.map((c) => (
              <a key={c.title} className="btwCard btwChannel" href={c.href} rel={c.href.startsWith('http') ? 'noopener' : undefined}>
                <span className="btwChannelIco">
                  <Icon name={c.icon} />
                </span>
                <h3>{c.title}</h3>
                <span className="btwHandle">{c.handle}</span>
                <p>{c.text}</p>
                <span className="btwGo">{c.go} →</span>
              </a>
            ))}
          </div>

          <div className="btwTwo">
            <div className="btwCard">
              <h3>Report a problem from the app</h3>
              <p>
                On the desktop: <b>Settings › Help › Report a problem</b>. On the phone: <b>Settings › Send feedback</b>.
              </p>
              <p>It sends a description and cleaned logs to BT LABS, and shows exactly what is sent first.</p>
            </div>
            <div className="btwCard btwWarn">
              <h3>Your recovery phrase stays with you</h3>
              <p>
                Never send your recovery phrase, PIN or password to anyone: not in a chat, not by email, not to BT LABS.
                Nobody needs it to help you.
              </p>
            </div>
          </div>
        </section>

        <section className="btwSection" style={{marginTop: 'clamp(36px, 6vw, 72px)'}}>
          <div className="btwWrap btwTwo" style={{marginTop: 0}}>
            <section className="btwCard" aria-labelledby="btwSelf">
              <p className="btwCardHead" id="btwSelf">
                Find it in the docs
              </p>
              <ul className="btwList">
                {SELF_HELP.map(([label, to]) => (
                  <li key={to}>
                    <Link to={to}>{label}</Link>
                  </li>
                ))}
              </ul>
            </section>
            <div style={{display: 'grid', gap: 14, alignContent: 'start'}}>
              <div className="btwCard">
                <h3>A security problem</h3>
                <p>
                  Report it privately, not in a public group. <Link to="/security/">How to report a security issue</Link>.
                </p>
              </div>
              <div className="btwCard">
                <h3>About Epic Cash itself</h3>
                <p>
                  The coin and its network have their own community:{' '}
                  <a href="https://t.me/epiccash" rel="noopener">
                    Epic Cash on Telegram
                  </a>
                  . BT LABS does not run it.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
