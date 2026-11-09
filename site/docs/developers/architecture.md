---
title: Architecture
description: How BT Wallet, the lepic-flutter binding and the LEPIC wallet core fit together.
---

# Architecture

BT Wallet is one Flutter app for desktop and phone. The wallet itself is LEPIC, a Rust
library that runs inside the app's own process. The app reaches it through lepic-flutter, a Dart
package generated with flutter_rust_bridge. There is no separate wallet program and no wallet API
server to start.

## The stack

```text
+------------------------------------+
| Flutter app (one codebase)         |
|  lib/main.dart          -> Mobile  |
|  lib/main_desktop.dart  -> Desktop |
+-----------------+------------------+
                  | Dart calls,
                  | Futures, Streams
+-----------------v------------------+
| lepic-flutter (Dart package lepic) |
|  Dart API: EpicWallet, ...         |
|  generated bridge glue             |
|  build hook: bundles the library   |
+-----------------+------------------+
                  | FFI
+-----------------v------------------+
| liblepic_ffi (crate lepic-ffi)     |
+-----------------+------------------+
                  |
+-----------------v------------------+
| LEPIC engine (lepic-wallet)        |
|  + contacts (lepic-wallet-contacts)|
+--+----------+----------+-------+---+
   |          |          |       |
 node      storage   transports  keys
 client    (SQLite)  file, Epicbox, (keychain,
                     HTTP, Tor     crypto)
```

| Layer | What it holds | Where |
|---|---|---|
| App | Screens, settings, the platform secret store, the bundled tor binary and, on desktop, an optional Epic node binary | wallet-for-epic, `app/` |
| Binding | The Dart API, the generated Dart half of the bridge, the build hook that bundles the native library | [lepic-flutter](lepic-flutter.md) |
| Core | The FFI API, the wallet engine and every crate below it | [LEPIC](lepic.md) |

The app has two entry points on one codebase: `lib/main.dart` starts the phone app
and `lib/main_desktop.dart` the desktop interface. Both run on the same wallet core through the
binding.

## Layers inside LEPIC

LEPIC is a Cargo workspace of small crates in layers:

1. **Pure crates** at the bottom: crypto, transaction primitives, keys, the slate model and its
   codecs, sealed envelopes, contact formats. They do no I/O, read no clock and create no
   randomness of their own, so they are deterministic and can be fuzzed.
2. **I/O crates** next: each talks to one outside thing, such as the node, the SQLite database, an
   Epicbox relay, a socket or Tor. The wallet database is encrypted at rest.
3. **The engine**, `lepic-wallet`, holds the wallet's rules.
4. **Methods**, `lepic-methods`, are the ways a slate travels: file, http, tor and epicbox.
5. **Contacts**, `lepic-wallet-contacts`, add pairing, contact mailboxes and sealed slates on top
   of the engine.
6. **Hosts** on top: the `lepic` command-line wallet and `lepic-ffi`, the FFI API the binding wraps.

The allowed edges between crates are fixed and checked by `cargo xtask deps-check`. The crate
table is on the [LEPIC](lepic.md) page, and the edges are in LEPIC's
[architecture page](https://github.com/BTLabsUK/lepic/blob/main/docs/architecture.md).

## Engine and ports

The engine depends on traits ("ports"), not on implementations. The host passes them in a `Ports`
value and builds a wallet with `Wallet::new(config, ports)`.

| Port | Implemented by |
|---|---|
| `NodeApi` | `NodeClient` in `lepic-node`; `MockNode` with the `mock` feature |
| `StoreOpener` | `EncryptingSqliteStores` over `lepic-store`; wrappers in `lepic-cli` and `lepic-ffi` |
| `SecretVault` | A vault file in the CLI; the platform keystore through the app in `lepic-ffi` |
| `Clock`, `SharedRng`, `Handle` | The host's real ones; fixed ones in tests |
| `MethodLookup` | The method registry of `lepic-methods` |

The engine owns no runtime and no global state. `lepic-cli` and `lepic-ffi` create the Tokio
runtime and pass it in. Because the node, storage, keys, network and clock are all passed in, one
test can run several wallets side by side, and one process can hold wallets on different networks
(ADR 0011).

## Slates, codecs and methods

A slate is the message two wallets exchange to build a transaction. LEPIC keeps one version-free
slate model and several wire formats:

```text
 wire bytes  <-->  codec  <-->  domain Slate  <-->  engine
                    ^
                    | chosen by the method's
                    | format policy
```

- **Domain slate.** `lepic_slate::Slate` has an explicit stage (S1, S2, S3 for a payment; I1, I2,
  I3 for an invoice), explicit roles and typed fields (ADR 0002).
- **Codec.** Maps one wire format to the domain model and back. A codec never converts into
  another codec.

  | Format | Codec id | Crate |
  |---|---|---|
  | V2 JSON | `legacy-v2` | `lepic-legacy-slate` |
  | V3 JSON | `legacy-v3` | `lepic-legacy-slate` |
  | Binary `lepic.v1` | `lepic.v1` | `lepic-native-slate` |

- **Method.** A transport plus its format policy (ADR 0003) and what it knows about peers. The
  policy names the codecs the method reads, the one it writes for a new slate, and the rule for
  replies. The engine never names a codec; it looks a method up by name.

  | Method | Reads | Writes a new slate |
  |---|---|---|
  | file | V2 or V3 | V3; a reply goes to `<path>.response` |
  | http | V3 or V2 | V2; a reply keeps the shape that came in |
  | epicbox | V3 or V2, by shape | S1 as marked V2, I1 as marked V3; a reply keeps the shape, I2 is always marked V3 |

A LEPIC wallet adds `"lepic":{"version":1}` to the V2 and V3 JSON slates it sends over Epicbox;
stock `epic-wallet` ignores it. The binary `lepic.v1` slate is off by default
(`WalletConfig::native_direct`) and travels between LEPIC wallets only. The engine stores slates
as V3 JSON, and `lepic-wallet-contacts` converts at the edge.

Adding a method is one method module and one registration; adding a format is one codec module and
one registration. The wire formats are specified in LEPIC's
[protocol pages](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/README.md), and the
differences from `epic-wallet` are in [Upstream compatibility](upstream.md).

## Main flows

Each flow is a `Wallet` method that takes the method to use. Every step stores its result before it
returns.

**Send (standard flow, S1 to S2 to S3)**

1. `Wallet::send` selects outputs, builds change with its range proofs, locks the inputs and stores
   the transaction, the private context and S1.
2. The method's policy picks a codec, the codec encodes, and the method delivers S1, or the
   engine writes it for the user to carry. A stored send that failed to deliver waits for
   `resend` or `cancel`.
3. `Wallet::finalize` checks the answer (S2) against the stored send, completes the signatures
   and builds the transaction (S3). `Wallet::post` sends it to the node.

**Receive.** `Wallet::receive` decodes S1 with the method's policy, checks it against the chain
tip, adds an output and a partial signature, stores the result and returns S2 in the shape the
policy picks.

**Invoice (I1, I2, I3).** `issue_invoice` creates I1 for the payer, `pay_invoice` adds the payer's
inputs and signature (I2), and `finalize_invoice` completes I3 on the issuer's side, which posts
it.

**Refresh and scan.** `Wallet::refresh` brings outputs and transactions in line with the node's
UTXO set and kernels. A scan rebuilds outputs from the chain after a restore.

A relay message is acknowledged only after its effect is stored, or after it was rejected for good.
A message that fails for a transient reason stays on the relay for the next attempt.

## Mobile shape: listen and drain

A phone suspends apps in the background, so the Epicbox client has two modes:

| Mode | What it does | Used |
|---|---|---|
| `listen` | Keeps a connection open and receives as messages arrive | While the app is in the foreground |
| `drain` | Connects, processes everything waiting, disconnects | When the app returns to the foreground, and for the desktop's invoice checks |

The relay keeps a message for 7 days, so a wallet collects what arrived while the app slept. The
limits are in LEPIC's
[Epicbox notes](https://github.com/BTLabsUK/lepic/blob/main/docs/compat/epicbox.md).

Events (balance, transaction stage, sync progress, transport state) stream from the engine to the
app through the binding. `LepicRuntime` owns one multi-threaded Tokio runtime for the app, and logs
reach the app through a `LogSink` it implements or an on-device `LogRing`.

## Configuration

The rule is "All configuration in settings.toml (no hardcoded configuration)" (ADR 0030). The
code of the app, LEPIC and lepic-flutter holds no host, URL, IP address, onion address, port or
service path, and no server-related timeout, interval or limit.

| File | Holds | Where |
|---|---|---|
| `settings.toml` | The user's choices: Node and Epicbox lists, on/off switches | The wallet's data folder |
| `app-config.toml` | Operators, onions, service URLs, timeouts, intervals, ports, limits | Shipped read-only in `app/assets/config/` |
| `lepic-config.toml` | The same for the `lepic` CLI | Compiled into the CLI |

The first entry of each list is the one in use. The library crates take every value from the
caller and hold no default; through the binding, the app passes the servers in `WalletConfig` and
the timeouts and limits in `NetTuning`, whose fields are all required. Protocol values stay in code, such as what an address without a port
means, size limits, crypto parameters and consensus values. `tools/check-no-hosts.sh` fails the
check when a host, URL, IPv4 literal, port or API path appears in source. The app's defaults are in
[`app/assets/config/app-config.toml`](https://github.com/BTLabsUK/wallet-for-epic/blob/main/app/assets/config/app-config.toml).

## Related pages

- [LEPIC](lepic.md): the crates, their edges, the CLI.
- [lepic-flutter](lepic-flutter.md): the binding and how native libraries are bundled.
- [Security model](security-model.md): keys, secrets at the boundary, input validation.
- [Architecture decisions](decisions.md): the ADRs behind this design.
- LEPIC's own [architecture notes](https://github.com/BTLabsUK/lepic/blob/main/docs/architecture.md).
