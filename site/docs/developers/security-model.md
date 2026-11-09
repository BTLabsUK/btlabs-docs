---
title: Security model
description: How LEPIC and BT Wallet protect keys, secrets and wallet data, and what they treat as untrusted.
---

# Security model

This page describes how the wallet protects keys and data, and which inputs it treats as
untrusted. To report a vulnerability, see [Security](../security.md).

## Keys and seeds

The wallet's seed never sits on disk in the clear.

- **The vault.** LEPIC encrypts the seed under the wallet password with XChaCha20-Poly1305, the key
  derived with Argon2id, and writes the result (`lepic.vault`) into a secret store the app provides.
  LEPIC checks no password length; the app sets its own rule (ADR 0036).
- **The secret store** is the platform's own:

| Platform | Secret store |
|---|---|
| Android | Android Keystore-backed storage |
| iOS | iOS Keychain, this device only |
| Linux | The Secret Service (GNOME Keyring, KWallet) through libsecret |
| macOS | The login keychain |
| Windows | A DPAPI-encrypted file for the current user |
| `lepic` CLI | A vault file on disk, the same encryption |

- **PIN unlock.** LEPIC generates a random wallet password, seals it under the PIN together with a
  random PIN key that it writes into the secret store, and gives the app only the sealed text. A
  PIN has at least six characters by default. Failed password and PIN attempts are counted in the store. After three failures each
  attempt waits first: 30 seconds, doubling with each further failure, to at most one hour. These
  are LEPIC's defaults (`PinSettings`).
- **Recovery phrase.** Shown only after the password or PIN is checked, for the backup screen. It
  is the only way back to the funds if the device is lost.
- **Key paths.** The Epicbox address is derived as `epic-wallet` derives it. The onion address has
  its own key, derived from the seed under a label of its own (ADR 0044). A restore from the phrase
  brings back both. See [Upstream compatibility](upstream.md).

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
the call and clears the field afterwards. LEPIC's rules let only what ADR 0014 lists cross the
boundary.

## Wallet data at rest

- **Database.** SQLite with forward-only schema migrations. The database file and its write-ahead
  log are encrypted page by page with SQLite3 Multiple Ciphers: every 4 KiB page is sealed with
  ChaCha20-Poly1305 under a key derived from the seed (`wallet.enc.sqlite3`). The key stays in
  Rust, so a password or PIN change does not re-key the file. A wrong key or an altered page reads
  as "not a database" (ADR 0032). File sizes and change times stay visible.
- **Files.** On Unix the database and its key check file are created with mode 0600. Temporary
  tables and sorts stay in memory.
- **Private transaction context** (blinding factors and nonces of a transaction in progress) is
  sealed with XChaCha20-Poly1305 under a key derived from the wallet's root key. The slate id and
  participant are authenticated as associated data, so a sealed context copied to another row does
  not open.
- **App backups** (`.wfeh` files) are sealed under a key derived from the wallet root inside Rust;
  no key crosses the binding.
- **Logs.** Secret types redact themselves, and a test checks that known secrets never appear in
  captured output. A support bundle keeps only the values of log fields that say nothing about
  keys, amounts or addresses. Field names and rules are in LEPIC's
  [logging guide](https://github.com/BTLabsUK/lepic/blob/main/docs/logging.md).

## Untrusted input

Everything from the network, a file, a peer, a node or the host app is untrusted.

- **Reject, do not panic.** Bad input becomes a typed error. `unwrap`, `expect`, `panic!`,
  unchecked indexing and unchecked arithmetic are denied by workspace lints outside tests, and
  `unsafe` code is denied, except in the glue `flutter_rust_bridge` generates and one call that
  sets the store's key. Release builds keep overflow checks on.
- **Bounded work.** Untrusted input may cause only bounded work, and only validated data becomes
  stored state. Frames, files, responses, counts and messages have size limits checked before
  parsing.
- **The node is treated as hostile.** Response sizes are capped (8 MiB) and every field is
  validated. Commitments that were not requested or appear twice are refused, as are heights above
  the tip. An output the node does not hold is marked spent only after a second request misses it
  too.
- **Slates.** Decoding is strict: exact hex lengths, valid curve points, bounded counts and sizes.
  Finalize compares the fields the sender set with the stored S1 and validates the whole
  transaction before storing it. Payment proof signatures are verified with strict ed25519
  checks.
- **Fuzzing.** The parsers of slates, Epicbox messages, node responses, vault files and QR codes
  are fuzzed.

## Epicbox

- The relay's signature over each message is verified before anything in the message is parsed,
  and a message must be addressed to this wallet's key.
- **Acknowledge after store.** A message is acknowledged to the relay only after its effect is
  stored, or after it was rejected for good. A crash between receive and store loses nothing: the
  relay delivers it again.
- LEPIC notices (JSON messages about declined, withdrawn, posted and cancelled transactions) go
  only to a peer proven to run LEPIC (ADR 0016).

The message format is in LEPIC's
[Epicbox protocol page](https://github.com/BTLabsUK/lepic/blob/main/docs/protocols/epicbox.md).

## Tor

On desktop and Android each open wallet runs its own tor process (ADR 0018). See also the
user guide's [Tor](../users/tor.md) page.

- **Ephemeral onion.** The onion service is added over tor's control port with `ADD_ONION
  ED25519-V3` and the `DiscardPK` flag. Its key is derived from the seed in memory, never written to disk and never logged.
  No hidden-service directory exists.
- **Control port** with `SAFECOOKIE` authentication, so the cookie never crosses the connection.
  Tor exits with the wallet process. No shell is involved in starting it.
- **SOCKS by name.** Connections use the SOCKS domain address type, so tor resolves names and no
  DNS query leaves the machine. Each connection uses fresh SOCKS credentials, so it gets a circuit
  of its own.
- **TLS stays end to end.** With Epicbox or the node over Tor, only the byte stream changes: the
  TLS server name and certificate check stay the relay's or node's domain.
- **Nothing unencrypted through an exit.** LEPIC refuses a plain `http` node for any host but
  loopback and an onion address reached through Tor (ADR 0006). While Tor is on, the app's plain
  `http://` sends to another device are off.

## Contacts, invoices and linked devices

- **Pairing.** There is one pairing flow: a QR code, or a one-time invite (a link or five pairing
  words). Then both sides compare four emoji with their names. Pairing keys come from their own
  branch of the seed and are never the Epicbox, Tor or payment-proof key. See
  [Pairing](../users/pairing.md).
- **Profile.** A wallet's profile travels in the feature word of its pairing messages, to paired
  contacts only, and grants nothing (ADR 0041).
- **Domain proof.** A contact can claim a domain. The domain's key signs the pairing's signing key,
  and the app checks that against `https://<domain>/.well-known/epic-wallet.json`, over HTTPS with
  no redirects, through the wallet's network setting (ADR 0043). A proven domain leaves the meaning
  of "verified" unchanged.
- **Relay moves.** LEPIC reports a contact's relay move and the app decides (ADR 0039). BT Wallet
  follows a move to a public host on its own and shows it on the contact page. A contact with a
  proven domain or a BT Labs key asks first: the user accepts or refuses.
- **Sealed slates.** Between contacts, slates travel in an envelope sealed with HPKE (X25519,
  HKDF-SHA256, ChaCha20-Poly1305) and signed with Ed25519, so only the contact opens it and the
  sender is authenticated.
- **Invoices.** A wallet accepts an invoice only from a verified, paired contact the user allowed,
  through that contact's mailbox, sealed and signed by that contact. **Allow invoices** is a
  per-contact switch on the paying side, off by default, available once the contact is verified.
  An invoice never pays itself: paying needs the user's action and the invoiced amount.
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
- [Threat model](https://github.com/BTLabsUK/wallet-for-epic/blob/main/THREAT_MODEL.md) of the app.
- [Architecture decisions](decisions.md): ADR 0014 (secrets), 0018, 0021, 0022 (Tor), 0024
  (pairing), 0032 (database), 0039 (relay moves), 0041 (profile), 0043 (domain proof), 0044 (onion
  key).
- [Dependencies](dependencies.md): how dependencies are checked.
