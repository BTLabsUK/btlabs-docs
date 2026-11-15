---
title: LEPIC
description: "LEPIC, the Epic Cash client library and command-line wallet in Rust: the lepic CLI, the service API, the crates and the FFI."
---

# LEPIC

LEPIC (light Epic) is an Epic Cash client library and command-line wallet in Rust. It runs as a
library inside the process of the program that uses it: it creates and restores wallets, scans the
chain through an Epic node, and sends and receives transactions with the standard `epic-wallet` and
with other LEPIC wallets. There is no wallet server to start.

| Use | Through |
|---|---|
| A Rust program | The crates, from git (see [LEPIC from Rust](#quick-start-lepic-from-rust)) |
| A script or a service | The [`lepic` command-line wallet](#the-lepic-command-line-wallet), including `lepic serve`, which holds the wallet open for other commands |
| A desktop or mobile app | The FFI library `lepic-ffi`, through [lepic-flutter](lepic-flutter.md); BT Wallet is built this way |

Repository: [github.com/BTLabsUK/lepic](https://github.com/BTLabsUK/lepic).
Licence: Apache-2.0. Rust edition 2024, toolchain pinned in `rust-toolchain.toml`.

:::warning
LEPIC is beta (version 0.5.0). Its APIs may still change before 1.0. Try the `lepic` command-line
wallet on floonet, the test network, before using it with real funds.
:::

## The `lepic` command-line wallet

`lepic` is a light Epic Cash wallet for the terminal. It keeps keys and history on the machine,
asks an Epic node for chain data, and exchanges transactions with other wallets, `epic-wallet`
included, through slate files, an Epicbox relay, or directly over HTTP or Tor. It does not mine or
store the chain.

```bash
cargo xtask install                   # build and install to ~/.local/bin/lepic
lepic --network floonet wallet init   # create a test wallet, write down the phrase
lepic --network floonet wallet info   # balances, from the node at 127.0.0.1:13413
```

| Command group | Examples |
|---|---|
| `wallet` | `init`, `restore` (with `--from-height`), `import-seed`, `import-history`, `info`, `address`, `scan` |
| `tx` | `send`, `receive`, `finalize`, `post`, `list`, `show`, `cancel`, `resend`, `release` |
| `invoice` | `issue`, `pay`, `list`, `decline` |
| `epicbox` | `listen`, `drain`, `status`, `peer` |
| `http`, `tor` | `listen`; `tor address` |
| `node` | `status` |
| `contact` | `invite`, `accept`, `list`, `check`, `move`, `move-home`, `allow-invoices`, `invoice`, `collect` |
| `profile` | `show`, `set`, `domain` |
| `serve` | Holds the wallet open and answers commands sent with `--service` |

Settings come from a flag, an environment variable (`LEPIC_*`), the config file
`~/.lepic/config.toml`, or the default, in that order. Servers come from `~/.lepic/settings.toml`,
written on first use; timeouts and limits are compiled in from `lepic-config.toml`. Passwords are
never taken from command-line arguments: they come from the file `LEPIC_PASSWORD_FILE` names,
`LEPIC_PASSWORD`, a hidden prompt, or one line of standard input. Plain
`http://` and `ws://` are accepted only for a loopback host.

The full guide is
[docs/cli.md](https://github.com/BTLabsUK/lepic/blob/main/docs/cli.md) in
the repository.

## Crates

| Crate | Role | I/O |
|---|---|---|
| `lepic-crypto` | Checked boundary over the vendored secp256k1-zkp library: commitments, Bulletproofs, aggregate signatures, ECDSA, ECDH | none |
| `lepic-primitives` | Serialization, hashing, transaction types, weights and fees, per-network chain parameters | none |
| `lepic-keychain` | Mnemonic to seed, BIP32, key paths, switch commitments, the seed vault, the app data file format | none |
| `lepic-slate` | The slate model and codec registry | none |
| `lepic-legacy-slate` | The V2 and V3 JSON slate codecs `epic-wallet` reads and writes | none |
| `lepic-native-slate` | The binary `lepic.v1` slate between LEPIC wallets | none |
| `lepic-seal` | Sealed envelopes (HPKE) | none |
| `lepic-contact` | Contact pairing formats (RFC 0002): invites, cards, the pairing words check | none |
| `lepic-node` | Client for the node's foreign JSON-RPC API, with strict response checks | network |
| `lepic-store` | SQLite storage behind repository traits, migrations, the database encrypted at rest | disk |
| `lepic-transport` | Transport traits, registry, format policy, the file transport | disk |
| `lepic-epicbox` | Epicbox addresses, message crypto, relay client, `mux/1` push sessions | network |
| `lepic-epic1` | The epic1 address and payment link (RFC 0003) | none |
| `lepic-peer` | The native direct endpoint between LEPIC wallets | network |
| `lepic-legacy-rpc` | The `epic-wallet` foreign API over HTTP: client and listener | network |
| `lepic-tor` | Tor: onion v3 addresses and the wallet's onion key, a tor child process per wallet, SOCKS5 | network, process |
| `lepic-wallet` | The engine: accounts, selection, send, receive, finalize, cancel, scan, refresh, events | through ports |
| `lepic-methods` | The file, http, tor and epicbox transaction methods | through ports |
| `lepic-wallet-contacts` | Contacts on top of the engine: pairing, mailboxes, sealed slates, invoices, epic1 payments | through ports |
| `lepic-telemetry` | `tracing` subscribers for the hosts, redaction helpers | stderr, files |
| `lepic-cli` | The `lepic` binary | all |
| `lepic-ffi` | The FFI API, built with flutter_rust_bridge; the library Flutter apps load as `liblepic_ffi` | all |

`xtask` holds the build, check, vector and packaging commands (`cargo xtask check`,
`cargo xtask mobile` for the FFI libraries, and others).

Three folders sit outside the product workspace. `conformance/` and `fuzz/` each have their own
`Cargo.lock`.

- `conformance/` runs the reference `epic-wallet` and node code to generate golden test vectors
  and to run differential tests. It is the only place those crates appear.
- `fuzz/` holds the fuzz targets for parsers of untrusted input.
- `interop/` runs LEPIC against real `epic-wallet` binaries, a node and an Epicbox relay on a
  private test network.

### Notes

- **Pure crates** (`lepic-crypto`, `lepic-primitives`, `lepic-keychain`, `lepic-slate`,
  `lepic-contact`) may not depend on Tokio or the filesystem, read a clock, or create their own
  randomness. Callers pass an RNG and the time in.
- **Feature code kept out of the money core.** Contact pairing lives in `lepic-wallet-contacts`,
  which drives the engine through its public calls and the hooks of `lepic_wallet::extension`. Nothing in consensus, keys of
  funds or the slates `epic-wallet` reads depends on it, so a review of the money core can leave
  it out.
- **No Epic crates.** LEPIC ports the behaviour it needs from the Epic node and `epic-wallet`
  instead of depending on them. See [Upstream compatibility](upstream.md).

## Allowed dependency edges

The edges below are the only ones allowed between LEPIC crates, for normal and build
dependencies. `cargo xtask deps-check` reads the list from LEPIC's `docs/architecture.md` and
enforces it; any other edge needs a new ADR. An edge is allowed, not required: `lepic-wallet`
uses neither `lepic-legacy-rpc` nor `lepic-tor`.

```text
lepic-crypto      -> (external only)
lepic-primitives  -> lepic-crypto
lepic-keychain    -> lepic-crypto, lepic-primitives
lepic-slate       -> lepic-crypto, lepic-primitives
lepic-native-slate -> lepic-slate, lepic-crypto, lepic-primitives
lepic-seal        -> (external only)
lepic-contact     -> lepic-seal
lepic-node        -> lepic-primitives, lepic-crypto
lepic-store       -> lepic-primitives
lepic-legacy-slate -> lepic-slate, lepic-crypto, lepic-primitives
lepic-transport   -> lepic-legacy-slate, lepic-slate, lepic-primitives, lepic-crypto
lepic-epicbox     -> lepic-transport, lepic-slate, lepic-crypto, lepic-primitives
lepic-epic1       -> lepic-contact, lepic-epicbox, lepic-crypto, lepic-primitives
lepic-peer        -> lepic-primitives
lepic-legacy-rpc  -> lepic-peer, lepic-transport, lepic-slate
lepic-tor         -> lepic-legacy-rpc
lepic-wallet      -> lepic-contact, lepic-store, lepic-node, lepic-transport, lepic-legacy-slate, lepic-slate, lepic-keychain, lepic-crypto, lepic-primitives
lepic-methods     -> lepic-wallet, lepic-transport, lepic-epicbox, lepic-legacy-rpc, lepic-peer, lepic-legacy-slate, lepic-tor, lepic-node, lepic-slate, lepic-keychain, lepic-crypto, lepic-primitives
lepic-wallet-contacts -> all crates above
lepic-telemetry   -> (external only)
lepic-cli         -> lepic-wallet, lepic-wallet-contacts, lepic-methods, lepic-telemetry, lepic-epicbox, lepic-transport, lepic-node, lepic-store, lepic-keychain, lepic-primitives
lepic-ffi         -> lepic-wallet, lepic-wallet-contacts, lepic-methods, lepic-telemetry, lepic-epicbox, lepic-tor, lepic-transport, lepic-node, lepic-store, lepic-keychain, lepic-primitives
```

Any crate may take `lepic-telemetry` as a dev-dependency for log-capture test helpers, and
`lepic-wallet` takes `lepic-wallet-contacts` as one so the contact tests run on the engine's
test harness.

## The `tor` feature

`lepic-ffi` has a default cargo feature `tor`, which pulls in `lepic-tor` and everything that
uses it. Built without it, no tor controller, SOCKS client, onion service or Tor transport is
compiled in:

```bash
cargo xtask mobile --package --no-tor
```

The API stays the same in both builds, so one generated binding serves both. Without Tor:

- `start_tor`, `refresh_tor`, `onion_address`, `previous_onion_address`, `send_tor` and
  `resend_tor` fail with `Unsupported`.
- `tor_status` is `Off`; `epicbox_over_tor` and `node_over_tor` read `false` and their setters
  change nothing, so the relay and the node are always reached directly.
- `validate_onion_address` is `false` for every address.

`cargo xtask mobile --package` writes a `FEATURES` file next to each library so the binding's
build hook can tell the two builds apart. `lepic-cli` always keeps Tor. The app's switch for this
build is described on the [lepic-flutter](lepic-flutter.md#without-tor) page.

## Quick start: LEPIC from Rust

LEPIC needs Rust and a C compiler. It is not on crates.io yet, so take it from git:

```toml
[dependencies]
lepic-wallet = { git = "https://github.com/BTLabsUK/lepic" }
lepic-primitives = { git = "https://github.com/BTLabsUK/lepic" }
```

Read a slate from `epic-wallet` without opening a wallet:

```rust
use lepic_primitives::params::Network;
use lepic_wallet::slate::{CodecRegistry, MediaType, V2JsonCodec, V3JsonCodec, WireSlate};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = std::env::args().nth(1).ok_or("usage: inspect <slate.json>")?;
    let json = std::fs::read_to_string(path)?;

    // The legacy JSON formats epic-wallet reads and writes, with mainnet's minimum fee.
    let base_fee = Network::Mainnet.params().default_base_fee();
    let mut codecs = CodecRegistry::new();
    codecs.register(Box::new(V3JsonCodec::new(base_fee)))?;
    codecs.register(Box::new(V2JsonCodec::new(base_fee)))?;

    // A malformed slate is a typed error, never a panic.
    let slate = codecs.decode(&WireSlate::text(MediaType::JSON, json))?;
    println!(
        "{} {:?}: amount {}, fee {} (base units)",
        slate.id(),
        slate.stage(),
        slate.amount().value(),
        slate.fee().value(),
    );
    Ok(())
}
```

The full wallet (create or restore, scan, send and receive) is the `lepic-wallet` engine with its
ports. A Flutter app uses it through [lepic-flutter](lepic-flutter.md).

## Related pages

- [Architecture](architecture.md): the layers, ports and main flows.
- [Dependencies](dependencies.md): the dependency policy and the main crates.
- [Architecture decisions](decisions.md): the ADRs.
- [Contributing](contributing.md): how changes are made and checked.
