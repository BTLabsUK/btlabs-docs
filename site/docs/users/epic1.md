---
title: epic1 addresses and links
description: What an epic1 address and an epic1 link are, how a payment to them travels, and how to get paid and pay with them.
---

# epic1 addresses and links

An **epic1 address** is a wallet's own address for getting paid. It starts with `epic1` and is
117 characters long. It holds a version and two public keys: one that payments are sealed to, and
one that gives the address its own place in a mailbox. It names no mailbox. The same recovery
phrase always gives the same epic1 address, so it stays the same after a [restore](restore.md)
and when the mailbox list changes.

Each account has one epic1 address. Anyone with a wallet that has epic1 can pay it by pasting it,
opening it or scanning its QR code. The person who pays and the person who gets paid do not have
to be online at the same time. The payment is sealed so that only the payee's wallet can open it.

## Links

The address also comes as a link, written `epic:epic1…`. There are two kinds.

- A **payment link** is the address as a link. The payer chooses the amount.
- A **request link** is the address with an amount, a message, or both. They fill in the payer's
  Send screen, and the payer can change both.

The app makes a link from the address when you ask. It stores nothing, so there is no list of
links to keep and none to close. A link names no mailbox. Every link made from the same address
reaches the same account, and a payment of any amount to it arrives.

A link made outside the app, by a shop for example, can also list up to three web or Tor
addresses that take the payment directly. A payer's wallet pays such a link through those
addresses, one at a time in the link's order, and not through a mailbox.

## How a payment travels

![How an epic1 payment travels, in three lanes: payee's wallet, mailboxes, payer's wallet. 1. The payee's epic1 address or a link is shared. 2. The payer's wallet reads it and seals the payment for the payee. 3. On each mailbox, the address's place holds a copy; mailboxes both wallets list carry it. 4. The payee's wallet collects it, checks the amount and seals its answer. 5. On the mailbox, the payer's reply place holds the answer. 6. The payer's wallet collects the answer, finishes the transaction and posts it.](img/epic1-payment-path.svg)

1. The payee's wallet shares its epic1 address, or a link.
2. The payer's wallet reads it and builds the payment. It seals the payment so that only the
   payee's wallet can open it, and adds a reply place for the answer.
3. The payer's wallet posts a sealed copy to every mailbox in its own list.
4. The payee's wallet reads the mailboxes in its own list. It collects the payment, opens it and
   checks it.
5. The payee's wallet seals its answer for the payer and posts it back through every mailbox it
   read a copy on.
6. The payer's wallet collects the answer and asks the other mailboxes to drop their copies. It
   finishes the transaction and posts it to the Epic Cash network.

### The mailboxes

A mailbox is a server that holds payments and messages until a wallet reads them. Each wallet has
one list of mailboxes: the default ones, plus the ones you added, minus the ones you removed. The
wallet reads every mailbox in the list. The list is under **Network & privacy**; see
[Mailboxes](#mailboxes).

A payment arrives through a mailbox that both wallets list. Two wallets with the default list
share mailboxes, so a payment reaches the payee without either side setting anything. If the two
wallets share no mailbox, the payment is never collected: it ends at its deadline and its coins
are free again.

### The amount

A payee's wallet takes a payment of any amount. A request link only fills in the Send screen, so
the payer can pay a different amount. If the payee's wallet declines a payment, the payer's wallet
shows **Declined by the recipient**, and the payment's details say "The recipient declined this
payment. It was cancelled; the balance has not changed."

## epic1 and the Epicbox address

A wallet can have both. The [Legacy Epicbox address](addresses.md) (`es…@server`) names one
server and changes when the wallet moves to another server. The epic1 address names no mailbox
and does not change.

A wallet without epic1 cannot pay an epic1 address or link; it can pay the Legacy Epicbox
address. A payment to that address is a plain transaction.

## In the app

### Get paid

Open **Receive**. With epic1 on, the main code is the **epic1 address**. Copy it, or let the person
who pays scan its code. A payment of any amount to it arrives. **Copy link** and **Share** give
the same address as a payment link.

To ask for an amount or add a message, make a request link:

- On the phone, tap **Ask for an amount**, enter the **Amount** and a **Message (optional)**, then
  **Make link**.
- On the desktop, press **Ask for an amount** and fill in the same two fields, then **Make link**.

The QR code, **Copy link** and **Share** then carry the request link, and a line shows **Asks**
with the amount, or **Any amount** when there is only a message. **Clear** returns to the payment
link. Leaving the screen does the same, and the app keeps no record of the request.

A line on Receive shows **Listening for payments** while the wallet is connected. When no mailbox
can be reached it shows **No mailbox can be reached.** and **Mailboxes** opens the list. Once a
payment arrives, the wallet answers it by itself.

The Legacy Epicbox address shows under **Receive** only while its switch is on. On the desktop it
is in the **Other ways to receive** column.

### Pay

1. Paste the address or link on **Send**, scan its QR code, or open it. A
   [contact](pairing.md#contacts) with an epic1 address can be picked too.
2. Check the review: the recipient, the amount and the message. A request link fills in the amount
   and message, with **From the link** under each. You can change both. If you change the amount,
   the line reads **The link asks** and the amount.
3. Press **Send**.

### While it waits

The wallet posts the payment to every mailbox in its list. Once a mailbox takes it, the app shows
**Waiting for the recipient** until the payee's wallet answers. On the desktop, **Payment sent**
says "It shows on Home and under Activity until it completes." The phone shows **Sent** once the
payee's wallet answers.

**Cancel and unlock** cancels the payment and frees its coins. The desktop then shows **Payment
cancelled**, the phone **This payment was cancelled.**

### If no mailbox is shared

If your list has no default mailbox, a payment can fail at once with **No shared mailbox**.
Nothing was sent and no coins are locked. The step asks for the **Recipient's mailbox** (a host or
host:port) and offers **Add and pay**. The wallet tests the mailbox, adds it to your list, then
sends the payment. If the test fails, **Add anyway and pay** adds it all the same. **Cancel** returns to the review with your amount and message kept. A wallet that keeps a
default mailbox does not see this step.

### Turn it on or off

The switch is **epic1**, under **Settings › Transactions** on the desktop and **Settings ›
Payments** on the phone. It also covers in-person codes and epic1 files. With it off, Receive
shows no epic1 address or link, and an epic1 address on Send stops with **epic1 is off in the
payment settings.** See [Payment methods](payment-methods.md#epic1).

### Mailboxes

The list is under **Settings › Network & privacy**. On the phone, open **Mailboxes** (it shows
the number of entries). On the desktop it is the **Mailboxes** section.

Each row shows the host with **Default** or **Added by you**, its state, and when it last
answered:

| State | Meaning |
| --- | --- |
| **Connected · push on** | The mailbox answers and tells the wallet when mail arrives. |
| **Connected · no push** | The mailbox answers but does not offer to tell the wallet when mail arrives. The wallet asks again later. |
| **Not answering** | The mailbox failed, with the number of failures. It stays in the list. |
| **Connecting…** | The wallet has not tried it yet in this session. |

A mailbox that stops answering stays in the list, and the others carry the mail meanwhile. The
wallet does not add, remove or reorder mailboxes by itself.

**Add a mailbox:** type or paste a host or host:port, then press **Add {host}**. The wallet tests
it first: **Secure connection**, **Epicmail greeting** and **Push**. If all three pass, the
mailbox is added. If one fails, the results show with **{host} did not pass the test**, and **It
can still be added. Its state shows in the list.** **Add anyway** saves it; **Cancel** does not.
The wallet refuses an address that is not a host, a local or private address, a list that already
holds 16, and any add while Tor is on and not connected.

**Remove a mailbox:** press the bin on its row. **Undo** brings it back. The last mailbox cannot be
removed (**Keep at least one.**). Removing the last default mailbox while added ones remain asks
first: without a default mailbox, only wallets that list one of your mailboxes can pay you, and
paying an epic1 link asks for the recipient's mailbox. **Reset to defaults** restores the default
list.

When no mailbox in the list answers, Home shows **No mailbox can be reached**: payments and
messages wait until one answers.

The Legacy Epicbox address has its own server setting; see [Epicbox](epicbox.md).

### After the update

A wallet that existed before this update shows a notice on Home once: **epic1 address changed**
on the phone, **This wallet's epic1 address changed** on the desktop. Links and codes shared
before the update no longer work. Share the address again. **Receive** opens the Receive screen.
A wallet made or restored in this version does not show it.

After a [restore](restore.md) with epic1 on, the wallet reads the mailboxes in its list once for
payments waiting for the account's epic1 address.

## For advanced users

The address, the link format and the delivery rules are in LEPIC's
[epic1 guide](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epic1.md).
