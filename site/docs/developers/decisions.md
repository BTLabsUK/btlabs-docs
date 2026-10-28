---
title: Architecture decisions
description: A summary of LEPIC's architecture decision records (ADRs 0001 to 0029), grouped by theme.
---

# Architecture decisions

LEPIC records each design decision as an architecture decision record (ADR): one decision, why it
was made, and what it costs. The full records are in
[docs/adr](https://gitlab.com/epic-cash-bt/lepic/-/blob/main/docs/adr/README.md) *(available soon)*.

## How ADRs work

- Status is **accepted**, **proposed** (still needs a decision or a prototype), or
  **superseded by NNNN**.
- An accepted record is never rewritten. A decision changes by a new record that supersedes the
  old one, in whole or in part; the old record stays, marked with what replaced it.
- A new dependency edge between crates needs an ADR.
- For facts about formats and behaviour, golden vectors and running code win over ADRs.

## Foundations

**0001 Port the node and wallet logic; no Epic crates in the product graph.** *Accepted.* LEPIC
ports the behaviour it needs from the Epic node and `epic-wallet` into its own crates, because
depending on them would compile mining and chain-storage code into a phone app. The only Epic
code it links is the secp256k1-zkp library, pinned to a commit.

**0009 Separate conformance workspace on public pins, golden vectors.** *Accepted; version table
superseded by 0020.* A separate workspace runs the reference code to write golden vectors and run
differential tests; the product crates test against the committed vectors without the reference
code.

**0020 Reference wallet and node move to epic-wallet v4.1.0.** *Accepted.* The reference code,
golden vectors and interop images are pinned to `epic-wallet` and the Epic node `v4.1.0`.

**0010 Latest stable crates and toolchain, banned list, update bots.** *Accepted.* Latest stable
Rust and crates, set once in the workspace; `cargo deny` checks advisories, licences, sources and
a banned list in CI. See [Dependencies](dependencies.md).

**0011 No process-global state; network and settings are parameters.** *Accepted; `ChainParams`
contents superseded by 0013.* The network, runtime, clock, RNG and paths are passed in, so two
wallets on different networks can run in one process.

**0013 Network parameters live with the format that uses them.** *Accepted.* `ChainParams` holds
only consensus values a wallet needs; each format crate maps the network to its own version
bytes.

**0008 tracing everywhere, host-installed subscribers, typed errors.** *Accepted.* Libraries emit
`tracing` events and never install a subscriber; errors are typed per crate, and the binding
exposes one error enum with stable numeric codes.

## Slates and formats

**0002 One version-free slate model, one codec per wire format.** *Accepted.* One typed slate
model with an explicit stage and roles; legacy V2 and V3 JSON codecs reproduce `epic-wallet`
exactly. Encoding keeps everything or fails with a typed error.

**0003 Transports declare the slate formats they speak.** *Accepted; file row superseded by
0015.* Each transport has a format policy: what it accepts, what it sends, how it replies. The
engine never names a codec.

**0015 The file method writes V3; Epicbox stays V2.** *Accepted.* Slate files are written in V3,
so payment proofs and TTL can travel in files. Epicbox sends payments in the V2 shape and invoice
stages in V3.

**0012 A compact native slate format for LEPIC-to-LEPIC methods.** *Proposed.* A compact binary
slate with an armored text form, offered only to peers that advertise support. Legacy peers never
receive it.

**0025 Slates as animated QR codes in `ur:epic-slate`.** *Accepted.* Two phones exchange a slate
as a looping sequence of QR codes (BC-UR, deflated slate text). The codes are not encrypted, and
the method is offered on mobile only.

## Epicbox and direct transactions

**0004 Async Epicbox client with listen and drain modes, acknowledge after store.** *Accepted.*
`listen` holds a connection; `drain` connects, processes what waits and disconnects, for a
suspended phone. A message is acknowledged only after its effect is stored.

**0016 LEPIC notices over Epicbox, sent only to proven peers.** *Accepted.* Short notices
(`declined`, `withdrawn`, `posted`) tell each side of an invoice what the other did. They go only
to peers that proved they run LEPIC.

**0017 The wallet foreign API over HTTP in its own crate.** *Accepted.* `lepic-foreign` sends and
listens over the HTTP foreign API, compatible with `epic-wallet`. The listener serves only
`check_version` and `receive_tx` and binds to loopback unless the user chooses otherwise.

## Tor

**0018 Tor on desktop through a bundled tor child process.** *Accepted.* The app bundles a `tor`
binary and LEPIC runs one per open wallet, driven over its control port. The onion address is the
one `epic-wallet` derives, published ephemerally; its key is never written to disk.

**0021 Epicbox over Tor.** *Accepted.* With Tor on, the relay connection goes through tor, to the
relay's onion when known, else through an exit. TLS still checks the relay's domain.

**0022 Node over Tor.** *Accepted.* The node is reached through the same tor, with its own
setting. Nothing goes through a Tor exit unencrypted.

**0026 Tor is a build feature of the binding.** *Accepted.* `lepic-ffi`'s default `tor` feature
can be turned off for a library with no Tor code; the API stays the same.

## Storage, keys and secrets

**0005 SQLite storage, platform keystore for secrets, legacy seed import.** *Accepted;
database-import bullet superseded by 0019.* SQLite with a real schema, private transaction context
encrypted at rest, seeds in the platform keystore or an Argon2id vault, and read-only import of an
`epic-wallet` `wallet.seed`.

**0006 rustls with ring, hyper for HTTP, tokio-tungstenite for websockets.** *Accepted.* TLS is
rustls with the ring provider, chosen for small mobile builds that need only a C compiler.

**0014 Which secrets may cross the Flutter boundary.** *Accepted.* Only secrets the user types or
configures go into Rust; only the recovery phrase comes out, after a credential check; the PIN key
goes only to the app's secret store. See [Security model](security-model.md).

**0019 Import the transaction history of an epic-wallet wallet.** *Accepted.* The old wallet's
database is copied and read, never opened in place or written. History is imported and checked
against the seed and the chain scan, which stays the only source of spendable funds.

**0027 Minimum confirmations is a per-wallet setting, default 6.** *Accepted.* Received outputs
and change become spendable after 6 confirmations by default, adjustable per wallet from 1 to 30.

**0028 Per-transaction state lives in tables that cascade with the transaction.** *Accepted.*
Per-transaction records move from key-value settings into typed tables that are deleted with
their transaction.

## Binding

**0007 flutter_rust_bridge bindings for the existing Flutter frontend.** *Accepted; secrets line
superseded by 0014, delivery bullet superseded by 0023.* `lepic-ffi` uses flutter_rust_bridge:
opaque handles, async calls and streams, one error enum, panics turned into errors at the
boundary.

**0023 The Flutter binding lives in its own repository.** *Accepted.* The Dart package is
[lepic-flutter](lepic-flutter.md), pinned to a LEPIC commit. Hash checks on both sides keep the
generated Rust and Dart halves together.

## Contacts

**0024 Contact pairing, sealed slates, and invoice trust on paired contacts.** *Proposed.* Wallets
pair once and then exchange slates in an HPKE envelope signed with Ed25519, through per-contact
mailboxes. Allowing invoices is a per-contact switch for verified contacts. The format is
specified in RFC 0002.

**0029 Contacts are a crate on top of the engine.** *Accepted.* Contact code moves into
`lepic-wallet-contacts`, which drives the engine from outside, so the money core can be reviewed
without it.
