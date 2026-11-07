---
title: Linked devices
description: One wallet on two of your own devices, kept in step with encrypted notices.
---

# Linked devices

Linked devices is there for everyone and has no switch. It is under **Settings › Linked devices** on
the desktop, where it carries an **Experimental** badge, and under
**Settings › This wallet › Linked devices** on the phone.

## What it adds

The recovery phrase opens the same wallet on any device, and the chain gives each device the
balance and every confirmed payment. What the chain does not show is what only the device that made
a payment knows: who was paid, the message, and a payment still under way. Without a link, the
other device shows such a payment as **Sent from another device**, with the amount only, once it is
confirmed.

Linking adds that. Each device tells the other when it starts a payment and how it ends. The coins
it spends are held on the other until the chain shows them spent, so two devices do not pick the
same coins, and the payment shows as **Sent from** and the device's name, with its details.

## Link a device

**Both devices must already have this wallet**, restored from the same recovery phrase: linking
does not create it on the other device.

1. Open **Linked devices** on both devices and choose **Link a device**.
2. On one device, open **Link a device** and scan the QR shown on the other.
3. Both show the same four pictures while they link. There is nothing to tap: the app checks them.

One other device can be linked: remove it to link a different one. **Pause sync** stops the notices;
while paused, they wait on the servers for up to 7 days. Node only and Kill switch pause it too.

Both devices answer payments to the address, and the sender takes the first answer. The payment shows
once, as received on the device the sender used. A third app on the same recovery phrase is not
supported: it hears nothing of the link, and its payments show once the chain confirms them.

## Security

- **Own keys for each link.** They are made when the devices link and cannot be worked out from the
  recovery phrase alone.
- **Encrypted end to end.** Only the linked devices can read a notice. The servers carry it and
  cannot read it.
- **Removing a device ends the link on both.** Either device can do it. Neither gets more notices,
  and the device that did not remove it shows who did.
- **The link does not protect the money.** A device that holds the recovery phrase can still spend.

## Limits

- **Only while the app is open.** Nothing syncs in the background. The app catches up when it
  starts, resumes, unlocks or refreshes.
- **The chain decides.** A notice is a heads-up; a payment counts once the chain shows it.
- **A server down delays notices.** Notices go through the first one or two servers of the Epicbox
  list, shown under the device.

## A lost device

Open **Linked devices**, choose the device and choose **Remove**. The link ends on both devices and
coins it held are released.

:::danger
Removing a device does not protect the money. The device still holds the recovery phrase, and a
device with the phrase can always spend. If it may be in someone else's hands, make a new wallet
with a new recovery phrase and send all the coins to it.
:::

A device restored from the phrase is not linked: link it again.

## Coins held by another device

When the linked device starts a payment, the coins it spends are held on this device: they are left
out of sends, **Max** and the fee estimates, Outputs shows them as **Held by** that device's
payment, and Send says how much is held.

- They become the payment **Sent from** that device once the chain shows them spent.
- They come back when that device cancels the payment, or it fails or expires.
- With no word from that device they come back on their own: 10 blocks after the payment's time ran
  out, 1,440 blocks (about a day) after it was posted without reaching the chain, after 7 days at the
  latest, or when the device is removed.

**Release** beside the held coins frees them at once, on this device only. If the other device
still finishes its payment, a payment made here with the same coins fails; nothing is lost, as the
chain takes only one.
