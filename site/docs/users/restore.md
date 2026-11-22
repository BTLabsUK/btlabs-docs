---
title: Restore and move a wallet
description: Restore from the recovery phrase, bring back wallet data, and import wallets from older Epic Cash apps.
---

# Restore and move a wallet

## Restore from the recovery phrase

1. Open **Restore from phrase**:
   - **Desktop:** on the first screen, or, from the Deeper view, **Unlock › Add a wallet** or
     **Settings › Wallets**.
   - **Phone:** on the first screen, or under **Settings › This wallet**.
2. Enter the words. If every word is in the word list but the phrase does not check out, a word is
   wrong or out of order.
3. Choose a password (desktop) or a PIN (phone).
4. The wallet opens and scans the blockchain for its outputs. The balance appears after that first
   scan; the payments it finds are labelled **Restored** on the desktop, **Found on the chain** on the
   phone.

A restore can start the scan from a later block or date, which is faster when you know the wallet
is newer than that.

## Your epic1 address after a restore

The same phrase gives the same epic1 address, so links and codes you shared before keep working.
With epic1 on, the wallet reads the mailboxes in its list once for payments waiting for the
address, and for messages from contacts. There is no gap to fill and nothing to set.

## What a restore cannot bring back

What was never on the blockchain: who paid what, notes and labels, contacts, invoices, pairings,
settings and wallet names. The [wallet data file](backups.md) keeps them: import it right after the
restore, when the wallet offers it.

## Recheck balance

When the balance looks wrong, run **Recheck balance** (desktop: **Settings › Wallet › Recheck balance**;
phone: **Settings › This wallet › Recheck balance**). It reads the whole blockchain again for this
wallet's outputs. With **Recheck from a height** on in [Advanced](advanced.md), it can start from a
block height or a date.

## From other Epic Cash wallets

A recovery phrase from any Epic Cash wallet restores in BT Wallet.

On the desktop, **Import wallets** on the first screen also reads wallets of older apps and wallet
folders, including their transaction history. The import only reads the old wallets
and files and never deletes or changes them.

:::warning
Before you import, have a backup of every wallet: its recovery phrase, and its wallet files if you
keep them. You import at your own risk.
:::

## The same wallet on two devices

After restoring on a second device, link the two devices: see [Linked devices](linked-devices.md).
Two unlinked installs on one recovery phrase are not supported.

<details>
<summary>For advanced users</summary>

Both installs see the same balance and share the one epic1 address, and only one of them reads a
mailbox at a time. Without a link, payments made on one show on the other only after the chain
confirms them. See [Linked devices](linked-devices.md#two-installs-on-one-address).

</details>
