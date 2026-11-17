---
title: epic1 addresses and links
description: What an epic1 address and an epic1 link are, how a payment to a link travels, and how to get paid and pay with one.
---

# epic1 addresses and links

An **epic1 address** is a wallet's own address for getting paid. It names the wallet, not a server.
The same recovery phrase always gives the same epic1 address, so it stays the same after a
restore.

An [Epicbox address](addresses.md) (`es…@server`) holds the name of one server, so it changes when
the wallet moves to another server. An epic1 address holds no server, mailbox or transport, so it
stays the same when the server changes. Where to deliver a payment goes in the link instead.

To get paid, the wallet shares an **epic1 link**: the epic1 address plus where to deliver the
payment, and the amount when one is asked. Anyone with a wallet that has epic1 can pay the link by
pasting it, opening it or scanning its QR code. The person who pays and the person who gets paid
do not have to be online at the same time.

The payment is sealed so that only the payee's wallet can open it. It travels through an Epicbox
server, which holds it until the payee's wallet collects it.

## How a payment travels

![How an epic1 payment travels, in three lanes: payee's wallet, Epicbox server, payer's wallet. 1. The payee's wallet makes an epic1 link or QR code. 2. The payer's wallet reads the link and seals the payment for the payee. 3. On the Epicbox server, the link's mailbox holds the payment; if that server does not take it, the payer's wallet tries the next server in the link. 4. The payee's wallet collects it, checks the amount and seals its answer. 5. On the Epicbox server, the payer's reply mailbox holds the answer. 6. The payer's wallet collects the answer, finishes the transaction and posts it.](img/epic1-payment-path.svg)

1. The payee's wallet makes an epic1 link, shown as text and as a QR code. The link names a mailbox
   on an Epicbox server, and the amount when one is asked.
2. The payer's wallet reads the link and builds the payment. It seals the payment so that only the
   payee's wallet can open it, and adds a reply mailbox on the payer's own Epicbox server.
3. The payer's wallet posts the sealed payment to the first server the link names. If that server
   does not take it, the payment can go to the next server in the link.
4. The payee's wallet collects the payment from the server, opens it and checks it. A payment with
   a different amount from the one the link asks is refused.
5. The payee's wallet seals its answer for the payer and posts it to the payer's reply mailbox.
6. The payer's wallet collects the answer, finishes the transaction and posts it to the Epic Cash
   network.

## epic1 and the Epicbox address

A wallet has both. The [Epicbox address](addresses.md) (`es…@server`) names one mailbox on one
Epicbox server, and payments to it go to that mailbox.

An epic1 address works differently:

- **It names the wallet only.** It holds two public keys: one that payments are sealed to, one
  that checks the payee's payment proofs. It holds no server, mailbox or amount.
- **The link says where to deliver.** An epic1 link adds a mailbox made for that link, on one to
  three Epicbox servers, and can add an amount and a message.
- **The payer's wallet seals and posts.** It seals the payment to the epic1 address, posts it to the
  first server in the link, and moves on to the next server when one does not take it.
- **The payee's wallet answers.** It collects the payment, checks the amount against the link and
  sends its answer to the reply mailbox the payer named.
- **One account, many addresses.** An account can have numbered epic1 addresses, for example one
  per shop or per invoice. Payments to every one of them come to the same account.

An epic1 address on its own, without a link, cannot be paid in BT Wallet. A wallet without epic1
cannot pay an epic1 link; it can pay the Epicbox address.

## In the app

BT Wallet makes every link for the account's first epic1 address, on the wallet's own Epicbox
server. The app does not show the epic1 address on its own or issue numbered addresses.

### Get paid

1. Open **Receive**.
   - On the desktop, press **Make link** on the **epic1 link** panel ("Anyone with epic1 can pay
     this link."). Click the covered QR code to show it.
   - On the phone, tap **Other ways to receive**, then **epic1 link**. The link and its QR code
     appear.
2. Give the link to the person who pays: **Copy link**, **Share** on the phone, or let them scan the
   QR code.

To ask for a set amount, use **Ask an amount** on the desktop or **Ask for an amount** on the
phone. Enter the amount and, if you like, a message. The new link asks that amount.

On the phone, the epic1 link page shows **Listening for payments** while the wallet is connected to
its Epicbox server. Once a payment arrives, the wallet answers it by itself.

### Pay a link

1. Paste the link on **Send**, scan its QR code, or open it. A [contact](pairing.md#contacts) whose
   address is an epic1 link can be picked too.
2. Check the review: **To** (the address), **Amount** and **Server**. A note from the recipient
   shows as **Message** on the phone and **Note from the recipient** on the desktop. An amount the
   link asks is **Set by the recipient** and cannot be changed.
3. Press **Send**.

If the link names a server that is not in the wallet's server list, **Send through this server?**
comes first. **Use server** goes on.

### While it waits

The send shows **Waiting for the recipient** until the payee's wallet answers. Then the phone
shows **Sent** and the desktop shows **Payment sent**.

- If no server took the payment, the desktop shows **No server took the payment yet.** and the
  phone shows which server did not take it. **Try next server** posts it to the link's next server.
- **Cancel and unlock** cancels the payment and frees its coins. The phone then shows **Payment
  cancelled. The coins are free again.**

### Turn it on or off

The switch is **epic1**, under **Settings › Transactions** on the desktop and **Settings ›
Payments** on the phone. It is on by default. It also covers in-person codes and epic1 files. With
it off, Receive has no epic1 link, and an epic1 link on Send stops with **epic1 is off in the
payment settings.** See [Payment methods](payment-methods.md#epic1).

After a [restore](restore.md) with epic1 on, the wallet checks the link mailboxes on its own
Epicbox server once for payments waiting there.

## For advanced users

- **The address.** bech32m over 65 bytes: a version byte (`01`), the Ed25519 proof key and the
  X25519 seal key. The prefix is `epic` on mainnet, so an address starts with `epic1` and is 115
  characters long. Both keys derive from the seed, the account and the address number. The number
  is not in the address.
- **The link.** `epic:epic1…?epicbox=<mailbox>@<server>&amount=…&message=…`. Each `epicbox` entry is
  an Epicbox address on a server, at most three entries, tried in order. `amount` is decimal EPIC
  with up to 8 decimals. A link with no usable `epicbox` entry cannot be paid; there is no default
  server.
- **Link mailboxes.** Each link gets its own Epicbox mailbox, derived from the seed. Links shown on
  screen take the next of 50 mailboxes in turn. The wallet's collect checks every link mailbox in
  use.
- **Sealing.** The payment is an anonymous envelope sealed to the epic1 seal key with HPKE (RFC
  9180, X25519, HKDF-SHA256, ChaCha20-Poly1305). Inside the seal it carries the payer's one-time
  reply key and the reply mailbox on the payer's server. The answer is sealed to that reply key.
  Envelopes are posted as `BEGINEPICTX.` text.
- **Servers named in a link** are checked: host names of letters, digits and dots, no hyphens. A
  server on this device is refused. A server on the local network brings up **Use a server on the
  local network?** on the desktop or **Use a local network server?** on the phone, because only
  wallets on the same network can pay such a link.
- **Payment proofs.** When the payer asks for one, the payee's wallet signs it with the proof key of
  the address that was paid.
- **Numbered addresses.** Each address of an account has a number, starting at 0. A restored wallet
  looks 50 numbers past the highest one it knows for payments.
- The formats are specified in LEPIC's RFC 0003, sections 5.13, 5.14 and 5.19.
