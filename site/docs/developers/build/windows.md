---
title: Build for Windows
description: Build the Epic Cash Desktop installer on Windows with PowerShell.
---

# Build for Windows

Run in PowerShell 7 on Windows:

```powershell
pwsh -NoProfile -File app\tool\build_windows_release.ps1 -Lepic <path or URL of LEPIC> -LepicFlutter <path or URL of lepic-flutter>
```

`-Lepic` and `-LepicFlutter` are mandatory. Each names a repository that contains the commit pinned
in `tools\lepic.rev` and `tools\lepic-flutter.rev`; see [Build from source](index.md).

## Needs

- Flutter, at the version in `scripts/linux/flutter.version` (3.47.5). The script looks in
  `%USERPROFILE%\flutter\bin`; pass `-Flutter` for another folder.
- `rustup` and `cargo`. LEPIC's `rust-toolchain.toml` picks the Rust version.
- Visual Studio 2022 Build Tools with the C++ workload.
- CMake and Git on `PATH`.
- Inno Setup 6. The script expects `ISCC.exe` in
  `%LOCALAPPDATA%\Programs\Inno Setup 6`; pass `-Iscc` for another path.

The script stops at once when `flutter`, `rustup`, `cargo`, `cmake` or `git` is missing.

## What it does

1. Clones LEPIC and lepic-flutter into `app\third_party\` at the pinned commits.
2. Builds `lepic_ffi.dll` with a static C runtime, so the library needs no runtime DLLs of its own.
3. Runs `flutter build windows --release`, with the version from `app\pubspec.yaml`, and checks the
   exe's version information.
4. Copies the Visual C++ runtime DLLs next to `epic_wallet.exe`.
5. Signs the exe, builds the installer with Inno Setup, and signs the installer.

## Options

| Option | Effect |
| --- | --- |
| `-OutDir` | Output folder. Default `app\build\installer`. |
| `-NoTor` | Build without Tor; see [Build variants](variants.md). |
| `-TorBundle` | Folder from `tools/fetch-tor.sh win`, bundled as `bin\tor-bundle`. Without it, Tor shows as not included. |
| `-NodeBin` | Path to `epic.exe`, bundled as the built-in node. |
| `-LepicCache` | An earlier `app\third_party\lepic` to copy first, so unchanged Rust crates are not rebuilt. |
| `-Dist msstore` | Build the Microsoft Store package instead; see [Build variants](variants.md). |

## Signing

The script signs with a code-signing certificate from the Windows certificate store, named by its
SHA-1 thumbprint: `-SignThumbprint` or the `WFE_SIGN_THUMBPRINT` variable. The Windows SDK's
`signtool.exe` signs with SHA-256 and a timestamp. Without a thumbprint the build goes on unsigned
and says so; Windows SmartScreen then warns on a first install.

## Output

In the output folder:

- `epic-cash-desktop-<version>-windows-x64-setup.exe`
- `epic-cash-desktop-<version>-windows-x64-setup.exe.sha256`

With `-NoTor` the name has `-notor` after the version. The installer and the exe carry the file
version `YY.MM.patch.0`; see [Releases](../releases.md).

The app keeps its data in `%USERPROFILE%\.epic_cash_desktop`. Uninstalling leaves that folder.

## Portable zip

`app\tool\build_windows.ps1` builds a portable folder with `epic_wallet.exe`, zipped as
`build\epic_wallet-windows-x64-<version>.zip`, without an installer.
