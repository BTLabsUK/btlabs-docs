---
title: Advanced settings
description: The switches that add the parts most people never need.
---

# Advanced settings

**Advanced** is a page in Settings for the parts most people never need. Everything on it is off to
begin with. A switch adds its part where it belongs, and **Hide everything again** switches them all
off.

| Switch | What it adds |
| --- | --- |
| **Outputs** | The Outputs page: the coins the balance is made of and what you can do with them |
| **Technical details** | Slate ID, kernel, commitments and block height on a payment. Without it the **More** link shows them once |
| **Send options** | Phone: Strategy and Split change under **Settings › Transactions**. Desktop: a fold on Send, where one send chooses Smallest or All and whether to split the change |
| **Server details** | Hosts, latency, version and block height in the lists and the status card |
| **Recheck from a height** | Phone: Recheck balance from a block height or a date. Desktop: Recheck balance can also drop unconfirmed transactions; Restore offers a start block to everyone |
| **Local node** (desktop) | This computer's own node: the **This computer** option under **Settings › Node**, its sync panel, and **Start node** on Overview |
| **Logs** (desktop) | The Logs group under **Settings › Files & logs**. **Report a problem** can attach the log either way |
| **Direct · File Transfer** (phone) | File Transfer under **Settings › Transactions**: pay or get paid with a file you pass on yourself |

Pairing, invoices and Linked devices have no switch here: they are there for everyone. Linked devices
is marked **Experimental** in the app.

## In other places

- **Connection mode**: [Normal, Tor only, Node only or Kill switch](network-modes.md), under
  **Settings › Network & privacy**.
- **Node failover**, on by default: under **Settings › Network & privacy** on the phone, as
  **Switch node automatically** under **Settings › Node** on the desktop. See
  [Nodes](nodes.md#change-the-node).
- **Confirmations**: how many blocks a received payment waits before its outputs can be spent. 6 by
  default, any count from 1 to 30. It is under **Settings › Payments** on the desktop and on the
  Advanced page on the phone. Fewer confirmations give less protection against chain reorganisations.
- **View** on the desktop: Shallow, Deeper or Deep end, how much of the wallet shows. Only the display
  changes: every view sends and receives the same way, with the same keys and coins.
