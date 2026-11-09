---
title: Upstream compatibility
description: How LEPIC stays compatible with epic-wallet and the Epic node, where it adds checks, and which formats it adds.
---

# Upstream compatibility

LEPIC is an implementation of the Epic Cash wallet written from scratch; it does not link `epic-wallet`
or the Epic node. It reads and writes the formats of `epic-wallet` and the node, so a LEPIC wallet
and a stock wallet can exchange slates, Epicbox messages and foreign API calls. This page explains
how that is kept true, where LEPIC adds checks of its own, and which formats exist only between
LEPIC wallets.

LEPIC's [compatibility notes](https://github.com/BTLabsUK/lepic/tree/main/docs/compat) write up
each format and the review of each upstream release.

## How compatibility is kept

- **One reference release.** The reference is the latest release of
  [`epic-wallet`](https://github.com/EpicCash/epic-wallet/releases) and of the
  [Epic node](https://github.com/EpicCash/epic/releases), pinned to exact commits. The tags and
  commits are in [`interop/pins.env`](https://github.com/BTLabsUK/lepic/blob/main/interop/pins.env)
  and in ADRs
  [0020](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0020-reference-epic-wallet-4-1.md)
  and [0038](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0038-reference-node-4-1-2.md).
- **Port, do not depend.** LEPIC ports the behaviour it needs into its own crates (ADR 0001).
  `Cargo.lock` holds no `epic_*` package. The one library of Epic origin it links is
  `grin_secp256k1zkp`, vendored in `third_party/` with its changes listed in
  [`PATCHES.md`](https://github.com/BTLabsUK/lepic/blob/main/third_party/grin_secp256k1zkp/PATCHES.md).
- **Golden vectors.** The `conformance/` workspace runs the pinned reference code and writes JSON
  vectors under `testdata/vectors/<area>/`. The areas are `aggsig`, `app_data`, `engine`,
  `epicbox`, `keys`, `pairing`, `primitives`, `slates`, `slates_native`, `smoke`, `store` and
  `store_key`. LEPIC's tests reproduce them without the reference code (ADR 0009). Where sources disagree, golden vectors and
  running code rank above ADRs, and ADRs above the compatibility notes.
- **Differential tests.** The conformance workspace's `differential` member runs the reference
  code and LEPIC on the same inputs.
- **Interop stack.** `interop/` builds the reference node, `epic-wallet` and an Epicbox relay at
  the pinned commits and runs LEPIC against them on a Docker private network with no route out.
- **Drift check.** `upstream.toml` has one `[[module]]` entry per ported module with its `path`,
  its upstream repository and files, and the upstream commit it follows.
  `cargo xtask upstream-drift` lists the upstream commits that touched those files after that
  commit and exits with code 2 when there are any. A scheduled CI job runs it.

```bash
cargo xtask vectors verify    # replay every golden vector
cargo xtask upstream-drift    # upstream commits after the recorded ones
```

## Formats LEPIC matches

| Area | What LEPIC matches |
|---|---|
| Seed and keys | BIP-39 English phrases, BIP32 derivation, commitments, range proofs and the key identifier format |
| Kernels and fees | Kernel message and signature, fee and weight rules, aggregate signatures |
| Slates | V2 and V3 JSON, including the version header and the encoding of numbers |
| Foreign API | JSON-RPC 2.0 at `/v2/foreign` with `check_version`, `receive_tx` and `build_coinbase` |
| Epicbox | Relay frames, `key@domain` addresses and the message cipher |
| Import | The `wallet.seed` file and the `epic.db` history, read-only |

The foreign listener answers `check_version` and `receive_tx`. `build_coinbase` is served only when
the host turns it on, to this computer unless the host opens it further (ADR 0046, ADR 0048). Any
other method answers JSON-RPC error `-32601`.

## Checks LEPIC adds

These checks apply to input and to storage. They do not change what a conforming wallet or node
produces.

- **Decoding.** Slates are decoded strictly and limited to `MAX_WIRE_SLATE_LEN` (8 MiB). Slate
  messages are limited to `MAX_MESSAGE_LEN` (256 bytes) and an Epicbox message to 4 MiB.
  Commitments and public keys must be curve points. Decoding rejects what it cannot encode back
  (ADR 0002).
- **Finalize and receive.** Finalize compares the sender's fields with the stored first message
  and validates the whole transaction before storing it. Receive checks the time to live against
  the node's tip.
- **Cancel and release.** A posted transaction is not cancelled. A cancelled, released or expired
  transaction stays watched, first by its kernel and then by its outputs, so its outputs return if
  the peer completes it (`lepic-wallet/src/release.rs`).
- **Refresh.** An unspent or locked output the node does not hold is marked spent once a second
  request misses it too.
- **Epicbox.** A message is acknowledged only after the store holds its effect, so a crash between
  receipt and storage does not lose a slate (ADR 0004).
- **Storage.** SQLite with one table per record kind (ADR 0028), the database encrypted at rest
  (ADR 0032), and the private transaction context sealed on its own.
- **Transaction states.** A transaction is Sent, Received, Finalized, Posted, Confirmed, Cancelled
  or Expired, and `lepic-wallet/src/state.rs` allows only the listed transitions.

## Formats only between LEPIC wallets

A stock wallet never receives one of these in a form it must parse.

- **The LEPIC marker.** V2 and V3 slates may carry `"lepic":{"version":1}`, which stock wallets
  ignore and drop. Over Epicbox it also holds the feature bits the wallet claims, inside the
  encrypted message; a file or pasted slate may hold a reply key for a sealed answer.
- **EPICTX native slates.** `lepic.v1` is a binary slate format with a 51-byte header
  ([ADR 0012](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0012-native-slate-format.md),
  [ADR 0052](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0052-legacy-at-the-edge-native-between-lepic-wallets.md)).
  It is off unless the host turns it on (`WalletConfig::native_direct`).
- **Contact pairing and sealed slates.** A sealed envelope (HPKE, Ed25519 signatures) between
  paired wallets, carried inside Epicbox messages or files. The owner's profile (ADR 0041), the
  domain proof (ADR 0043), the contact check (ADR 0040) and relay moves (ADR 0039) use the same
  envelopes.
- **Notices.** JSON messages over Epicbox about declined, withdrawn, posted and cancelled
  transactions (ADR 0016).
- **Animated QR slates.** BC-UR `epic-slate` parts (ADR 0025).
- **History import.** The `epic.db` history of an `epic-wallet` wallet, checked against the seed and
  the chain scan (ADR 0019).

## Where LEPIC chooses differently

- **Slate files are V3.** The file method writes V3 and reads V2 or V3; a reply goes to
  `<path>.response` (ADR 0015).
- **Minimum confirmations.** The default is 6. It is a per-wallet setting of at least 1 (ADR 0027).
- **The onion has its own key.** The onion key is derived from the seed under the label
  `lepic-wallet onion key v1`, apart from the Epicbox key (ADR 0044).
- **Epicbox.** The relay cipher follows `epic-wallet`. The sealed envelope for paired contacts is a
  separate layer on top.

## Related pages

- [Architecture decisions](decisions.md), in particular ADRs 0001, 0009, 0020 and 0038
- [LEPIC](lepic.md)
- [Testing](testing.md)
