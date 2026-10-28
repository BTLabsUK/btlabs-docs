---
title: Network modes
description: Standard, Tor only and Offline, and what each one lets the wallet reach.
---

# Network modes

How the wallet reaches the network is one choice on the **Advanced** page in Settings, under
Network.

| Mode | What it does |
| --- | --- |
| **Standard** | Connects directly. [Tor](tor.md) is its own switch. The default. |
| **Tor only** | Tor is always on and its switch is locked. Nothing goes over the open internet. |
| **Offline** | No Epicbox, no Link beyond local addresses, no Tor, no status checks. |

## Tor only

While Tor starts or has failed, the wallet says **Waiting for Tor**, and whatever needs the network
waits, with the reason on the disabled action. On the desktop, Link · HTTP receiving is off, because
a plain address would reveal the computer. Not in the iPhone app or the builds without Tor.

## Offline

The balance and history stay as last seen. **Direct · File Transfer**, and on the phone
**Direct · QR Payment**, still work: they use the node in use to read the chain and to post, a
public one too, and the screen says so.

For the most privacy, use a node on this computer or on the local network: then the balance
refreshes and Recheck balance runs as well. Give that node by its IP address, for example
`192.168.1.20:3413`; names are not looked up. On the desktop, Link · HTTP can then receive over the
local network, with HTTP receiving set to **From the internet**.

The sidebar (desktop) or Home (phone) says when the wallet is offline or waiting for Tor. Setting
the mode back to **Standard** brings everything back.
