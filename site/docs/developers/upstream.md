---
title: Upstream compatibility
description: How LEPIC matches epic-wallet and the Epic node, where it is the same byte for byte, where it is stricter, and what it adds.
---

# Upstream compatibility

LEPIC is a new implementation of the Epic Cash wallet, not a fork of `epic-wallet`. It must
still produce and accept exactly what `epic-wallet` and the Epic node produce and accept on every
method it supports. This page explains how that is kept true, and where LEPIC deliberately
differs.

A detailed comparison for reviewers will be linked here when it is published.

## How compatibility is kept

- **One target release.** LEPIC targets [`epic-wallet`](https://github.com/EpicCash/epic-wallet)
  and the [Epic node](https://github.com/EpicCash/epic) `v4.1.0`, pinned to exact commits
  (ADR 0020). Moving to a new release means new pins, new test data and a review of every
  upstream change, module by module.
- **Port, not depend.** LEPIC ports the behaviour it needs into its own crates instead of linking
  the Epic crates, which would bring mining and chain-storage code into a phone build (ADR 0001).
  The one Epic library it links is
  [rust-secp256k1-zkp](https://github.com/EpicCash/rust-secp256k1-zkp), pinned to a commit.
- **Golden vectors.** A separate conformance workspace runs the pinned reference code and writes
  test vectors: keys, proofs, signatures, slates at every stage, Epicbox messages. LEPIC's tests
  must reproduce them byte for byte, without access to the reference code (ADR 0009). Where a
  vector and a document disagree, the vector wins.
- **Differential tests** run the reference code and LEPIC side by side on the same inputs.
- **Interop suite.** `interop/` builds the public Epicbox relay, the node `v4.1.0` and
  `epic-wallet` `v4.1.0` from source and runs LEPIC against them on a private Docker network with
  no route out.
- **Upstream drift job.** `upstream.toml` records, for each ported module, the upstream files and
  commit it came from. `cargo xtask upstream-drift` lists upstream commits that touched those
  files since; a weekly CI job runs it and reports changes not yet reviewed.

```bash
cargo xtask vectors verify    # replay every golden vector
cargo xtask upstream-drift    # upstream commits since the recorded pins
```

The formats LEPIC matches are written up in its
[compatibility notes](https://gitlab.com/btlabs/lepic/-/tree/main/docs/compat) *(available soon)*:
legacy slates, Epicbox, keys and proofs, the node API, the foreign API, transaction states and the
`epic-wallet` database. Protocol-level documentation is on the
[Epic Cash developer docs](https://devdocs.btlabs.uk).

## The same, byte for byte

These are pinned by golden vectors from the reference code:

| Area | What matches |
|---|---|
| Seed and keys | BIP39 English, the entropy as the BIP32 input, the same master key, child derivation and identifier format |
| Commitments and proofs | Switch commitments, both range-proof builders, tried in the same order on restore |
| Kernels and fees | Kernel signature message and hash, fee and weight formula, body serialization and read-check order, kernel sums |
| Signatures | Aggregate signature calls and argument order |
| Addresses | Epicbox address, payment-proof key, and the onion address, so all three survive a restore |
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
- **Storage.** SQLite with a real schema instead of a key-value layout, private transaction
  context encrypted at rest, seeds in the platform keystore or an Argon2id vault.
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
- **LEPIC notices** over Epicbox about invoices, sent only to peers proven to run LEPIC.
- **Transaction history import** from an `epic-wallet` database, checked against the seed and the
  chain scan.

## Differences stated openly

- **Minimum confirmations.** Outputs become spendable after 6 confirmations by default, a
  per-wallet setting from 1 to 30. `epic-wallet`'s command line defaults to 10 (ADR 0027).
- **Slate files are V3.** LEPIC writes every slate file in the V3 shape, which `epic-wallet` reads;
  `epic-wallet` writes V2 unless the slate needs V3. Compatibility of files is shown by the
  differential and interop suites, not by byte equality (ADR 0015).
- **Foreign API.** The HTTP listener serves only `check_version` and `receive_tx`; every other
  method, including coinbase building for mining, is answered "method not found". Invoices travel
  over Epicbox.
- **Node status.** LEPIC uses only the node's foreign API and judges sync from the tip and the
  version, because public nodes do not expose the owner API.
- **Epicbox message encryption** is kept exactly as `epic-wallet` defines it, so the two can talk.
  LEPIC's own sealed envelope is a separate layer for paired contacts.
- **One key, two uses.** The onion address and the Epicbox address derive from the same 32-byte
  secret, as in `epic-wallet`. LEPIC keeps this so the onion address matches what `epic-wallet`
  prints.

## Related pages

- [Architecture decisions](decisions.md): ADR 0001, 0009 and 0020 in particular.
- [LEPIC](lepic.md)
- [Testing](testing.md)
