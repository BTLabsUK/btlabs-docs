---
title: Advanced settings
description: The switches that add the parts most people never need, and the experimental features.
---

# Advanced settings

**Advanced** is a page in Settings for the parts most people never need. Everything on it is off to
begin with, so the wallet stays simple. A switch adds its part where it belongs, and
**Hide everything again** switches them all off.

| Switch | What it adds |
| --- | --- |
| **Outputs** | The Outputs page: the coins the balance is made of, Split and Consolidate |
| **Technical details** | Slate ID, kernel, commitments and block height on a payment |
| **Send options** | Which outputs a send spends (Smallest or All) and Split change |
| **Server details** | Hosts, latency, version and block height in the node and Epicbox lists |
| **Recheck from a height** | Recheck balance from a block height or a date |
| **Built-in node** (desktop) | A node on this computer: Local node under **Settings › Node** |
| **Logs** (desktop) | The Logs group in Help, to open the log folder or clear the logs |

## Also on the page

- **Network**: the [network mode](network-modes.md), Standard, Tor only or Offline.
- **Node failover**, on by default: see [Nodes](nodes.md#change-the-node).
- **Confirmations**: how many blocks a received payment waits before its outputs can be spent. 6 by
  default, any count from 1 to 30. Fewer confirmations are faster but give less protection against
  chain reorganisations.

## Experimental

Off to begin with; they can still change.

- **Pairing**: pair with contacts, so transaction files between you are sealed. See
  [Contacts, pairing and invoices](pairing.md).
- **Invoices**: requests and invoices between paired contacts. Needs Pairing.
- **Linked devices**: one wallet on several of your devices. See [Linked devices](linked-devices.md).

Off, they are hidden and nothing is checked for them; what was set up stays saved and comes back
when the switch is on again.
