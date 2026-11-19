# Install apps with Primitive Store

Status date: 2026-11-19. **Status: draft.** Primitive Store is designed but not built yet (plan phases S3 and S4). Until
it ships, install each Primitive app by hand from its GitHub release (§7). This guide describes how the store will work.

Primitive Store installs apps on a **jailbroken Kindle e-reader** over Wi-Fi, checks every download, keeps apps up to
date, and removes them cleanly. It is part of Primitive Launcher.

## 1. What you need

- A **jailbroken** Kindle e-reader. The store does not jailbreak a Kindle; see the KindleModding wiki
  (kindlemodding.org) for that. Keep your jailbreak's hotfix up to date.
- **Primitive Launcher**, installed once by USB (§2). The store comes with it.
- **Wi-Fi** for installing and updating. Browsing what you have already opened works without it.
- Free space on the Kindle: about three times the size of the app while it installs.

Apps say which Kindles they run on. Newer Kindles are **hard-float** (`armhf`), older firmware is **soft-float**
(`armel`). The store works this out by itself and only offers what runs on your Kindle.

## 2. Install Primitive Launcher (once)

1. On a computer, open the launcher's latest release:
   `https://github.com/DoanNguyenTrong/kindle-primitive-launcher/releases/latest`, and download
   `primitive-launcher-<version>.zip` and its `.sha256` file.
2. Optional, to check the download: compare the zip's SHA-256 with the `.sha256` file
   (`shasum -a 256 <zip>` on macOS and Linux, `certutil -hashfile <zip> SHA256` on Windows).
3. Unzip it. Connect the Kindle by USB while its normal home screen is showing.
4. Copy the `launcher` and `documents` folders onto the Kindle drive. Merge `documents` with the one already there;
   your books stay.
5. Eject the Kindle and unplug it.
6. Open **Launcher** in the Kindle library. The first time, it also sets itself up to start with the Kindle.

The full guide, including how to leave the launcher and how to uninstall it, is the launcher's `INSTALL.md` (inside the
zip).

## 3. Find an app

Tap the **Store** tile on the launcher's home screen. Four tabs are at the bottom:

- **Today**: collections picked by us, such as "Start here" and "New and updated".
- **Apps**: categories (Reading, Productivity, Internet, Games, Music & Audio, Drawing & Design, Developer Tools,
  Utilities, System). Tap one to see its apps.
- **Updates**: what can be updated, and everything you installed.
- **Search**: type a name or a word; results show as you search.

Tap an app to open its page: what it does, pictures of it, what is new, its version history, **What this app changes**,
and information such as its size, licence and the Kindles it was tested on.

## 4. Install an app

1. On the app's page, tap **Get**.
2. A sheet shows the app's size, what it needs (for example a newer launcher), and **What this app changes**:
   - "Uses the internet."
   - "Stops the Kindle's own screen while it runs."
   - "Starts when the Kindle starts."
   - "Changes the Kindle's system files."
   - "Runs its own install steps."
   - or "Changes nothing outside its own folder."
3. Tap **Install**. Apps in the **System** category, and apps that start with the Kindle or change system files, ask a
   second time.
4. The sheet shows the steps: **Downloading**, **Checking**, **Installing**. Checking compares the download with the
   fingerprint (SHA-256) published in the store; a download that does not match is deleted and nothing is installed.
5. When it is done, the button turns into **Open**, and the app is on your home screen.

If the app needs another app first, the store offers to install it and does that first.

Some apps show **Link** instead of **Get**. The store cannot install those for you (for example, they need steps on a
computer). Their page explains how to install them and links to their author's instructions.

## 5. Update apps

- When updates are ready, the Store tile shows a badge. The store looks for updates when it opens, and once a day while
  Wi-Fi is on (you can turn the daily check off in the launcher's Settings > Store).
- Open **Updates**. Tap **Update** next to one app, or **Update all**.
- An update keeps the old version until the new one is in place. If anything fails, the old version stays.
- Updating **Primitive Launcher** restarts the launcher. If the new version does not start, the Kindle falls back to its
  own home screen; open **Launcher** in the library to return.

## 6. Remove an app

Open **Updates**, find the app in the installed list, and tap **Remove**, then confirm. The store deletes exactly the
files it installed. Files you made with the app outside its own folder (for example books or notes in `documents`)
stay.

The store will not remove an app that another installed app needs; remove that one first. It never removes Primitive
Launcher; to uninstall the launcher, follow its `INSTALL.md`.

## 7. Install by hand (without the store)

Every app in the store also has a GitHub release with a zip for each kind of Kindle (`armhf` or `armel`) and an
`INSTALL.md` inside. To install by hand:

1. Download the zip for your Kindle and its `.sha256` file from the app's releases page, and check it (§2 step 2).
2. Connect the Kindle by USB and copy the folders from the zip onto the Kindle drive, as its `INSTALL.md` says.
3. Eject and unplug. The app appears in the library and on the launcher's home screen.

An app installed by hand is not in the store's installed list. Install it once from the store to let the store update it.

## 8. When something goes wrong

| What you see | What to do |
|---|---|
| "Not available for your Kindle" | The app has no version for your Kindle's type (`armhf` or `armel`) or firmware. Its page says which ones it supports. |
| "Not enough space" | Free space on the Kindle (remove books or apps) and try again. The store needs about three times the app's size while it installs. |
| "Download failed" | Check Wi-Fi and try again. GitHub may be busy; try later. |
| "Check failed" | The download did not match its fingerprint and was deleted. Try again later; if it keeps failing, report it (below). |
| The Kindle turned off during an install | Open the launcher. The store finishes or undoes the cut install by itself. |
| An installed app does not show | Close and reopen the Store tile, or restart the launcher (Settings > Device > Restart the launcher). |
| The store shows old information | Tap **Refresh** at the top of the store. Over USB, you can also delete `launcher/store/cache` to start fresh. |
| A file already exists and is unmanaged | Move the existing file somewhere safe before retrying. This can happen with customized entries from a manual install. |
| The launcher does not start after an update | The Kindle shows its own home screen. Open **Launcher** in the library. If that fails three times, the launcher turns its boot start off by itself; see its `INSTALL.md`. |

The launcher's log is `launcher/log-launcher.txt` on the Kindle drive. To report a problem, open an issue on the app's
GitHub repo (its page in the store links to it) with your Kindle model, firmware, the app's version, and the log.

## 9. Safety

What the store checks: that the app runs on your Kindle, its fingerprint (SHA-256) before anything is opened, that it
only writes where it says it will, and, for apps in the catalog, that a reviewer read its install steps.

What it cannot promise: jailbreaking and changing a Kindle's software carry risk, and apps from other developers are
their own work. Read **What this app changes** before installing, and prefer apps tested on your Kindle model.
