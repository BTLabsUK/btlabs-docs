---
title: Build from source
description: How the app, LEPIC and lepic-flutter fit together for a build, and where to find the steps for each platform.
---

# Build from source

Epic Cash Desktop and Epic Cash Mobile are built from three repositories:

| Repository | What it is |
| --- | --- |
| [wallet-for-epic](https://gitlab.com/epic-cash-bt/wallet-for-epic) *(available soon)* · [GitHub mirror](https://github.com/BTLabsUK/wallet-for-epic) | The Flutter app and its build scripts |
| [lepic-flutter](https://gitlab.com/epic-cash-bt/lepic-flutter) *(available soon)* · [GitHub mirror](https://github.com/BTLabsUK/lepic-flutter) | The Flutter binding, the Dart package `lepic` |
| [LEPIC](https://gitlab.com/epic-cash-bt/lepic) *(available soon)* · [GitHub mirror](https://github.com/BTLabsUK/lepic) | The Rust wallet core, built into a native library |

See [Architecture](../architecture.md) for how they work together at run time.

## How a build uses them

The app pins the other two by commit:

- `tools/lepic-flutter.rev` holds the lepic-flutter commit.
- `tools/lepic.rev` holds the LEPIC commit. It must equal the `lepic.rev` inside the pinned
  lepic-flutter; the scripts stop when the two differ.

Clone the app; `tools/lepic.sh sync` then clones LEPIC and lepic-flutter at the pinned commits into
`app/third_party/` (git-ignored), and `build` builds the native library:

```bash
git clone https://gitlab.com/epic-cash-bt/wallet-for-epic
cd wallet-for-epic
. tools/env.sh
tools/lepic.sh sync            # clone or move both repositories to the pinned commits
tools/lepic.sh build linux     # the native library for this host
tools/lepic.sh build android   # the three Android ABIs (needs the NDK and cargo-ndk)
```

To build from local checkouts of LEPIC or lepic-flutter instead, point `LEPIC_REPO` and
`LEPIC_FLUTTER_REPO` at them (a path or a git URL) before `sync`.

`build` refuses to run when a clone is not at its pin or has local changes. To work on LEPIC itself,
see [Dev environment](../dev-environment.md) and [LEPIC](../lepic.md).

## Quick dev run

```bash
. tools/env.sh
tools/lepic.sh sync
tools/lepic.sh build linux

cd app
flutter pub get
flutter run -d linux -t lib/main_desktop.dart    # desktop
flutter run -t lib/main.dart                     # phone or emulator
```

For an Android device or emulator, run `tools/lepic.sh build android` first.

## Release builds

| Platform | Page | Script |
| --- | --- | --- |
| Linux (AppImage) | [Linux](linux.md) | `scripts/build-linux.sh` |
| Windows (installer) | [Windows](windows.md) | `app/tool/build_windows_release.ps1` |
| Android (APK, App Bundle) | [Android](android.md) | `app/tool/build_android_release.sh` |
| macOS and iOS (previews) | [Apple platforms](apple.md) | `tools/build-apple.sh` |
| Without Tor, store builds | [Build variants](variants.md) | `WFE_TOR`, `WFE_DIST` |

Related: [Dev environment](../dev-environment.md), [Testing](../testing.md),
[Releases](../releases.md), [Contributing](../contributing.md).
