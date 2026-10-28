---
title: Build for macOS and iOS
description: Build the macOS and iOS previews on a Mac with tools/build-apple.sh.
---

# Build for macOS and iOS

macOS (Epic Cash Desktop) and iOS (Epic Cash Mobile) are previews. The build runs on a Mac and
needs no Apple developer account.

```bash
tools/build-apple.sh                          # doctor, sources, lepic, macos, dmg, ios-sim
tools/build-apple.sh doctor sources lepic     # or name the steps you want
```

Minimum systems: macOS 12 and iOS 15.

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

- `Epic Cash Desktop.app`
- `EpicCashDesktop-<version>-macos.dmg`
- `EpicCashMobile-<version>-ios-simulator.zip`
- `EpicCashMobile-<version>-ios-unsigned.ipa`
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
| `WFE_NODE_BIN_MAC_ARM64`, `WFE_NODE_BIN_MAC_X64` | `epic` node binaries (version 4.1 or newer) to bundle as the built-in node, one per architecture. Without them the app has no built-in node. |
| `WFE_NODE_FETCH=1` | Download the pinned arm64 node release instead. |
| `WFE_TOR=0` | Build without Tor. |
| `SIM_DEVICE` | Simulator name or UDID. Default: the first available iPhone. |
| `CARGO_TARGET_DIR` | LEPIC's cargo output folder. |
