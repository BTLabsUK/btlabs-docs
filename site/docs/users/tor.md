---
title: Tor
description: One switch routes the wallet's connections through Tor and gives it its own .onion address.
---

# Tor

Tor hides the wallet's IP address from the servers it talks to. It is one switch, off by default,
on Epic Cash Desktop and on Android. Tor runs inside the app: there is nothing to install. The
iPhone app and the [builds without Tor](install.md#builds-without-tor) have no Tor.

| App | Where |
| --- | --- |
| Desktop | **Settings › Privacy › Tor** |
| Android | **Settings › Privacy & network › Tor network** |

## With Tor on

- The connection to the Epicbox server goes through Tor.
- The connection to the node goes through Tor, unless the node runs on this computer.
- The app's own requests go through Tor: the status site, the price, the update check and problem
  reports.
- A send to a `.onion` address goes through Tor (**Link · Tor**).
- The wallet has a Tor address of its own, ending in `.onion`. Other wallets can pay straight to
  it, from anywhere, with nothing to open on the router. Receiving at it works while the app is
  open; Epicbox keeps working beside it.

Nothing you share changes: the same Epicbox address, the same node, the same server. A Link send to an `http(s)` address does not go over Tor; Send says so. On
the desktop, Link · HTTP receiving is off while Tor is on: payments straight from another wallet
arrive at the Tor address.

## No quiet fallback

While Tor starts, what goes over Tor waits; nothing goes around it. If Tor cannot connect, it says
**Not connected**, with **Retry** or turning Tor off. The desktop shows Tor's state in the sidebar.

Tor is slower than a direct connection. It is blocked or not allowed in some countries; there it
does not connect.

## Tor only

**Tor only**, a [network mode](network-modes.md) in Advanced, keeps the switch on and locked.
Nothing goes over the open internet, and node failover moves only to nodes reachable over Tor.
