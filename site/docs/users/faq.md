---
title: FAQ
description: Short answers to common questions about BT Wallet.
---

# FAQ

## Is it free?

Yes. The apps and their source are under the Apache License 2.0. Each payment pays the network fee,
which goes to the miners.

## Who holds my coins?

You do. The keys are made and kept on your device, and nobody else can spend the EPIC without your
recovery phrase. BT LABS cannot see or move your coins and cannot recover a lost phrase.

## Can I use the same wallet on my phone and my computer?

Yes: restore the same recovery phrase on both. To keep them in step, turn on
[Linked devices](linked-devices.md).

## Does the other person need to be online when I pay?

Not over Epicbox: the payment waits on the server until their wallet opens. Link methods need the
other wallet open; File Transfer and QR Payment pass the messages by hand. See
[Payment methods](payment-methods.md).

## Why is part of my balance locked after a send?

A send spends whole outputs and the change comes back as a new output, which confirms like any
payment. See [How Epic Cash works](how-it-works.md#outputs-and-change).

## Can I cancel a payment?

Before the other wallet has answered, yes, for certain. After it is posted to the network, no. See
[Cancelling a payment](cancel.md).

## Does it work with other Epic Cash wallets?

Yes. Epicbox, Link · HTTP, Link · Tor and transaction files work with the standard Epic Cash
wallet and others. A recovery phrase from another Epic Cash wallet restores here. Pairing, invoices,
QR Payment and Linked devices need BT Wallet on both sides.

## Do I need to run a node?

No. The wallet uses a public node by default. Running your own is an option: see
[Nodes](nodes.md).

## Is Tor required?

No. Tor is off by default and optional. There are also builds with Tor left out. See [Tor](tor.md).

## What does the app send to BT LABS?

Only what is listed on [Privacy](privacy.md): requests to the default node and status site, the
update check, and a problem report when you send one. No analytics.

## Can I test without real money?

The app runs on the main network only. To try it, make a wallet and move a very small amount of EPIC
between two wallets of your own.

## Where do I report a bug or a security problem?

A bug: **Report a problem** in the app's Help, or support@btlabs.uk. A security problem: see
[Security](../security.md).
