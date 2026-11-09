---
title: LEPIC
description: LEPIC is the Rust wallet core of BT Wallet; this page maps its crates, ports, slate formats and hosts.
---

# LEPIC

LEPIC is an Epic Cash wallet written as a Rust library. It runs inside the process of the program
that uses it: the `lepic` command-line wallet, or BT Wallet through the Flutter binding
[lepic-flutter](lepic-flutter.md). It creates and restores wallets, refreshes and scans against an
Epic node, and sends, receives, finalizes and posts transactions. It speaks the wire formats of
`epic-wallet` and the Epic node, and adds formats of its own for exchanges between two LEPIC
wallets.

Source: [github.com/BTLabsUK/lepic](https://github.com/BTLabsUK/lepic). The repository's own pages
go deeper than this one: [architecture](https://github.com/BTLabsUK/lepic/blob/main/docs/architecture.md),
[CLI](https://github.com/BTLabsUK/lepic/blob/main/docs/cli.md),
[FFI](https://github.com/BTLabsUK/lepic/blob/main/docs/ffi.md),
[configuration](https://github.com/BTLabsUK/lepic/blob/main/docs/configuration.md) and
[protocols](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/README.md).

## Workspace

LEPIC is a Cargo workspace. The crates sit in layers, and a crate may use only the crates the
architecture page lists for it. `cargo xtask deps-check` fails when the real dependencies differ
from that list.

| Layer | Crates | Does |
|---|---|---|
| Pure | `lepic-crypto`, `lepic-primitives`, `lepic-keychain`, `lepic-slate`, `lepic-legacy-slate`, `lepic-native-slate`, `lepic-seal`, `lepic-contact` | Compute only: no I/O, no clock, no randomness of their own |
| I/O | `lepic-node`, `lepic-store`, `lepic-transport`, `lepic-epicbox`, `lepic-epic1`, `lepic-peer`, `lepic-legacy-rpc`, `lepic-tor`, `lepic-telemetry` | Each talks to one outside thing: the node, the database, a relay, a socket, Tor |
| Engine | `lepic-wallet` | The wallet's rules, with the outside reached through ports |
| Methods | `lepic-methods` | The file, http, tor and epicbox ways a slate travels, each behind a feature |
| Contacts | `lepic-wallet-contacts` | Pairing, contact mailboxes, sealed slates and contact invoices, on top of the engine |
| Hosts | `lepic-cli`, `lepic-ffi` | Build the ports, the Tokio runtime and logging, and present the result |

`xtask` holds the repository's tooling. `conformance/`, `fuzz/`, `interop/`, `console/` and
`third_party/` sit outside the workspace. Every crate has a README under `crates/<crate>/`.

The workspace pins its toolchain in `rust-toolchain.toml`, with the Android and iOS targets, and
sets the minimum Rust version in `Cargo.toml`. No crate is published.

## Optional parts

| Feature | Crate | Effect |
|---|---|---|
| `tor` (default) | `lepic-ffi` | Compiles `lepic-tor` and the Tor paths; without it every Tor call fails with `Unsupported` (ADR 0026) |
| `legacy` (default) | `lepic-transport`, `lepic-methods` | The V2 and V3 codecs and the methods that need them; `cargo xtask no-legacy` builds without it (ADR 0052) |
| `sqlite` (default) | `lepic-store`, `lepic-wallet`, `lepic-wallet-contacts` | The SQLite store |
| `file`, `epicbox`, `http`, `tor` | `lepic-methods` | One method each; `file` and `legacy` are on by default |
| `mock` | `lepic-ffi`, `lepic-node` | A scripted node and relay for tests; an app build never uses it |

`lepic-wallet` depends on `lepic-legacy-slate` without a feature: the engine stores slates as V3
JSON.

## Ports

The engine asks for what it needs as traits and generic parameters. The host supplies them in a
`Ports` value (`crates/lepic-wallet/src/ports.rs`), and builds a wallet with
`Wallet::new(config, ports)`.

| Port | Gives the engine |
|---|---|
| `NodeApi` | Chain tip, outputs, kernels, and the push of a transaction |
| `StoreOpener` | The wallet database, opened or created |
| `SecretVault` | The sealed seed, created or unlocked with a password |
| `Clock`, `SharedRng`, `Handle` | The time, randomness and a Tokio runtime handle |
| `MethodLookup` | The transaction methods, found by name |

The engine keeps no global state, so several wallets on different networks can run in one process
(ADR 0011). `lepic_wallet::extension` has four hooks (`ReplyKeys`, `NativeSlates`,
`ContactNotices`, `PairRequests`) that `lepic-wallet-contacts` installs once per wallet. The
engine holds no host name, URL, port or timeout; the host passes them (ADR 0030, ADR 0036).

## Slates and methods

A slate is the document two wallets pass back and forth to build one transaction.
`lepic_slate::Slate` is the one version-free model. A codec converts it to and from one wire
format, and a method pairs a transport with the formats it reads and writes.

| Format | Codec id | Crate |
|---|---|---|
| V2 JSON, plain or with the LEPIC marker | `legacy-v2` | `lepic-legacy-slate` |
| V3 JSON, plain or with the LEPIC marker | `legacy-v3` | `lepic-legacy-slate` |
| Binary `lepic.v1` | `lepic.v1` | `lepic-native-slate` |

Each method sets its own format policy:

| Method | Reads | Writes a new slate |
|---|---|---|
| file | V2 or V3 | V3; a reply goes to `<path>.response` |
| http | V3 or V2 | V2; a reply keeps the shape that came in |
| epicbox | V3 or V2, by shape | S1 as marked V2, I1 as marked V3; a reply keeps the shape, I2 is always marked V3 |

Native slates are off by default (`WalletConfig::native_direct`). They travel sealed in an
envelope between paired contacts, or over Epicbox to a peer whose marker claimed them. See
[Architecture](architecture.md#slates-codecs-and-methods) and the
[protocol pages](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/README.md).

## What the engine does

The main calls on `Wallet` are `send`, `receive`, `finalize`, `post`, `issue_invoice`,
`pay_invoice`, `finalize_invoice`, `refresh`, `resend` and `cancel`. The Epicbox client in
`lepic-epicbox` has `listen`, which holds a relay connection open, and `drain`, which collects
what waited at the relay and returns. The state machine for transactions is in
`crates/lepic-wallet/src/state.rs`. The engine fails with `WalletError`; `lepic-ffi` maps it to
`WalletErrorKind`, whose numeric codes are stable (ADR 0007).

## Data at rest

| Data | Protection |
|---|---|
| Seed | A vault: XChaCha20-Poly1305 under an Argon2id key from the password |
| Database | SQLite3 Multiple Ciphers, ChaCha20-Poly1305 page encryption, keyed from the seed (ADR 0032) |
| Private transaction context | Sealed under a key from the root key and bound to its row |

`EncryptingSqliteStores` opens the encrypted database, and `DataDirLock` keeps two processes from
opening one data directory. The [security model](security-model.md) lists what each key protects.

## Hosts

- **`lepic-cli`** builds the `lepic` binary. It reads the password from a file, the environment, a
  prompt or standard input, keeps a wallet per data directory, and can run as a service with a
  local wallet API (`lepic serve`). Its settings come from flags, `LEPIC_*` variables,
  `config.toml` and `settings.toml`.
- **`lepic-ffi`** is the API a Flutter app calls. `LepicRuntime` owns the Tokio runtime, logs reach
  the app through `LogSink` or `LogRing`, and `crates/lepic-ffi/bridge.sha256` fingerprints the API
  files so the generated bridge halves cannot drift. [lepic-flutter](lepic-flutter.md) holds the
  Dart half.

## Decisions and compatibility

The design decisions are listed in [Decisions](decisions.md). How LEPIC matches `epic-wallet` and
the Epic node is in [Upstream compatibility](upstream.md), and the crates LEPIC builds on are in
[Dependencies](dependencies.md). To build and test it, see [Dev environment](dev-environment.md)
and [Testing](testing.md).
