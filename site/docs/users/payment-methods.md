---
title: Payment methods
description: Epicbox, Link · HTTP, Link · Tor, Direct · File Transfer and Direct · QR Payment, and when to use each.
---

# Payment methods

A payment is a handshake between two wallets. The messages between them travel one of three ways.

| Method | Both online at once? | Server in between | Apps |
| --- | --- | --- | --- |
| **Epicbox** | no | an Epicbox server | both |
| **Link · HTTP** | yes | none | both |
| **Link · Tor** | yes | none (Tor) | desktop, Android |
| **Direct · File Transfer** | no | none | both |
| **Direct · QR Payment** | side by side | none | phone |

Each method has a switch in **Settings › Transactions**. **Epicbox** is on by default. A method
that is off does not appear on Send and Receive. **Send starts on** picks the method the Send
screen opens with.

## Epicbox

The everyday way and the default. The Epicbox server holds each message until the other wallet
comes online, so nobody has to be online at the same time. Messages are encrypted, and the server
cannot spend anything. See [Epicbox](epicbox.md).

## Link · HTTP and Link · Tor

Straight to the other wallet, with no server in between. The other wallet must be open and
reachable right now.

- **Link · HTTP** sends to a web address such as `http://host:3415`. Receiving this way is on the
  desktop only, and it is off until you turn it on under **Settings › Receiving**. To be paid from
  outside your own network, the port has to be reachable from the internet.
- **Link · Tor** sends to an address of 56 characters ending in `.onion`, over Tor. With
  [Tor](tor.md) on, the wallet has its own `.onion` address and can be paid at it, with nothing to
  open on the router.

If a Link send cannot reach the other wallet, try again later or send the same payment as a file.

## Direct · File Transfer

The manual way: the messages travel by hand, for example by email, chat or a USB stick. It works
without Epicbox and without both wallets being online at the same time.

1. **Sender:** on Send, choose **Direct · File Transfer**, enter the amount and save (desktop) or
   share (phone) the file. It ends in `.tx`. The outputs are locked from now on.
2. **Recipient:** opens the file, on the desktop under
   **Receive › Transaction files › Sign a transaction file**, on the phone under
   **Receive › Direct · File**. The wallet signs it and makes a response file ending in
   `.response`. They send that file back.
3. **Sender:** opens the response file, on the desktop under
   **Receive › Transaction files › Finalize a response file**, on the phone under
   **Receive › Direct · File**. The wallet finishes the transaction and posts it.

Other Epic Cash wallets have their own names for these steps; the files are the same. If the
response file never comes, [cancel the send](cancel.md) to unlock the outputs.

## Direct · QR Payment

Two phones next to each other pay with an animated QR code, with no connection between them.
Each phone needs only its node. Epic Cash Mobile only; the desktop has no camera scanning.

1. **Sender:** on Send, choose **Direct · QR Payment**, enter the amount and tap **Show QR**. The
   code stays hidden until you show it, counts 3, 2, 1, and hides itself again.
2. **Receiver:** on **Receive › Direct · QR**, tap **Scan payment QR**, accept the payment, then
   show the reply code the same way.
3. **Sender:** taps **Scan their reply**. The wallet posts the payment.

Keep the code in the frame until every part is read: a larger payment is a moving code in several
parts, and the ring and the count show how far the scan got. Nothing in the code is encrypted, so
show it only to the person you pay. Screenshots are blocked on the code screen. The send can be
cancelled until you scan the reply.

## Send defaults

With **Send options** on in [Advanced](advanced.md), **Settings › Transactions** also holds which
outputs a send spends (**Smallest** or **All**) and whether its change is split. See
[How Epic Cash works](how-it-works.md#smallest-or-all).
