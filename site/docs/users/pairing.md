---
title: Contacts, pairing and invoices
description: Contacts, pairing with a contact once, verifying, and invoices between paired contacts.
---

# Contacts, pairing and invoices

## Contacts

A contact is a name and an address: Epicbox, HTTP or Tor; the row says which. Send to a contact
from its page, or pick one on Send. Contacts are kept on the device and are included in the
[wallet data file](backups.md).

## Pairing (experimental)

Pairing and invoices are experimental and off to begin with. Turn them on in
**Settings › Advanced › Experimental**. Off, they are hidden and nothing is checked for them;
pairings already made stay saved and come back when the switch is on again.

Pairing links two wallets once. Each wallet keeps a key made for that one contact; nothing about it
is shared with the Epicbox server. After pairing, a transaction file to that contact is
**sealed**: only their wallet can open it, and it cannot be changed or forged on the way. Payments
over Epicbox keep working as before.

1. Open **Contacts** and choose **Pair**.
2. Choose a way: **Spoken**, **Invite by message** or **In person**.
3. Verify together, then **They match**.

Pairing needs BT Wallet on both sides. A contact that is not paired
still gets ordinary transaction files and Epicbox payments.

### Three ways to pair

- **Spoken.** One wallet shows five pairing words and leaves a sealed invite on the connection
  servers (by default epicbox.epiccash.com, epicbox.stackwallet.com and the BT LABS server, epicbox.btlabs.uk). The
  other wallet types the words under **Got words or a link?** and finds it. Both wallets must be
  online and reach one of these servers, so spoken invites need Epicbox. The words expire.
- **Invite by message.** Three messages in any chat: the invite, the reply, the finish link. No
  server is needed, so this works when a network blocks Epicbox.
- **In person.** Each phone scans the other's code. No network is used.

The wallet reads the clipboard only while Pairing is on, only when it comes to the front or the
Pair screen opens, and offers each link once. It never stores or logs what it reads.

### Why verify

After pairing, both wallets show the same four pictures and names. They come from the two wallets'
keys, so a pairing that someone changed on the way shows different words on the two screens.

- Compare them on a call or in person, then tap **They match**. The contact becomes **Verified**.
- **Skip for now** leaves it **Paired, not verified**: transaction files are still sealed, but the
  contact cannot send invoices until the words are checked.
- If the words differ, tap **They do not match**. The pairing is dropped on this side. Pair again,
  in person or with a fresh invite.

The word names stay in English in every language, so two people whose apps use different languages
can still compare them.

## Invoices (experimental)

Invoices need Pairing. Only a **Verified** contact you allow can ask you to pay:
**Allow invoices** on the contact page, or under **Settings › Invoices**.

- An invoice shows under **Invoices › Pay** with the contact's name, the amount and a reference.
- Nothing is paid until you approve it with the wallet password or PIN.
- An invoice never adds money to your wallet.
- Turning the switch off is immediate: new invoices from that contact are dropped and open ones are
  declined. Invoices from anyone else are dropped unread.

To ask for a payment: **Invoices › Issue** on the desktop, **Request a payment** on the phone. On
the phone a request can also be shown as a QR code the payer scans. A request nobody pays expires.

An exchange that pairs with you deposits and withdraws this way. Deposit: the exchange asks, you
approve, the exchange posts. Withdrawal: the exchange sends the payment, your wallet answers on its
own, the exchange posts.

## After a restore

- **With the wallet data file**, a restore brings every pairing back unchanged: same keys, same
  Verified marks, same settings. Contacts notice nothing.
- **Without it**, the pairings are gone from this wallet, but the keys are not: they come from the
  recovery phrase. Pair again with a contact who kept the pairing, and their wallet finds the same
  keys and keeps the Verified mark.
- A contact sees **Keys changed** only when the phrase is a different one. That can mean a new
  wallet, or someone else using the name. Check the words again before trusting it.

Use a pairing on one device at a time. For one wallet on several of your own devices, see
[Linked devices](linked-devices.md).
