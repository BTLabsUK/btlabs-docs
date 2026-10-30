---
title: Contributing
description: "How to propose a change to the app, LEPIC or lepic-flutter: commit format, sign-off and checks."
---

# Contributing

Contributions to LEPIC, lepic-flutter and the app follow the same rules.

## Before you start

1. Build and run the project: [Build from source](build/index.md) and
   [Dev environment](dev-environment.md).
2. Read [Architecture](architecture.md), [Decisions](decisions.md) and, for security-relevant
   code, [Security model](security-model.md).
3. Check which repository the change belongs in: [LEPIC](https://gitlab.com/epic-cash-bt/lepic)
   for wallet logic, [lepic-flutter](https://gitlab.com/epic-cash-bt/lepic-flutter)
   for the binding, [wallet-for-epic](https://gitlab.com/epic-cash-bt/wallet-for-epic)
   for the app.

## Making a change

- One branch per task, named `<type>/<slug>`, for example `feat/legacy-v3-codec`.
- Each commit holds one logical change. Keep formatting, renames and refactors apart from changes in
  behaviour, and stage files by name.
- Every commit builds and passes the checks below.
- A change to wire formats, keys, proofs or storage needs golden vectors; see
  [Testing](testing.md#golden-vectors).
- Logs never contain secrets.

## Checks

LEPIC, from a git checkout:

```bash
cargo xtask check
```

The app:

```bash
cd app
flutter analyze
flutter test
```

`tools/check.sh` runs the full app gate. See [Testing](testing.md).

## Commit messages

Commits follow Conventional Commits:

```text
<type>(<scope>)[!]: <description>

<body: what changed and why, wrapped at 72 columns>

BREAKING CHANGE: <what breaks and how to migrate>
Signed-off-by: Full Name <email>
```

- Types: `feat`, `fix`, `perf`, `refactor`, `test`, `docs`, `build`, `ci`, `chore`, `revert`.
- LEPIC scopes: `primitives`, `crypto`, `keychain`, `slate`, `contact`, `node`, `store`,
  `transport`, `epicbox`, `wallet`, `telemetry`, `ffi`, `cli`, `xtask`, `conformance`, `fuzz`,
  `interop`, `deps`, `ci`, `docs`, `repo`. Leave the scope out only when a change spans the whole
  repository.
- Description: imperative mood, lowercase first word, no trailing period. The subject line is at
  most 72 characters.
- Body: why the change exists and what it affects, including any effect on wire formats, stored
  data or the public API. A breaking change gets `!` after the scope and a `BREAKING CHANGE:`
  footer.
- Describe the correction, never an attack. No exploit detail.

### Commit-message hook

LEPIC ships a `commit-msg` hook that rejects malformed messages. Enable it once per clone:

```bash
git config core.hooksPath .githooks
```

CI runs the same check, so a skipped hook only moves the failure later.

## Sign-off

Add a sign-off to every commit with `git commit -s`. It certifies the
[Developer Certificate of Origin 1.1](https://developercertificate.org/): you wrote the change or
have the right to submit it under the project license (Apache License 2.0).

## Security issues

Do not open a public issue for a vulnerability. Send it privately to support@btlabs.uk; see
[Security](../security.md).
