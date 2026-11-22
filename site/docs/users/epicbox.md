---
title: Epicbox
description: The server that carries payments between wallets and holds them while the other wallet is offline.
---

# Epicbox

Both wallets take part in every transaction, so their messages need a meeting point. An Epicbox
server is that meeting point: it holds a payment sent to this wallet until the wallet comes online,
and carries the wallet's answer back. The messages are encrypted, and Epicbox cannot spend the coins.

The Legacy Epicbox address is the wallet's public key, then `@` and the name of its Epicbox
server. Other Epic Cash wallets use Epicbox too, and two wallets can use different servers.

An [epic1 address](epic1.md) does not use this server setting. It uses the wallet's list of
mailboxes, under **Settings › Network & privacy**; see [Mailboxes](epic1.md#mailboxes).

## Change the Legacy Epicbox server

- **Desktop:** **Settings › Transactions › Epicbox**.
- **Phone:** tap the Epicbox icon on the Wallet tab, or **Settings › Network & privacy › Epicbox**.

The servers are listed with their state. Pick one and confirm, or type an address to filter the
list or add a server. Choosing another server changes the part after `@` of the Legacy Epicbox address, so give the new address
to the people who pay you.

If the server stops answering, or the network you are on blocks it, the wallet says so and offers
another server.

## Servers in the list

The list holds `epicbox.epiccash.com`, which is the default, then `epicbox.stackwallet.com`,
`epicbox.epicnet.us` and the BT LABS server `epicbox.btlabs.uk`. The BT LABS server is reached over
Tor at its onion address when [Tor](tor.md) is on. Its former name, `flooepicbox.btlabs.uk`,
is retired and takes no payments: a wallet that still has an address ending in it needs to switch
to a current server and share the new address.

## Turn off Legacy Epicbox address

**Legacy Epicbox address** is a switch under **Settings › Transactions** on the desktop and
**Settings › Payments** on the phone. It covers the wallet's legacy Epicbox address only, the one
stock Epic Cash wallets use. Off, the wallet does not read that address or send to legacy Epicbox
addresses, and Receive shows no Epicbox address. Payments sent to the address wait on the server
until the switch is on again.

Contacts, linked devices, epic1 payments and pairing use the mailbox list and keep working with
the switch off. **Node only** and **Kill switch** stop them; see
[Connection modes](network-modes.md).

The Epicbox protocol is described on the
[Epic Cash Developer Hub](https://devdocs.btlabs.uk).
