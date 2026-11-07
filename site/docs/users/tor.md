---
title: Tor
description: What goes through Tor, where it is turned on, and the wallet's own .onion address.
---

# Tor

Tor hides the wallet's IP address from the servers it talks to. It is off by default, on the desktop
app and on Android. Tor runs inside the app: there is nothing to install. The iPhone app and the
[builds without Tor](install.md#builds-without-tor) have no Tor.

| App | Where |
| --- | --- |
| Desktop | **Settings › Network & privacy › Tor only**. The Tor row in the sidebar shows its state. |
| Android | The Tor switch in **Settings › Network & privacy**, or the Tor only [connection mode](network-modes.md). |

**Link · Tor** under **Settings › Payments** (desktop) or **Settings › Transactions** (phone) is Tor
for payments alone: it gives the wallet a Tor address to be paid at and does not move the other
connections.

## With Tor on

- The connection to the Epicbox server goes through Tor.
- The connection to the node goes through Tor, unless the node runs on this computer or your local
  network.
- The app's own requests go through Tor: the status site, the price, the update check and problem
  reports. The price then comes from BT LABS' copy, never from CoinGecko directly.
- A send to a `.onion` address goes through Tor (**Link · Tor**).
- The wallet has a Tor address of its own, ending in `.onion`. Other wallets can pay straight to
  it, from anywhere, with nothing to forward on the router. Receiving at it works while the app is
  open; Epicbox keeps working beside it.

The addresses you share do not change. A Link send to an `http(s)` address does not go over Tor;
Send says so, and in Tor only it waits with **Plain http:// cannot go over Tor**. On the desktop,
Link · HTTP receiving is off while Tor is on: payments straight from another wallet arrive at the
Link · Tor address.

## No quiet fallback

While Tor starts or is not connected, what goes over Tor waits; nothing goes around it. **Retry**, or
turn Tor off.

Tor is blocked or not allowed in some countries; there it does not connect.

## Tor only

**Tor only** keeps Tor on until you leave the mode. Nothing goes over the open internet except a node
on this computer or your local network, and node failover moves only to nodes reachable over Tor. See
[Connection modes](network-modes.md).
