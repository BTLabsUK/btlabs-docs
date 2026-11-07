---
title: Releases
description: How the app and LEPIC are versioned and what cutting a release involves.
---

# Releases

## Versioning

**The app** (BT Wallet, one version on every platform) uses calendar versions,
`YY.MM.patch`:

- `YY.MM` is the year and month of the release. A new month's release is `YY.MM.0`.
- A fix to an earlier release raises that release's patch: `26.10.0` becomes `26.10.1`.
- A test build may carry `-rcN`, for example `26.10.1-rc1`. It never reaches the update channel.

**LEPIC** uses Semantic Versioning, `MAJOR.MINOR.PATCH`, independent of the app. While the version
is `0.y.z`, a minor bump means a breaking change. The app shows the LEPIC version at its pin, for
example `26.11.4 · core 0.3.1`.

The version lives in one place, `version:` in `app/pubspec.yaml`, and only `tools/version.sh set`
writes it. Everything else is derived.

## Platform numbers

| Platform | Number | 26.10.0 | 26.10.1 |
| --- | --- | --- | --- |
| Build number | `YY·1000000 + MM·10000 + patch·100 + rebuild` | `26100000` | `26100100` |
| Android | versionName `YY.MM.patch`, versionCode = build number | `26100000` | `26100100` |
| Windows | file and installer version `YY.MM.patch.0` | `26.10.0.0` | `26.10.1.0` |
| Linux | `bt-wallet-YY.MM.patch-linux-x86_64.AppImage` | `26.10.0` | `26.10.1` |
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

A release goes through `tools/rel`, the release runner, from the main checkout. It builds every
platform from one commit, checks the files and the update path, stops for approval, and publishes
in a fixed order.

```bash
tools/rel flow                          # the stages in order
tools/rel cut --version 26.11.0         # make release/26.11.0 with the version commit
tools/rel plan 26.11.0 --commit <tip>   # what will run; changes nothing
tools/rel start 26.11.0 --commit <tip>  # checks and builds; stops at the publish gate
tools/rel resume --publish              # publish after approval
```

1. `cut` makes `release/<version>` from the newest commit whose checks passed and commits the
   version there, in `app/pubspec.yaml` and `app/lib/src/app_version.dart`.
2. `start` runs the source check, `tools/check.sh --full`, or reuses its result for the same
   commit. Then it builds every platform, with Tor and without, signs Android and checks the
   files. The builds use the scripts in [Build from source](build/index.md).
3. The update check installs the release files and updates the previous release to this one.
4. The run stops at the publish gate until the release is approved.
5. `resume --publish` tags the release as `v<version>`, then publishes the downloads, the page, the
   source and the GitHub release. The signed manifests go last, and the run reads them back from
   the live sources.

`tools/rel flow` lists every stage and what it depends on.

## The update manifest

The in-app updater reads a signed `update-v2.json`. Each release also writes `update.json`, the
same release and serial in the old format, for installs up to 26.10.23.
`app/tool/release_android.sh` writes the unsigned payload and signs it when a signing key or the
release signer is available. `tools/publish-update-json.sh` publishes both.

The app reads the sources in `[updates] manifests` of `app/assets/config/app-config.toml`: BT Labs'
download server, the GitHub copy of the signed public files
(`github.com/BTLabsUK/btlabs-epic.github.io`) and the latest GitHub release, in that order
(`updateManifestSources` in `app/lib/src/updater.dart`). It checks every copy against the same keys
and uses the valid copy with the highest serial, the first source on a tie.

The manifest schema takes plain `X.Y.Z` versions only, so a test build (`-rcN`) is refused.

An update installs on Android only when its version code is higher and it is signed with the same
key as the installed app.
