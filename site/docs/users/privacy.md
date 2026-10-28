---
title: Privacy
description: What is on the blockchain, what the wallet sends and to whom, and what never leaves the device.
---

# Privacy

## What the blockchain shows

Epic Cash uses Mimblewimble. On many blockchains anyone can look up an address and see its balance
and history. On Epic Cash:

- **No addresses on the blockchain.** The Epicbox address only tells Epicbox where to deliver
  messages.
- **No amounts on the blockchain.** Amounts are hidden with cryptography, and the network can still
  check that no coins were created out of nothing.
- **Notes stay off the blockchain.** A message added to a send goes only to the other wallet.

## What leaves the device

| To | What | Why |
| --- | --- | --- |
| The node (default `node.btlabs.uk`) | which outputs the wallet asks about, transactions to post; the IP address | balance, confirmations, sending |
| The Epicbox server | encrypted payment messages; the IP address | Epicbox payments |
| The other wallet | the payment messages, and your note if you add one | every payment |
| `status.btlabs.uk` | a request for the list of nodes and Epicbox servers and their state | the server lists; a switch in **Settings › Privacy** turns it off |
| CoinGecko (`api.coingecko.com`), or BT LABS' copy | a request for the EPIC price in your currency | the fiat value; a setting turns prices off |
| The update feed | a request for the signed update information | in-app updates; not in store builds or builds without Tor |
| `support.btlabs.uk` | a problem report, only when you send one | **Report a problem** shows exactly what is sent |
| Linked devices' servers | encrypted notices between your own devices | only with [Linked devices](linked-devices.md) on |

On the desktop, the HTTP receiving check asks `api.ipify.org` for the public IP address and
`portchecker.io` whether the port is reachable, only when you run that check.

With [Tor](tor.md) on, all of the above except a node on this computer go through Tor, so they do
not see your IP address. In [Offline](network-modes.md) mode the wallet reaches only the node you
give it.

## What never leaves the device

- The recovery phrase and the keys. They are kept in the Android Keystore, the iOS Keychain, or on
  the desktop in a vault file encrypted under the wallet password.
- Contacts, wallet names, labels and notes. They are in the [wallet data file](backups.md) only
  when you export one.
- The clipboard. The wallet reads it only for pairing links, only while Pairing is on, and never
  stores or logs it.

The apps have no analytics, no tracking and no push notifications.

## Logs and problem reports

Logs stay on the device. **Report a problem** in Help sends a description and cleaned logs: the
report screen shows exactly what leaves before you send it.
