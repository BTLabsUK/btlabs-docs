---
title: Addresses
description: What an Epicbox, epic1, HTTP or Tor address looks like, and how to check one.
---

# Addresses

| Kind | Looks like | Goes by |
| --- | --- | --- |
| Epicbox | about 52 characters starting with `es`, `@`, the server: `es…@epicbox.epiccash.com` | Epicbox |
| epic1 | 117 characters starting with `epic1`, or a link `epic:epic1…` | epic1 |
| HTTP | a web address of the other wallet, such as `http://host:3415` | Link · HTTP |
| Tor | 56 characters ending in `.onion` | Link · Tor |

Send picks the method from the address pasted into the To field.

- An **Epicbox address** is the wallet's public key, then `@` and the name of its Epicbox server.
  The recipient can be offline.
- An **epic1 address** names no server. The payment waits in the address's own mailbox on the
  Epicbox servers both wallets use, so the recipient can be offline. An **epic1 link** is the
  address with an amount or a message. See [epic1 addresses and links](epic1.md).
- An **HTTP** or **Tor** address is the recipient's own wallet, which must be open when you send.
- Some wallets show a Tor address without `.onion`; both are the same address.
- A **Paired address** is made when you [pair](pairing.md#after-pairing) with a contact. It is not
  shown, and nothing is pasted for it.

## Checking an address

When someone reads an address out, compare the **first six and the last six characters**. The
app highlights them on Receive.

## Addresses and privacy

Epic Cash has no addresses on the blockchain. The Epicbox address only tells Epicbox where to
deliver messages, and is never written on the blockchain. It is safe to share.

Choosing another Epicbox server changes the part after `@`, so give the new address to the people
who pay you. See [Epicbox](epicbox.md).

## In the builds without Tor

A `.onion` address shows **"This version cannot send to Tor addresses."** under To, and no method
is offered for it. A contact's Tor address stays saved but cannot be paid.
