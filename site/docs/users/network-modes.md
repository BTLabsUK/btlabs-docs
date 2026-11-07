---
title: Connection modes
description: Normal, Tor only, Node only and Kill switch, and what each one lets the wallet reach.
---

# Connection modes

How much of the internet the wallet uses is one choice, **Connection mode**, under
**Settings › Network & privacy**. Help calls these the network modes. The wallet remembers the
choice. Off **Normal**, a mark on Home or the title bar names the mode: tap it to change it.

| Mode | What connects |
| --- | --- |
| **Normal** | Node, Epicbox, Link, the status site, price and update checks. The default. |
| **Tor only** | The same, with every connection through [Tor](tor.md). |
| **Node only** | Only the node in use. |
| **Kill switch** | Nothing, the node included. |

Services a mode turns off show as **Off (Node only)** in grey. Nothing is cancelled when you switch:
a send waiting for its recipient over Epicbox continues when you leave the mode, or switch to Tor
only.

## Tor only

Every connection goes through Tor, the node and Epicbox included. A node on this computer or your
local network may stay direct. Until Tor is ready nothing connects, the status icons say
**Waiting for Tor**, and nothing falls back to the open internet. Link · HTTP receiving stays off.
Not in the iPhone app or the [builds without Tor](install.md#builds-without-tor).

## Node only

The wallet reaches only the node in use, the first in the node list. Epicbox, Link, the status site,
price and update checks, explorer links, problem reports, pairing and linked devices are off.
**Direct · File Transfer**, and on the phone **Direct · QR Payment**, work. With Tor on, the node is
reached over Tor.

The node in use sees every request. A node on this device or your own network keeps that to
yourself and answers fast. Any node works.

## Kill switch

Nothing connects, the node included. The wallet opens with the last known balance and history. You
can make, sign and finish a payment by **Direct · File Transfer**, and on the phone by
**Direct · QR Payment**, show your address, back up and export. Sends that are waiting pause, and
continue when you leave the mode.

### Paying from Kill switch

1. Make the payment, and finish it when the reply comes back.
2. It shows as **Finished, not posted**.
3. Choose **Save file**, on the phone also **Show QR**; on the desktop you can **Copy** the text.
4. On an online device open **Post a finished payment**: on the phone in the Activity menu, on the
   desktop under **Receive › Transaction files**. Load the file, scan the code or paste the text,
   then press **Post**. Any Epic Cash wallet can do this; it needs no key.
5. The payment shows as **To be posted elsewhere**, then **Confirming** once it is seen on the chain
   after you leave Kill switch.
