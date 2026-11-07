---
title: Install
description: Download and install BT Wallet on each platform.
---

# Install

Every release is on the download page:
**[epiccash.btlabs.uk/releases](https://epiccash.btlabs.uk/releases/)**.
Each file has its SHA-256 checksum under it, and `SHA256SUMS` sits next to the files.

| Device | Needs |
| --- | --- |
| Windows | Windows 10 or 11, 64-bit |
| Linux | x86-64, Ubuntu 22.04 or newer |
| Android | Android 7 or newer, arm64 |
| macOS (preview) | macOS 12 or newer, Apple silicon |
| iPhone, iPad (preview) | iOS 15 or newer |

Coming from Epic Cash Desktop or Epic Cash Mobile, the app's names up to 26.10.24? See
[From Epic Cash Desktop or Epic Cash Mobile](#from-epic-cash-desktop-or-epic-cash-mobile).

## Windows

1. Download `bt-wallet-<version>-windows-x64-setup.exe`.
2. Run it. It installs for your user only; no administrator rights are needed.

Windows may warn that the publisher is unknown. Check the checksum, then choose to run it.

## Linux

1. Download `bt-wallet-<version>-linux-x86_64.AppImage`.
2. Allow it to run, either way:
   - In the file manager: right-click the file › Properties › Permissions › tick
     **Allow executing file as program**, then double-click it.
   - In a terminal, from the download folder (put in the version you downloaded):

     ```bash
     chmod +x bt-wallet-26.11.4-linux-x86_64.AppImage
     ./bt-wallet-26.11.4-linux-x86_64.AppImage
     ```

The AppImage needs `fusermount3`, which default Ubuntu desktops have. Without FUSE, start it with
`--appimage-extract-and-run`. It also uses GTK 3, `libsecret` and OpenGL from the system, which
desktop installs have.

## Android

1. Download `bt-wallet-<version>-android-arm64-v8a.apk` on the phone.
2. Open the file. Allow installs from this source when Android asks.

A newer APK installs over an older one and keeps the wallets.

**Google Play:** BT Wallet is in testing on Google Play. The store page will be linked here
when it opens to everyone. The Play build and the APK are the same app with the same app data,
so a phone can move between them without a restore.

## macOS (preview)

1. Download `bt-wallet-<version>-macos.dmg`.
2. Open it, drag **BT Wallet** to Applications and open it. The disk image and the app are signed
   by BT LABS and notarised by Apple.
3. When macOS asks whether the app may use its saved data in the keychain, enter your Mac login
   password and choose **Always Allow**.

The app runs on Macs with Apple silicon (M1 or newer); an Intel Mac cannot run it. It checks for
updates and opens the new disk image; drag the app over the old one.

## iPhone and iPad (preview)

The download is an unsigned `.ipa`. An iPhone installs only signed apps, so sign and install it
with your own Apple ID, using a sideloading tool such as Sideloadly or AltStore. With a free Apple
ID the app stops opening after a while and has to be installed again the same way; the wallet
stays on the phone.

The iPhone app has no Tor.

## From Epic Cash Desktop or Epic Cash Mobile

Up to 26.10.24 the app was called Epic Cash Desktop on computers and Epic Cash Mobile on phones.
It is the same wallet; what to do depends on the device.

- **Windows, Linux:** install BT Wallet over the old app, or let the old app update itself. The
  wallets and settings stay. On Windows the old shortcuts are replaced by **BT Wallet**.
- **macOS:** drag BT Wallet to Applications. The wallets and settings stay. On its first start
  BT Wallet offers to move the old **Epic Cash Desktop** to the Bin.
- **Android:** BT Wallet is a new app. It installs beside Epic Cash Mobile and starts empty, and
  Epic Cash Mobile is offered no update. Restore each wallet in BT Wallet from its
  [recovery phrase](restore.md), import its [wallet data file](backups.md#export-wallet-data) if
  you have one, then uninstall Epic Cash Mobile, so that two apps never use one Epicbox address.

## Builds without Tor

Every platform also has a file with `-notor` in its name: the same app with Tor left out
completely, for places where Tor is unwanted or blocked.

- It cannot send to Tor (`.onion`) addresses, and has no Tor settings or Tor help.
- It updates itself like the normal app (**Settings › About**).
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
