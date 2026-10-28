---
title: Cancelling a payment
description: When Cancel is certain, when it is not, and what happens to the coins.
---

# Cancelling a payment

Cancel is in **Activity**: open the payment, then **Cancel** (on the phone, **Cancel payment**).

## Sending

A payment you send waits for the other wallet to answer. While it waits, Cancel is certain:
nothing can reach the network without your wallet, and the coins are yours again at once. The
other wallet may still show the payment as waiting, but it cannot finish it.

Once the answer is in, your wallet finishes the payment and posts it to the network in one step.
A posted payment cannot be cancelled, undone or refunded; only the recipient can pay it back. If
the network refused it, the wallet offers to post it again or to cancel. That cancel asks the
network first and goes ahead only when the network does not have the payment.

A payment that stays unanswered cancels by itself after 1,440 blocks, and the coins are free
again. This holds for Epicbox, Link and Direct payments alike.

**A send looks stuck.** Usually the other wallet is offline. Wait, or cancel it and send again; a
cancelled payment cannot go through later.

## Receiving

When a payment arrives, your wallet answers at once, and nothing of yours is locked. From then on
the sender's wallet finishes and posts it, so Cancel stays out of the way for a while, and longer
while the sender reports it posted.

After that, Cancel clears a payment the sender never posted. It is not certain: the wallet asks
the network first and refuses when the payment is already there. A cancelled payment stays
watched. If the sender posts it later, it arrives anyway and shows as received.

## Invoices (experimental)

A request you sent holds no coins until it is paid. Withdraw it any time before then: the payer can
no longer pay it, and nothing moves. A request nobody pays expires. A request shown as a QR code
can be paid once; a second scan is refused.

A request you paid is the other way round: the other side holds your signed payment and finishes
it. Cancel comes once its time runs out, or sooner when the other side withdraws it. Cancelling
frees the coins here, but the other side could still post the payment until these coins are spent
again. On the desktop, sending them to yourself, offered with the cancel, makes it final.

See [Pairing and invoices](pairing.md).
