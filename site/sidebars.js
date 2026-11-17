// @ts-check
/**
 * Two sidebars, one per audience. The order is the order a reader needs things in.
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  users: [
    'users/index',
    'users/install',
    'users/first-wallet',
    'users/recovery-phrase',
    {
      type: 'category',
      label: 'Sending and receiving',
      link: {type: 'doc', id: 'users/send-and-receive'},
      items: ['users/send-and-receive', 'users/payment-methods', 'users/epic1', 'users/addresses', 'users/cancel'],
    },
    {
      type: 'category',
      label: 'Contacts and devices',
      items: ['users/pairing', 'users/linked-devices'],
    },
    {
      type: 'category',
      label: 'Network and privacy',
      items: ['users/nodes', 'users/epicbox', 'users/tor', 'users/network-modes', 'users/privacy'],
    },
    {
      type: 'category',
      label: 'Wallet care',
      items: ['users/backups', 'users/restore', 'users/updates', 'users/advanced', 'users/settings-file'],
    },
    'users/how-it-works',
    'users/troubleshooting',
    'users/faq',
    'users/glossary',
  ],
  developers: [
    'developers/index',
    'developers/architecture',
    {
      type: 'category',
      label: 'LEPIC',
      link: {type: 'doc', id: 'developers/lepic'},
      items: [
        {type: 'doc', id: 'developers/lepic/cli/index', label: 'CLI guide'},
        {type: 'doc', id: 'developers/lepic/recipes', label: 'Recipes'},
        {type: 'doc', id: 'developers/lepic/cli/reference', label: 'Command reference'},
        {type: 'doc', id: 'developers/lepic/api/v1/index', label: 'API guide'},
        {type: 'doc', id: 'developers/lepic/api/v1/explorer', label: 'API explorer'},
        {type: 'doc', id: 'developers/lepic/api/v1/reference', label: 'API reference'},
      ],
    },
    'developers/lepic-flutter',
    'developers/security-model',
    'developers/decisions',
    'developers/upstream',
    {
      type: 'category',
      label: 'Build from source',
      link: {type: 'doc', id: 'developers/build/index'},
      items: [
        'developers/build/linux',
        'developers/build/windows',
        'developers/build/android',
        'developers/build/apple',
        'developers/build/variants',
      ],
    },
    'developers/dev-environment',
    'developers/dependencies',
    'developers/testing',
    'developers/releases',
    'developers/contributing',
    'security',
  ],
};

export default sidebars;
