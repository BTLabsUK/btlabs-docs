---
title: Troubleshooting
description: The usual causes when something goes wrong, and what to do.
---

# Troubleshooting

Most problems are a node still syncing, a recipient who has not answered yet, or, on the desktop, a
busy port.

## "Node not synced": cannot send

Sending opens when the node has caught up. Wait, or choose another node: **Settings › Node** on the
desktop, the node icon on the Wallet tab on the phone. See [Nodes](nodes.md).

## "Epicbox not answering"

The wallet cannot reach its Epicbox server. If it stays like this, check the connection or pick
another server ([Epicbox](epicbox.md)). Meanwhile **Direct · File Transfer** works.

## A send says "Waiting for recipient"

Their wallet has not answered yet. Ask them to open it. If they never will,
[cancel the send](cancel.md) in Activity to unlock the outputs.

## A payment has not arrived

- Check that the node is synced and Epicbox is connected: the status icons on the phone's Wallet
  tab, or Receive on the desktop.
- After a change of Epicbox server, the sender needs the new address.
- The sender's wallet also has to finish the transaction; then it waits for its confirmations.

## Tor says "Not connected"

Tor could not reach its network. **Retry**, or turn Tor off; nothing goes out over Tor meanwhile.
Tor is blocked in some countries. See [Tor](tor.md).

## "Port 3415 is in use by another program" (desktop)

Another program, often another Epic wallet, uses the port for Link · HTTP payments. Close it, then
press **Try again** on Receive. Epicbox, Link · Tor and Direct · File Transfer keep working
meanwhile.

## "Another Epic program is using this folder" (desktop)

Another Epic wallet or node has the same files open. Close it and try again.

## "Wrong password" or a forgotten PIN

- **Desktop:** check Caps Lock and the keyboard layout. A forgotten password: **Forgot password?** on
  the unlock screen sets a new one with the recovery phrase. See
  [Recovery phrase](recovery-phrase.md).
- **Phone:** **Forgot PIN?** deletes the wallet on the unlock screen; restore it from its recovery
  phrase with a new PIN. Without the phrase the EPIC cannot be recovered.

## An action is greyed out and names a mode, or says "Waiting for Tor"

A [connection mode](network-modes.md) is on under **Settings › Network & privacy**. Set the mode back
to Normal there, or wait for Tor to connect.

## The balance looks wrong

Run **Recheck balance** (desktop: **Settings › Wallet › Recheck balance**; phone:
**Settings › This wallet › Recheck balance**). It reads the whole blockchain again for this wallet's
outputs.

## Payments by another wallet

A row called **Sent from another device** or **Received by another device** is a payment of another
wallet that uses the same recovery phrase. The chain shows these coins spent or received, so this
wallet lists it with the amount only.

If you use no other wallet with this phrase, ask another node first: switch to another node and run
Recheck balance. A node that leaves coins out of its answers can make them look spent. If they still
show spent, someone else may have the recovery phrase: move the EPIC to a new wallet with a new
phrase.

## Coins held by another device

See [Linked devices](linked-devices.md#coins-held-by-another-device).

## Still stuck

**Report a problem** in Help sends a description and cleaned logs to BT LABS. The screen shows
exactly what is sent. Or write to support@btlabs.uk. Never send your recovery phrase to anyone.
