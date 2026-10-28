---
title: Restore and move a wallet
description: Restore from the recovery phrase, bring back wallet data, and import wallets from older Epic Cash apps.
---

# Restore and move a wallet

## Restore from the recovery phrase

1. Open **Restore from phrase**:
   - **Desktop:** on the first screen, **Unlock › Add a wallet**, or **Settings › All wallets**.
   - **Phone:** on the first screen, or under **Settings › This wallet**.
2. Enter the words. If every word is in the word list but the phrase does not check out, a word is
   wrong or out of order.
3. Choose a password (desktop) or a PIN (phone).
4. The wallet opens and scans the blockchain for its outputs. The balance appears after that first
   scan; the payments it finds are labelled **Restored**.

A restore can start the scan from a later block or date, which is faster when you know the wallet
is newer than that.

## What a restore cannot bring back

What was never on the blockchain: who paid what, notes and labels, contacts, invoices, pairings,
settings and wallet names. The [wallet data file](backups.md) keeps them: import it right after the
restore, when the wallet offers it.

## Recheck balance

When the balance looks wrong, run **Recheck balance** (desktop: **Settings › Recheck balance**;
phone: **Settings › This wallet › Recheck balance**). It reads the whole blockchain again for this
wallet's outputs. With **Recheck from a height** on in [Advanced](advanced.md), it can start from a
block height or a date.

## From other Epic Cash wallets

A recovery phrase from any Epic Cash wallet restores in Epic Cash Desktop and Epic Cash Mobile.

On the desktop, **Import wallets** on the first screen also reads wallets of the older Epic Wallet
apps and wallet folders, including their transaction history. The import only reads the old wallets
and files and never deletes or changes them.

:::warning
Before you import, have a backup of every wallet: its recovery phrase, and its wallet files if you
keep them. You import at your own risk.
:::

## The same wallet on two devices

Restoring the same phrase on a second device works; both see the same balance. Payments made on one
show on the other as **Sent from another wallet** once confirmed. To keep them in step, see
[Linked devices](linked-devices.md).
