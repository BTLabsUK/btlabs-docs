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
| The node (default `node.epiccash.com`) | which outputs the wallet asks about, transactions to post; the IP address | balance, confirmations, sending |
| The Epicbox server (default `epicbox.epiccash.com`) | encrypted payment messages; the IP address | Epicbox payments |
| The other wallet | the payment messages, and your note if you add one | every payment |
| `status.btlabs.uk` | a request for the server list and its state, and the EPIC price; on the desktop also your public IP address and a port check for HTTP receiving | the server lists and the fiat value; a status switch and a price switch turn the first two off |
| CoinGecko (`api.coingecko.com`) | a request for the EPIC price | only when BT LABS' copy gives no price and Tor is off |
| The update feed (`epiccash.btlabs.uk`, GitHub) | a request for the signed update information | in-app updates; not in store builds |
| GitHub (`btlabs.json`) | a request for the signed settings file from BT LABS | donation and server details |
| `support.btlabs.uk` | a problem report, only when you send one | **Report a problem** shows what is sent |
| Linked devices' servers | encrypted notices between your own devices | only with [Linked devices](linked-devices.md) on |

With [Tor](tor.md) on, these requests go through Tor, so they do not see your IP address. Requests
to a node or Epicbox server on this computer or your local network stay direct. In
[Node only](network-modes.md#node-only) the wallet reaches only the node in use; in
[Kill switch](network-modes.md#kill-switch) it reaches nothing.

## What never leaves the device

- The recovery phrase and the keys. They are kept in the Android Keystore, the iOS Keychain, or on
  the desktop in a vault file encrypted under the wallet password.
- Contacts, wallet names, labels and notes. They are in the [wallet data file](backups.md) only
  when you export one.
- The clipboard. The wallet reads it when you press Paste or use a paste action, and does not store
  or log it.

The apps contain no advertising or analytics code, and no push notifications.

## Logs and problem reports

Logs stay on the device. **Report a problem** sends a description. Logs go along only if you attach
them, with the recovery phrase, PIN and other secrets removed first. The report screen shows what is
sent before you send it.
