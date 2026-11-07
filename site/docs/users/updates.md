---
title: Updates
description: How each build gets new versions, and how the app checks an update before installing it.
---

# Updates

| Build | How it updates |
| --- | --- |
| Android APK from the download page | in the app: **Settings › About** |
| Windows installer, Linux AppImage | in the app: the sidebar and **Settings › About › Updates** |
| Google Play | Google Play |
| macOS (preview) | in the app: the sidebar and **Settings › About › Updates** |
| iPhone (preview) | download the new version from the page |
| Builds without Tor | in the app, like the builds with Tor |

## In-app updates

The app reads a signed update file published with each release and checks the signature with keys
built into the app before it shows or downloads anything. An unsigned, forged, expired or older
file means "No update information available", and nothing is offered.

The same signed file is published in three places, and the app reads all of them: BT Labs'
download server (`epiccash.btlabs.uk`; with Tor on, its onion address), the GitHub copy of BT Labs'
signed public files, and the latest GitHub release of wallet-for-epic. Each copy is checked against the same keys, and the newest
valid one is used, so one place being down or blocked never stops an update. The file names the
builds with Tor and, in a section of its own, the builds without Tor; each build takes only its own.

- **Android:** the app downloads the APK for the phone, checks its size and SHA-256, and hands it to
  Android's installer, which also insists on the same app, a higher version and the same signing
  key. The first time, Android asks you to allow installs from BT Wallet.
- **Desktop:** when a newer version is out, a slim line above the page says so, with **Update** and
  ×, which closes it for that version; the sidebar says so too. Where the app can install the
  update by itself, a click downloads it, checks it, and offers **Restart to update**; otherwise it
  opens the download page. On Windows, an update that did not finish is offered again at the next
  start. On macOS the app downloads the new disk image, checks it and opens it: drag the app over
  the old one.

Updates keep your wallets and settings.

Epic Cash Mobile, the Android app up to 26.10.24, is offered no update: BT Wallet is a separate
Android app. [Install](install.md#from-epic-cash-desktop-or-epic-cash-mobile) says how to move.

## Versions

The app's version is the year, the month and a patch number: `26.11.4` is a release of November
2026. **Settings › About** shows it together with the version of the wallet core, for example
`26.11.4 · core 0.3.1`. What changed in each version is in the
[changelog](https://epiccash.btlabs.uk/releases/changelog/).
