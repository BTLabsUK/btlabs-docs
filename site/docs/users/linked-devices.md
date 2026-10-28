---
title: Linked devices
description: One wallet on two or more of your own devices, kept in step with encrypted notices.
---

# Linked devices

Linked devices is experimental and off to begin with: turn it on in
**Settings › Advanced › Experimental**. Then it is under **Settings › This wallet › Linked devices**
on the phone, and in the **Linked devices** section of Settings on the desktop.

## What it adds

The recovery phrase opens the same wallet on any device, and the chain gives each device the
balance and every confirmed payment. What the chain does not show is what only the device that made
a payment knows: who was paid, the message, and a payment still under way. Without a link, the
other device shows such a payment as **Sent from another wallet**, with the amount only, once it is
confirmed.

Linking adds that. Each device tells the others when it starts a payment and how it ends. The coins
it spends are held on the others until the chain shows them spent, so two devices do not pick the
same coins, and the payment shows as **Sent from** and the device's name, with its details.

## Link a device

**Both devices must already have this wallet**, restored from the same recovery phrase: linking
does not create it on the other device.

1. Open **Linked devices** on both devices and choose **Link a device**.
2. One device shows a code; the other scans it or pastes it.
3. Both show four pictures. Choose **They match** on each device only if they are the same, in the
   same order.

Up to 5 devices can be linked. **Pause sync** stops the notices for a while.

## Security

- **Own keys for each link.** They are made when the devices link and cannot be worked out from the
  recovery phrase alone.
- **Encrypted end to end.** Only the linked devices can read a notice. The servers carry it and
  cannot read it.
- **Removing a device cuts it off.** It gets no more notices, and the other devices make fresh keys
  between them.
- **The link does not protect the money.** A device that holds the recovery phrase can still spend.

## Limits

- **Only while the app is open.** Nothing syncs in the background. The app catches up when it
  starts, resumes, unlocks or refreshes.
- **The chain decides.** A notice is a heads-up; a payment counts once the chain shows it.
- **A server down delays notices.** Notices go through the one or two servers chosen under
  **Servers**. With two servers, every notice goes to both.

## A lost device

Open **Linked devices**, choose the device and choose **Remove**. It stops getting this wallet's
notices, the remaining devices make fresh keys between them, and coins it held are released.

:::danger
Removing a device does not protect the money. The device still holds the recovery phrase, and a
device with the phrase can always spend. If it may be in someone else's hands, make a new wallet
with a new recovery phrase and send all the coins to it.
:::

A device restored from the phrase is not linked: link it again.

## Coins held by another device

When a linked device starts a payment, the coins it spends are held on this device: they are left
out of sends, Send all and the fee estimates, Outputs shows them as **Held by** that device's
payment, and Send says how much is held.

- They become the payment **Sent from** that device once the chain shows them spent.
- They come back when that device cancels the payment, or it fails or expires.
- With no word from that device they come back on their own: 10 blocks after the payment's time ran
  out, 1,440 blocks after it was posted without reaching the chain, at the latest after a week, or
  when the device is removed.

**Release** beside the held coins frees them at once, on this device only. If the other device
still finishes its payment, a payment made here with the same coins fails; nothing is lost, as the
chain takes only one.
