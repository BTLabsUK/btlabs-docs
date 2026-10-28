// @ts-check
// The BT LABS wallet documentation: Epic Cash Desktop, Epic Cash Mobile, LEPIC and lepic-flutter.
// The look is the Epic Cash Developer Hub's (devdocs.btlabs.uk): its custom.css, colour-mode
// toggle, table-of-contents panel and prism theme are copied here unchanged, so the two sites read
// as one family. The Markdown under docs/ is also the source of the GitHub wikis
// (tools/wiki-sync.py), which is why the pages use plain Markdown only (WRITING.md).
import {darkPrismTheme} from './src/prism-themes.js';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Epic Cash Wallet Docs',
  tagline: 'Epic Cash Desktop, Epic Cash Mobile and the LEPIC wallet core',
  favicon: 'img/favicon.png',

  future: {
    v4: true,
    faster: false,
  },

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
    {tagName: 'meta', attributes: {property: 'og:site_name', content: 'Epic Cash Wallet Docs'}},
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
        theme: {customCss: ['./src/css/custom.css', './src/css/btlabs.css']},
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
        title: 'BT LABS',
        logo: {
          alt: 'Epic Cash',
          src: 'img/epic-logo-nav.png',
          width: 65,
          height: 26,
        },
        items: [
          {to: '/users/', label: 'Use the wallet', position: 'left'},
          {to: '/users/install/', label: 'Install', position: 'left'},
          {to: '/developers/', label: 'Developers', position: 'left'},
          {to: '/developers/build/', label: 'Build', position: 'left'},
          {to: '/developers/lepic/', label: 'LEPIC', position: 'left'},
          {to: '/security/', label: 'Security', position: 'left'},
          {href: 'https://devdocs.btlabs.uk', label: 'Developer Hub', position: 'right'},
        ],
      },
      footer: {
        style: 'dark',
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
            title: 'BT LABS',
            items: [
              {label: 'Epic Cash wallets', href: 'https://epiccash.btlabs.uk'},
              {label: 'btlabs.uk', href: 'https://btlabs.uk'},
              {label: 'Report a security issue', to: '/security/'},
              {label: 'epiccash.com', href: 'https://epiccash.com'},
            ],
          },
        ],
        copyright: '<span class="epicFooterBy">BT LABS</span>',
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
