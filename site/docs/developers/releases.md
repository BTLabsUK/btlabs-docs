---
title: Releases
description: How the app and LEPIC are versioned and what cutting a release involves.
---

# Releases

## Versioning

**The app** (Epic Cash Desktop and Epic Cash Mobile share one version) uses calendar versions,
`YY.MM.patch`:

- `YY.MM` is the year and month of the release. A new month's release is `YY.MM.0`.
- A fix to an earlier release raises that release's patch: `26.10.0` becomes `26.10.1`.
- A test build may carry `-rcN`, for example `26.10.1-rc1`. It never reaches the update channel.

**LEPIC** uses Semantic Versioning, `MAJOR.MINOR.PATCH`, independent of the app. While the version
is `0.y.z`, a minor bump means a breaking change. The app shows the LEPIC version at its pin, for
example `26.10.0 · core 0.1.0`.

The version lives in one place, `version:` in `app/pubspec.yaml`, and only `tools/version.sh set`
writes it. Everything else is derived.

## Platform numbers

| Platform | Number | 26.10.0 | 26.10.1 |
| --- | --- | --- | --- |
| Build number | `YY·1000000 + MM·10000 + patch·100 + rebuild` | `26100000` | `26100100` |
| Android | versionName `YY.MM.patch`, versionCode = build number | `26100000` | `26100100` |
| Windows | file and installer version `YY.MM.patch.0` | `26.10.0.0` | `26.10.1.0` |
| Linux | `EpicCashDesktop-YY.MM.patch-x86_64.AppImage` | `26.10.0` | `26.10.1` |
| iOS | `YY.MM.patch` | `26.10.0` | `26.10.1` |

`rebuild` (0 to 99, normally 0) numbers a second build of the same version:
`tools/version.sh set 26.10.0 1` gives `26100001`.

Windows version fields hold at most 65535, so the build number never goes there.

## Version commands

```bash
tools/version.sh show             # the numbers per platform
tools/version.sh check            # every place agrees with pubspec.yaml; exit 1 on drift
tools/version.sh set 26.10.1      # set a release version
tools/version.sh set 26.10.1-rc1  # set a test build
tools/version.sh core             # write the LEPIC version from the pin
```

`tools/check.sh` runs the check, and `app/test/version_test.dart` fails when the Dart side drifts.
After moving the LEPIC pin, run `tools/version.sh core`.

## Steps of a release

1. Set the version: `tools/version.sh set YY.MM.patch`. It writes `app/pubspec.yaml` and
   `app/lib/src/app_version.dart`, then runs the check. Commit the change.
2. Run `tools/version.sh check` and `tools/check.sh`.
3. Build each platform. Every script reads the version from `app/pubspec.yaml`:
   - `app/tool/build_android_release.sh`, see [Android](build/android.md)
   - `scripts/build-linux.sh`, see [Linux](build/linux.md)
   - `app\tool\build_windows_release.ps1`, see [Windows](build/windows.md)
4. Run the [release checks](testing.md#release-check).
5. Upload the builds to the download location, then write the signed update manifest with
   `app/tool/release_android.sh <download-base-url> "notes"`. Set `WFE_DESKTOP_RELEASE=1` when
   desktop builds ship in the same release.
6. Publish the signed `update.json` to every source the apps read with
   `tools/publish-update-json.sh <signed update.json>`: BT Labs' download server, the GitHub copy
   of the signed public files (`github.com/BTLabsUK/btlabs-epic.github.io`, read as the raw
   file on `main`) and the GitHub release
   (`github.com/BTLabsUK/wallet-for-epic/releases/latest/download/update-v2.json`), in that order (`updateManifestSources` in
   `app/lib/src/updater.dart`). The apps check all of them and use the valid copy with the higher
   serial; a source that is down, private or flagged is skipped.
7. Tag the release commit, for example `git tag -a v26.10.0 -m "Epic Cash 26.10.0"`.

## The update manifest

The in-app updater reads a signed `update.json`. `release_android.sh` writes the unsigned payload
and signs it when the signing key is available. The manifest schema takes plain `X.Y.Z` versions
only, so a test build (`-rcN`) is refused. See [Security model](security-model.md).

An update installs on Android only when its version code is higher and it is signed with the same
key as the installed app.
