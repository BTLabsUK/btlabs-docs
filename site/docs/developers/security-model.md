---
title: Security model
description: How LEPIC and the Epic Cash apps protect keys, secrets and wallet data, and what they treat as untrusted.
---

# Security model

This page describes how the wallet protects keys and data, and which inputs it treats as
untrusted. To report a vulnerability, see [Security](../security.md).

## Keys and seeds

The wallet's seed never sits on disk in the clear.

- **The vault.** LEPIC encrypts the seed under the wallet password with XChaCha20-Poly1305, the key
  derived with Argon2id, and writes the result (`lepic.vault`) into a secret store the app provides.
  A password set for a new wallet has at least eight characters.
- **The secret store** is the platform's own:

| Platform | Secret store |
|---|---|
| Android | Android Keystore-backed storage |
| iOS | iOS Keychain, this device only |
| Linux | The Secret Service (GNOME Keyring, KWallet) through libsecret |
| Windows | A DPAPI-encrypted file for the current user |
| `lepic` CLI | A vault file on disk, the same encryption |

- **PIN unlock.** LEPIC generates a random wallet password, seals it under the PIN together with a
  random PIN key that it writes into the secret store, and gives the app only the sealed text. The
  sealed text alone, or with the vault, does not reveal the PIN. A new PIN has at least six
  characters. Failed password and PIN attempts are counted in the store, and after the third
  failure each attempt waits first, longer after each further failure.
- **Recovery phrase.** Shown only after the password or PIN is checked, for the backup screen. It
  is the only way back to the funds if the device is lost.
- **Key paths.** Keys are derived as `epic-wallet` derives them, so a restore from the phrase
  brings back the same Epicbox address, payment-proof key and onion address. See
  [Upstream compatibility](upstream.md).

:::warning
The PIN can be guessed offline, slowed only by Argon2id, by whoever holds both the sealed text
and the secret store's contents. The store is kept on the device and excluded from backups.
:::

## Secrets at the Flutter boundary

The app's interface is Dart; the wallet is Rust. Dart strings cannot be wiped, so every secret
that crosses is deliberate and listed (ADR 0014):

| Direction | What | When |
|---|---|---|
| Dart to Rust | Password, PIN, recovery phrase the user types | Create, open, restore, change password or PIN, phrase check |
| Dart to Rust | Node API secret the user configures | Calls that take a wallet configuration; Rust wipes it on drop |
| Dart to Rust | `wallet.seed` file and its password | Import from `epic-wallet` |
| Rust to Dart | Recovery phrase, after a credential check | Backup screen |
| Rust to the secret store, and back | The PIN key | PIN wallets only |
| Both ways | A pairing invite link and its five pairing words | Show and share only; never stored or logged |
| Never | Seed bytes, private keys, blinding factors, nonces, vault keys, the generated PIN-unlock password | |

Rust copies what it receives into memory it wipes, and wipes its own copies of what it returns.
It cannot wipe the Dart string, so the app passes a typed secret straight from the text field to
the call and clears the field afterwards. Every function of the FFI API is checked against this
list.

## Wallet data at rest

- **Database.** SQLite with a real schema and forward-only migrations.
- **Private transaction context** (blinding factors and nonces of a transaction in progress) is
  sealed with XChaCha20-Poly1305 under a key derived from the wallet's root key. The slate id and
  participant are authenticated as associated data, so a sealed context copied to another row does
  not open.
- **App backups** (`.wfeh` files) are sealed under a key derived from the wallet root inside Rust;
  no key crosses the binding.
- **Logs.** Secret types redact themselves, and a test checks that known secrets never appear in
  captured output. A support bundle keeps only the values of log fields that say nothing about
  keys, amounts or addresses. Field names and rules are in LEPIC's
  [logging guide](https://gitlab.com/btlabs/lepic/-/blob/main/docs/logging.md) *(available soon)*.

## Untrusted input

Everything from the network, a file, a peer, a node or the host app is untrusted.

- **Reject, do not panic.** Bad input becomes a typed error. `unwrap`, `expect`, `panic!`,
  unchecked indexing and unchecked arithmetic are denied by workspace lints outside tests, and
  `unsafe` code is denied. Release builds keep overflow checks on.
- **Bounded work.** Untrusted input may cause only bounded work, and only validated data becomes
  stored state. Frames, files, responses, counts and messages have size limits checked before
  parsing.
- **The node is treated as hostile.** Response sizes are capped and every field is validated.
  Commitments that were not requested or appear twice are refused, as are heights above the tip.
  An output is marked spent only after two answers agree it is missing.
- **Slates.** Decoding is strict: exact hex lengths, valid curve points, bounded counts and sizes.
  Finalize compares every field the sender set with the stored S1 and accepts exactly one added
  output, then validates the whole transaction before storing it. Payment proofs are verified with
  strict ed25519 checks.
- **Fuzzing.** The parsers of slates, Epicbox messages, node responses, vault files and QR codes
  are fuzzed.

## Epicbox

- The relay's signature over each message is verified before anything in the message is parsed,
  and a message must be addressed to this wallet's key.
- **Acknowledge after store.** A message is acknowledged to the relay only after its effect is
  stored, or after it was rejected for good. A crash between receive and store loses nothing: the
  relay delivers it again.
- Inbound processing is idempotent: a redelivered or repeated slate is not a second payment.
- LEPIC notices (non-slate messages about invoices) go only to peers that proved they run LEPIC.

Protocol detail is on the [Epic Cash developer docs](https://devdocs.btlabs.uk).

## Tor

On desktop and Android each open wallet runs its own tor process (ADR 0018). See also the
user guide's [Tor](../users/tor.md) page.

- **Ephemeral onion.** The onion service is added over tor's control port with `ADD_ONION` and
  `DiscardPK`. Its key is derived from the seed in memory, never written to disk and never logged.
  No hidden-service directory exists.
- **Control port** with `SAFECOOKIE` authentication, so the cookie never crosses the connection.
  Tor exits with the wallet process. No shell is involved in starting it.
- **SOCKS by name.** Connections use the SOCKS domain address type, so tor resolves names and no
  DNS query leaves the machine. Each connection uses fresh SOCKS credentials, so it gets a circuit
  of its own.
- **TLS stays end to end.** With Epicbox or the node over Tor, only the byte stream changes: the
  TLS server name and certificate check stay the relay's or node's domain.
- **Nothing unencrypted through an exit.** Plain `http` is refused for any host but loopback and
  `.onion`.

## Contacts, invoices and linked devices

- **Pairing.** Two wallets pair by QR in person, or online with a one-time invite (a link or five
  pairing words), then both sides compare four emoji with their names. Pairing keys come
  from their own branch of the seed and are never the Epicbox, Tor or payment-proof key. See
  [Pairing](../users/pairing.md).
- **Sealed slates.** Between contacts, slates travel in an envelope sealed with HPKE (X25519,
  HKDF-SHA256, ChaCha20-Poly1305) and signed with Ed25519, so only the contact opens it and the
  sender is authenticated.
- **Invoice trust only on paired contacts.** Invoices are accepted only from paired contacts.
  Allowing a contact to send invoices is a per-contact switch, available once the contact is
  verified. An invoice never pays itself: paying needs the user's action and the invoiced amount.
- **Linked devices.** Devices on one wallet exchange notices through a private pairing, sealed in
  HPKE PSK mode. A notice must come through the pairing of a linked device and name that device,
  is size-limited before parsing, deduplicated and applied in order. A notice can hold or release
  coins, add history details or propose servers; it never sends, signs or changes a setting on its
  own. See [Linked devices](../users/linked-devices.md).

:::note
An Epicbox answer to an unknown slate raises an `unknownSlate` event carrying the sender's address
and slate id. Neither is verified, so the event only informs the user; an app never acts on it or
shows that sender as trusted.
:::

## Out of scope

- Weaknesses in the Epic node, `epic-wallet` or the Epicbox relay belong to those projects.
  LEPIC keeps the Epicbox message encryption exactly as `epic-wallet` defines it, for
  compatibility.
- A device that is already compromised, or another process running as the same user. On Windows,
  any process of the same user that reads the app's protection value can open the DPAPI store.
- Slate files, pasted slate text and QR slates are not encrypted unless sealed for a contact:
  whoever sees them can read the slate. See [Privacy](../users/privacy.md).
- Secrets held in Dart memory until the garbage collector reuses it.

## Related pages

- [Security](../security.md): how to report a vulnerability.
- [Architecture decisions](decisions.md): ADR 0014 (secrets), 0018, 0021, 0022 (Tor), 0024
  (pairing).
- [Dependencies](dependencies.md): how dependencies are checked.
