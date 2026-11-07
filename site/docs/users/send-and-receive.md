---
title: Send and receive
description: Receive your first EPIC, send to someone, and what happens in between.
---

# Send and receive

In Epic Cash both wallets take part in every payment (see
[How Epic Cash works](how-it-works.md)). The app does the steps; you share an address and approve.

## Receive

1. Open **Receive**.
2. Copy the **Epicbox address**, or show its QR code, and give it to the person who pays.
3. The payment shows up in Activity on its own.

The Epicbox address is about 52 characters starting with `es`, then `@` and the name of the Epicbox
server, for example `es…@epicbox.epiccash.com`. It is safe to share: people need it to
pay you, and nobody can take anything with it.

- **Desktop:** receiving starts by itself after unlock, once the node is synced. If the wallet is
  closed when someone pays, Epicbox holds the payment and the wallet collects it at the next
  unlock.
- **Phone:** receiving works while the app is open and the node is synced. A payment sent while
  the app is closed waits on the Epicbox server and arrives at the next unlock.

A new payment first waits for the sender's wallet to finish it, then shows as **Confirming**.
After the set number of confirmations (6 by default) it can be spent.

## Send

1. Open **Send** and paste the recipient's address, scan its QR code, open a
   [payment link](#payment-links), or pick a contact.
2. Enter the amount. The **Network fee** and the balance after the send are shown before you
   confirm.
3. Add a message if you like. It goes only to the other wallet, never to the blockchain.
4. **Review** on the desktop, **Continue** on the phone, check, then **Send … EPIC**. The desktop asks
   for the wallet password, the phone for the PIN.

Now the recipient's wallet has to answer. Over Epicbox they do not have to be online right now:
the payment waits until their wallet opens. Meanwhile the outputs the send uses are locked, so
they cannot be spent twice. When the answer comes back, the wallet finishes the transaction and
posts it to the network by itself.

**No answer?** The status says **Waiting for recipient**. Ask them to open their wallet. If the
answer never comes, [cancel the send](cancel.md) to unlock the outputs. A send nobody answers
cancels by itself after 1,440 blocks (about a day).

**Declined by the receiver** means their wallet refused the payment. The send is cancelled and its
coins are free to spend again.

An address of a known exchange can bring up a hint: **Looks like an exchange address. Check
the message.** Exchanges may call the message the on-chain note. The hint does not change the
address or the amount, and does not stop the send.

Sending needs a synced node. An Epicbox address also needs the Epicbox server to answer; a Link
address needs the recipient's wallet open and reachable at that moment.

## Payment links

A payment link opens by tapping, scanning, pasting or sharing, and fills in Send. There are two kinds.

- **`epiccash://pay/1/…`**, or a web link ending in `/p#1/…`. The wallet checks the service's
  signature, the payee's signature, the network, the expiry, and that the link was not made for someone
  else. A link that fails shows why and fills in nothing. You can change the amount; Send notes it.
- **A plain `epic:` link**, for example
  `epic:<address>?amount=0.01&message=VEND-0026&require=message&min=0.01`. The desktop app registers
  `epic:` and `epiccash:` on every platform.

## Other ways to pay

Send picks the method from the address in the To field. For the other methods, and when to use
them, see [Payment methods](payment-methods.md):

- **Link · HTTP** and **Link · Tor**: straight to the other wallet while it is open.
- **Direct · File Transfer**: a transaction file passed by hand.
- **Direct · QR Payment**: phone to phone, with an animated QR code.

## Activity

Every payment has a row in **Activity** with its state in words:
Waiting for recipient, Confirming 2 of 6, Received, Sent, Cancelled. Open a row for its steps and
details. Search finds a payment by name, address or transaction ID.

Rows labelled **Restored** or **Found by scan** come from a restore or a
[recheck](troubleshooting.md#the-balance-looks-wrong). Rows called **Sent from another device** or
**Received by another device** are payments of another wallet that uses the same recovery phrase
(see [Troubleshooting](troubleshooting.md#payments-by-another-wallet)). **Mining reward** rows are
block rewards; they show as **Maturing** until they can be spent.
