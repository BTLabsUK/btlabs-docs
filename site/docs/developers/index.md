---
title: Developer guide
description: The three repositories behind Epic Cash Desktop and Epic Cash Mobile, and where to start reading.
---

# Developer guide

Epic Cash Desktop and Epic Cash Mobile are one Flutter app on top of LEPIC, a wallet core written in
Rust. Three repositories, all under the Apache License 2.0:

| Repository | Language | What it is |
| --- | --- | --- |
| [wallet-for-epic](https://gitlab.com/bt-labs-group/wallet-for-epic) *(available soon)* | Dart, Flutter | The app: desktop and phone interfaces, build and release scripts |
| [lepic-flutter](https://gitlab.com/bt-labs-group/lepic-flutter) *(available soon)* | Dart, Rust glue | The Flutter binding: the Dart API over LEPIC and the native build hook |
| [lepic](https://gitlab.com/bt-labs-group/lepic) *(available soon)* | Rust | LEPIC: the wallet engine, its crates, the `lepic` CLI and the FFI API |

```text
 Epic Cash Desktop / Epic Cash Mobile   (wallet-for-epic, Flutter)
                 |
                 |  package:lepic
                 v
        lepic-flutter   (Dart API, flutter_rust_bridge, build hook)
                 |
                 |  liblepic_ffi  (.so / .dll / .dylib)
                 v
        LEPIC   (Rust crates: engine, keys, slates, Epicbox, node, Tor, storage)
                 |
     node  ·  Epicbox relay  ·  other wallets (HTTP, Tor, files)
```

The app pins exact commits of lepic-flutter and LEPIC, and the binding pins the same LEPIC commit,
so every build names the code it was made from.

## Where to start

- **Understand it:** [Architecture](architecture.md), then [LEPIC](lepic.md) and
  [lepic-flutter](lepic-flutter.md).
- **Trust it:** [Security model](security-model.md), [Decisions](decisions.md) (the ADRs) and
  [LEPIC and upstream](upstream.md).
- **Build it:** [Build from source](build/index.md) and
  [Development environment](dev-environment.md).
- **Change it:** [Testing](testing.md), [Contributing](contributing.md) and
  [Releases](releases.md).

## Epic Cash itself

The Epic Cash node, the reference wallet, the Epicbox relay protocol, slates and the APIs are
documented on the [Epic Cash Developer Hub](https://devdocs.btlabs.uk). These pages cover only the
BT LABS wallets and their core.

## Status

Pre-release. LEPIC is `0.y.z`: its APIs still change. Report security issues privately; see
[Security](../security.md).
