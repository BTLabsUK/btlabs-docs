---
title: How Epic Cash works
description: Why both wallets take part, confirmations, outputs and change, fees.
---

# How Epic Cash works

## Both wallets take part

Epic Cash uses Mimblewimble. Instead of writing an address and an amount on the blockchain, the two
wallets build each transaction together, like a handshake:

1. The sender's wallet starts it and locks the outputs being sent.
2. The receiver's wallet adds its part and signs.
3. The sender's wallet signs too, finishes the transaction and posts it to the network.

Something has to carry the messages between the two wallets: **Epicbox** holds each message while
the other wallet is offline; **Link · HTTP** and **Link · Tor** go straight to the other wallet
while it is open; **Direct · File Transfer** and **Direct · QR Payment** are the manual ways. See
[Payment methods](payment-methods.md).

## Confirmations

When the network accepts a transaction, a miner puts it in a block. The block that holds the
transaction is the first confirmation, and every block after it adds one more and makes the
transaction harder to undo.

The wallet treats a transaction as final after a set number of confirmations, **6 by default** (a
setting in [Advanced](advanced.md), from 1 to 30). Until then it shows as **Confirming**, and
received outputs cannot be spent yet. The wallet sees new blocks only through its node: if
confirmations do not move, check that the node is synced.

## Outputs and change

The balance is a set of outputs, like notes in a wallet. To send 3 EPIC from a 5 EPIC output, the
wallet spends the whole output: 3 EPIC go to the recipient, a small fee goes to the miners, and the
rest comes back as a new output, the **change**.

That is why part of the balance can be unavailable for a while after a send:

- **Locked**: outputs in a send that is not finished yet. They are unlocked if the send is
  cancelled.
- **Awaiting finalization**: a transaction still waiting for the other wallet.
- **Confirming**: outputs in a block with fewer confirmations than the setting, including the change.

With **Outputs** on in Advanced, the outputs are listed under **Outputs**.

## Smallest or All

Which outputs a send spends:

- **Smallest** (the default) takes the smallest spendable outputs until the amount and fee are
  covered. Only those are locked while the send confirms; the rest can be sent right away.
- **All** spends every spendable output and returns one change output. Everything is locked until
  it confirms, and the fee is a little higher because each input costs. Sending the whole balance
  always uses All.

## Split and consolidate

Both are network transactions from this wallet to itself, and both lock every spendable output
until they confirm.

- **Split** makes 2 to 10 outputs of nearly equal value, so sends can follow each other.
- **Consolidate** merges every spendable output into one.
- **Split change** (on by default) does the same inside an ordinary send when few outputs would be
  left, for 0.004 EPIC per extra output.

Both are under **Outputs › Manage outputs**. Activity shows each as two entries, a send and a
receive, both with this wallet.

## Fees

Every transaction pays a small network fee, shown as **Network fee** before sending. It goes to the
miners. The fee depends on how many outputs the transaction spends and creates, not on the amount.
**All**, next to the amount, fills in the whole spendable balance minus the exact fee, so no change
is left.

More detail for developers is on the [Epic Cash Developer Hub](https://devdocs.btlabs.uk).
