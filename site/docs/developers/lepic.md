---
title: LEPIC
description: The crates of LEPIC, the Rust wallet core, how they depend on each other, and the lepic command-line wallet.
---

# LEPIC

LEPIC (light Epic) is the Epic Cash wallet core in Rust. It runs as a library inside the app's
process: it creates and restores wallets, scans the chain through an Epic node, and sends and
receives transactions with the standard `epic-wallet`. Epic Cash Desktop and Epic Cash Mobile use
it through [lepic-flutter](lepic-flutter.md).

Repository: [github.com/BTLabs-EPIC/lepic](https://github.com/BTLabs-EPIC/lepic) *(available soon)*.
Licence: Apache-2.0. Rust edition 2024, toolchain pinned in `rust-toolchain.toml`.

:::warning
LEPIC is pre-alpha (version 0.1.0). APIs still change. Use floonet, the test network, and do not
put real funds in it yet.
:::

## Crates

| Crate | Role | I/O |
|---|---|---|
| `lepic-crypto` | Safe boundary over the pinned secp256k1-zkp library: commitments, Bulletproofs, aggregate signatures, ECDSA, ECDH | none |
| `lepic-primitives` | Serialization, hashing, transaction types, weights and fees, per-network chain parameters | none |
| `lepic-keychain` | Mnemonic to seed, BIP32, key paths, switch commitments, proof builders, seed vault formats | none |
| `lepic-slate` | Slate domain model, legacy V2 and V3 JSON codecs, codec registry, `ur:epic-slate` QR form | none |
| `lepic-contact` | Contact pairing formats (RFC 0002): sealed envelope, cards, invites, the pairing words check | none |
| `lepic-node` | Client for the node's foreign JSON-RPC API, with strict response checks | network |
| `lepic-store` | SQLite storage behind repository traits, migrations, encrypted private context | disk |
| `lepic-transport` | Transport traits, registry, format policy, the file transport | disk |
| `lepic-epicbox` | Epicbox addresses, message crypto, relay client and transport | network |
| `lepic-foreign` | The wallet foreign API over HTTP: client, listener, `http` transport | network |
| `lepic-tor` | Tor: onion v3 addresses, a tor child process per wallet, SOCKS5, the `tor` transport | network, process |
| `lepic-wallet` | The engine: accounts, selection, send, receive, finalize, cancel, scan, refresh, events | through ports |
| `lepic-wallet-contacts` | Contacts on top of the engine: pairing, mailboxes, sealed slates, contact invoices | through ports |
| `lepic-telemetry` | `tracing` subscribers for the CLI and mobile, redaction helpers | stderr, files |
| `lepic-cli` | The `lepic` binary | all |
| `lepic-ffi` | The FFI API, built with flutter_rust_bridge; the library apps load as `liblepic_ffi` | all |

`xtask` holds the build, check, vector and packaging commands (`cargo xtask check`,
`cargo xtask mobile`, and others).

Three folders sit outside the product workspace, each with its own `Cargo.lock`:

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
  which drives the engine through its public calls and two hooks. Nothing in consensus, keys of
  funds or the slates `epic-wallet` reads depends on it, so a review of the money core can leave
  it out.
- **No Epic crates.** LEPIC ports the behaviour it needs from the Epic node and `epic-wallet`
  instead of depending on them. See [Upstream compatibility](upstream.md).

## Allowed dependency edges

The edges below are the only ones allowed between LEPIC crates, for normal and build
dependencies. `cargo xtask deps-check` enforces them; any other edge needs a new ADR.

```text
lepic-crypto      -> (external only)
lepic-primitives  -> crypto
lepic-keychain    -> crypto, primitives
lepic-slate       -> crypto, primitives
lepic-contact     -> (external only)
lepic-node        -> primitives, crypto
lepic-store       -> primitives
lepic-transport   -> slate
lepic-epicbox     -> transport, slate,
                     crypto, primitives
lepic-foreign     -> transport, slate
lepic-tor         -> foreign, transport,
                     slate
lepic-wallet      -> all crates above
lepic-wallet-contacts
                  -> all crates above
lepic-telemetry   -> (external only)
lepic-cli         -> wallet, wallet-contacts,
                     telemetry, epicbox,
                     foreign, tor, transport,
                     node, store, keychain,
                     primitives
lepic-ffi         -> the same as lepic-cli
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

- `start_tor`, `refresh_tor`, `onion_address`, `send_tor` and `resend_tor` fail with
  `Unsupported`.
- `tor_status` is `Off`; `epicbox_over_tor` and `node_over_tor` read `false` and their setters
  change nothing, so the relay and the node are always reached directly.
- `validate_onion_address` is `false` for every address.

`cargo xtask mobile --package` writes a `FEATURES` file next to each library so the binding's
build hook can tell the two builds apart. `lepic-cli` always keeps Tor. The app's switch for this
build is described on the [lepic-flutter](lepic-flutter.md#without-tor) page.

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
| `wallet` | `init`, `restore`, `import-seed`, `import-history`, `info`, `address`, `scan` |
| `tx` | `send`, `receive`, `finalize`, `post`, `list`, `show`, `cancel`, `resend`, `release` |
| `invoice` | `issue`, `pay`, `list`, `decline` |
| `epicbox` | `listen`, `drain` |
| `http`, `tor` | `listen`; `tor address` |
| `node` | `status` |

Settings come from a flag, an environment variable (`LEPIC_*`), the config file
`~/.lepic/config.toml`, or the default, in that order. Passwords are never taken from command-line
arguments: they come from `LEPIC_PASSWORD`, a hidden prompt, or one line of standard input. Plain
`http://` and `ws://` are accepted only for a loopback host.

The full guide is
[docs/cli.md](https://github.com/BTLabs-EPIC/lepic/blob/main/docs/cli.md) *(available soon)* in
the repository.

## Quick start: LEPIC from Rust

LEPIC needs Rust and a C compiler. It is not on crates.io yet, so take it from git:

```toml
[dependencies]
lepic-wallet = { git = "https://github.com/BTLabs-EPIC/lepic" }
lepic-primitives = { git = "https://github.com/BTLabs-EPIC/lepic" }
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

Apps use the full wallet (create or restore, scan, send and receive) through
[lepic-flutter](lepic-flutter.md).

## Related pages

- [Architecture](architecture.md): the layers, ports and main flows.
- [Dependencies](dependencies.md): the dependency policy and the main crates.
- [Architecture decisions](decisions.md): the ADRs.
- [Contributing](contributing.md): how changes are made and checked.
