---
title: epic1 addresses and links
description: What an epic1 address and an epic1 link are, how a payment to them travels, and how to get paid and pay with them.
---

# epic1 addresses and links

An **epic1 address** is a wallet's own address for getting paid. It starts with `epic1` and is
117 characters long. It holds a version and two public keys: one that payments are sealed to, and
one that gives the address its own mailbox. It names no server. The same recovery phrase always
gives the same epic1 address, so it stays the same after a [restore](restore.md) and when the
wallet changes its Epicbox server.

An **epic1 link** is the address, written `epic:epic1…`, and it can add an amount and a message.
A link made outside the app, by a shop for example, can also list up to three servers that take
the payment directly. Anyone with a wallet that has epic1 can pay an
epic1 address or link by pasting it, opening it or scanning its QR code. The person who pays and
the person who gets paid do not have to be online at the same time.

The payment is sealed so that only the payee's wallet can open it.

## How a payment travels

![How an epic1 payment travels, in three lanes: payee's wallet, Epicbox servers, payer's wallet. 1. The payee's epic1 address or a link is shared. 2. The payer's wallet reads it and seals the payment for the payee. 3. On each Epicbox server, the address's mailbox holds a copy; servers both wallets use carry it. 4. The payee's wallet collects it, checks the amount and seals its answer. 5. On the Epicbox server, the payer's reply mailbox holds the answer. 6. The payer's wallet collects the answer, finishes the transaction and posts it.](img/epic1-payment-path.svg)

1. The payee's wallet shares its epic1 address, or a link with the amount it asks.
2. The payer's wallet reads it and builds the payment. It seals the payment so that only the
   payee's wallet can open it, and adds a reply mailbox for the answer.
3. The payer's wallet posts a sealed copy to the address's mailbox on every Epicbox server in its
   own list.
4. The payee's wallet watches its mailbox on the servers in its own list. It collects the payment,
   opens it and checks it.
5. The payee's wallet seals its answer for the payer and posts it to the payer's reply mailbox, on
   the server it collected the payment from.
6. The payer's wallet collects the answer and asks the other servers to drop their copies. It
   finishes the transaction and posts it to the Epic Cash network.

A link that lists servers is paid through those servers only, one at a time in the link's order,
and not through the mailbox.

### The servers

Each wallet uses its own Epicbox server and the servers under **Extra Epicbox servers**. By
default that list holds `epicbox.btlabs.uk`, `epicbox.epiccash.com` and `epicbox.epicnet.us`. Two
wallets with the default list share a server, so a payment reaches the payee without either side
setting anything.

A payment arrives only through a server that both wallets list. A private Epicbox server carries
a payment only when the payer's wallet lists it too. If the two wallets share no server, the
payment is never collected: it ends at its deadline and its coins are free again.

### The amount

A link that asks an amount is paid that amount only. The payee's wallet declines a payment with
another amount. The payer's wallet then shows **Declined by the recipient**, and the payment's
details say "The recipient declined this payment. It was cancelled; the balance has not changed."

### Numbered addresses

An account has numbered epic1 addresses. Number 0 is the public address, shown on Receive. Each
link that asks an amount is made on the next numbered address, so every such link has its own
mailbox. Payments to every address come to the same account.

At most 256 links are open per account. A retired link's address does not answer, and payments to
it stop arriving. Number 0 is never retired.

## epic1 and the Epicbox address

A wallet has both. The [Epicbox address](addresses.md) (`es…@server`) names one server and changes
when the wallet moves to another server. The epic1 address names no server and does not change.

A wallet without epic1 cannot pay an epic1 address or link; it can pay the Epicbox address. A
payment to the Epicbox address is a plain transaction.

## In the app

### Get paid

Open **Receive**. With epic1 on, the code shown first is the **epic1 address**. The Epicbox
address is in the row under it; **Show as a code** swaps the two. Copy the epic1 address, or let
the person who pays scan its code. A payment of any amount to it arrives.

To ask for an amount, make a link:

- On the desktop, press **Make link** on the **epic1 link** panel ("Anyone with epic1 can pay this
  link."). Then **Ask an amount** asks for a set amount. Click the covered QR code to show it.
- On the phone, tap **Other ways to receive**, then **epic1 link**. Tap **Ask for an amount**,
  enter the **Amount** and a **Message (optional)**, then **Make link**.

Give the link with **Copy link**, **Share** on the phone, or let the person who pays scan the QR
code. On the phone, the epic1 link page shows **Listening for payments** while the wallet is
connected. Once a payment arrives, the wallet answers it by itself.

### Pay

1. Paste the address or link on **Send**, scan its QR code, or open it. A
   [contact](pairing.md#contacts) with an epic1 address can be picked too.
2. Check the review, **Review payment** on the desktop and **Review** on the phone: the
   recipient, the amount, and **Server** when the link lists servers. A message from the recipient
   shows as **Message** on the phone and **Note from the recipient** on the desktop. An amount the
   link asks cannot be changed; the desktop marks it **Set by the recipient**.
3. Press **Send**.

### While it waits

Once a server takes the payment, the app shows **Waiting for the recipient** until the payee's
wallet answers. On the desktop, **Payment sent** says "It shows on Home and under Activity until
it completes." The phone shows **Sent** once the payee's wallet answers.

- If no server took the payment, the app shows **No server took the payment yet.** The phone also
  names the server that did not take it. With a link that lists servers, **Try next server** posts
  it to the next one. A payment to an address went to every server at once, so it has no next one.
- **Cancel and unlock** cancels the payment and frees its coins. The desktop then shows **Payment
  cancelled**, the phone **This payment was cancelled.**

### Turn it on or off

The switch is **epic1**, under **Settings › Transactions** on the desktop and **Settings ›
Payments** on the phone. It also covers in-person codes and epic1 files. With it off, Receive
shows no epic1 address or link, and an epic1 address on Send stops with **epic1 is off in the
payment settings.** See [Payment methods](payment-methods.md#epic1).

**Extra Epicbox servers** is under **Settings › Transactions** on the desktop and **Settings ›
Network & privacy** on the phone. Each server shows **Takes payment links**, **No payment links**
or **Payment links not checked**.

### Open links

**Open links**, next to the epic1 switch, shows how many links are open, for example **3 of 256**.
Each link shows **Made** with its day. Once it is paid, the desktop shows **Last paid** with the
day, and the phone adds **Paid**. **Retire** asks first, then closes the link, and payments to it
stop arriving. With 256 open, making another link stops with **Too many links are open.** and the
place to retire one.

After a [restore](restore.md) with epic1 on, the wallet reads the mailboxes of the account's
addresses once for payments waiting there.

## For advanced users

The address, the link format and the delivery rules are in LEPIC's
[epic1 guide](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epic1.md).
