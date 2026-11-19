---
title: epic1 for developers
description: How the epic1 address is built, which cryptography protects a payment, and how a payment travels between two LEPIC wallets.
---

# epic1 for developers

An epic1 address is how one LEPIC wallet pays another with native, sealed slates. A classic
address is read by many wallets, so a LEPIC wallet sends it only the stock slates those wallets
read ([Legacy transactions](legacy-transactions.md)), and native payments get an address of
their own. The epic1 address holds everything a payer needs: it names no mailbox server, so the
payee can change mailboxes without a new address, and delivery is a separate layer.
[ADR 0062](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0062-the-address-decides-the-protocol.md),
[ADR 0063](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0063-the-epic1-address-carries-its-own-mailbox.md),
[ADR 0065](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0065-mail-goes-where-the-receiver-reads.md)
and [ADR 0066](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0066-one-address-per-account.md)
give the reasons; the [epic1](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epic1.md)
and [Delivery](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/delivery.md) guides
have the detail. For using epic1 in the app, see [epic1 addresses and links](../users/epic1.md).

Words: Epicmail is the mail protocol, a mailbox is a server that runs it, and a slot is the box
of one key on a mailbox. LEPIC's code and older records say relay for a mailbox and mailbox for a
slot.

## The address

```text
data  = version (01) || seal key (32) || delivery key (33)     66 bytes
text  = bech32m("epic", data)    mainnet, 117 characters
        bech32m("tepic", data)   floonet, 118 characters
```

Payments are sealed to the **seal key**. The **delivery key**, read as an Epicbox key, is the
address's slot, the same on every mailbox. Both derive from the seed, the account, the network
and index 0, so each account has one address and a restore gives the same one. The address names
no mailbox, transport or index, and carries no proof key: an epic1 payment has no payment proof.

The payment link is the address, `epic:<address>`. A request link adds an amount, a message or
both, and up to three `http` or `tor` entries; it only fills in the payer's Send screen. The
payee stores nothing for a link, and nothing matches a payment to it
([The links](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epic1.md#the-links)).

## The cryptography

| Part | What it is | Crate |
|---|---|---|
| Address text | bech32m of the 66 bytes, lower case ([RFC 0003 §5.13](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#513-epic1-address)) | `lepic-epic1` |
| Seal and delivery keys | Keyed BLAKE2b-256 of the seed over a label and the account, network and index; X25519 and secp256k1 ([RFC 0003 §5.2](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#52-keys-and-derivation)) | `lepic-wallet` |
| Envelope | HPKE base mode: DHKEM(X25519, HKDF-SHA256), HKDF-SHA256, ChaCha20-Poly1305; anonymous, hint zero ([RFC 0003 §5.4](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#54-hpke)) | `lepic-seal` |
| Padding | Padmé of the content length, at least 768 bytes ([RFC 0003 §5.7](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#57-padding)) | `lepic-seal` |
| Reply key and reply slot | One X25519 key and one slot per slate, derived from the seed and the slate id ([RFC 0002 §2.3](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0002-contact-pairing.md#23-one-time-reply-keys)) | `lepic-wallet-contacts`, `lepic-wallet` |
| Post to a slot | Epicbox message encryption and signature to the slot's key ([Epicbox](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epicbox.md#messages)) | `lepic-epicbox` |

A mailbox server learns which slot gets mail, when, the size, and the poster's IP address and post
key; it can drop, delay or replay a message, but it cannot read or change a sealed envelope
([RFC 0003 §7.1](https://github.com/BTLabsUK/lepic/blob/main/docs/rfcs/0003-epictx-native-slates.md#71-per-party)).
Payments to one address share its slot, while each answer goes to a reply slot of its own, so a
mailbox cannot join two payments by their reply slot. The
[security model](security-model.md#contacts-invoices-and-linked-devices) covers the rest.

## A payment

1. **Read.** `lepic epic1 read` (`epic1_read`) reads the address or link and stores nothing.
2. **Seal.** `lepic epic1 pay`, or `lepic tx send --to` with the address or link, builds the S1
   (`epic1_pay`) with a TTL of 1440 blocks unless the send sets one, and seals it with
   `TxKey::Epic1` to the address's seal key. The envelope carries the payer's reply key and the
   key of a one-time reply slot, and names no mailbox.
3. **Post.** The outbox posts the payment to the address's delivery slot on every mailbox of the
   payer's list, one copy per mailbox; it is posted when any mailbox takes it. A mailbox's
   health is shown and never drops it from the list. When the payer and payee share no mailbox,
   the payment fails at once with `NoSharedMailbox`, which lists the shipped mailboxes. A link
   with `http` or `tor` entries is posted to those entries instead, one at a time, and answered
   in the same request.
4. **Collect.** The payee's collect reads its delivery slot by push, opens the envelope with the
   account's seal key, checks it and signs the S2. Any amount is taken.
5. **Answer.** The payee seals the S2 to the reply key and posts it to the reply slot on every
   mailbox of its list and on every mailbox it read a copy of the payment on
   ([ADR 0065](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0065-mail-goes-where-the-receiver-reads.md)).
6. **Finalize.** The payer's collect reads the answer, checks it is the S2 of its S1, finalizes
   it and posts the transaction. For a payment that went to the mailbox, it then sends the
   payee a `posted` notice and asks the other mailboxes to drop their copies of the payment.
7. **Refusal.** A payee with `refuse_unsolicited_payments` on sends a `declined` notice to the
   reply slot for every payment to the address. The payer cancels the payment and frees its
   inputs.
8. **Deadline.** Once the chain reaches the payment's cutoff, its TTL height or the wallet's
   own limit for the transaction if that comes first, the outbox stops posting it, and the
   next refresh expires it if it was not finalized.

## The mailbox list

A wallet has one list for all native mail: the mailboxes shipped with the release, plus the ones
the user added, minus the shipped ones the user removed; 1 to 16 entries. The host stores only
the added and the removed entries (`added` and `removed` in `settings.toml`), so a release that
changes the shipped list reaches every install. [Delivery](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/delivery.md#the-mailbox-list)
has the rules.

- A message goes to every mailbox of the list. Mail to a contact also goes to the mailbox on the
  contact's card. An answer also goes to every mailbox a copy was read on.
- A link names no mailbox: a `mailbox=` entry is reported as ignored, and no reply mailbox
  travels inside a payment.
- The core never adds, removes or drops a mailbox on its own. The user does, with
  `lepic mailbox list|add|remove|probe`. `add` probes the host first and refuses one that fails
  unless `--anyway` is given; local and private hosts are always refused.
- A payer who shares no mailbox with the payee gets `NoSharedMailbox`. A host may pass mailboxes
  for one payment, and `lepic epic1 pay` takes a repeatable `--mailbox`.
- Restore reads every mailbox that answers and reports the rest.

The app holds the list itself. After a wallet opens it calls
`mailbox_set(shipped, added, removed)`, then `mailbox_list` (origin and health), `mailbox_probe`,
`mailbox_add(host, anyway)` and `mailbox_remove(host)`, and stores the `added` and `removed` each
change hands back. `epic1_pay` takes an optional `mailboxes` list, `epic1_restore` returns the
mailboxes it could not read in `not_read`, and a read link counts its ignored entries in
`ignored_mailboxes`. The error kinds are `NoSharedMailbox` (119), `MailboxInvalid` (120),
`MailboxNotPublic` (121), `MailboxListFull` (122) and `LastMailbox` (123). See the
[FFI guide](https://github.com/BTLabsUK/lepic/blob/main/docs/ffi.md).

## What the host does

The core runs collect in a loop, which reads by push and posts what the outbox owes. An app
starts the loop with `set_delivery` after it opens the wallet and asks for one more collect with
`delivery_wake` ([FFI](https://github.com/BTLabsUK/lepic/blob/main/docs/ffi.md#delivery-loop));
the CLI has `lepic contact collect`, and `lepic serve` runs the loop on its own
([CLI](https://github.com/BTLabsUK/lepic/blob/main/docs/cli.md#lepic-serve-and-the-wallet-api)).

Two installs on one phrase share the address, and a slot has one reader at a time on each
mailbox. The newest attach takes it. The replaced install attaches again after a 10-minute
hold-off, at session start or when the host resumes. Linked devices tell each other; unlinked
installs reconcile through the chain.

## Limits

- An account has one epic1 address, at index 0. Numbered addresses and links made before this
  model are not read: a payment to one is not taken, and its payer's wallet cancels it at its
  deadline.
- A payment read on a second mailbox is not taken again; its stored answer is posted again.
- Invoices go only between paired contacts that the payer verified and allowed to send
  invoices; no invoice or pair request travels over an epic1 link.

## Related pages

- [Upstream compatibility](upstream.md)
- [Security model](security-model.md)
- [Legacy transactions](legacy-transactions.md)
- [epic1 addresses and links](../users/epic1.md)
