---
title: Backups and wallet data
description: The recovery phrase backs up the money; the wallet data file backs up everything else.
---

# Backups and wallet data

Two things, for two jobs:

| | Recovery phrase | Wallet data file |
| --- | --- | --- |
| Brings back the balance | yes | no |
| Brings back history, notes, labels, contacts, invoices, pairings, settings, wallet names | no | yes |
| Restores a wallet on its own | yes | no |
| Where | on paper | a file ending in `.wfeh` |

## The recovery phrase

The recovery phrase brings back everything that is on the blockchain, which is the balance. Keep it
on paper. See [Recovery phrase](recovery-phrase.md).

## Export wallet data

**Settings › This wallet › Export wallet data** saves the rest in one file, for example
`epic-history-mainnet-20260930.wfeh`. On the phone, share it or save it to the device, and keep a
copy off the phone, such as in email or cloud storage.

- The file is encrypted under a key that comes from the wallet's recovery phrase. It can only be
  imported into the same wallet.
- It holds no recovery words and cannot restore a wallet on its own.
- **Export CSV** is something else: a readable list of payments for a spreadsheet. It is not
  encrypted and cannot be imported.

To bring the data back: restore the wallet from its recovery phrase first, then import the file.
The wallet offers that right after a restore.

## The wallet's files on the desktop

The app keeps its wallets in its data folder: `.epic_cash_desktop` in your home folder (on Windows
`C:\Users\<name>\.epic_cash_desktop`). **Settings › This wallet › Wallet folder** opens it. A copy
of the folder is not a substitute for the recovery phrase: the phrase works when the files are
lost.

### Clean up old wallet folders

**Remove from list** in **Settings › All wallets** takes a wallet off the list but leaves its folder
on disk. To delete the folder:

1. Open the data folder: **Open folder** next to **Settings › This wallet › App files**.
2. Open `wallets`. Each added wallet has its own folder named by a long ID; the first wallet's folder
   is `mainnet`.
3. To tell them apart, open an ID folder, then its `mainnet` folder, and read `WALLET.txt`.
4. Make sure you have that wallet's recovery phrase written down, or that it holds no EPIC you want
   to keep.
5. Close Epic Cash Desktop and delete that one ID folder. Leave `mainnet`, `wallets.json` and
   everything else as it is.

:::warning
Deleting a wallet folder without its recovery phrase loses the EPIC in it.
:::

Versions before 26.10.16 kept their data in `~/.local/share/com.blacktyger.epicwallet` on Linux and
in `%APPDATA%\com.blacktyger\EpicWallet` on Windows. Once every wallet from there has been restored
in the current app and shows its balance, that old folder can go too.
