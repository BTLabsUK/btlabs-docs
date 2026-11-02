// @ts-check
// The BT Wallet documentation: BT Wallet for Epic Cash (desktop and mobile), LEPIC and lepic-flutter.
// The base is the Epic Cash Developer Hub's theme (devdocs.btlabs.uk): its custom.css, table-of-contents
// panel and prism theme are copied here unchanged. On top of it, src/css/looks.css gives the site the
// BT Wallet landing page's three looks (Night, Grid, Day; src/components/look.js), and the colour-mode
// toggle is the look switch. The Markdown under docs/ is also the source of the GitHub wikis
// (tools/wiki-sync.py), which is why the pages use plain Markdown only (WRITING.md).
import {darkPrismTheme} from './src/prism-themes.js';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'BT Wallet Docs',
  tagline: 'BT Wallet for Epic Cash, desktop and mobile, and the LEPIC wallet core',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
    faster: false,
  },

  // A fixed namespace, so the colour mode's key is known: theme-btw. The look script in headTags
  // writes it (it was theme-eaa, a hash of the URL, which it migrates).
  storage: {type: 'localStorage', namespace: 'btw'},

  // Self-hosted; see deploy/. DOCS_URL overrides the origin for a preview build.
  url: process.env.DOCS_URL || 'https://docs.btlabs.uk',
  baseUrl: '/',
  trailingSlash: true,

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',
  markdown: {
    format: 'detect',
    hooks: {onBrokenMarkdownLinks: 'throw'},
  },

  i18n: {defaultLocale: 'en', locales: ['en']},

  // Offline search, as on the Developer Hub: the index ships with the site and no query leaves
  // the reader's browser.
  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      /** @type {import('@easyops-cn/docusaurus-search-local').PluginOptions} */
      ({
        hashed: true,
        language: ['en'],
        indexBlog: false,
        docsRouteBasePath: '/',
        indexDocs: true,
        indexPages: false,
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        searchBarShortcutHint: false,
        searchResultLimits: 10,
        searchResultContextMaxLength: 60,
      }),
    ],
  ],

  headTags: [
    // The look before the first paint (src/components/look.js): the saved one, Day for a reader whose
    // saved theme was light, else Night. It also stores the look's colour mode, which Docusaurus's own
    // inline script (later, in <body>) then applies, so the look and the mode never disagree.
    {
      tagName: 'script',
      attributes: {},
      innerHTML:
        "(function(){var d=document.documentElement,l='a';try{l=localStorage.getItem('btw-look')||((localStorage.getItem('theme-btw')||localStorage.getItem('theme-eaa'))==='light'?'c':'a')}catch(e){}l=l==='b'||l==='c'?l:'a';d.setAttribute('data-look',l);try{localStorage.setItem('theme-btw',l==='c'?'light':'dark')}catch(e){}})();",
    },
    // Here and not in looks.css: the build inlines a font file this small into the CSS as a data:
    // URL, which the CSP (font-src 'self') blocks. A <style> in <head> keeps it a request to /fonts/.
    {
      tagName: 'style',
      attributes: {},
      innerHTML:
        "@font-face{font-family:'JetBrains Mono';src:url('/fonts/jetbrainsmono-nl.woff2') format('woff2');font-weight:100 800;font-display:swap}",
    },
    {tagName: 'link', attributes: {rel: 'icon', href: '/img/favicon.svg', type: 'image/svg+xml'}},
    {tagName: 'link', attributes: {rel: 'apple-touch-icon', href: '/img/apple-touch-icon.png'}},
    {tagName: 'meta', attributes: {property: 'og:site_name', content: 'BT Wallet Docs'}},
    {tagName: 'meta', attributes: {property: 'og:type', content: 'website'}},
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
        },
        blog: false,
        sitemap: {ignorePatterns: ['/404', '/404.html', '/search', '/search/**']},
        theme: {customCss: ['./src/css/custom.css', './src/css/btlabs.css', './src/css/looks.css']},
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.png',
      colorMode: {
        defaultMode: 'dark',
        respectPrefersColorScheme: false,
      },
      docs: {
        sidebar: {hideable: true, autoCollapseCategories: false},
      },
      navbar: {
        title: 'BT Wallet',
        logo: {
          alt: 'BT Wallet',
          src: 'img/bt-wallet-mark-ink.svg',
          srcDark: 'img/bt-wallet-mark-gold.svg',
          width: 30,
          height: 26,
        },
        items: [
          {to: '/users/', label: 'Use the wallet', position: 'left'},
          {to: '/users/install/', label: 'Install', position: 'left'},
          {to: '/developers/', label: 'Developers', position: 'left'},
          {to: '/developers/build/', label: 'Build', position: 'left'},
          {to: '/developers/lepic/', label: 'LEPIC', position: 'left'},
          {to: '/security/', label: 'Security', position: 'left'},
          {to: '/support/', label: 'Support', position: 'right'},
          {href: 'https://devdocs.btlabs.uk', label: 'Developer Hub', position: 'right'},
        ],
      },
      footer: {
        style: 'dark',
        logo: {
          alt: 'BT Wallet for Epic Cash',
          src: 'img/bt-wallet-lockup-row-light.svg',
          srcDark: 'img/bt-wallet-lockup-row-dark.svg',
          href: 'https://epiccash.btlabs.uk',
          width: 220,
          height: 53,
        },
        links: [
          {
            title: 'Wallet',
            items: [
              {label: 'Get started', to: '/users/'},
              {label: 'Install', to: '/users/install/'},
              {label: 'Troubleshooting', to: '/users/troubleshooting/'},
              {label: 'FAQ', to: '/users/faq/'},
            ],
          },
          {
            title: 'Developers',
            items: [
              {label: 'Architecture', to: '/developers/architecture/'},
              {label: 'Build from source', to: '/developers/build/'},
              {label: 'Security model', to: '/developers/security-model/'},
              {label: 'Epic Cash Developer Hub', href: 'https://devdocs.btlabs.uk'},
            ],
          },
          {
            title: 'Support',
            items: [
              {label: 'Get help', to: '/support/'},
              {label: 'Telegram', href: 'https://t.me/BTLABS_EPIC'},
              {label: 'X', href: 'https://x.com/BTLabsUK'},
              {label: 'support@btlabs.uk', href: 'mailto:support@btlabs.uk'},
            ],
          },
          {
            title: 'BT LABS',
            items: [
              {label: 'BT Wallet', href: 'https://epiccash.btlabs.uk'},
              {label: 'Download', href: 'https://epiccash.btlabs.uk/releases/'},
              {label: 'btlabs.uk', href: 'https://btlabs.uk'},
              {label: 'Report a security issue', to: '/security/'},
            ],
          },
        ],
        copyright:
          'An independent, open-source wallet by <span class="epicFooterBy">BT LABS</span>. Not made by the Epic Cash project. Use it within the law where you live.',
      },
      prism: {
        theme: darkPrismTheme,
        darkTheme: darkPrismTheme,
        additionalLanguages: ['rust', 'toml', 'bash', 'powershell', 'dart', 'yaml', 'json', 'ini'],
      },
      tableOfContents: {minHeadingLevel: 2, maxHeadingLevel: 3},
    }),
};

export default config;
