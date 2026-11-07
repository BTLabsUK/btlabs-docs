---
title: Contacts, pairing and invoices
description: Contacts, pairing with a contact once, checking the words, payments and files after pairing, and invoices.
---

# Contacts, pairing and invoices

## Contacts

A contact is a name and an address: Epicbox, HTTP or Tor; the row says which. Send to a contact
from its page, or pick one on Send. Contacts are kept on the device and are included in the
[wallet data file](backups.md).

## Pairing

Pairing links two wallets once: with a request to a contact you have paid over Epicbox, or with
your invite, scanned as a QR or opened as a link. Each wallet keeps a key made for that one
contact; nothing is shared with anyone else.

After pairing, payments, transaction files and invoices between the two wallets are **sealed**:
only the other wallet can read them, and the contact's identity is checked.

1. Open **Contacts** and choose **Pair**.
2. Pair with a contact, or show your invite and let them scan it.
3. Check the words together, then **They match**. A request needs no words.

Pairing needs BT Wallet on both sides. A contact that is not paired still gets ordinary transaction
files and payments to the public Epicbox address.

### Two ways to pair

- **Pair with a contact.** For a contact you have paid, or been paid by, over Epicbox. The request
  goes to that address and their wallet shows it when it opens. One tap, and both sides are
  **Verified** without words. A request goes only to a wallet shown to run BT Wallet: a marked
  payment between the two addresses in the last 30 days. For anyone else, **Pair** shows your
  invite.
- **Pair by invite.** **Contacts › Pair** shows an invite, good for 7 days. The other person scans
  it or opens the link. Both wallets finish over Epicbox, then compare four words. With Epicbox
  off, the same screen carries the answer and the finish link by hand, with **Share** and **Paste**.

A name is optional. Leave it empty to pair without one: the other side sees **Unnamed wallet**.

### Why check the words

After an invite, both wallets show the same four pictures and names. They come from the two
wallets' keys, so a pairing changed on the way shows different words on the two screens.

- Compare them in person, by voice or by video, never in the chat the invite came through.
- **They match** makes the contact **Verified**: the wallet behind the address in your Contacts.
- **They do not match** ends the pairing on both sides, and nothing sent through it is finished.
  A mistaken No ends it too. Pair again with a fresh invite.

### What the contact page shows

| Label | Means |
| --- | --- |
| **Waiting** | The other wallet is not heard yet. |
| **Paired, not verified** | The words have not been checked. |
| **Verified** | The words matched, or a request paired the two wallets. |
| **Keys changed** | The contact's keys are different. Sealing and invoices pause until you choose **Keep the old keys** or **Use the new keys**. Verify the contact again. |
| **Not answering** | On a paired shop or exchange: the check after a long gap got no answer. Invoices and payments may not reach them. |
| **Ended** | The pairing is over. |
| **Removed by** and a name | The contact removed the pairing. |

**Verified BT Labs service** marks an invite whose key is one of BT LABS' services. A **Domain** row means
a service claims a web domain, and it reads **verified**, **not verified yet** or **refused**. The
wallet checks the claim at `https://<domain>/.well-known/epic-wallet.json`, over HTTPS, with no
redirects. **Automated service** marks a contact that a program answers. **No payments** marks a
contact that takes none: its coin is struck through on Send, and pasting or scanning it is refused.

### After pairing

Send offers two addresses for a paired contact.

- **Paired address.** Send starts on it, and the payment is sealed. It uses separate keys and is not
  shown. It runs over Epicbox, on a server suggested at pairing. The suggestion is accepted only if
  the server is in your list; otherwise the wallet asks.
- **Public address.** The contact's ordinary address. Send picks it when the contact last answered
  from another wallet app, when nothing has been heard in a long while, when a paired payment went
  unanswered, or when the server is down.

A paired payment nobody answers offers **Cancel and send to their public Epicbox address**. The
wallet asks first. A contact paired by invite has no public address unless you add one.

**Seal transaction files** on the contact page covers files only.

When a contact moves to another Epicbox server, the wallet follows a move to a public server and
says so on the contact page. A contact with a proven domain or a BT LABS key asks first:
**Accept** also adds the server to your Epicbox servers, and if you refuse, nothing changes and the
contact is not told.

## Invoices

Only a **Verified** contact you allow can ask you to pay. **Allow invoices** starts off. It is on
the contact page, on the verified result right after pairing, and under **Settings › Invoices** on
the desktop or **Settings › This wallet › Invoices** on the phone.

- An invoice shows under **Invoices › Pay** on the desktop and **Invoices › To pay** on the phone,
  with the contact's name, the amount and a reference.
- Nothing is paid until you approve it with the wallet password or PIN.
- An invoice never adds money to your wallet.
- Turning the switch off is immediate: new invoices from that contact are dropped and open ones are
  declined.

To ask for a payment: **Invoices › Issue** on the desktop, **Request a payment** on the phone.  nobody pays expires
after 24 hours. The time is **Time to pay** under **Settings › Invoices**, at most 48 hours.

An exchange that pairs with you deposits and withdraws this way. Deposit: the exchange asks, you
approve, the exchange posts. Withdrawal: the exchange sends the payment, your wallet answers on its
own, the exchange posts.

## After a restore

- **With the wallet data file**, a restore brings every pairing back unchanged: same keys, same
  Verified marks, same settings. Contacts notice nothing.
- **Without it**, the pairings are gone from this wallet, but the keys are not: they come from the
  recovery phrase. Pair again with a contact who kept the pairing, and their wallet finds the same
  keys and keeps the Verified mark. **Seal transaction files** and **Allow invoices** start at their
  defaults.
- A contact sees **Keys changed** only when the phrase is a different one. That can mean a new
  wallet, or someone else using the name. Check the words again before trusting it.

Use a pairing on one device at a time. Imported data on a second device asks before it uses the
contacts. For one wallet on two of your own devices, see [Linked devices](linked-devices.md).
