---
title: Dependencies
description: LEPIC's dependency policy, the main Rust crates and Dart packages, and the third-party pieces the apps bundle.
---

# Dependencies

LEPIC keeps a small, current and checked dependency graph. This page lists the policy, the main
crates of LEPIC, the main Dart packages of the app, and the third-party pieces the apps bundle.

## Licences of the three repositories

| Repository | Licence |
|---|---|
| [LEPIC](lepic.md) | Apache-2.0 |
| [lepic-flutter](lepic-flutter.md) | Apache-2.0 |
| wallet-for-epic (BT Wallet) | Apache-2.0 |

Parts of LEPIC are ported from the Epic Cash node and wallet, which are Apache-2.0 and descend
from Grin. Parts of the app are ported from the Epic Cash desktop wallet, also Apache-2.0. Each
repository's `NOTICE` file names what was ported.

## LEPIC's dependency policy

The policy is ADR 0010. `cargo deny check` enforces it in CI on every change and in a weekly job;
the configuration is `deny.toml` at the repository root.

- **Current versions.** The latest stable Rust, pinned in `rust-toolchain.toml`, and the latest
  stable release of each crate when it is added. Every external crate is set once in the root
  `Cargo.toml` with default features off; crates enable only the features they use.
- **Advisories.** Known vulnerabilities and yanked crates fail the check.
- **Licences.** Allowed: Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, ISC, Unicode-3.0, Zlib,
  CC0-1.0, MPL-2.0, CDLA-Permissive-2.0 (the Mozilla root certificates in `webpki-roots`) and
  BlueOak-1.0.0 (`minicbor`, used by the `ur` crate for QR slates).
- **Duplicate versions** fail the check, unless listed with the dependency that holds them back.
- **Banned crates.** Proof-of-work code (RandomX, ProgPoW), chain storage (CRoaring, LMDB),
  OpenSSL and native-tls, `aws-lc-rs`, and crates that need CMake, bindgen or a C++ bridge at build
  time. Builds need only Rust and a C compiler.
- **Sources.** Only crates.io, plus one git source:
  [rust-secp256k1-zkp](https://github.com/EpicCash/rust-secp256k1-zkp), the library Epic Cash
  itself uses, pinned to an exact commit.
- **Not used directly:** `failure`, `log4rs`, `lazy_static`, `once_cell`, `chrono`, `log`.
- **Pinned CI.** Dependencies and CI actions are pinned, and update bots propose updates weekly.

A commit that adds a crate says why it is needed, that it is maintained, and what else was
considered.

## Main Rust crates

| Area | Crates |
|---|---|
| Curve, commitments, proofs | `grin_secp256k1zkp` from `EpicCash/rust-secp256k1-zkp`, pinned |
| Async runtime | `tokio` |
| TLS | `rustls` with the ring provider, `webpki-roots`, `tokio-rustls` |
| HTTP | `hyper`, `hyper-util`, `hyper-rustls` |
| Websockets (Epicbox) | `tokio-tungstenite` |
| Storage | `rusqlite` with the bundled SQLite |
| Password KDF and encryption | `argon2`, `chacha20poly1305`, `pbkdf2` (for `epic-wallet` formats) |
| Hashes and MACs | `blake2`, `sha2`, `sha3`, `hmac`, `hkdf`, `ripemd` |
| Signatures and envelopes | `ed25519-dalek`, `x25519-dalek`, `hpke` |
| Secrets in memory | `zeroize`, `secrecy` |
| Mnemonic | `bip39` |
| QR slates | `ur`, `minicbor`, `miniz_oxide` |
| Serialization, errors, logging | `serde`, `serde_json`, `thiserror`, `tracing` |
| Binding | `flutter_rust_bridge`, at an exact version shared with the Dart package |
| CLI | `clap` |

Exact versions are in the root `Cargo.toml` and `Cargo.lock`. Release builds use fat LTO, one
codegen unit, stripped symbols and overflow checks.

## Main Dart packages of the app

| Package | Used for |
|---|---|
| `lepic` (lepic-flutter) | The wallet core |
| `flutter_rust_bridge` | Loading the native library |
| `flutter_riverpod` | App state |
| `flutter_secure_storage` | The platform secret store |
| `ffi`, `win32` | The Windows secret store (DPAPI) |
| `local_auth` | Biometric unlock |
| `crypto`, `cryptography` | Hashes; sealing support reports |
| `zxcvbnm` | The password strength hint |
| `mobile_scanner` | Scanning QR codes (Android, iOS) |
| `pretty_qr_code` | Showing QR codes |
| `file_picker`, `share_plus` | Slate files and sharing |
| `path_provider` | App folders |
| `window_manager`, `snap_layouts` | The desktop window |
| `flutter_svg` | Help illustrations |
| `intl`, `flutter_localizations` | Translations |

Versions are pinned in `app/pubspec.yaml`.

## Bundled third-party pieces

| Piece | Where | Licence |
|---|---|---|
| `tor`, from the Tor Expert Bundle | Desktop builds, next to the app; Android as a native library | 3-clause BSD; the licence file lists the libraries it ships with |
| `epic`, the Epic node | Desktop builds, optional, for the built-in node | Apache-2.0 |
| Montserrat, JetBrains Mono, Noto Sans Thai | Fonts in the app | SIL Open Font License 1.1 |
| Password word lists (from zxcvbn-ts) | App assets | MIT |
| Language flags (flag-icons) | App assets | MIT |
| Status icons | App font | MIT and Apache-2.0 |

The tor bundle is pinned by version and SHA-256 in the app repository. The tor binary is not part
of LEPIC's dependency graph; LEPIC starts it as a separate process. Builds without Tor
(`WFE_TOR=0`) leave the tor binary out, and the native library can be built without LEPIC's Tor
code (see [lepic-flutter](lepic-flutter.md#without-tor)).

## Related pages

- [LEPIC](lepic.md)
- [Security model](security-model.md)
- [Architecture decisions](decisions.md)
