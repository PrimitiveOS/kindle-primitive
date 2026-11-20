# Install apps with Store on PrimitiveOS

Store is the app store for PrimitiveOS on **jailbroken Kindle e-readers**. It downloads apps over Wi-Fi, checks each
package, and manages installs, updates, and removals. Open it from the **Store** tile in Primitive Launcher.

## 1. What you need

- A **jailbroken** Kindle e-reader. The store does not jailbreak a Kindle; see the KindleModding wiki
  (kindlemodding.org) for that. Keep your jailbreak's hotfix up to date.
- **Primitive Launcher 0.4.6 or later**, installed once by USB (§2).
- **Wi-Fi** to refresh Store and to download apps. You can browse the saved catalog offline.
- Free space on the Kindle: about three times the size of the app while it installs.

Store checks your Kindle's firmware and architecture before offering an installation. The **Study and work** releases
published on 20 November 2026 support **hard-float** (`armhf`) on firmware 5.16.3 or later.

## 2. Install Primitive Launcher (once)

Primitive Launcher is the only manual app install for initial setup. If Launcher is already installed, go to
[Find an app](#3-find-an-app) or [Update apps](#5-update-apps).

1. Download and extract the Launcher ZIP for your Kindle. Check it against the matching `.sha256` file.
   [Latest Launcher release](https://github.com/PrimitiveOS/kindle-primitive-launcher/releases/latest)
2. Connect the Kindle by USB while Amazon's Kindle interface is open. Copy `launcher/` to the root of the Kindle
   drive and `documents/Launcher.sh` into your existing Kindle `documents/` folder.
3. Eject and unplug the Kindle. Open **Launcher** in the Kindle library.

The release includes the full guide and checksum commands. [Launcher installation guide](https://github.com/PrimitiveOS/kindle-primitive-launcher/blob/main/docs/INSTALL.md)

## 3. Find an app

Tap **Store** on the Launcher home screen. If Store is already installed, the tile opens it. Otherwise, connect to
Wi-Fi and eject the Kindle drive before tapping **Store**. Launcher finds a compatible Store release in the catalog,
checks the download's size and SHA-256, and installs it. Store opens when installation finishes if you stay on the
home screen. You can also tap **Store** again to open it. Tap **Done** in Store to return to Launcher.

Four tabs are at the bottom:

- **Today**: open a collection such as **Start here**, **Made by Primitive**, or **Study and work**. Browse
  **Study and work** for practice, reference, and planning apps, or use **Search** to find one by name.
- **Apps**: categories (Reading, Productivity, Internet, Games, Music & Audio, Drawing & Design, Developer Tools,
  Utilities, System). Tap one to see its apps.
- **Updates**: what can be updated, and everything you installed.
- **Search**: type a name or a word. Use the page controls to see more results.

Store opens the saved catalog immediately. To fetch new listings, connect to Wi-Fi and tap **Refresh**. If you tap
**Done** during a refresh, Store stops the refresh safely and returns to Launcher.
[Live Store collections](https://primitiveos.github.io/kindle-primitive-catalog/v1/collections.json)

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

- When updates are ready, the Store tile shows a badge. With **Daily update check** enabled, Store checks an old or
  missing catalog when it opens and Wi-Fi is connected. Change the setting from the Store gear or
  **Launcher Settings › Store**.
- Open **Updates**. Tap **Update** next to one app, or **Update all**.
- An update keeps the old version until the new one is in place. If anything fails, the old version stays.
- For a **Primitive Launcher** update, tap **Done** when Store says the update is ready. Launcher restarts and
  checks the new version. It restores the previous version if the startup trial fails.

## 6. Remove an app

In Launcher 0.5.9 and later, open **Settings › Apps › Installed apps**. Tap **Uninstall** beside the app and confirm.
The list and Home refresh as soon as removal finishes. You can uninstall offline.

The package manager removes the app’s recorded files and keeps personal files outside that list. If another installed
app requires the package, remove the dependent app first. Launcher and Store are protected. Store’s **Updates** page
also offers **Remove**.

## 7. Apps you installed before Store

Store manages apps it has installed. For apps previously installed by hand, check their product page and follow any
prompts in Store to bring them under Store management.

## 8. When something goes wrong

| What you see | What to do |
|---|---|
| "Not available for your Kindle" | The app has no version for your Kindle's type (`armhf` or `armel`) or firmware. Its page says which ones it supports. |
| "Not enough space" | Free space on the Kindle (remove books or apps) and try again. The store needs about three times the app's size while it installs. |
| "Download failed" | Check Wi-Fi and try again. GitHub may be busy; try later. |
| "Check failed" | The download did not match its fingerprint and was deleted. Try again later; if it keeps failing, report it (below). |
| The Kindle turned off during an install | Open **Store**. It checks the interrupted install and finishes or undoes it when possible. |
| An installed app does not show | Close and reopen the Store tile, or restart the launcher (Settings > Device > Restart the launcher). |
| Store shows old information or new apps are missing | Connect to Wi-Fi and tap **Refresh**. If it still shows old information, use **Clear saved catalog** in Store settings, then tap **Refresh** again. |
| A file already exists and is unmanaged | Move the existing file somewhere safe before retrying. This can happen with customized entries from a manual install. |
| The launcher does not start after an update | The Kindle shows its own home screen. Open **Launcher** in the library. If that fails three times, the launcher turns its boot start off by itself; see its `INSTALL.md`. |

The launcher's log is `launcher/log-launcher.txt` on the Kindle drive. To report a problem, open an issue on the app's
GitHub repo (its page in the store links to it) with your Kindle model, firmware, the app's version, and the log.

## 9. Safety

Store checks the package's declared firmware and architecture, verifies its fingerprint (SHA-256) before unpacking,
and checks which paths it can install. The app's information page lists any Kindle models verified by hands-on
testing.

What it cannot promise: jailbreaking and changing a Kindle's software carry risk, and apps from other developers are
their own work. Read **What this app changes** before installing, and prefer apps tested on your Kindle model.
