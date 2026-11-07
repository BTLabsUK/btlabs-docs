---
title: The settings file
description: The file that holds the Node and Epicbox lists and three switches.
---

# The settings file

One file holds your Node and Epicbox lists and three switches: the status site, the update check and
prices. Everything else comes with the app.

On the phone the file is changed in the app, not by hand. On the desktop you can also edit it.

| System | File |
| --- | --- |
| Linux, macOS | `~/.epic_cash_desktop/settings.toml` |
| Windows | `%USERPROFILE%\.epic_cash_desktop\settings.toml` |

**Open folder** next to **Settings › Files & logs › App files** opens the folder.

- **The first server of each list is the one in use.** Picking a server moves it to the top, and
  reordering the list changes the one in use. When the first node does not answer, the next one is
  tried.
- **The first Epicbox server is in the Epicbox address of every wallet.** Moving another one to the
  top gives each wallet a new address. Payments sent to an old address do not arrive.
- A change in the app is written to the file at once. A change you save in the file applies while
  the app runs.
- With an error in the file, the last good settings stay in use, a notice names the line, and a
  broken file is never overwritten.
- If the app has to write while the file has errors, it first saves the file as
  `settings.toml.bad-<time>`, then writes a good one.
- A deleted file is written again.
