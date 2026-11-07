---
title: Architecture decisions
description: A summary of LEPIC's architecture decision records (ADRs 0001 to 0049), grouped by theme.
---

# Architecture decisions

LEPIC records each design decision as an architecture decision record (ADR): one decision, why it
was made, and what it costs. The full records are in
[docs/adr](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/README.md).

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
code it links is the secp256k1-zkp library, vendored from a pinned commit.

**0009 Separate conformance workspace on public pins, golden vectors.** *Accepted; version table
superseded by 0020.* A separate workspace runs the reference code to write golden vectors and run
differential tests; the product crates test against the committed vectors without the reference
code.

**0020 Reference wallet and node move to the latest epic-wallet release.** *Accepted; node row
for interop and `upstream.toml` superseded by 0038.* The
reference code, golden vectors and interop images are pinned to the latest release of `epic-wallet`
and the Epic node; [ADR 0020](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0020-reference-epic-wallet-4-1.md) names the tags and commits.

**0038 The reference node moves for interop and `upstream.toml`.** *Accepted.* The interop images
and `upstream.toml` follow a later Epic node release. The conformance workspace and golden vectors
stay on the node that `epic-wallet` links.

**0010 Latest stable crates and toolchain, banned list, update bots.** *Accepted.* Latest stable
Rust and crates, set once in the workspace; `cargo deny` checks advisories, licences, sources and
a banned list. See [Dependencies](dependencies.md).

**0011 No process-global state; network and settings are parameters.** *Accepted; `ChainParams`
contents superseded by 0013.* The network, runtime, clock, RNG and paths are passed in, so two
wallets on different networks can run in one process.

**0013 Network parameters live with the format that uses them.** *Accepted.* `ChainParams` holds
only consensus values a wallet needs; each format crate maps the network to its own version
bytes.

**0008 tracing everywhere, host-installed subscribers, typed errors.** *Accepted.* Libraries emit
`tracing` events and never install a subscriber; errors are typed per crate, and the binding
exposes one error enum with stable numeric codes.

**0030 All configuration in settings.toml.** *Accepted.* Configuration comes from settings files,
not from code. See [Architecture](architecture.md#configuration).

**0036 Policy values are host parameters.** *Accepted.* A value that is policy becomes a parameter
the host may pass, with LEPIC's earlier value as its default. The password length and the cap on
minimum confirmations move to the hosts.

**0033 One registry of seed-derived keys and signature domains.** *Proposed.* Every new key that
is not a funds key is a keyed BLAKE2b-256 hash of the seed under a label of its own, with one
function and one label constant in the crate that owns it.

**0034 Trust, versioning and probing between Epic wallets.** *Proposed.* What the software behind
a key has shown and what the user has with a contact are kept as two separate axes.

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
(`declined`, `withdrawn`, `posted`, `cancelled`) tell each side of a payment what the other did. They go only
to peers that proved they run LEPIC.

**0017 The wallet foreign API over HTTP in its own crate.** *Accepted.* `lepic-foreign` sends and
listens over the HTTP foreign API, compatible with `epic-wallet`. The listener serves
`check_version` and `receive_tx`, and binds to loopback unless the user chooses otherwise.

**0046 A wallet for a mining node.** *Accepted.* The wallet can build a coinbase on a node's
request. A restore from the phrase finds the output.

**0048 Block rewards are for this computer unless the host opens them.** *Accepted.* `build_coinbase`
is off by default. Turned on, it answers loopback callers unless the host opens it to others. Tor's
listeners never serve it.

## Tor

**0018 Tor on desktop through a bundled tor child process.** *Accepted; the onion key superseded
by 0044.* The app bundles a `tor` binary and LEPIC runs one per open wallet, driven over its
control port. The onion is published ephemerally; its key is never written to disk.

**0044 The onion has its own key.** *Accepted.* The onion key is derived from the seed under a
label of its own, so the onion address and the Epicbox address no longer share a key. The earlier
address stays available as `previous_onion_address`, and publishing it is the host's choice.
BT Wallet does not publish it.

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

**0032 Wallet database encrypted at rest with SQLite3 Multiple Ciphers.** *Accepted.* Amends 0005
and 0010. The database file is encrypted page by page under a key derived from the seed.

**0006 rustls with ring, hyper for HTTP, tokio-tungstenite for websockets.** *Accepted.* TLS is
rustls with the ring provider, chosen for small mobile builds that need only a C compiler.

**0014 Which secrets may cross the Flutter boundary.** *Accepted.* Only secrets the user types or
configures go into Rust; only the recovery phrase comes out, after a credential check; the PIN key
goes only to the app's secret store. See [Security model](security-model.md).

**0019 Import the transaction history of an epic-wallet wallet.** *Accepted.* The old wallet's
database is copied and read, never opened in place or written. History is imported and checked
against the seed and the chain scan, which stays the only source of spendable funds.

**0027 Minimum confirmations is a per-wallet setting, default 6.** *Accepted; the cap of 30
superseded by 0036.* Received outputs and change become spendable after 6 confirmations by
default, adjustable per wallet. LEPIC requires at least 1; BT Wallet allows 1 to 30.

**0035 Restore from a start height.** *Accepted.* A restore may start its scan at a height the
caller picks. LEPIC holds no default height.

**0037 One send-to-self primitive.** *Accepted.* `send_to_self` replaces the separate calls that
moved a wallet's own coins. A send makes 1 to 10 outputs.

**0031 An offline session for cold wallets.** *Accepted.* A session opened offline refuses every
network call before any name lookup. Payment stages use the highest tip a refresh confirmed, and
the finished transaction is saved or shown as a code for another device to post.

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

**0039 The host applies a contact's relay move.** *Accepted.* LEPIC reports a contact's move and
the app decides whether to apply it.

**0040 The contact check and moving one's own home relay.** *Accepted.* A signed, empty message
asks a paired contact for its current card; answers are paced by host parameters.

**0041 The owner's profile in the feature word.** *Accepted.* Bits 16 to 31 of the feature word
are the owner's profile. It goes to paired contacts only and grants nothing.

**0042 Draining the old home after moving one's own.** *Accepted.* After a move, the old mailboxes
can be read for a set number of days, at most a year.

**0043 Domain proof for paired contacts.** *Accepted.* A contact can prove a domain with a file
that domain serves. See [Security model](security-model.md#contacts-invoices-and-linked-devices).

**0045 Refusing slates nobody asked for.** *Proposed.* Two policy switches, off by default, refuse
unsolicited payments and invoices.

**0047 The mailbox is the default between paired contacts.** *Accepted.* The host picks the route
of a send. BT Wallet sends through the pairing when it can carry payments, and keeps the payments
address as the fallback.

**0049 Keeping messages that cannot be taken yet.** *Accepted.* A notice that arrives before its
slate waits for it. A message from a contact that would otherwise be dropped can be kept in a
local quarantine, off unless the host sets a size.
