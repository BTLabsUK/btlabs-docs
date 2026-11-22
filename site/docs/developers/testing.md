---
title: Testing
description: How to run the app's checks and LEPIC's check, golden vector, conformance, interop, fuzz and binding tests.
---

# Testing

## The app

Two commands. `tools/t` runs the Flutter tests, `tools/check.sh` is the gate for the code. Source
`tools/env.sh` first.

```bash
tools/t                        # the tests your change reaches, plus a fixed set of sentinel tests
tools/t --list                 # the selection and why; runs nothing
tools/t full                   # every test file
tools/check.sh                 # the fast gate
tools/check.sh --list          # what the gate would run; runs nothing
tools/check.sh --full          # everything
```

`tools/t` skips a file that passed with the same inputs; `--no-cache` runs it anyway. It exits 0 when
green, 1 when a test failed and 2 on a usage or infrastructure error. Results are in
`.test-results/latest.json`.

`tools/check.sh` runs these steps. A failed step does not stop the run: the check ends with exit 1
and names every step that failed.

1. `tools/version.sh check`: every version number agrees with `app/pubspec.yaml`.
2. The install contract, UI targets, no hosts in code, document names and the workflow files.
3. The bot's tests and the release tools' tests, when those folders changed.
4. LEPIC at the pin.
5. `dart run bin/core_check.dart`: the wallet core under plain Dart, with no Flutter.
6. `flutter analyze`.
7. `tools/t affected`.

`--full` always runs the bot's and release tools' tests, and adds LEPIC's golden vectors. It runs
`tools/t full --no-cache` in place of step 7, then the integration tests `simple_test` and
`history_test` on Linux under `xvfb-run`, and the web build (`tool/build_web.sh`). The runner's options
are in the header of [`tools/t`](https://github.com/BTLabsUK/wallet-for-epic/blob/main/tools/t).

### Single tests and variants

```bash
tools/t file app/test/amount_test.dart
tools/t file app/test/tor_build_test.dart --dart-define WFE_TOR=false
cd app && xvfb-run -a flutter test -d linux integration_test/simple_test.dart
```

Run integration tests one file per command. They need an unlocked keyring (`tools/check.sh` starts
one with `dbus-run-session` and `gnome-keyring-daemon --unlock`). Tor-specific tests are skipped in a build without Tor;
run a set both ways when you touch Tor code. For the switch, see [Build variants](build/variants.md).

### Screenshot tours

`app/tool/screenshot_tour_test.dart` renders a tour of the screens. It is a test file, run with
`flutter test tool/screenshot_tour_test.dart`; `--dart-define=TOUR_LOCALE=de` picks a language.

## LEPIC

```bash
cargo xtask check
```

This is the gate every LEPIC commit passes. Run it from a git checkout with `cargo-nextest` and
`cargo-deny` installed. The first run needs network access, because it fetches the lockfiles of
`conformance/`, `fuzz/` and `interop/probe/`. It stops at the first failing step:

1. `cargo fmt --check`
2. `cargo clippy --workspace --all-targets --locked`, warnings denied
3. the same clippy for `lepic-ffi` without its default features (the build without Tor)
4. `cargo nextest run --workspace --locked`
5. `cargo test --workspace --doc --locked`: the doctests, which nextest does not run
6. `cargo deny check`
7. `deps-check`: crate edges and banned crates against the architecture
8. `legacy-imports`: the legacy lane depends on no native crate
9. `ci-lint`: workflow pins, read-only token permissions and checkout credentials
10. `repo-lint`: workspace lints, unsafe code, pure crates, the vendored library, the bridge
    fingerprint and interop images
11. the lockfile checks for `conformance/`, `fuzz/` and `interop/probe/`
12. `vectors verify`
13. `no-legacy`: the crates that build without the legacy formats

Each gate also runs alone, for example `cargo xtask vectors verify` or `cargo xtask repo-lint`.
CI runs `cargo xtask check`, the fuzz build (`cargo xtask fuzz --build`), `cargo xtask ci-lint`
with `actionlint`, `cargo test --locked` in `conformance/`, and the mobile library builds. The
interop scenarios run against live nodes and wallets, outside CI.

### Golden vectors

Slates, keys, signatures, Epicbox messages and stored data are checked byte for byte against JSON
files in `testdata/vectors/<area>/`. The pinned reference code in `conformance/` writes them.
`cargo xtask vectors verify` replays the stored vectors without the reference code;
`cargo xtask vectors generate [--area <area>]` regenerates them. A change to a wire format, key,
proof or storage layout comes with its vectors.

### Conformance

`conformance/` is a workspace of its own, with a `vectors` member that generates the vectors and a
`differential` member that runs the reference code and LEPIC on the same inputs. It builds the
reference node and wallet, which need CMake, a C++ compiler, libclang and the OpenSSL headers, so
they never enter LEPIC's dependency graph.

```bash
cd conformance
cargo test --locked
cd ..
cargo xtask soak --iterations 100 --seed 1   # randomized differential runs
```

Each soak iteration runs one seeded scenario against the reference wallet. Iteration `i` uses
seed `seed + i`, so `--iterations 1 --seed <seed>` replays one failure.

### Interop suite

```bash
interop/run.sh            # build, start a clean stack, run every scenario, tear it down
interop/run.sh --keep     # leave the stack running
interop/run.sh --no-build # reuse the binaries already built
```

It runs `lepic` against an unmodified reference node, `epic-wallet` and Epicbox relay at the pinned
commits, on a Docker private network with no route out and a local test chain. It needs Docker
with the Compose plugin, `git`, `jq`, `bash` and `python3` with its `sqlite3` module. The first
run compiles the reference programs from source. It exits 0 only when every scenario passed. The
scenarios cover sends, receives and invoices in both directions over Epicbox, files and http,
relay restarts, repeated messages, cancel and history import. Each is driven with
`lepic --output json`.

`interop/acceptance/run.sh` runs the acceptance steps against the installed `lepic`;
`--stack-only` starts a clean stack and keeps it, so you can try the CLI by hand. The `interop/`
READMEs in the
[LEPIC repository](https://github.com/BTLabsUK/lepic/blob/main/interop/README.md) list every
scenario and option.

### Fuzzing

```bash
cargo xtask fuzz --build                   # build the targets only
cargo xtask fuzz --smoke                   # every target for 60 seconds
cargo xtask fuzz --smoke --target tx_decode
cargo xtask fuzz --full --jobs 4           # every target for 10 minutes, four at a time
```

There are 32 targets, among them `tx_decode`, `slate_v3`, `epicbox_message` and `foreign_rpc`.
Fuzzing uses the pinned nightly Rust in `fuzz/rust-toolchain.toml` and `cargo-fuzz`. A target may
use up to 2.5 GB of memory, so keep `--jobs` within the machine's memory. See
[docs/fuzzing.md](https://github.com/BTLabsUK/lepic/blob/main/docs/fuzzing.md).

### Upstream drift

```bash
cargo xtask upstream-drift
```

Lists commits in the reference node and wallet that touched code LEPIC ports, after the commits
recorded in `upstream.toml`. It exits with code 2 when it finds any. A scheduled CI workflow runs
it and the advisory check.

### Size and speed budgets

`cargo xtask budget` measures the size of the library per mobile target and the time and memory of
a restore, a store workload and an Epicbox drain, and fails when one is over its limit. It is not
part of `cargo xtask check`; see
[docs/budgets.md](https://github.com/BTLabsUK/lepic/blob/main/docs/budgets.md).

## The binding

In the lepic-flutter repository:

```bash
tool/lepic.sh test           # flutter test against a scripted-node library
tool/lepic.sh check          # both bridge halves match the pinned LEPIC
```

`tool/lepic.sh test` builds `lepic-ffi` with the `mock` feature (a scripted node and relay), then
runs `flutter test`. Run it on x86_64 Linux. `tool/lepic.sh emulator-test [<serial>]` runs the
device test app on an attached Android device. See [lepic-flutter](lepic-flutter.md#tests).
