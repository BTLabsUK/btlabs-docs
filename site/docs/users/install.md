---
title: Install
description: Download and install Epic Cash Desktop or Epic Cash Mobile on each platform.
---

# Install

Every release is on the download page:
**[examples.btlabs.uk/epic-cash-wallets](https://examples.btlabs.uk/epic-cash-wallets/)**.
Each file has its SHA-256 checksum under it, and `SHA256SUMS` sits next to the files.

| Device | App | Needs |
| --- | --- | --- |
| Windows | Epic Cash Desktop | Windows 10 or 11, 64-bit |
| Linux | Epic Cash Desktop | x86-64, Ubuntu 22.04 or newer |
| Android | Epic Cash Mobile | Android 7 or newer, arm64 |
| macOS (preview) | Epic Cash Desktop | macOS 12 or newer |
| iPhone, iPad (preview) | Epic Cash Mobile | iOS 15 or newer |

## Windows

1. Download `epic-cash-desktop-<version>-windows-x64-setup.exe`.
2. Run it. It installs for your user only; no administrator rights are needed.

Windows may warn that the publisher is unknown. Check the checksum, then choose to run it.

## Linux

1. Download `EpicCashDesktop-<version>-x86_64.AppImage`.
2. Allow it to run, either way:
   - In the file manager: right-click the file › Properties › Permissions › tick
     **Allow executing file as program**, then double-click it.
   - In a terminal, from the download folder (put in the version you downloaded):

     ```bash
     chmod +x EpicCashDesktop-26.10.21-x86_64.AppImage
     ./EpicCashDesktop-26.10.21-x86_64.AppImage
     ```

The AppImage needs `fusermount3`, which default Ubuntu desktops have. Without FUSE, start it with
`--appimage-extract-and-run`. It also uses GTK 3, `libsecret` and OpenGL from the system, which
desktop installs have.

## Android

1. Download `epic-cash-mobile-<version>-arm64-v8a.apk` on the phone.
2. Open the file. Allow installs from this source when Android asks.

A newer APK installs over an older one and keeps the wallets.

**Google Play:** Epic Cash Mobile is in testing on Google Play. The store page will be linked here
when it opens to everyone. The Play build and the APK are the same app with the same app data,
so a phone can move between them without a restore.

## macOS (preview)

1. Download `EpicCashDesktop-<version>-macos.dmg`.
2. Open it and drag **Epic Cash Desktop** to Applications.
3. The first start is blocked, because the app is not signed by an Apple developer. Open
   **System Settings › Privacy & Security** and click **Open Anyway**. Or, in Terminal:

   ```bash
   xattr -dr com.apple.quarantine "/Applications/Epic Cash Desktop.app"
   ```

4. When macOS asks whether the app may use its saved data in the keychain, enter your Mac login
   password and choose **Always Allow**. A new version asks again.

Apple silicon and Intel Macs are both supported; the built-in node runs on Apple silicon only.
There are no in-app updates on macOS yet: download new versions from the page.

## iPhone and iPad (preview)

The download is an unsigned `.ipa`. An iPhone installs only signed apps, so sign and install it
with your own Apple ID, using a sideloading tool such as Sideloadly or AltStore. With a free Apple
ID the app stops opening after a while and has to be installed again the same way; the wallet
stays on the phone.

The iPhone app has no Tor.

## Builds without Tor

Every platform also has a file with `-notor` in its name: the same app with Tor left out
completely, for places where Tor is unwanted or blocked.

- It cannot send to Tor (`.onion`) addresses, and has no Tor settings or Tor help.
- It does not update itself: get new versions from the download page.
- It installs over the normal app, and the normal app over it. Wallets and settings stay; Tor
  settings read as off.

## Check a download

Compare the file's SHA-256 with the one on the page:

| System | Command |
| --- | --- |
| Linux | `sha256sum <file>` |
| macOS | `shasum -a 256 <file>` |
| Windows (PowerShell) | `Get-FileHash <file>` |

## Next

[Create your first wallet](first-wallet.md).
