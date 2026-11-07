---
title: Upstream compatibility
description: How LEPIC matches epic-wallet and the Epic node, where it is the same byte for byte, where it is stricter, and what it adds.
---

# Upstream compatibility

LEPIC is a new implementation of the Epic Cash wallet, not a fork of `epic-wallet`. It must
still produce and accept exactly what `epic-wallet` and the Epic node produce and accept on every
method it supports. This page explains how that is kept true, and where LEPIC deliberately
differs.

Review notes for each upstream release are in LEPIC's
[compatibility notes](https://github.com/BTLabsUK/lepic/tree/main/docs/compat).

## How compatibility is kept

- **One target release.** LEPIC targets the latest release of
  [`epic-wallet`](https://github.com/EpicCash/epic-wallet/releases) and of the
  [Epic node](https://github.com/EpicCash/epic/releases), pinned to exact commits: [ADR 0020](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0020-reference-epic-wallet-4-1.md) and [ADR 0038](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0038-reference-node-4-1-2.md) name
  them, and [`interop/pins.env`](https://github.com/BTLabsUK/lepic/blob/main/interop/pins.env) holds the tags the interop suite builds. Moving to a new release means new pins, new test data and a review of every
  upstream change, module by module.
- **The built-in node.** The desktop app bundles the latest
  [Epic node release](https://github.com/EpicCash/epic/releases) as its built-in node.
- **Port, not depend.** LEPIC ports the behaviour it needs into its own crates instead of linking
  the Epic crates, which would bring mining and chain-storage code into a phone build (ADR 0001).
  The one Epic library it links is
  [rust-secp256k1-zkp](https://github.com/EpicCash/rust-secp256k1-zkp), vendored from a pinned
  commit with the changes listed in
  [`PATCHES.md`](https://github.com/BTLabsUK/lepic/blob/main/third_party/grin_secp256k1zkp/PATCHES.md).
- **Golden vectors.** A separate conformance workspace runs the pinned reference code and writes
  test vectors: keys, proofs, signatures, slates at every stage, Epicbox messages. LEPIC's tests
  must reproduce them byte for byte, without access to the reference code (ADR 0009). Where a
  vector and a document disagree, the vector wins.
- **Differential tests** run the reference code and LEPIC side by side on the same inputs.
- **Interop suite.** `interop/` builds the public Epicbox relay, the node and
  `epic-wallet` from source at the pinned tags and runs LEPIC against them on a private Docker network with
  no route out.
- **Upstream drift check.** `upstream.toml` records, for each ported module, the upstream files and
  commit it came from. `cargo xtask upstream-drift` lists upstream commits that touched those
  files since. It runs every week and reports changes not yet reviewed.

```bash
cargo xtask vectors verify    # replay every golden vector
cargo xtask upstream-drift    # upstream commits since the recorded pins
```

The formats LEPIC matches are written up in its
[compatibility notes](https://github.com/BTLabsUK/lepic/tree/main/docs/compat):
legacy slates, Epicbox, keys and proofs, the node API, the foreign API, transaction states, the
`epic-wallet` database, the `ur:epic-slate` format, the `.wfeh` backup format and the secp256k1-zkp
fork. Protocol-level documentation is on the
[Epic Cash developer docs](https://devdocs.btlabs.uk).

## The same, byte for byte

These are pinned by golden vectors from the reference code:

| Area | What matches |
|---|---|
| Seed and keys | BIP39 English, the entropy as the BIP32 input, the same master key, child derivation and identifier format |
| Commitments and proofs | Switch commitments, both range-proof builders, tried in the same order on restore |
| Kernels and fees | Kernel signature message and hash, fee and weight formula, body serialization and read-check order, kernel sums |
| Signatures | Aggregate signature calls and argument order |
| Addresses | Epicbox address and payment-proof key, so both survive a restore |
| Epicbox | Message encryption, frames and signed texts, the same JSON |
| Slates | Legacy V2 and V3 JSON, quirks included: integers as strings, nulls, version header, key order |
| Wallet logic | Output selection, change splitting, the fee check on receive, confirmation counting |
| Node API | The same foreign JSON-RPC calls and parameters |
| Import | The `wallet.seed` file format, read-only |

## Where LEPIC is stricter, and why

None of these affect a slate, message or response that `epic-wallet` or the node produces.

- **Input.** LEPIC refuses data upstream would read but never writes: key paths deeper than the
  format allows, malformed integer strings, a plain kernel with a lock height, kernel features
  that disagree with the slate, commitments and public keys that are not curve points, range
  proofs outside the size bounds, received participant messages over 256 bytes. Rejecting at
  decode keeps bad data out of storage.
- **Finalize.** Every field the sender set is compared with the stored S1, exactly one added
  output is accepted, and the whole transaction is validated before it is stored. Payment proofs
  are verified with strict ed25519 checks.
- **Receive.** The TTL is checked against the node's tip, zero amounts and fees below the minimum
  are refused, and a repeated S1 is answered with the stored S2 instead of an error. The receiver
  keeps no private context.
- **Cancel.** A posted transaction cannot be cancelled. When the other side could complete the
  transaction alone, the node's pool and chain are asked for the kernel first, and a cancelled
  send stays watched so its outputs come back if it is mined after all.
- **Scan and refresh.** The same walk over the chain, but each page is checkpointed so a scan can
  resume, an output is marked spent only after two missing answers, and heights above the tip are
  refused. Node responses are size-capped and validated field by field.
- **Epicbox.** Frames are size-limited before parsing, the signature is verified before the
  content is parsed, and a message is acknowledged only after its effect is stored, so a crash
  between receive and store does not lose a slate.
- **Tor.** The onion service is published ephemerally over tor's control port, so its key is never
  on disk; names resolve inside tor; TLS still checks the relay's or node's domain.
- **Storage.** SQLite with a real schema instead of a key-value layout, the database encrypted at
  rest (ADR 0032), private transaction context sealed on its own, seeds in the platform keystore
  or an Argon2id vault.
- **Transaction states.** Explicit states (sent, received, finalized, posted, confirmed,
  cancelled, expired) with a checked transition table, mapped one to one onto upstream's types, so
  an imported `epic-wallet` history reads back correctly.

## New, with no upstream equivalent

All of these are additive: a stock `epic-wallet` never receives anything it cannot parse.

- **Contact pairing and sealed slates** (RFC 0002): an HPKE envelope with Ed25519 signatures
  between paired wallets, carried inside ordinary Epicbox messages or files. See
  [Security model](security-model.md#contacts-invoices-and-linked-devices).
- **Animated QR slates** in `ur:epic-slate`, which wrap the legacy slate text unchanged.
- **A `lepic` marker** on legacy slates, which stock wallets ignore. It is a capability hint only;
  no signature covers it.
- **LEPIC notices** over Epicbox about invoices and cancelled payments, sent only to peers proven
  to run LEPIC.
- **Contact features:** the owner's profile (ADR 0041), domain proof (ADR 0043), the contact check
  and relay moves (ADR 0039, 0040), all inside the pairing's own envelopes.
- **Transaction history import** from an `epic-wallet` database, checked against the seed and the
  chain scan.

## Differences stated openly

- **Minimum confirmations.** Outputs become spendable after 6 confirmations by default, a
  per-wallet setting of at least 1 (BT Wallet allows 1 to 30). `epic-wallet`'s command line defaults to 10 (ADR 0027).
- **Slate files are V3.** LEPIC writes every slate file in the V3 shape, which `epic-wallet` reads;
  `epic-wallet` writes V2 unless the slate needs V3. Compatibility of files is shown by the
  differential and interop suites, not by byte equality (ADR 0015).
- **Foreign API.** The HTTP listener serves `check_version` and `receive_tx`. `build_coinbase` is
  off unless the host turns it on, and then answers this computer only unless the host opens it
  further; Tor's listeners never serve it (ADR 0046, 0048). Every other method is answered "method
  not found". Invoices travel over Epicbox.
- **Node status.** LEPIC uses only the node's foreign API and judges sync from the tip and the
  version, because public nodes do not expose the owner API.
- **Epicbox message encryption** is kept exactly as `epic-wallet` defines it, so the two can talk.
  LEPIC's own sealed envelope is a separate layer for paired contacts.
- **The onion has its own key.** In `epic-wallet` the onion address and the Epicbox address derive
  from one key. LEPIC derives the onion key from the seed under a label of its own (ADR 0044), so
  its onion address differs from what `epic-wallet` prints for the same phrase. The earlier address
  stays available as `previous_onion_address`; BT Wallet does not publish it.

## Related pages

- [Architecture decisions](decisions.md): ADR 0001, 0009 and 0020 in particular.
- [LEPIC](lepic.md)
- [Testing](testing.md)
