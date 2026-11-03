---
title: Nodes and your own node
description: What a node does for the wallet, public nodes, the built-in node, and your own node.
---

# Nodes and your own node

The wallet needs a node to read the blockchain (the balance and confirmations) and to post
transactions to the network. It never stores the blockchain itself.

## Public nodes

A public node is one that others run. It works right away. Whoever runs it can see the wallet's IP
address and which outputs it asks about; [Tor](tor.md) or a VPN hides the address. The default is
`node.btlabs.uk`; others in the list include `node.epiccash.com` and `node.epicnet.us`.

## Change the node

- **Desktop:** **Settings › Node**.
- **Phone:** tap the node icon on the Wallet tab, or **Settings › Privacy & network › Node**.

The nodes are listed with their state. Pick one to switch to it at once, with no restart, or type an
address to filter the list or add a node. Star a node to keep it in your list. With **Server
details** on in [Advanced](advanced.md), the list also shows hosts, latency, version and block
height.

Sending needs a synced node. **Behind** or **Not responding** means pick another; the wallet offers
one.

**Node failover** is on by default. When your node has not answered for a while, the wallet moves to
the next working node in your list, for this session only: your own choice stays saved, and the
wallet goes back to it at the next start, or as soon as you pick a node yourself. It never moves in
Offline mode or away from a node on this computer, and with Tor only it moves only to a node
reachable over Tor.

## The built-in node (desktop)

The desktop app can run its own Epic Cash node on this computer. Turn on **Built-in node** in
[Advanced](advanced.md), then choose **Local node** under **Settings › Node**.

The local node first downloads the whole blockchain, which needs disk space, and then it is yours.
While it syncs, the wallet uses a public node. The blockchain is kept in the app data folder. On
macOS the built-in node runs on Apple silicon only.

## Your own node elsewhere

Run an Epic Cash node on another machine and add its address under Node, for example
`http://192.168.1.20:3413`. In [Offline mode](network-modes.md), give the node by its IP address:
names are not looked up.

How to run a node is on the
[Epic Cash Developer Hub](https://devdocs.btlabs.uk).

### Owner access (desktop)

For a node on this computer, your home network or a VPN, or one you mark as yours, the desktop app
asks the node directly and offers **Owner access** under **Settings › Node**: the node's sync stage
and peers, and banning a peer. Owner access uses the node's API secret, so the node must have one
set:

- In the node's `epic-server.toml`, the line `api_secret_path` names the secret file, by default
  `.api_secret` in the node's data folder (`~/.epic/main` on mainnet). It is set in the file the node
  writes itself; some downloaded or bootstrap configurations have it commented out with `#`.
- Commented out, the node asks for no secret on its owner API at all: anyone who can reach the API
  port can use it. Remove the `#`, make sure the file exists, and restart the node.
- Paste the first line of that file under **Owner access**. The secret is kept in the computer's
  keyring, never in the settings or the wallet data file.

:::note
`api_http_addr` decides who can reach the node's API. The default `127.0.0.1:3413` is this computer
only; another machine on your network needs the node's network address there.
:::
