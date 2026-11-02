---
title: Report a security issue
description: How to report a vulnerability in Epic Cash Desktop, Epic Cash Mobile, LEPIC or lepic-flutter.
---

# Report a security issue

Write to **support@btlabs.uk**. Do not open a public issue for a vulnerability.

Include:

- the app or library and its version or commit (the app's version is in **Settings › About**);
- what an attacker controls;
- what happens;
- the smallest reproduction you have.

Never send a recovery phrase, a wallet file of a wallet with funds, or a password. A wallet with no funds,
or a very small amount, is enough to show almost anything.

## In scope

Anything in Epic Cash Desktop, Epic Cash Mobile, LEPIC or lepic-flutter that can:

- lose or lock funds;
- leak keys, the recovery phrase or wallet data;
- make the wallet accept an invalid transaction;
- crash it from untrusted input: node responses, Epicbox messages, slates, files, QR codes.

## Out of scope

Issues in the Epic Cash node, the reference `epic-wallet` or the Epicbox relay belong to those
projects. If you find one through these apps, report it to them privately and tell us only what we
need to protect our users.

## Supported versions

The apps and LEPIC are pre-1.0. Only the latest release receives fixes.

How the wallet protects keys and handles untrusted input is described in the
[Security model](developers/security-model.md).
