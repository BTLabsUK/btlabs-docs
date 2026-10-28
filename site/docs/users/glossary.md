---
title: Glossary
description: The words the app uses, in plain language.
---

# Glossary

The terms as the app writes them, in alphabetical order.

- **Address**: Where a payment goes. An Epicbox address (`es…@server`), an HTTP address, or a Tor address (`….onion`). Never written on the blockchain. See [Addresses](addresses.md).
- **Advanced**: The Settings page with the parts most people never need, all off to begin with. See [Advanced settings](advanced.md).
- **Awaiting finalization**: A transaction still waiting for the other wallet.
- **Change**: The part of a spent output that comes back to your wallet as a new output.
- **Confirmation**: One block on top of the block holding a transaction. Final after 6 by default.
- **Confirming**: In a block, but with fewer confirmations than the setting. Not spendable yet.
- **Consolidate**: A payment to yourself that merges every spendable output into one.
- **Direct · File Transfer**: Paying with a transaction file (`.tx`) and a response file (`.response`) passed by hand.
- **Direct · QR Payment**: Paying phone to phone with an animated QR code. Epic Cash Mobile only.
- **Epicbox**: The server that carries payment messages between wallets and holds them while the other wallet is offline. See [Epicbox](epicbox.md).
- **EPIC**: The coin of Epic Cash.
- **Export wallet data**: Saves history, notes, contacts, invoices and settings in an encrypted wallet data file (`.wfeh`). See [Backups and wallet data](backups.md).
- **Floonet, Usernet**: Test networks. Their coins have no value. Mainnet holds real EPIC.
- **Held by**: Coins a linked device is spending, held on this device until its payment ends.
- **Invoice**: A request to be paid, sent between paired contacts. Experimental.
- **Link · HTTP, Link · Tor**: Paying straight to the other wallet while it is open, at a web address or a `.onion` address.
- **Linked devices**: One wallet on several of your own devices, kept in step. Experimental.
- **Locked**: Outputs in a send that is not finished yet.
- **Mimblewimble**: The protocol Epic Cash uses: no addresses or amounts on the blockchain.
- **Network fee**: What a transaction pays the miners. Depends on the number of outputs, not the amount.
- **Network modes**: Standard, Tor only and Offline. See [Network modes](network-modes.md).
- **Node**: A program connected to the Epic Cash network. The wallet reads the blockchain and posts through it. See [Nodes](nodes.md).
- **Output**: One piece of the balance, like a note in a wallet.
- **Pair, Paired, Verified**: Linking your wallet once with a contact's, so files between you are sealed. Verified means the four pictures were checked together. See [Pairing](pairing.md).
- **Recheck balance**: Reads the whole blockchain again for this wallet's outputs.
- **Recovery phrase**: The 24 words that are the backup and the key to the money. See [Recovery phrase](recovery-phrase.md).
- **Restored, Found by scan**: Payments the wallet found on the blockchain after a restore or a recheck.
- **Sealed**: A transaction file only the paired contact's wallet can open.
- **Sent from another wallet, Received by another wallet**: A payment made by another wallet with the same recovery phrase.
- **Slate**: The message two wallets pass back and forth to build a transaction.
- **Smallest, All**: Which outputs a send spends: the fewest small ones, or all of them.
- **Split, Split change**: Making several outputs of nearly equal value, on its own or inside a send.
- **Tor**: A network that hides the wallet's IP address. See [Tor](tor.md).
- **Waiting for recipient**: A send the other wallet has not answered yet.
