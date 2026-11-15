---
title: The lepic command-line wallet
description: "Install lepic, create or restore a wallet, receive, send and run the wallet API, with the full command reference."
---

# The lepic command-line wallet

`lepic` is the command-line wallet of [LEPIC](../../lepic.md). It is for a terminal, a script or a
service. This page shows the common tasks. [Every command and option](reference.md) is listed in
the reference, which is generated from the program's own help.

:::warning
LEPIC is beta software. Try it on floonet, the test network, with `--network floonet` before using
it on mainnet. Keep the recovery phrase and test restores before relying on a wallet.
:::

## Install

`lepic` is built from source, with Rust and a C compiler:

```bash
git clone https://github.com/BTLabsUK/lepic && cd lepic
cargo build --release -p lepic-cli
./target/release/lepic --version
```

```text
lepic 0.5.0
```

## How a command is set up

- **Network.** `--network mainnet` (the default) or `--network floonet`.
- **Data directory.** One wallet per directory. Without `--data-dir` it is `~/.lepic/<network>`,
  for example `~/.lepic/floonet`. Two `lepic` processes cannot open the same directory at once.
- **Password.** Commands that open the wallet read it from the file `LEPIC_PASSWORD_FILE` names
  (readable by its owner only), else from `LEPIC_PASSWORD`, else from a hidden prompt, else from
  one line of standard input. It is never taken from an argument.
- **Settings.** Each option can also be set by a `LEPIC_*` variable or in `~/.lepic/config.toml`.
  The node and Epicbox servers are in `~/.lepic/settings.toml`, written on first use.
- **Output.** Text by default. `--output json` prints JSON, and the exit code says what happened
  (the [table](reference.md#exit-codes) is in the reference).
- **Node.** Commands that read the chain need an Epic node. Floonet uses `http://127.0.0.1:13413`
  unless `node_url` says otherwise. Without a node they stop with exit code 9.

The examples below read the password from a file:

```bash
printf '%s\n' 'a long password' > ./pw && chmod 600 ./pw
export LEPIC_PASSWORD_FILE=$PWD/pw
```

## Create a wallet

```bash
lepic --network floonet --data-dir ./wallet wallet init
```

```text
Wallet created on floonet in /home/user/wallet.
Write down the recovery phrase. It is not shown again:

    <24 words>

To receive, give the sender the address `lepic wallet address` prints, or
answer their slate file with `lepic tx receive <FILE>`.
```

`--words 12` (or 15, 18, 21) makes a shorter phrase. The phrase restores the wallet; whoever has
it can spend the funds, so it is written down on paper and kept off the computer.

## Restore a wallet

The phrase is read from standard input or a hidden prompt, then the new password is read as above:

```bash
printf '%s\n' "$PHRASE" | lepic --network floonet --data-dir ./restored wallet restore
```

`wallet restore` scans the chain for the wallet's outputs and needs a node. `--from-height H`
starts the scan at a block height instead of genesis, so outputs below it are not found.
`--no-scan` skips the scan; `lepic wallet scan` runs it later.

A wallet restored from its phrase has the same Epicbox address as the original. Wallets made by
`epic-wallet` are brought over with `wallet import-seed FILE`.

## Receive

Show the address to give to the sender:

```bash
lepic --network floonet --data-dir ./wallet wallet address
```

```text
zzexampleexampleexampleexampleexampleexampleexample@epicbox.example
```

The host after `@` is the Epicbox relay the wallet uses. A payment sent to the address waits at
the relay until the wallet connects:

```bash
lepic epicbox listen    # stays connected and handles slates as they arrive
lepic epicbox drain     # handles what is waiting once, then exits
```

Other ways in:

```bash
lepic tx receive ./payment.slate   # a slate file; the reply goes to ./payment.slate.response
lepic http listen --port 3415      # an HTTP listener for wallets that pay over HTTP
lepic tor listen --tor-binary /opt/tor/tor --lib-dir /opt/tor   # an onion address
```

`lepic tx list` shows the account's transactions, and `lepic wallet info` the balances after a
refresh against the node.

## Send

`lepic tx send AMOUNT` takes one destination. The amount is in EPIC.

```bash
lepic tx send 1.5 --to ADDRESS@HOST               # through Epicbox
lepic tx send 1.5 --to http://HOST:3415           # straight to a listening wallet
lepic tx send 1.5 --to NAME.onion --tor-binary /opt/tor/tor --lib-dir /opt/tor
lepic tx send 1.5 --to-file ./payment.slate       # a slate file to hand over
lepic tx send 1.5 --to-contact ID                 # a paired contact
```

Over HTTP and Tor the transaction is finished and posted by the same command. Over Epicbox the
other wallet answers when it next connects, and the next `epicbox listen` or `epicbox drain`
finishes and posts it. With a file, the receiver runs `lepic tx receive`, and the sender then runs
`lepic tx finalize ./payment.slate.response`.

`--message TEXT` adds a message, `--account LABEL` picks the account to spend from, and
`--slate-id UUID` (a version 4 UUID the caller stores first) makes a repeated send a no-op that
reports the first one. `lepic tx cancel TX_ID` cancels a transaction that is not posted.

## Run the wallet API

`lepic serve` keeps the wallet open and answers the [wallet API](../api/v1/index.md) on a Unix
socket. It also listens on Epicbox and refreshes the wallet while it runs.

```bash
lepic --network floonet --data-dir ./wallet serve --socket ./w.sock &
curl --unix-socket ./w.sock http://lepic/api/v1/status
```

```json
{"version":"0.5.0","uptime_s":2,"listeners":{"epicbox":{"state":"connected"}},...}
```

The answer is cut here. The socket file can be opened only by the user that runs serve. `--http` also answers payments
over HTTP, and `--owner-tls` also answers the API over TLS to clients added with
`lepic api client add`. While serve runs, other `lepic` commands on the same wallet go through
it. Connecting, roles and conventions are in the [API guide](../api/v1/index.md), and every
endpoint is in the [API reference](../api/v1/reference.md).

## More

The reference covers the rest: contacts and pairing (`contact`), invoices (`invoice`), in-person
codes (`in-person`), epic1 links (`epic1`), `.epictx` files (`epictx`), the profile (`profile`)
and the interactive shell (`shell`, also opened by `lepic` with no command). The repository's
[docs/cli.md](https://github.com/BTLabsUK/lepic/blob/main/docs/cli.md) and
[docs/configuration.md](https://github.com/BTLabsUK/lepic/blob/main/docs/configuration.md) go
further on files and settings.
