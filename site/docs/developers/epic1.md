---
title: epic1 for developers
description: How the epic1 address is built, which cryptography protects a payment, and how a payment travels between two LEPIC wallets.
---

# epic1 for developers

An epic1 address is how one LEPIC wallet pays another with native, sealed slates. A classic
address is read by many wallets, so a LEPIC wallet sends it only the stock slates those wallets
read ([Legacy transactions](legacy-transactions.md)), and native payments get an address of
their own. The epic1 address holds everything a payer needs: it names no relay, so the payee can
change relays without a new address, and delivery is a separate layer that the payee's settings
choose. [ADR 0062](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0062-the-address-decides-the-protocol.md)
and [ADR 0063](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0063-the-epic1-address-carries-its-own-mailbox.md)
give the reasons; the [epic1](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epic1.md)
and [Delivery](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/delivery.md) guides
have the detail. For using epic1 in the app, see [epic1 addresses and links](../users/epic1.md).

## The address

```text
data  = version (01) || seal key (32) || delivery key (33)     66 bytes
text  = bech32m("epic", data)    mainnet, 117 characters
        bech32m("tepic", data)   floonet, 118 characters
```

Payments are sealed to the **seal key**. The **delivery key**, read as an Epicbox key, is the
address's mailbox, the same on every relay. Both derive from the seed, the account, the network
and the address's index, so a restore gives the same addresses. The address names no relay,
transport or index, and carries no proof key: an epic1 payment has no payment proof. A link,
`epic:<address>?…`, adds an amount, a message and up to three `http` or `tor` entries
([The link](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epic1.md#the-link)).

## The cryptography

| Part | What it is | Crate |
|---|---|---|
| Address text | bech32m of the 66 bytes, lower case ([RFC 0003 §5.13](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#513-epic1-address)) | `lepic-epic1` |
| Seal and delivery keys | Keyed BLAKE2b-256 of the seed over a label and the account, network and index; X25519 and secp256k1 ([RFC 0003 §5.2](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#52-keys-and-derivation)) | `lepic-wallet` |
| Envelope | HPKE base mode: DHKEM(X25519, HKDF-SHA256), HKDF-SHA256, ChaCha20-Poly1305; anonymous, hint zero ([RFC 0003 §5.4](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#54-hpke)) | `lepic-seal` |
| Padding | Padmé of the content length, at least 768 bytes ([RFC 0003 §5.7](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#57-padding)) | `lepic-seal` |
| Reply key and reply mailbox | One X25519 key and one mailbox per slate, derived from the seed and the slate id ([RFC 0002 §2.3](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0002-contact-pairing.md#23-one-time-reply-keys)) | `lepic-wallet-contacts`, `lepic-wallet` |
| Mailbox post | Epicbox message encryption and signature to the mailbox key ([Epicbox](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epicbox.md#messages)) | `lepic-epicbox` |

A relay learns which mailbox gets mail, when, the size, and the poster's IP address and post
key; it can drop, delay or replay a message, but it cannot read or change a sealed envelope
([RFC 0003 §7.1](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#71-per-party)).
Payments to one address share its mailbox, while each answer goes to a reply mailbox of its
own, so a relay cannot join two payments by their reply mailbox. The
[security model](security-model.md#contacts-invoices-and-linked-devices) covers the rest.

## A payment

1. **Read.** `lepic epic1 read` (`epic1_read`) reads the address or link and stores nothing.
2. **Seal.** `lepic epic1 pay` (`epic1_pay`) builds the S1 with a TTL of 1440 blocks unless the
   send sets one, and seals it with `TxKey::Epic1` to the address's seal key. The envelope
   carries the payer's reply key and the key of a one-time reply mailbox, and names no relay.
3. **Post.** The outbox posts the payment to the address's delivery mailbox on every usable
   relay of the payer's relay list at once; it is posted when any relay takes it. A link with
   `http` or `tor` entries is posted to those entries instead, one at a time, and answered in
   the same request.
4. **Collect.** The payee's collect reads its delivery mailboxes by relay push, opens the
   envelope with the seal key of one of its open addresses, checks it and signs the S2.
5. **Answer.** The payee seals the S2 to the reply key and posts it to the reply mailbox on the
   relay it read the payment from.
6. **Finalize.** The payer's collect reads the answer, checks it is the S2 of its S1, finalizes
   it and posts the transaction. For a payment that went to the mailbox, it then sends the
   payee a `posted` notice and asks the other relays to drop their copies of the payment.
7. **Refusal.** A payee that refuses sends a `declined` notice to the reply mailbox, with reason
   `amount` for an amount other than the link asks, or `declined` for a payment it does not
   take. The payer cancels the payment and frees its inputs.
8. **Deadline.** Once the chain reaches the payment's cutoff, its TTL height or the wallet's
   own limit for the transaction if that comes first, the outbox stops posting it, and the
   next refresh expires it if it was not finalized.

## What the host does

The core runs no timer: the host calls collect, which reads by push and posts what the outbox
owes, as [Delivery](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/delivery.md#what-the-host-does)
describes. An app calls `contacts_collect` and `contacts_push_start`
([FFI](https://github.com/BTLabsUK/lepic/blob/main/docs/ffi.md#epicbox-push-sessions)); the CLI
has `lepic contact collect`, and `lepic serve` collects on its own
([CLI](https://github.com/BTLabsUK/lepic/blob/main/docs/cli.md#lepic-serve-and-the-wallet-api)).

## Limits

- An account holds at most 256 open addresses past index 0, links and plain addresses together.
- A payment read on a second relay is not taken again; its stored answer is posted again.
- A retired address takes no payment; index 0 is never retired.
- Invoices go only between paired contacts that the payer verified and allowed to send
  invoices; no invoice or pair request travels over an epic1 link.

## Related pages

- [Upstream compatibility](upstream.md)
- [Security model](security-model.md)
- [Legacy transactions](legacy-transactions.md)
- [epic1 addresses and links](../users/epic1.md)
