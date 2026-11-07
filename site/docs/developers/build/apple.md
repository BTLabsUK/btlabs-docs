---
title: Build for macOS and iOS
description: Build the macOS and iOS previews on a Mac with tools/build-apple.sh.
---

# Build for macOS and iOS

BT Wallet for macOS and iOS is a preview. The build runs on a Mac and
needs no Apple developer account.

```bash
tools/build-apple.sh                          # doctor, sources, lepic, macos, dmg, ios-sim
tools/build-apple.sh doctor sources lepic     # or name the steps you want
```

Minimum systems: macOS 12 on Apple silicon, and iOS 15. macOS builds are arm64 only: the
built-in node has no Intel build.

## Needs

- A Mac with Xcode 26 or newer, its command line tools selected (`xcode-select`), and an iOS
  Simulator runtime (`xcodebuild -downloadPlatform iOS`).
- Flutter 3.47.5 and Rust (`rustup`).
- `git`, `curl`, `jq`, `lipo`, `codesign` and `hdiutil`.

The `doctor` step checks all of this. The script runs on macOS only.

## Steps

| Step | What it does |
| --- | --- |
| `doctor` | Prints and checks the toolchain. |
| `sources` | Puts the LEPIC and lepic-flutter clones in `app/third_party` at the pinned commits, cloning from `LEPIC_REPO` and `LEPIC_FLUTTER_REPO` when missing. |
| `lepic` | Builds the library for `aarch64-apple-darwin`, `x86_64-apple-darwin`, `aarch64-apple-ios` and `aarch64-apple-ios-sim`. |
| `macos` | `flutter build macos --release`, bundles the node and Tor, and signs ad hoc. |
| `dmg` | Packs the app into a compressed `.dmg` with an Applications link. |
| `ios-sim` | Builds for the iOS Simulator, installs and starts it there, and zips the app. |
| `ipa` | `flutter build ios --release --no-codesign`, zipped as an unsigned `.ipa`. |
| `smoke` | Runs `integration_test/simple_test.dart` on macOS and in the Simulator, and starts the built app. |
| `live` | A mainnet check: needs internet and talks to public nodes and Epicbox. |
| `all` | Every step above except `live`. |

A failing step writes a `FAIL` line to `results.txt` before the script exits.

## Output

Everything goes to `build-apple/` at the repository root, or to `APPLE_OUT`:

- `BT Wallet.app`
- `bt-wallet-<version>-macos.dmg`
- `bt-wallet-<version>-ios-simulator.zip`
- `bt-wallet-<version>-ios-unsigned.ipa`
- logs and `results.txt`, one `PASS` or `FAIL` line per step

With `WFE_TOR=0` the names have `-notor` after the version; see [Build variants](variants.md).

## Signing

The macOS app is signed ad hoc, so macOS shows its warning for an app from an unidentified
developer. The `.ipa` is unsigned: installing it on a device needs signing with an Apple developer
team first. None of the steps above needs one.

## Environment

| Variable | Effect |
| --- | --- |
| `APPLE_OUT` | Output folder. |
| `LEPIC_REPO`, `LEPIC_FLUTTER_REPO` | Where `sources` clones from. |
| `WFE_NODE_BIN_MAC_ARM64` | An `epic` node binary to bundle as the built-in node. Without it the script downloads the node release pinned in [`tools/build-apple.sh`](https://github.com/BTLabsUK/wallet-for-epic/blob/main/tools/build-apple.sh) and checks its SHA-256. |
| `WFE_NODE_FETCH=0` | No download: without `WFE_NODE_BIN_MAC_ARM64` the app has no built-in node. |
| `WFE_TOR=0` | Build without Tor. |
| `SIM_DEVICE` | Simulator name or UDID. Default: the first available iPhone. |
| `CARGO_TARGET_DIR` | LEPIC's cargo output folder. |
