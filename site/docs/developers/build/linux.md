---
title: Build for Linux
description: Build the BT Wallet AppImage in an Ubuntu 22.04 container.
---

# Build for Linux

```bash
scripts/build-linux.sh
```

The output is `build-linux/bt-wallet-<version>-linux-x86_64.AppImage`.

Linux release builds always run in an Ubuntu 22.04 container, never on the host. A binary needs the
glibc it was linked against, so building on the oldest supported system gives an app that starts on
22.04 and on every newer one.

## Needs

- Docker.
- `git`, `rsync` and `tar` on the host.
- `curl` and `jq` on the host, unless you build without Tor: the script fetches the Tor bundle there
  (`tools/fetch-tor.sh`).
- Nothing else for LEPIC and lepic-flutter. The script reads each pinned commit from `LEPIC_REPO`
  or `LEPIC_FLUTTER_REPO` when set, else from `$HOME/lepic` or `$HOME/lepic-flutter` when it has
  the commit, else from GitHub (see [Build from source](index.md)).

## What it does

1. Exports LEPIC at `tools/lepic.rev` and lepic-flutter at `tools/lepic-flutter.rev` into a cache
   folder outside the repository, and checks that the two pins agree.
2. Builds the container image from `scripts/linux/Dockerfile`.
3. Copies a snapshot of the committed tree into a work folder, so the build never touches
   `app/build` or `.dart_tool`.
4. In the container: builds LEPIC (`cargo xtask mobile --package`), runs
   `flutter build linux --release`, and packs the AppImage.

## Switches

| Variable | Effect |
| --- | --- |
| `WFE_WORKTREE=1` | Build the working tree, uncommitted changes included, instead of `HEAD`. The build id gets `-dirty` when the tree has changes. |
| `WFE_TOR=0` | Build without Tor; see [Build variants](variants.md). |
| `WFE_TARGET` | Flutter entry point. Default `lib/main_desktop.dart`. |
| `WFE_NODE_BIN` | Path to an `epic` node binary to bundle as the built-in node. |
| `WFE_BUILD_LEPIC=0` | Skip the LEPIC build and use the library already in `native/`. |
| `LEPIC_REPO`, `LEPIC_FLUTTER_REPO` | Where the pinned commits are read from. |

Extra arguments are passed on to `flutter build linux`.

## Toolchain pins

- Ubuntu 22.04 base image, `scripts/linux/Dockerfile`.
- Flutter: `scripts/linux/flutter.version` (currently 3.47.5).
- Rust: the `channel` in LEPIC's `rust-toolchain.toml`, passed to the image as `RUST_VERSION`.
- appimagetool 1.9.1 with the type2 runtime 20251108, both checked against pinned SHA-256 sums.

Build caches are Docker volumes named `wfe-linux-pub`, `wfe-linux-cargo`, `wfe-linux-home`,
`wfe-linux-build`, and `wfe-linux-lepic-target` (`wfe-linux-lepic-target-notor` without Tor).

## Running the AppImage

The AppImage runtime is a static binary with libfuse3 built in. It needs no `libfuse2`, only a
`fusermount3` helper, which a default Ubuntu desktop has. Without FUSE:

```bash
./bt-wallet-<version>-linux-x86_64.AppImage --appimage-extract-and-run
```

glibc, GTK and the other system libraries are not bundled. The system must provide GTK 3,
`libsecret-1-0` and libEGL/GL (Mesa). A minimal container lacks `libsecret` and libEGL.

The app keeps its data in `~/.epic_cash_desktop`. For install steps for users, see
[Install](../../users/install.md).
