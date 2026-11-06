---
title: Privacy
description: What is on the blockchain, what the wallet sends and to whom, and what stays on the device.
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

The full list, with the servers and how long BT LABS keeps logs, is the
[privacy policy](https://btlabs.uk/privacy/). In short, the wallet talks to these:

| To | What | When |
| --- | --- | --- |
| A node (the default is `node.epiccash.com`) | which outputs the wallet asks about, transactions to post; the IP address | always, for balance, confirmations and sending |
| An Epicbox server (the default is `epicbox.epiccash.com`) | encrypted payment messages; the IP address | Epicbox payments |
| The other wallet | the payment messages, and your note if you add one | each payment |
| `status.btlabs.uk` | the server list and its state, the EPIC price, and on the desktop the public IP address and port check for receiving over HTTP | the status switch and the price switch in **Settings** turn the first two off |
| CoinGecko (`api.coingecko.com`) | a request for the EPIC price in your currency | only when the BT LABS copy gives no price and the Tor switch is off |
| The update feed (`epiccash.btlabs.uk`, GitHub) | a request for the signed update information | in-app updates; not in store builds |
| A signed settings file from BT LABS | a request for donation and server details | when the app checks for settings |
| `support.btlabs.uk` | a problem report | only when you send one; **Report a problem** shows what is sent |
| Linked devices' servers | encrypted notices between your own devices | with [Linked devices](linked-devices.md) on |

Receiving over HTTP on the desktop used `api.ipify.org` and `portchecker.io` in versions up to
26.10.23. Later versions ask `status.btlabs.uk`.

With [Tor](tor.md) on, these requests go through Tor, so the servers do not see your IP address.
Requests to a node or Epicbox server on this computer or your local network stay direct. In
[Offline](network-modes.md) mode the wallet reaches only the node you give it.

## What stays on the device

- The recovery phrase and the keys. They are kept in the Android Keystore, the iOS Keychain, or on
  the desktop in a vault file encrypted under the wallet password. The wallet does not send them.
- Contacts, wallet names, labels and notes. They are in the [wallet data file](backups.md) only
  when you export one.
- The clipboard. The wallet reads it when you press Paste or use a paste action, and does not store
  or log it.

The apps contain no advertising or analytics code. Android builds up to 26.10.23 from Google Play
and the BT LABS website used Google ML Kit to read QR codes; see the policy.

## Logs and problem reports

Logs stay on the device. **Report a problem** in Help sends a description and the newest part of the
app log, cleaned of secrets by pattern matching: the report screen shows what is sent before you
send it. The log can be turned off for a report.
