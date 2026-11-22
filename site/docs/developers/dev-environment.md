---
title: Dev environment
description: The toolchain versions the app and LEPIC build with, the variables tools/env.sh sets, and editor setup.
---

# Dev environment

## Toolchain versions

| Tool | Version | Where it is pinned |
| --- | --- | --- |
| Flutter | 3.47.5 | `scripts/linux/flutter.version` |
| Dart | `^3.13.4` | `app/pubspec.yaml` (comes with Flutter) |
| Rust | 1.99.0 | `rust-toolchain.toml` in LEPIC |
| Rust, fuzzing | `nightly-2026-10-02` | `fuzz/rust-toolchain.toml` in LEPIC |
| Android NDK | 28.2.13676358 | `tools/env.sh` |
| JDK | 21 | `tools/env.sh` (Android code targets Java 17) |
| `cargo-ndk` | 4.1.2 | LEPIC's mobile CI workflow |
| Xcode | 26 or newer | `tools/build-apple.sh doctor` |
| Ubuntu (Linux release build) | 22.04 | `scripts/linux/Dockerfile` |

Check these files for the current values before you install; the table follows them. With `rustup`
installed, entering a LEPIC checkout installs the pinned Rust and the targets it lists (Android and
iOS) by itself.

LEPIC has no other Rust or Dart requirements. lepic-flutter needs Flutter 3.47.0 or newer and
generates its bridge with flutter_rust_bridge 2.13.0.

## tools/env.sh

Source it, do not run it:

```bash
. tools/env.sh
```

It sets user-space paths only; nothing needs `sudo`. Edit the paths at the top of the file if your
tools live elsewhere, or set a variable before sourcing.

| Variable | Default |
| --- | --- |
| `JAVA_HOME` | a JDK 21 under `~/.local/opt` |
| `ANDROID_HOME`, `ANDROID_SDK_ROOT` | `~/Android/Sdk` |
| `ANDROID_NDK_VERSION` | `28.2.13676358` |
| `ANDROID_NDK_HOME`, `ANDROID_NDK_ROOT` | `$ANDROID_HOME/ndk/$ANDROID_NDK_VERSION` |
| `FLUTTER_ROOT` | `~/flutter` |

It also puts `~/.cargo/bin`, `~/.pub-cache/bin`, the Android SDK tools, Flutter and the JDK on
`PATH`.

## First build

```bash
. tools/env.sh
tools/lepic.sh sync
tools/lepic.sh build linux
cd app && flutter pub get && flutter analyze
```

The full steps are on [Build from source](build/index.md).

## LEPIC

```bash
git clone https://github.com/BTLabsUK/lepic.git
cd lepic
git config core.hooksPath .githooks   # commit message check
cargo install cargo-deny cargo-nextest --locked   # `cargo xtask check` runs both
cargo xtask check
```

`cargo xtask check` is the gate every commit passes. Run it from a git checkout. Its first run
needs network access to fetch the lockfiles of `conformance/`, `fuzz/` and `interop/probe/`. Run
`cargo xtask` without arguments to list the commands, for example `cargo xtask install` (builds
the `lepic` binary and installs it in `~/.local/bin`, or in the `--dir` you give). The `conformance/`
workspace uses the same pinned Rust as the product; building the reference node and wallet in it
needs CMake, a C++ compiler, libclang and the OpenSSL headers. See [Testing](testing.md) and
[Contributing](contributing.md).

To try a LEPIC change in the app, point `LEPIC_REPO` at your clone. The pin in `tools/lepic.rev`
must name a commit that exists there, and lepic-flutter's own `lepic.rev` must name the same
commit. See [lepic-flutter](lepic-flutter.md).

## Editors

- **Flutter app**: open `app/` in VS Code with the Dart and Flutter extensions, or in Android Studio
  or IntelliJ with the Flutter plugin. Point the SDK path at the Flutter version above.
- **Rust**: open the LEPIC folder with rust-analyzer. The repository's `.editorconfig` sets UTF-8,
  LF line endings, a final newline, four-space indents, and two for Markdown, YAML, JSON and TOML.
- Format and lint before you commit: `cargo fmt` and `cargo clippy` for LEPIC, `flutter analyze` for
  the app. Do not run `dart format` on the app.
- Linux desktop runs need the GTK 3 and `libsecret` development packages, plus `clang`, `cmake`,
  `ninja-build` and `pkg-config`.
