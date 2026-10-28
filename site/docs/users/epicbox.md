---
title: Epicbox
description: The server that carries payments between wallets and holds them while the other wallet is offline.
---

# Epicbox

Both wallets take part in every transaction, so their messages need a meeting point. An Epicbox
server is that meeting point: it holds a payment sent to this wallet until the wallet comes online,
and carries the wallet's answer back. The messages are encrypted, and Epicbox cannot spend the coins.

The Epicbox address is the wallet's public key, then `@` and the name of its Epicbox server. Other
Epic Cash wallets use Epicbox too, and two wallets can use different servers.

## Change the server

- **Desktop:** **Settings › Transactions › Epicbox**.
- **Phone:** tap the Epicbox icon on the Wallet tab, or **Settings › Privacy & network › Epicbox**.

The servers are listed with their state. Pick one and confirm, or type an address to filter the
list or add a server. Choosing another server changes the part after `@`, so give the new address
to the people who pay you.

If the server stops answering, or the network you are on blocks it, the wallet says so and offers
another server.

## Turn Epicbox off

Epicbox is a switch under **Settings › Transactions**. Off, the wallet connects to no Epicbox
server: no Epicbox payments or invoices, and Receive shows no Epicbox address. Payments sent to the
address wait on the server until it is on again.

The Epicbox relay protocol is described on the
[Epic Cash Developer Hub](https://devdocs.btlabs.uk).
