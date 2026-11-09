---
title: Architecture decisions
description: What each of LEPIC's architecture decision records (ADRs 0001 to 0052) decides, grouped by theme.
---

# Architecture decisions

LEPIC records each design decision as an architecture decision record (ADR): the context, the
decision and its consequences. This page states what each record decides, as it holds in the code.
The records are in
[docs/adr](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/README.md); each entry below links
its record. The numbers are fixed, and a record keeps its number and file name.

## Status

| Status | Meaning |
|---|---|
| accepted | The decision holds in the code |
| proposed | The design is in the code; accepting the record is the project owner's decision (`docs/direction.md`) |
| superseded | Another record replaced it, in whole or in part; the record says which part |

ADRs 0012, 0024, 0033, 0034, 0045 and 0050 are proposed. Nine accepted records name a part that a
later record replaced: 0003, 0005, 0007, 0009, 0011, 0018, 0020, 0027 and 0046. Each entry below
says which.

A dependency edge between crates that the architecture page does not list needs an ADR. Where an ADR and the golden vectors or the code
disagree about a format or behaviour, the vectors and the code win.

## Foundations

- **[0001](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0001-port-not-depend.md) Port, do not depend** (*accepted*). LEPIC ports the behaviour it needs from the Epic node and `epic-wallet` into its own crates. `Cargo.lock` holds no `epic_*` package. `upstream.toml` lists each ported module and the upstream paths it follows. The one Epic-origin library it links is `grin_secp256k1zkp`, vendored in `third_party/`.

- **[0006](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0006-tls-and-http.md) TLS and HTTP** (*accepted*). TLS is rustls with the `ring` provider, checked against the `webpki-roots` roots. HTTP is `hyper` 1.x, HTTP/1.1 only, and websockets use `tokio-tungstenite` with the handshake feature only. The node client accepts a plain `http` URL only for a loopback host, or for an onion address when the connection runs through Tor; any other fails with `PlainHttpToRemoteHost`. Node answers are limited to 8 MiB.

- **[0010](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0010-dependency-policy.md) Dependency and toolchain policy** (*accepted*). The toolchain and dependency versions are set once, in the workspace. `deny.toml` checks advisories, licences, sources and a list of banned crates. The release profile uses `opt-level = "s"`, fat LTO, one codegen unit, stripped symbols and overflow checks. See [Dependencies](dependencies.md).

- **[0011](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0011-no-global-state.md) No process-global state** (*accepted*). The network, runtime, clock, randomness and paths are passed in. The only statics are the secp256k1 context, a Windows SID cache and a mutex in the CLI's password change. Several wallets on different networks can run in one process. The contents of `ChainParams`: see ADR 0013.

- **[0013](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0013-network-parameters.md) Network parameters live with the format that uses them** (*accepted*). `lepic-primitives` defines `Network` (`Mainnet`, `Floonet`) and `ChainParams` with the consensus values, among them a coinbase maturity of 1,440 blocks on mainnet and 30 on floonet. Each format crate maps the network to its own version bytes.

- **[0008](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0008-logging-and-errors.md) Logging and errors** (*accepted*). Libraries emit `tracing` events and install no subscriber. The host installs one (`CliTelemetry` in the CLI, `HostLayer` and `LogRing` for the binding). Errors are typed per crate.

- **[0030](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0030-all-configuration-in-settings-toml.md) All configuration in settings.toml** (*accepted*). No host, URL, port or timeout sits in code. The CLI reads `settings.toml`, created from `settings.default.toml`, and a compiled-in `lepic-config.toml`. A host app passes the same values through its own settings.

- **[0036](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0036-policy-values-are-host-parameters.md) Policy values are host parameters** (*accepted*). A value that is policy is a parameter with a default: `WalletPolicy` on the engine, `HostPolicy` and `PinSettings` in `lepic-ffi`. An out-of-range value fails with `InvalidArgument`. The library checks no password length. A confirmation count has a lower bound of 1 and no upper bound.

## Slates and methods

- **[0002](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0002-slate-domain-and-codecs.md) One slate model, one codec per wire format** (*accepted*). `Slate` is the version-free model. Each wire format has a `Codec` in a `CodecRegistry`. Decoding is strict and limited to `MAX_WIRE_SLATE_LEN` (8 MiB). Encoding is lossless: a slate that a format cannot carry fails with `EncodeError::Unrepresentable`.

- **[0003](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0003-transport-format-policy.md) Transports declare the formats they speak** (*accepted*). A `TransportId` names a transport. The capability traits `Outbound`, `Inbound` and `Exchange` describe what it can do. A `FormatPolicy` names the formats a method reads and writes, and `Methods::register` adds a method. The file row of the policy table: see ADR 0015.

- **[0015](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0015-file-method-writes-v3.md) The file method writes V3** (*accepted*). The file method reads V2 or V3 and writes V3. A reply goes to `<path>.response`.

- **[0012](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0012-native-slate-format.md) A compact native slate format** (*proposed*). `lepic.v1` is a binary slate format with a 51-byte header. Its magic bytes are `89 45 53 4C`. RFC 0003 holds the layout. The design is in the code; the record is marked proposed.

- **[0025](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0025-animated-qr-slates.md) Slates as animated QR codes** (*accepted*). A slate travels as BC-UR `epic-slate` parts: version 1 carries a legacy slate, version 2 a native one, both as CBOR with deflate. `lepic_slate::ur_slate` encodes and decodes them.

- **[0051](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0051-transaction-methods-in-one-crate.md) Transaction methods in one crate** (*accepted*). `lepic-methods` holds the file, http, tor and epicbox methods behind features. The engine knows no method by name and reaches one through the `Method` trait.

- **[0052](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0052-legacy-at-the-edge-native-between-lepic-wallets.md) Legacy at the edge, native between LEPIC wallets** (*accepted*). Everything that exists because stock `epic-wallet` speaks it is called legacy and sits in `lepic-legacy-slate`, `lepic-legacy-rpc` and the `legacy` cargo feature. Between two LEPIC wallets, slates travel as EPICTX native slates, sealed. `cargo xtask no-legacy` builds without the legacy layer.

## Epicbox, notices and Tor

- **[0004](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0004-epicbox-client.md) Epicbox client with listen and drain** (*accepted*). The client has a listen mode that holds a connection open and a drain mode that collects what waits and returns. It reconnects with `Backoff` and acknowledges a message only after the store has it. `set_servers` replaces the relay list. `ListenHandle::finish` waits up to 30 seconds.

- **[0016](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0016-epicbox-notices.md) LEPIC notices over Epicbox** (*accepted*). A notice is JSON `{"lepic":1,"type":...}` with a `pad` key, limited to `MAX_NOTICE_LEN` (8,192 bytes). Types cover a declined, withdrawn, posted (with `excess`) and cancelled transaction, and the pairing messages.

- **[0018](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0018-tor-on-desktop.md) Tor through a bundled tor child process** (*accepted*). `lepic-tor` holds the onion v3 codec, a control-port client, the tor child process, a SOCKS5 client and the onion listener. The host bundles a `tor` binary and passes `TorSettings`. The onion key: see ADR 0044.

- **[0021](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0021-epicbox-over-tor.md) Epicbox over Tor** (*accepted*). A `Tunnel` trait and a `TunnelConnector` carry the relay connection. `OnionRoutes` maps relay hosts to onion addresses, with `[[tor.onions]]` limited to 256 entries.

- **[0022](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0022-node-over-tor.md) Node over Tor** (*accepted*). `NodeDialer` lets `HttpTransport::with_dialer` reach the node through Tor. `lepic-ffi` supplies `TorNodeDialer`.

- **[0026](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0026-tor-as-a-build-feature.md) Tor is a build feature of the binding** (*accepted*). The `tor` feature of `lepic-ffi` is on by default. Without it, Tor calls fail with `Unsupported` and `tor_status` reports `Off`.

- **[0044](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0044-the-onion-has-its-own-key.md) The onion has its own key** (*accepted*). The onion service key is a separate registry key, labelled `lepic-wallet onion key v1`, and is not the wallet's Epicbox key.

- **[0017](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0017-foreign-api-over-http.md) The foreign API over HTTP in its own crate** (*accepted*). `lepic-legacy-rpc` holds the rpc types, url handling, client, dialer and server. `lepic_methods::http` re-exports its types.

- **[0050](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0050-one-wallet-api.md) One wallet API** (*proposed*). `lepic serve` exposes one wallet API, described by an OpenAPI 3.1 document generated with `utoipa`. Owner calls are under `/v1`, `POST /v2/foreign` is the foreign API, and `/v1/peer` and `/v1/peer/slates` serve peers.

## Contacts and trust

- **[0024](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0024-contact-pairing-and-invoice-trust.md) Contact pairing, sealed slates and invoice trust** (*proposed*). Two wallets pair through a key schedule (slot below 65,536, a 16-byte salt) that yields X25519, Ed25519 and hint keys. Messages travel in a sealed envelope from `lepic-seal`: HPKE base mode, DHKEM X25519 HKDF-SHA256, ChaCha20-Poly1305, a 16-byte header. RFC 0002 holds the design. The design is in the code; the record is marked proposed.

- **[0029](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0029-contacts-on-the-engine.md) Contacts on the engine** (*accepted*). `lepic-wallet-contacts` builds on `lepic-wallet`. `ContactBook` holds contacts, and `install(&wallet)` adds the contact hooks to a wallet.

- **[0033](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0033-key-and-domain-registry.md) One registry of keys and signature domains** (*proposed*). `lepic-wallet/src/namespace.rs` lists every seed-derived key by purpose. A key is a keyed BLAKE2b-256 under the label `"lepic-wallet <purpose> v<n>"`. The design is in the code; the record is marked proposed.

- **[0034](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0034-trust-versioning-and-probing.md) Trust, versioning and probing** (*proposed*). Two axes describe a contact: compatibility (what its software can do) and relationship (what the pairing proves). The design is in the code; the record is marked proposed.

- **[0039](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0039-the-host-applies-a-relay-move.md) The host applies a contact's relay move** (*accepted*). The engine reports a contact's move to a mailbox on another relay as `Event::ContactRelayMoveRequested`. The host decides whether to call `ContactBook::apply_relay_move`; the core makes no judgement on the kind of contact.

- **[0040](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0040-contact-check-and-own-relay-move.md) The contact check and moving one's own home relay** (*accepted*). A contact check is a signed envelope of type `09` with an empty body. A paired contact answers with a contact update (type `05`) that carries its current card. `contacts_move_home` moves a wallet's own home relay and posts one contact update to each contact.

- **[0041](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0041-the-owners-profile-in-the-feature-word.md) The owner's profile in the feature word** (*accepted*). The feature word has an extension (`0x82`): bits 0 to 15 are capabilities and bits 16 to 31 are the host profile (`PROFILE_SHIFT` is 16). The CLI names bit 0 `no-payments` and bit 1 `automated`.

- **[0042](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0042-draining-the-old-home-after-moving-ones-own.md) Draining the old home after moving one's own** (*accepted*). After a move, each moved contact's old mailbox is read until the end of a drain period, at most `MAX_HOME_DRAIN` (a year). The CLI takes `lepic contact move-home <HOST> --drain-days N`, with 0 to 365 days; the default is 0.

- **[0043](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0043-domain-proof-for-paired-contacts.md) Domain proof for paired contacts** (*accepted*). A contact can prove it controls a domain with an Ed25519 signature over `"epic-domain/1" || net || sig_key || issued_at || domain`.

- **[0045](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0045-refusing-slates-nobody-asked-for.md) Refusing slates nobody asked for** (*proposed*). `WalletPolicy` has `refuse_unsolicited_payments` and `refuse_unsolicited_invoices`. Both are off by default. The design is in the code; the record is marked proposed.

- **[0047](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0047-the-mailbox-is-the-default-between-paired-contacts.md) The mailbox is the default between paired contacts** (*accepted*). A host chooses the route for a send to a paired contact. The core states no default. The reference host sends through the pairing when it can carry payments, and keeps the payments address as the fallback, which it never uses automatically.

- **[0049](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0049-keeping-messages-that-cannot-be-taken-yet.md) Keeping messages that cannot be taken yet** (*accepted*). A message that opens under a contact's key but cannot be processed goes to a quarantine in `settings` rows, together with notices that arrive before their slate. `quarantine_max_bytes` turns it on (default off) and is limited to 64 MiB.

## Storage and keys

- **[0005](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0005-storage.md) SQLite storage, platform keystore, legacy seed import** (*accepted*). The `WalletStore` trait has a `SqliteStore` (WAL mode, forward-only migrations) and a `MemoryStore`. Parked invoices are limited to 100 in total and 10 per sender. Secrets live in the host's `SecretStore`. A wallet's `WalletSeedFile` can be read for import. The database-import bullet: see ADR 0019.

- **[0019](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0019-import-epic-wallet-history.md) Import the transaction history of an epic-wallet wallet** (*accepted*). The import reads `epic.db` and its `-wal` file read-only from a copy in an `ImportWorkDir`. Rows with the `p` prefix are never read. The result is stored as `imported_transactions` records.

- **[0028](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0028-transaction-records-in-tables.md) Transaction records in tables** (*accepted*). Per-transaction state has one table per record kind (`tx_marks`, `tx_watch`, `tx_watch_outputs` and others) with `ON DELETE CASCADE` on the transaction.

- **[0032](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0032-store-encrypted-at-rest.md) Database encrypted at rest** (*accepted*). The database uses SQLite3 Multiple Ciphers with ChaCha20-Poly1305 only. `sqlite3mc-src` is pinned, and the build sets `SQLITE_TEMP_STORE=3` and `SQLITE3MC_SECURE_MEMORY=1`.

- **[0031](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0031-offline-session.md) An offline session** (*accepted*). `WalletConfig::offline` makes node calls fail with `NodeError::Offline`, and the Epicbox connector fails before any lookup.

- **[0035](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0035-restore-from-a-start-height.md) Restore from a start height** (*accepted*). `restore_from_height` starts a restore scan at a given height. The setting `wallet.restore_scan_required` records that a scan is due. The CLI takes `--from-height`.

- **[0037](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0037-one-send-to-self.md) One send-to-self primitive** (*accepted*). `send_to_self` takes `SelfInputs` (`All`, `Smallest` or `Named`) and has a default output limit of 500.

- **[0027](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0027-minimum-confirmations.md) Minimum confirmations** (*accepted*). The default is 6, set per wallet in `wallet.minimum_confirmations`. A count is never fewer than 1. The upper bound of 30: see ADR 0036.

- **[0046](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0046-a-wallet-for-a-mining-node.md) A wallet for a mining node** (*accepted*). `Wallet::build_coinbase` (`lepic-wallet/src/coinbase.rs`) lets an Epic node mine to a LEPIC wallet through the foreign API. Who is served and how many candidates are kept: see ADR 0048.

- **[0048](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0048-block-rewards-for-this-computer.md) Block rewards for this computer** (*accepted*). `CoinbaseAccess` is `Off`, `LocalOnly` or `Remote`. The CLI opens it with `http listen --coinbase` and `--coinbase-remote`.

## Bindings

- **[0007](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0007-mobile-bindings.md) Mobile bindings with flutter_rust_bridge** (*accepted*). `lepic-ffi` is the API a Flutter app calls. Every failure is a `WalletErrorKind` with a stable numeric code, and a Rust panic becomes the `Panic` kind. The secrets line: see ADR 0014. Delivery: see ADR 0023.

- **[0014](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0014-secrets-at-the-flutter-boundary.md) Which secrets cross the Flutter boundary** (*accepted*). Only secrets the user types or configures enter Rust. Only the recovery phrase leaves it, after a credential check. The PIN key leaves only for the app's secret store. A PIN has at least 6 digits, three failures are free, then the delay is 30 seconds, doubling up to 1 hour. Pairing links are `epiccash://pair/1/` with five pairing words. See [lepic-flutter](lepic-flutter.md).

- **[0023](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0023-binding-in-its-own-repository.md) The binding lives in its own repository** (*accepted*). lepic-flutter holds the Dart half and `lepic.rev`, the LEPIC commit it builds. LEPIC holds `frb_generated.rs` and `bridge.sha256`.

## Compatibility and testing

- **[0009](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0009-conformance.md) Conformance workspace and golden vectors** (*accepted*). `conformance/` is a separate workspace with `vectors` and `differential` members. Golden vectors are JSON files at `testdata/vectors/<area>/<name>.json`. Product crates test against the committed vectors. The version table: see ADR 0020.

- **[0020](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0020-reference-epic-wallet-4-1.md) Reference wallet release** (*accepted*). The conformance workspace, golden vectors and interop images follow one `epic-wallet` release. The ADR names it. The node pin of the interop images and `upstream.toml`: see ADR 0038.

- **[0038](https://github.com/BTLabsUK/lepic/blob/main/docs/adr/0038-reference-node-4-1-2.md) Reference node for interop** (*accepted*). The interop images and `upstream.toml` follow one Epic node release. [Upstream compatibility](upstream.md) explains the pins.
## Related

[LEPIC](lepic.md) maps the crates these decisions shape. [Upstream compatibility](upstream.md)
covers ADRs 0001, 0009, 0020 and 0038, and [Dependencies](dependencies.md) covers ADRs 0006, 0010
and 0032.
