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

The Epicbox address is a long code that starts with `es` and ends in `@` and the name of the
Epicbox server, for example `es…@epicbox.epiccash.com`. It is safe to share: people need it to
pay you, and nobody can take anything with it.

- **Desktop:** receiving starts by itself after unlock, once the node is synced. If the wallet is
  closed when someone pays, Epicbox holds the payment and the wallet collects it at the next
  unlock.
- **Phone:** receiving works while the app is open and the node is synced. A payment sent while
  the app is closed waits on the Epicbox server and arrives at the next unlock.

A new payment first waits for the sender's wallet to finish it, then shows as **Confirming**.
After the set number of confirmations (6 by default) it can be spent.

## Send

1. Open **Send** and paste the recipient's address, scan its QR code, or pick a contact.
2. Enter the amount. The **Network fee** and the balance after the send are shown before you
   confirm.
3. Add a message if you like. It goes only to the other wallet, never to the blockchain.
4. **Review send**, check, then send. The desktop asks for the wallet password, the phone for the
   PIN.

Now the recipient's wallet has to answer. Over Epicbox they do not have to be online right now:
the payment waits until their wallet opens. Meanwhile the outputs the send uses are locked, so
they cannot be spent twice. When the answer comes back, the wallet finishes the transaction and
posts it to the network by itself.

**No answer?** The status says **Waiting for recipient**. Ask them to open their wallet. If the
answer never comes, [cancel the send](cancel.md) to unlock the outputs. A send nobody answers
cancels by itself after 1,440 blocks.

Sending needs a synced node. An Epicbox address also needs the Epicbox server to answer; a Link
address needs the recipient's wallet open and reachable at that moment.

## Other ways to pay

Send picks the method from the address in the To field. For the other methods, and when to use
them, see [Payment methods](payment-methods.md):

- **Link · HTTP** and **Link · Tor**: straight to the other wallet while it is open.
- **Direct · File Transfer**: a transaction file passed by hand.
- **Direct · QR Payment**: phone to phone, with an animated QR code.

## Activity

Every payment has a row in **Activity** (on the phone, History) with its state in words:
Waiting for recipient, Confirming 2 of 6, Received, Sent, Cancelled. Open a row for its steps and
details. Search finds a payment by name, address or transaction ID.

Rows labelled **Restored** or **Found by scan** come from a restore or a
[recheck](troubleshooting.md#the-balance-looks-wrong). Rows called **Sent from another wallet** or
**Received by another wallet** are payments of another wallet that uses the same recovery phrase
(see [Troubleshooting](troubleshooting.md#payments-by-another-wallet)).
