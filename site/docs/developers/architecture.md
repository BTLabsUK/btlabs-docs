---
title: Architecture
description: How Epic Cash Desktop and Mobile, the lepic-flutter binding and the LEPIC wallet core fit together.
---

# Architecture

Epic Cash Desktop and Epic Cash Mobile are one Flutter app. The wallet itself is LEPIC, a Rust
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

The app has two entry points on one codebase: `lib/main.dart` starts the phone app (Epic Cash
Mobile) and `lib/main_desktop.dart` the desktop interface (Epic Cash Desktop). Both run on the
same wallet core through the binding.

## Layers inside LEPIC

LEPIC is a Cargo workspace of small crates in layers:

1. **Pure crates** at the bottom: crypto, transaction primitives, keys, slates, contact formats.
   They do no I/O, read no clock and create no randomness of their own, so they are
   deterministic and can be fuzzed.
2. **I/O crates** in the middle: the node client, SQLite storage, and the transports (file,
   Epicbox, HTTP, Tor).
3. **The engine**, `lepic-wallet`, above them, with contacts as a separate crate on top of it.
4. **Front ends** on top: the `lepic` command-line wallet and `lepic-ffi`, the FFI API the
   binding wraps.

The allowed edges between crates are fixed and checked by `cargo xtask deps-check`. The table of
crates and edges is on the [LEPIC](lepic.md) page.

## Engine and ports

The engine depends on traits ("ports"), not on implementations:

| Port | Implemented by |
|---|---|
| `NodeApi` | `lepic-node`; a mock node in tests |
| `StoreOpener` | SQLite stores over `lepic-store`; in-memory stores in tests |
| `Transport` | file, Epicbox, HTTP and Tor transports; a loopback in tests |
| `SecretVault` | the platform keystore through the app on mobile, a vault file in the CLI |
| `Clock`, `Rng` | real ones in the CLI and `lepic-ffi`; fixed ones in tests |

The engine owns no runtime and no global state. `lepic-cli` and `lepic-ffi` create the Tokio
runtime and pass it in. Because the node, storage, keys, network and clock are all passed in, one
test can run several wallets side by side, and one process can hold a mainnet and a floonet
wallet.

## Slates, codecs and transports

A slate is the message two wallets exchange to build a transaction. LEPIC keeps one
version-free slate model and several wire formats:

```text
 wire bytes  <-->  codec  <-->  domain Slate  <-->  engine
                    ^
                    | chosen by the transport's
                    | format policy
```

- **Domain slate.** Explicit stage (S1, S2, S3 for a payment; I1, I2, I3 for an invoice),
  explicit roles, typed fields. A slate decoded from a legacy format remembers its wire origin, so
  a reply can echo what the peer sent.
- **Codec.** Maps one wire format to the domain model and back: legacy V2 JSON and legacy V3
  JSON today. Encoding either keeps everything or fails with a typed error; nothing is dropped
  silently.
- **Transport.** Each transport declares a format policy: the codecs it accepts, the one it uses
  for a new slate, and the rule for replies. Epicbox sends the V2 shape for a new payment and
  replies in the shape it received; the file method writes V3.

Adding a payment method is one transport module and one registration; adding a format is one
codec module and one registration. Protocol-level detail of slates and Epicbox is on the
[Epic Cash developer docs](https://devdocs.btlabs.uk).

## Main flows

**Send (standard flow)**

1. The engine selects outputs, builds the S1 slate, stores the private transaction context
   encrypted, and locks the selected outputs, in one store transaction.
2. The transport's policy picks a codec, the codec encodes, the transport delivers.
3. The answer (S2) arrives through Epicbox, a file, HTTP or Tor. It is decoded, checked against
   the stored context, finalized and posted to the node. Only then is a relay message
   acknowledged.

**Receive** is the mirror: decode the S1, validate it, add the output and the partial signature,
store, and reply through the same transport in the format its policy prescribes.

Every inbound message is idempotent on `(slate_id, stage)`: a slate received twice is answered
with the same reply, not paid twice. A relay message is acknowledged only after its effect is
stored, or after it was rejected for good.

## Mobile shape: listen and drain

A phone suspends apps in the background, so the Epicbox client has two modes:

| Mode | What it does | Used |
|---|---|---|
| `listen` | Keeps a connection open and receives as messages arrive | While the app is in the foreground |
| `drain` | Connects, processes everything waiting, disconnects | Background work the app schedules |

The relay keeps every message until it is acknowledged, so nothing is lost while the app sleeps.
Events (balance, transaction stage, sync progress, transport state) stream from the engine to the
app through the binding.

## Related pages

- [LEPIC](lepic.md): the crates, their edges, the CLI.
- [lepic-flutter](lepic-flutter.md): the binding and how native libraries are bundled.
- [Security model](security-model.md): keys, secrets at the boundary, input validation.
- [Architecture decisions](decisions.md): the ADRs behind this design.
- LEPIC's own [architecture notes](https://github.com/BTLabsUK/lepic/blob/main/docs/architecture.md).
