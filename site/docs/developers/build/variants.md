---
title: Build variants
description: Build without Tor, and build for Google Play, F-Droid or the Microsoft Store.
---

# Build variants

Two switches change what a build contains. Unset, both give the standard build.

## Without Tor: WFE_TOR=0

The same app with Tor out of the package and out of the interface. `WFE_TOR=0` is the one name in
every script; the Dart code reads it as `--dart-define=WFE_TOR=false`.

| Platform | Command | Output |
| --- | --- | --- |
| Linux | `WFE_TOR=0 scripts/build-linux.sh` | `EpicCashDesktop-<version>-notor-x86_64.AppImage` |
| Windows | `build_windows_release.ps1 ... -NoTor` | `epic-cash-desktop-<version>-notor-windows-x64-setup.exe` |
| Android | `WFE_TOR=0 app/tool/build_android_release.sh` | `epic-cash-mobile-<version>-notor-arm64-v8a.apk` |
| Dev run | `WFE_TOR=0 tools/lepic.sh build linux`, then `flutter run --dart-define=WFE_TOR=false` | |

What changes:

- LEPIC is built without its `tor` feature (`--no-tor` in `cargo xtask mobile --package`), so the
  native library has no Tor code.
- No Tor binary is fetched or packed.
- The app has no Tor switch, no Link · Tor method and no Tor only network mode, and cannot send to
  `.onion` addresses.
- The in-app updater is off.
- The file names carry `-notor`, so the build cannot be mistaken for the standard one.

The native library is built per switch. When you change `WFE_TOR`, run `tools/lepic.sh build` again
before `flutter run` or `flutter test`. The Linux build script refuses a library that does not match
the switch.

## Distribution: WFE_DIST

`WFE_DIST` picks where the build is meant to be installed from. It is `web` (the default), `play` or
`fdroid` on Android, and `web` or `msstore` on Windows.

| | `web` | `play` | `fdroid` |
| --- | --- | --- | --- |
| For | direct download | Google Play | F-Droid |
| Output | arm64-v8a APK | App Bundle (arm64-v8a) | arm64-v8a APK |
| In-app updater | yes | no | no |
| QR scanner | `mobile_scanner` (Google ML Kit) | `mobile_scanner` (Google ML Kit) | `camera` and `flutter_zxing` |
| Tor | Tor Project binary | Tor Project binary | built from source |
| File name | `epic-cash-mobile-<v>-arm64-v8a.apk` | `epic-cash-mobile-<v>-play.aab` | `epic-cash-mobile-<v>-fdroid-arm64-v8a.apk` |

No build contains Firebase or other Google push code. The app id and signing key are the same in all
three. `tools/dist-check.sh` runs on every output of `build_android_release.sh` and fails a build
that has what its distribution must not have.

### Google Play

```bash
WFE_DIST=play app/tool/build_android_release.sh <out dir>
```

Add `WFE_EMULATOR_X86_64=1` to also build an x86_64 APK for emulator tests.

### F-Droid

The F-Droid build swaps the QR scanner for one without Google libraries, so the checkout has to be
prepared first. Do this in a fresh clone, never in a working tree: the preparation edits files.

```bash
git clone <wallet-for-epic repository> build-copy
cd build-copy && git checkout <tag or commit>
tools/dist-prep.sh fdroid                 # add --dry-run to list the edits only
WFE_DIST=fdroid app/tool/build_android_release.sh <out dir>
```

`dist-prep.sh fdroid` replaces `mobile_scanner` with `camera` and `flutter_zxing` in
`app/pubspec.yaml`, switches the scanner screens to the free backend, installs
`pubspec.fdroid.lock`, and fails if anything still names Firebase, Play services or ML Kit. The
build script then builds Tor from source with `tools/build-tor-android.sh`.

The F-Droid recipe is prepared but not yet submitted.

### Microsoft Store

```powershell
pwsh -NoProfile -File app\tool\build_windows_release.ps1 -Dist msstore -Lepic <LEPIC> -LepicFlutter <lepic-flutter> -NodeBin <epic.exe> -TorBundle <folder>
```

This builds `epic-cash-desktop-<version>-msstore-x64.msix`, an unsigned package that the Store
signs. It has no in-app updater and no installer, and it cannot be combined with `-NoTor`.
`-MsixName`, `-MsixPublisher` and `-MsixPublisherDisplayName` set the package identity, which must
match the one the Store assigned to the app.

See also [Android](android.md), [Windows](windows.md) and [Linux](linux.md).
