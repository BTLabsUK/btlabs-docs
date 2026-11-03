---
title: Build for Android
description: Build the signed BT Wallet APK, or the App Bundle, with the release script.
---

# Build for Android

```bash
. tools/env.sh
app/tool/build_android_release.sh [output-dir]
```

The default output folder is `app/build/release-<version>/`. The script builds LEPIC for Android
at the pinned commit, builds the arm64-v8a APK, copies it to the output folder, writes `SHA256SUMS`,
and verifies the result.

Outputs:

- `bt-wallet-<version>-android-arm64-v8a.apk`
- `SHA256SUMS`
- with `WFE_EMULATOR_X86_64=1`, also `emulator/bt-wallet-<version>-android-x86_64.apk` for emulator
  tests; it is not in `SHA256SUMS`.

## Needs

| Tool | Version |
| --- | --- |
| JDK | 21 (`tools/env.sh` sets `JAVA_HOME`; the Android code targets Java 17) |
| Android SDK | with build-tools (`aapt2`, `apksigner`, `zipalign`) |
| Android NDK | `28.2.13676358` |
| Rust | from LEPIC's `rust-toolchain.toml`, with the Android targets it lists |
| `cargo-ndk` | `cargo install cargo-ndk --version 4.1.2 --locked` |
| Flutter | `scripts/linux/flutter.version` |

`tools/env.sh` sets `ANDROID_HOME`, `ANDROID_NDK_HOME` and the related variables. Every one can be
overridden from the environment. The script also calls `tools/lepic.sh sync`, so
`LEPIC_REPO` and `LEPIC_FLUTTER_REPO` apply; see [Build from source](index.md). Unless you build
without Tor, `tools/fetch-tor.sh` downloads the Tor binary, so `curl` and `jq` are needed.

## Signing

Release builds are signed with a release key and never with the debug key. Without a usable key the
build stops before it makes an APK.

The key lives outside the repository, in a `key.properties` file with four fields: `storeFile`,
`storePassword`, `keyAlias` and `keyPassword`. Gradle finds it, in this order:

1. the `WFE_ANDROID_KEY_PROPERTIES` environment variable,
2. the Gradle property `-PwfeKeyProperties=<path>`,
3. a default location in the user's home folder.

Debug builds (`flutter run`) never read it.

:::note
The script's last step compares the APK's signing certificate with the one BT LABS releases are
signed with. A build signed with your own key is built and signed, but that check reports `FAIL`.
Use the APK for your own testing, and do not publish it as an official release.
:::

## What the script checks

It checks the package name, the version name and code, the app label, the LEPIC library in the APK,
that the native libraries are 16 KB aligned for Android 15 and newer, and that no Firebase or other
Google push code is present. Build numbers are explained in [Releases](../releases.md).

## Variants

| Command | Result |
| --- | --- |
| `WFE_TOR=0 app/tool/build_android_release.sh` | build without Tor |
| `WFE_DIST=play app/tool/build_android_release.sh` | App Bundle for Google Play |
| `WFE_DIST=fdroid app/tool/build_android_release.sh` | APK for F-Droid, from a prepared checkout |

See [Build variants](variants.md).

## Build by hand

To run a debug build on a device or emulator:

```bash
. tools/env.sh
tools/lepic.sh sync
tools/lepic.sh build android
cd app && flutter run -t lib/main.dart
```
