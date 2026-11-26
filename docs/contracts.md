# PrimitiveOS app, package, and catalog contracts

Status date: 2026-11-21. Status: frozen for the first store release (implementation plan A2); §1.1, the system
layer lines of a library entry, was added on 2026-11-21. The machine-readable versions are in [schema/](../schema/):
`app.schema.json` (a listing), `manifest.schema.json` (a package's manifest) and `index.schema.json` (the catalog
index). Check any file with `python3 schema/scripts/validate.py FILE...`.

Changing a contract means a new `schema` number and a note here. §1.2 (the media session) is an addition: no existing
app or listing changes. Apps keep working with the schema they were published
with.

## 1. The library entry (a scriptlet in `documents/`)

The first lines of a `.sh` file in `/mnt/us/documents/` are its header, in this order:

```sh
#!/bin/sh
# Name: Notes
# Author: Primitive AI
# Icon: data:image/png;base64,...     (optional: a PNG, used when the app has no icon file)
# DontUseFBInk
# Wake: redraw                        (optional: the app redraws when Primitive Launcher asks, §1.1)
```

`Name` is the label on the grid. `DontUseFBInk` says the scriptlet draws its own screen. The launcher shows any such
file on its grid; a `PrimitiveLauncherEntry` line marks entries the launcher itself runs.

### 1.1 Under Primitive Launcher (the system layer)

Primitive Launcher is the system layer over every app ([system architecture](system-architecture.md)). It runs an
entry with `PRIMITIVE_LAUNCHER=1` in the environment, in the app's own process group, and keeps running while the app
is open. Entries without the lines below keep working.

`# Wake: redraw` says that the app draws its whole screen again, in the current theme, when it gets `SIGUSR1`
([system architecture §4.1 and §4.2](system-architecture.md#4-contracts-between-the-system-layer-and-apps)). The
supervisor looks for this exact line, with nothing after it, in the first ten lines of the entry. The entry must be a
plain file, not a link. Put the line after the other header lines.

An entry with the line also ignores `SIGUSR1` in its own shell before it starts the app:

```sh
[ "${PRIMITIVE_LAUNCHER:-0}" = 1 ] && trap '' USR1
```

The signal goes to the whole process group, and a shell that runs the app as a child (not with `exec`) ends on it
otherwise. An ignored signal is passed on through `exec`, and the app's own handler replaces it. Opened from the
Kindle library without the launcher, the line does nothing.

What the system layer does with each kind of entry:

- **With the line.** Over the app, the launcher saves the app's screen for its own screens (quick settings, the power
  menu, the sleep picture) and puts it back when they close. It sends `SIGUSR1` to the app's process group when the
  screen must be drawn again: after the theme or the rotation changed while its screen was up, when it could not save
  the screen, and after the launcher started again over the app. When the supervisor keeps sleep and wake itself (the
  launcher is not running over the app), it sends `SIGUSR1` on wake.
- **Without the line.** The app never gets `SIGUSR1`, which would end it. The launcher puts its saved screen back, and
  after a theme change the app keeps the old theme until it starts again. When the supervisor keeps sleep and wake
  itself, it restarts the app on wake, so the screen is never left blank.

Never add the line to an app whose program does not handle `SIGUSR1`: the signal ends it. Native apps built on the
app kit (`primitive_app::run` in Tools) handle it. The Store's check for the line: (Store check: to be confirmed).

An app under the launcher follows these rules. The reasons and the details are in
[system architecture §4](system-architecture.md#4-contracts-between-the-system-layer-and-apps).

- It follows the system theme (`dark_mode` in `/mnt/us/launcher/settings.txt`) in everything it draws, its chrome and
  its content. It reads the theme at start and again on `SIGUSR1`. It has no light or dark switch of its own and
  never overrides the system theme.
- The swipe down from the top edge belongs to the launcher (quick settings). The app ignores it. Every other touch
  and the page buttons are the app's.
- It never puts the Kindle to sleep, never draws a lock screen or its own quick settings, never loads or unloads the
  stock screensaver, never sets `preventScreenSaver`, and never stops or starts the Kindle framework. It may save its
  data when the Kindle goes to sleep.
- Its redraw after the launcher's request does not flash. The launcher has already flashed the screen once for a
  theme change, and a second full (GC16) flash shows the old theme for a moment. Draw the whole screen with a
  non-flashing update.

### 1.2 Media session (optional, under Primitive Launcher)

An app that plays audio in the background shows its session in quick settings (the title, play or pause, previous and
next) by writing two files in `/var/tmp/media/` (RAM: cleared when the Kindle restarts). Apps that play no media do
nothing. The launcher only reads the first file and writes the second; it never runs app code.

`<app>.now` (the app's id, lower case letters, digits and `-`), written atomically (a temporary name, then a rename),
with one `key value` line each:

```text
app music
name Music
state playing           (playing | paused; a stopped session is removed or written as "state stopped")
title Evening Bells     (the track, as shown; may be empty)
artist                  (optional)
position 83             (seconds)
length 203              (seconds; 0 when unknown)
pid 20561               (the player's process id: the launcher shows the session only while it exists)
```

`<app>.cmd`, appended to by the launcher, one command per line. The app takes the file away when it reads it (a rename,
then the read, then the delete) and ignores lines it does not know:

```text
toggle                  (play when paused or stopped, pause when playing)
pause
next
previous
```

`/var/tmp/media/volume`: the media volume, one line with a level from 1 (quietest) to 8 (full). The launcher's sound row
reads and sets it while headphones are connected; a player applies it to its audio (it scales the samples; the stock
speaker level is not used, because the Bluetooth stack overrides it). No file means 8. A player reads it about once
a second, and restarts the segment it plays when it changes.

The launcher shows the card with the first session that plays, then the first that is paused. Commands for an app
without a live session are ignored. An app keeps the files current while its audio runs, once a second is enough.

## 2. The module folder

Every app's files live in one folder under `/mnt/us/`, named by its `dir` (the listing's `dir`, which defaults to the `id`).
Existing apps keep their folders: `launcher`, `browser`, `terminal`.

- `dir` is lower case letters, digits and `-`, unique in the store, and never changes.
- Reserved, refused by the listing schema and the installer: `documents`, `extensions`, `system`, `fonts`, `screensaver`,
  `koreader`, and any folder the Kindle or KOReader uses on `/mnt/us`.
- A KUAL extension goes to `/mnt/us/extensions/<dir>/` (it needs `config.xml` and `menu.json`).

## 3. The package (a zip per architecture)

Name: `<id>-<version>-<arch>.zip`, with one top folder `<id>-<version>/`:

```
<id>-<version>/
  manifest.json          required (§4)
  LICENSE                required: the licence of the app's own code
  INSTALL.md             required: how to install by hand over USB
  documents/...          optional: library entries (header contract §1)
  <dir>/...              optional: the module folder (§2)
  extensions/<dir>/...   optional: a KUAL extension
  hooks/post-install.sh  optional pair, reviewed in the catalog pull request
  hooks/pre-uninstall.sh optional pair, reviewed in the catalog pull request
```

Rules the installer enforces, and CI checks before publishing:

- Only the roots above are written. No absolute paths, no `..`, no backslashes, no links that leave the package.
- Every file in the zip except `manifest.json`, `LICENSE`, `INSTALL.md` and `hooks/` is listed in `manifest.files`.
- `arch` is `armhf` (hard-float, the Oasis 3 and newer) or `armel` (soft-float, older Kindles). Each package holds one arch.
- Hook packages declare both scripts and set `changes.hooks` in the listing. Store verifies an exact root-owned
  approval before running either script with `/` as its working directory, a 60 s limit, and separate PID and
  network namespaces. [Reviewed hook contract](store-architecture.md#64-hooks)

## 4. `manifest.json` (inside the package)

```json
{
  "schema": 1,
  "id": "primitive-browser",
  "dir": "browser",
  "version": "0.2.17",
  "arch": "armhf",
  "firmware": { "min": "5.16.3", "max": null },
  "requires": { "primitive-launcher": ">=0.3.21" },
  "files": ["browser/kb-kindle", "browser/icon.png", "documents/Browser.sh"],
  "hooks": []
}
```

`files` is the exact install and removal list. `requires` names other store apps with a `>=` version.

## 5. The listing (`apps/<id>/app.json` in the catalog)

Required fields: `schema`, `id`, `name` (≤ 40 characters), `subtitle` (≤ 40), `developer`, `categories` (one or two of the
store's categories), `description`, `repo`, `licence` (SPDX id, or the licence's name), `source`, `icon`, `changes`,
`versions`.

- `source`: `hosted` (our release assets, sha256-checked), `upstream` (the author's own release URL, pinned by sha256;
  nothing re-hosted), or `link` (instructions and a link; no install).
- `versions` are newest first. Keep each published release's package identity, contents, and checksum. Mark a broken
  version as `withdrawn` and record the reason.
- A `hosted` or `upstream` version lists `assets` for each architecture it has, with `url` (https), `sha256` and `size`.
  A `link` version has no `assets`.
- App IDs identify packages and installed records independently of the GitHub repository name. When moving a first-party
  repository, update `repo` and the repository component of its asset URLs after verifying the same assets at the new
  address. Keep the package ID, install directory, version tags, ZIP names, sizes, and checksums.
- `changes` states what the app does outside its own folder: `network`, `stops_kindle_ui`, `starts_at_boot`,
  `root_filesystem`, `hooks`, and a `notes` sentence. These flags are shown to the user before installing.
- `version` is `X.Y.Z` for our apps, or the upstream's own version (`2026.10` for KOReader), with an optional `-pN` when only
  our packaging changed.

Categories: `reading`, `productivity`, `internet`, `games`, `audio`, `creativity`, `developer`, `utilities`, `system`.

Icons are PNG, 256 × 256, grayscale. Screenshots are PNG, 632 × 840 (half the 1264 × 1680 screen), grayscale, up to five.

## 6. The catalog index (published under GitHub Pages)

`site/v1/index.json` lists every app's card: `id`, `dir`, `name`, `subtitle`, `categories`, `icon` (URL), `source`,
`latest_version`, `arch` (the architectures it has), `updated_at`, and `listing` (the URL of its full listing). Plus
`categories` and `generated_at`. The device fetches it on refresh and caches it; it fetches a listing when the user
opens an app.

Base URL: `https://primitiveos.github.io/kindle-primitive-catalog/v1/`. The `v1` changes only when the format breaks.

## 7. Devices and the choice of package

The store chooses, for the device:

1. `arch` from the device: the dynamic loader `/lib/ld-linux-armhf.so.3` present means `armhf`; otherwise `armel`
   (checked on the Oasis 3: present; a soft-float Kindle is still to be checked, implementation plan A4.1).
2. `firmware`: the firmware version from `/etc/prettyversion.txt` (for example `Kindle 5.18.2`) and
   `/etc/version.txt` (`System Software Version`), checked on the Oasis 3 (A4.2). The newest version whose `firmware.min`
   is at most the device's version, and whose `firmware.max` (if set) is at least it, is offered.
3. `requires`: each required app must be installed at a version that satisfies `>=`, or be installed first.
4. Model: the store records the model name for `tested_on` (`KindleOasis3`, KOReader's name). Model detection on the
   device is open (A4.3): the stock model code could not be read with the commands tried so far.

## 8. Versions

- Our apps: `X.Y.Z`. A device build bumps `Z`; a new phase bumps `Y` (`scripts/build-device.sh --minor`).
- The git tag is `vX.Y.Z` and matches `Cargo.toml` and `manifest.json`. A tag is never moved.
- A new app starts at `0.1.0`.
- Packages that repackage an upstream version: `<upstream version>-pN`.
