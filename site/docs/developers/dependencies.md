---
title: Dependencies
description: LEPIC's dependency policy and how it is enforced, the main Rust crates, the vendored libraries, and the Dart packages and third-party pieces the app bundles.
---

# Dependencies

LEPIC keeps a small dependency graph and checks it on every commit. This page covers the policy, the
checks that enforce it, the main Rust crates, the two vendored libraries, and what the BT Wallet app
adds.

## Licences

| Repository | Licence |
|---|---|
| [LEPIC](lepic.md) | Apache-2.0 |
| [lepic-flutter](lepic-flutter.md) | Apache-2.0 |
| wallet-for-epic (BT Wallet) | Apache-2.0 |

Parts of LEPIC are ported from the Epic Cash node and wallet, which are Apache-2.0 and descend from
Grin. Parts of the app are ported from the Epic Cash desktop wallet, also Apache-2.0. Each
repository's `NOTICE` file names what was ported, and ported files carry the copyright lines of the
files they derive from. LEPIC records each ported file's origin in `upstream.toml`
([Upstream compatibility](upstream.md)).

## LEPIC's dependency policy

The policy is [ADR 0010](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0010-dependency-policy.md).
`cargo deny check` enforces it with
[`deny.toml`](https://github.com/BTLabsUK/lepic/blob/main/deny.toml), and `cargo xtask check` runs
it.

- **Toolchain.** `rust-toolchain.toml` pins a stable Rust release with the Android and iOS
  targets. The workspace uses edition 2024 and sets `rust-version` in `Cargo.toml`. `fuzz/` pins a
  dated nightly in its own `rust-toolchain.toml`, and `conformance/` pins its own release.
- **One place for versions.** Every external crate is set once in `[workspace.dependencies]` of the
  root `Cargo.toml` with default features off. A crate enables only the features it uses.
- **Advisories.** A yanked crate fails the check.
- **Licences.** Allowed: Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, ISC, Unicode-3.0, Zlib,
  CC0-1.0, MPL-2.0, CDLA-Permissive-2.0 (the Mozilla root certificates in `webpki-roots`) and
  BlueOak-1.0.0 (`minicbor`, used by the `ur` crate for QR slates). The Unlicense is allowed for
  `sqlite3mc-src` alone. `cargo deny` runs with `all-features = true`.
- **Sources.** Only crates.io. A git source or an unknown registry fails the check.
- **Duplicate versions.** A second version of a crate fails unless `deny.toml` lists it in `skip`
  with the dependency that holds it back. Wildcard versions fail.
- **Banned crates.** Proof-of-work code (RandomX, ProgPoW), chain storage (CRoaring, every LMDB
  binding), OpenSSL, native-tls, hyper-tls and tokio-native-tls, `aws-lc-rs` and `aws-lc-sys`, and the
  C++ bridge and build tools (`cmake`, `bindgen`, `cxx`, `autocxx`, `cpp_build` and their helpers).
  A build needs Rust and a C compiler only. `cargo xtask deps-check` keeps its own copy of the list
  equal to `deny.toml`.
- **Not direct.** `failure`, `log4rs`, `lazy_static`, `once_cell`, `chrono` and `log` may appear
  deeper in the graph; no workspace crate depends on them directly, and `deps-check` enforces it.
- **Updates.** Dependabot proposes weekly updates for Cargo (the root, `conformance/` and `fuzz/`)
  and for GitHub Actions. Workflow actions are pinned to commit hashes.
- **Release profile.** `opt-level = "s"`, fat LTO, one codegen unit, stripped symbols and overflow
  checks.

```bash
cargo deny check       # advisories, licences, bans, sources
cargo xtask deps-check # crate layering, direct-dependency rules, the banned list
```

A commit that adds a crate says why it is needed, that it is maintained, and what else was
considered.

## Main Rust crates

| Area | Crates |
|---|---|
| Curve, commitments, proofs | `grin_secp256k1zkp`, vendored in `third_party/` |
| Async runtime | `tokio` |
| TLS | `rustls` with the `ring` provider, `webpki-roots`, `tokio-rustls` |
| HTTP | `hyper` (HTTP/1.1), `hyper-util`, `hyper-rustls`, `http-body-util` |
| Websockets (Epicbox) | `tokio-tungstenite` |
| Storage | `rusqlite` over a vendored `libsqlite3-sys`, which compiles SQLite3 Multiple Ciphers |
| Password KDFs and AEAD | `argon2`, `pbkdf2`, `chacha20poly1305` |
| Hashes and MACs | `blake2`, `sha2`, `sha3`, `hmac`, `hkdf`, `ripemd` |
| Signatures and envelopes | `ed25519-dalek`, `x25519-dalek`, `hpke` |
| Secrets in memory | `zeroize`, `secrecy` |
| Encodings | `bip39`, `bs58`, `base64` |
| QR slates | `ur`, `minicbor`, `miniz_oxide` |
| Serialization, errors, time, ids | `serde`, `serde_json`, `toml`, `thiserror`, `anyhow`, `jiff`, `uuid` |
| Logging | `tracing`, `tracing-subscriber`, `tracing-appender` |
| Randomness | `rand`, `rand_core`, `getrandom` |
| Binding | `flutter_rust_bridge`, at an exact version shared with the Dart package |
| CLI | `clap` |

Exact versions are in the root `Cargo.toml` and `Cargo.lock`.

### TLS and HTTP

[ADR 0006](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0006-tls-and-http.md) fixes
the stack: rustls with `ring`, the `webpki-roots` trust store, hyper 1.x over HTTP/1.1, and
`tokio-tungstenite` with only its handshake feature for Epicbox websockets. No crate links
OpenSSL or the platform's TLS library.

## Vendored libraries

`third_party/` sits outside the workspace. The root `Cargo.toml` points at it with a path
dependency and a `[patch.crates-io]` entry.

| Library | Holds | Record of changes |
|---|---|---|
| `grin_secp256k1zkp` | A copy of the Epic Cash fork of the secp256k1-zkp wrapper and its C library, with upstream backports and build fixes | [`PATCHES.md`](https://github.com/BTLabsUK/lepic/blob/main/third_party/grin_secp256k1zkp/PATCHES.md) |
| `libsqlite3-sys` | The Rust bindings of `rusqlite`, built from the SQLite3 Multiple Ciphers amalgamation in place of SQLite's | [`PATCHES.md`](https://github.com/BTLabsUK/lepic/blob/main/third_party/libsqlite3-sys/PATCHES.md) |

Each `PATCHES.md` names the upstream commit or release the copy comes from and lists every change.
The curve patches change no byte an operation produces and no accept or reject verdict; the
[compatibility note](https://github.com/BTLabsUK/lepic/blob/main/docs/compat/secp256k1-zkp-fork.md)
has the detail.

The SQLite build ([ADR 0032](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0032-store-encrypted-at-rest.md)):

- ChaCha20-Poly1305 is the only page cipher compiled in; every other scheme is off.
- `SQLITE_TEMP_STORE=3` keeps temporary tables, indices and sorts in memory.
- `SQLITE3MC_SECURE_MEMORY=1` compiles the secure-memory option, which wipes freed allocations on a
  connection that sets `PRAGMA memory_security = fill`; LEPIC's keyed connections do.
- The build refuses a system SQLite, SQLCipher, bindgen, loadable extensions and sessions, and needs
  only a C compiler.

The vendored `rand` and `getrandom` of the curve wrapper are older than the workspace's. `deny.toml`
lists them in `skip` until the wrapper moves.

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
| `camera`, `flutter_zxing` | Scanning QR codes (Android, iOS) |
| `pretty_qr_code` | Showing QR codes |
| `file_picker`, `share_plus`, `desktop_drop` | Slate files, sharing and dropping files on the desktop app |
| `toml` | The settings file |
| `path_provider` | App folders |
| `window_manager`, `snap_layouts`, `screen_retriever` | The desktop window |
| `screen_brightness` | Screen brightness while a QR code is shown |
| `flutter_svg` | Help illustrations |
| `intl`, `flutter_localizations` | Translations |

Versions are pinned in `app/pubspec.yaml`.

## Bundled third-party pieces

| Piece | Where | Licence |
|---|---|---|
| `tor`, from the Tor Expert Bundle | Desktop builds, next to the app; Android as a native library | 3-clause BSD; the licence file lists the libraries it ships with |
| `epic`, the Epic node | Desktop builds, optional, for the built-in node | Apache-2.0 |
| Montserrat, JetBrains Mono, Geist, Geist Mono, Noto Sans Thai, Noto Sans SC (subset) | Fonts in the app | SIL Open Font License 1.1 |
| Password word lists (from zxcvbn-ts) | App assets | MIT |
| Language flags (flag-icons) | App assets | MIT |
| Status icons | App font | MIT and Apache-2.0 |

The tor bundle is pinned by version and SHA-256 in `tools/tor-bundle.json` of the app repository. The tor binary is not part
of LEPIC's dependency graph; LEPIC starts it as a separate process. Builds without Tor
(`WFE_TOR=0`) leave the tor binary out, and the native library can be built without LEPIC's Tor
code (see [lepic-flutter](lepic-flutter.md#native-libraries)).

## Related pages

- [LEPIC](lepic.md)
- [Security model](security-model.md)
- [Architecture decisions](decisions.md)
