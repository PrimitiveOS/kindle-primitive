# Primitive Store: system architecture and requirements

Status date: 2026-11-19. Status: design, not built. Decisions D1–D7 are in
[kindle-platform-plan.md](kindle-platform-plan.md) §4 (S0).

Primitive Store is an app store for **jailbroken Kindle e-readers**, built and run by us, hosted entirely on GitHub. It
lists apps by category, installs them with a checked download, keeps them up to date, and removes them cleanly. It lives
inside Primitive Launcher as a screen with its own tile.

How to read the requirements: `FR-n` is a functional requirement, `NFR-n` a non-functional one. Each has a priority:
**M** (must, first release), **S** (should), **L** (later). Track them in the checklists in §11.

## 1. Sources and what we take from them

| Source | What we take | What we do differently |
|---|---|---|
| Apple App Store (iOS) | Tabs (Today, Apps, Games, Search); categories; the product page (icon, name, subtitle, one action button, screenshots, description, What's New, version history, an information block, a privacy label); an Updates list. | No accounts, payments, ratings or reviews. Our "privacy label" becomes **What this app changes** (§5.3), since on a Kindle the risk is system changes, not data collection. |
| KindleForge (`KindleTweaks/KindleForge`, `KindleTweaks/Repository`) | A single catalog file (`registry.json`, 28 entries) with name, folder, description, author, ABI (`hf`, `sf`), dependencies by name, and tags (UTILITY, MEDIA, PRODUCTIVITY, DEVELOPMENT, GAMES, EDITORS). Hard-float is detected by `/lib/ld-linux-armhf.so.3`. One folder per package with `install.sh`, `uninstall.sh` and `assets/`. | We pin **versions** and **sha256** for every download (KindleForge's scripts fetch whatever is newest at install time and check nothing). Installs are **declarative** (a file list), with scripts only as reviewed hooks. Versions history, updates and rollback. |
| KPM (`Gingrspacecadet/KPM`) | A shell package manager (needs `curl`, `unzip` or `tar`). Package format on its wiki (not read yet: plan O3). | No dependency on a terminal or `curl` on the device; the store downloads and unpacks in-process. |
| Primitive Launcher | The host: grid, single-instance reload of apps (`set_apps`), library entries, KUAL discovery, Wi-Fi, the boot copy on `/var/local`, and the UI language (the `primitive-ui` skill). | The store is a new screen of the launcher, not a separate program. |

## 2. Scope

In scope (first release):

- Our three apps as hosted packages: Primitive Launcher (self-update), Primitive Browser, Primitive Terminal (D4).
- Outside apps by **link** (D3) that meet the quality bar below: KOReader first.
- Every jailbroken Kindle e-reader (D5), hard-float (`armhf`) and soft-float (`armel`), each package declaring which.
- GitHub only: Releases for binaries, Pages for the catalog (D2). sha256 for integrity (D7).

Quality bar (the owner's, for every listing, ours or not): a real touch interface (no terminal, command line or
configuration files to use it); simple for everyone, in the spirit of Apple's apps; a kind of app that is popular on iOS
or Android (productivity, games, everyday tools); and it works with Primitive Launcher in front, the Kindle's own
interface stopped. Apps that need the Kindle's own interface (Illusion and other HTML booklets) do not qualify.

Out of scope: accounts, payments, ratings, reviews, analytics, push notifications, non-Kindle devices, Kindle Fire
tablets, apps that need a different jailbreak than the one installed.

## 3. System overview

```
 Publisher repos (one per app)            Catalog repo (kindle-primitive-catalog)          Kindle
 ┌──────────────────────────┐   PR with   ┌────────────────────────────────────┐  HTTPS  ┌──────────────────────┐
 │ source, tests            │  manifest   │ apps/<id>/app.json (source of truth)│ ──────▶ │ Primitive Launcher   │
 │ release.yml (shared      │ ──────────▶ │ CI: validate, download, sha256,     │ index   │  └ Store screen      │
 │  build workflow)         │             │     unpack check, licence check     │         │     ├ catalog cache  │
 │ GitHub Release:          │             │ build: site/v1/index.json,          │         │     ├ installer      │
 │  <id>-<v>-<arch>.zip     │◀─ download ─┤        site/v1/apps/<id>.json,      │         │     └ installed.json │
 │  .sha256, manifest.json  │  (by device)│        icons, screenshots           │         │ apps on /mnt/us      │
 └──────────────────────────┘             │ GitHub Pages: doannguyentrong.      │         └──────────────────────┘
                                          │  github.io/kindle-primitive-catalog │
 Upstream projects (linked) ─ download ─▶ └────────────────────────────────────┘
```

Three parts, each in its own repo:

1. **Publisher repos**: each app's repo builds a release on a `v*` tag: one zip per architecture, its `.sha256`, and the
   `manifest.json` that is also inside the zip. The shared workflow is in `kindle-primitive-build` (plan S2).
2. **Catalog** (`kindle-primitive-catalog`): one folder per app with `app.json` (the store listing and every version),
   icons and screenshots. A pull request adds or updates an app. CI validates it and publishes a static API on GitHub
   Pages. The catalog holds **no binaries**; it points at release assets.
3. **Store client** (in the launcher, crate `kl-store`): downloads the index, shows the store, installs, updates and
   removes apps, and records what it installed.

Nothing runs on a server of ours: GitHub Pages serves static JSON, and GitHub Releases serve the files.

## 4. Catalog

### 4.1 Categories

Apple's categories adapted to what a Kindle can do. Each app has one **primary** category and at most one secondary.
KindleForge's tags map onto them for imported entries.

| Id | Name | What belongs here | Apple's category | KindleForge tag |
|---|---|---|---|---|
| `reading` | Reading | E-book readers, comics, dictionaries, book downloaders. | Books, Reference | MEDIA |
| `productivity` | Productivity | Notes, flashcards, timers, to-do lists, writing. | Productivity, Education | PRODUCTIVITY, EDITORS |
| `internet` | Internet | Browsers, feeds, downloaders, network tools. | Utilities | UTILITY |
| `games` | Games | Puzzles, board games, emulators. Sub-genres: puzzle, board, arcade, emulator. | Games | GAMES |
| `audio` | Music & Audio | Music and audiobook players, radio (Bluetooth models). | Music | MEDIA |
| `creativity` | Drawing & Design | Drawing, handwriting, image tools. | Graphics & Design | — |
| `developer` | Developer Tools | Terminals, SSH, Linux environments, package managers. | Developer Tools | DEVELOPMENT |
| `utilities` | Utilities | Small tools: toggles, screensavers, button mappers, fonts. | Utilities | UTILITY |
| `system` | System | Things that change how the Kindle starts or runs: launchers, hotfix tools, KUAL. Shown with a warning. | — | UTILITY |

### 4.2 Collections (the "Today" tab)

Curated lists in the catalog (`collections.json`): an id, a title, one sentence, and app ids. First collections:
"Start here" (launcher, browser, terminal, KOReader), "New and updated", "Made by Primitive", "For writers",
"Games for e-ink". Collections are edited by pull request like apps.

### 4.3 Static API (GitHub Pages)

Base: `https://doannguyentrong.github.io/kindle-primitive-catalog/v1/` (the version in the path changes only when the
format breaks).

| File | Content | Size target |
|---|---|---|
| `index.json` | Every app's card: id, name, subtitle, categories, icon URL, latest version per arch, size, source kind, `updated_at`. Plus `categories` and `generated_at`. | < 100 KB |
| `collections.json` | The Today tab's collections. | < 10 KB |
| `apps/<id>.json` | The full listing: description, screenshots, What's New, every version with its assets, requirements, What this app changes. | < 50 KB each |
| `icons/<id>.png` | 256 × 256 grayscale PNG. | < 20 KB |
| `shots/<id>/<n>.png` | Screenshots, 632 × 840 (half of 1264 × 1680), grayscale. | < 80 KB each |

The device downloads `index.json` and `collections.json` on refresh, and an app's file, icon and screenshots when the
user opens it.

### 4.4 The app listing: `apps/<id>/app.json`

This is the file a publisher writes (see [store-submit-app.md](store-submit-app.md)). CI copies it to `v1/apps/<id>.json`
after checks. Schema version 1:

```json
{
  "schema": 1,
  "id": "primitive-browser",
  "dir": "browser",
  "name": "Primitive Browser",
  "subtitle": "A fast web browser made for e-ink",
  "developer": { "name": "Primitive AI", "url": "https://github.com/DoanNguyenTrong" },
  "categories": ["internet"],
  "description": "Several short paragraphs, plain text.",
  "repo": "https://github.com/DoanNguyenTrong/kindle-primitive-browser",
  "licence": "AGPL-3.0-only",
  "source": "hosted",
  "icon": "icon.png",
  "screenshots": ["shots/1.png", "shots/2.png"],
  "changes": {
    "network": true,
    "stops_kindle_ui": false,
    "starts_at_boot": false,
    "root_filesystem": false,
    "hooks": false,
    "notes": ""
  },
  "versions": [
    {
      "version": "0.2.16",
      "date": "2026-11-18",
      "notes": "What's New: one to five short lines.",
      "firmware": { "min": "5.16.3", "max": null },
      "requires": { "primitive-launcher": ">=0.3.0" },
      "tested_on": ["KindleOasis3"],
      "assets": {
        "armhf": {
          "url": "https://github.com/DoanNguyenTrong/kindle-primitive-browser/releases/download/v0.2.16/primitive-browser-0.2.16-armhf.zip",
          "sha256": "64 hex characters",
          "size": 4500000
        }
      }
    }
  ]
}
```

Field rules:

- `id`: lower case, `a-z 0-9 -`, unique, never changed.
- `dir`: the app's folder name under `/mnt/us/` (and `/mnt/us/extensions/` for a KUAL part). Defaults to `id`; unique in
  the catalog; never changed. Existing Primitive apps keep their folders: `launcher`, `browser`, `terminal`. Reserved
  and refused: `documents`, `extensions`, `system`, `koreader`, `fonts`, `screensaver`, and any folder the Kindle itself
  uses on `/mnt/us`.
- `source`: `hosted` (our release assets), `upstream` (the author's own release URL, pinned by sha256; we host nothing),
  or `link` (no install: the listing explains how to get it, with a link). D3 decides between them by licence.
- `versions`: newest first. A version is never edited after it is published; a fix is a new version. A broken version
  gets `"withdrawn": "<reason>"`: the store stops offering it and offers the next older version that is not
  withdrawn.
- `assets`: one entry per architecture the version supports: `armhf` (hard-float, firmware 5.16.3 and later) and/or
  `armel` (soft-float, older firmware). The firmware boundary must be confirmed on devices before the first release.
- `requires`: other store apps by id with a version range. Only `>=` ranges in schema 1.
- `changes`: the facts for What this app changes (§5.3). CI checks them against the package where it can (for example,
  hooks present means `hooks: true`).

### 4.5 The package: `<id>-<version>-<arch>.zip`

```
<id>-<version>/
  manifest.json                 the version's entry from app.json, plus "files"
  LICENSE
  INSTALL.md                    how to install by hand (USB), for users without the store
  documents/<Name>.sh           optional: the library entry (header contract below)
  <dir>/...                     the app's folder, installed to /mnt/us/<dir>/
  extensions/<dir>/...          optional: a KUAL extension, installed to /mnt/us/extensions/<dir>/
  hooks/post-install.sh         optional, reviewed (§6.4)
  hooks/pre-uninstall.sh        optional, reviewed
```

`manifest.json` adds `files`: every file the package installs, with its target path, so removal is exact. A package may
only write to these roots: `/mnt/us/<dir>/`, `/mnt/us/extensions/<dir>/`, and `/mnt/us/documents/` (its own entry files).
Anything else needs a hook and `changes.root_filesystem` or a specific `changes` flag.

Library entry header (the launcher's existing contract): `# Name:`, `# Author:`, optional `# Icon:` (PNG data URI), and
`# DontUseFBInk`, in that order, at the top of a `.sh` file in `documents/`.

## 5. Store client (on the Kindle)

### 5.1 Screens

The store follows the `primitive-ui` skill. It opens from a **Store** tile on the launcher's grid. A floating tab bar
(capsule, bottom, 4 tabs) switches between:

1. **Today**: collections from `collections.json`, each a card with its title, sentence and up to four app icons.
2. **Apps**: the category list (cards with icon, name, app count); a category opens a list of app rows.
3. **Updates**: installed apps with a newer version, each with **Update**, and **Update all** at the top; below, the
   installed apps with their version and **Remove**.
4. **Search**: a field with the shared keyboard; results as app rows, matched on name, subtitle, developer and category.

Every tab has a **Refresh** button at the top right that downloads the index again. There is no pull-to-refresh: a
swipe down from the top opens quick settings, as everywhere in the launcher. The store's options (daily update check)
are a **Store** page in the launcher's Settings.

**App row**: icon (rounded square), name, subtitle (gray), and an action capsule at the right: **Get**, **Update**,
**Open**, or **Link** for `link` entries.

**App page** (the product page): icon, name, subtitle, developer; the action capsule; an information strip (version,
size, category, licence); screenshots (two side by side, Previous and Next); description; What's New with the date and
a **Version history** row; **What this app changes** (§5.3); **Information** (developer, repository, licence, size,
architecture, firmware, tested on, requirements, hosted or upstream).

**Install sheet**: a pop-up that names the app, its size, what it changes, and its requirements, with Cancel and Install.
While installing, the pop-up shows the steps (Downloading, Checking, Installing) with the block progress row.

### 5.2 States of an app

`not installed` → `downloading` → `checking` → `installing` → `installed` → (`update available`) → `updating` →
`installed`. Failures return to the previous state with a message that says what failed and what to do. `link` apps are
always `not installed`.

### 5.3 What this app changes

Shown on every app page and in the install sheet, from the listing's `changes`:

| Flag | Text on the page |
|---|---|
| `network` | Uses the internet. |
| `stops_kindle_ui` | Stops the Kindle's own screen while it runs. |
| `starts_at_boot` | Starts when the Kindle starts. |
| `root_filesystem` | Changes the Kindle's system files. |
| `hooks` | Runs its own install steps. |
| none set | Changes nothing outside its own folder. |

Apps in the `system` category, and any app with `starts_at_boot` or `root_filesystem`, show a warning line in the install
sheet and need a second tap to confirm.

### 5.4 Device facts the store reads

| Fact | How | Status |
|---|---|---|
| Architecture | `/lib/ld-linux-armhf.so.3` exists: `armhf`; else `armel` (KindleForge's method). | To confirm on a soft-float device. |
| Firmware version | The Kindle's version file (for example `/etc/prettyversion.txt`). | To confirm on devices. |
| Model | The device code, mapped to a name (KOReader's device detection is the reference). | To design. |
| Free space | `statvfs` on `/mnt/us` (and `/var/local` for the launcher's own update). | Known. |
| Network | The launcher's Wi-Fi state. | Known. |

### 5.5 Files on the device

| Path | Content |
|---|---|
| `/mnt/us/launcher/store/cache/` | `index.json`, `collections.json`, app files, icons and screenshots, with their download date. |
| `/mnt/us/launcher/store/downloads/` | Zips being downloaded (`.part` until complete). Emptied after each install. |
| `/mnt/us/launcher/store/staging/` | Unpacked packages before they are moved into place. |
| `/mnt/us/launcher/store/installed.json` | For each installed app: id, version, arch, install date, source URL, sha256, and the full file list. |
| `/mnt/us/launcher/store/journal` | The step in progress, so an install cut by power loss is finished or undone at the next start. |

## 6. Installer

### 6.1 Install

1. **Resolve**: pick the newest version whose `assets` has the device's architecture and whose `firmware` range includes
   the device. Resolve `requires`; offer to install missing requirements first, newest compatible version.
2. **Check space**: package size × 3 (zip, staging, installed) must fit on `/mnt/us`.
3. **Download** over HTTPS from an allowed host (§8) to `downloads/<file>.part`; rename when complete. Resume if the
   server allows it.
4. **Verify**: sha256 of the zip equals the listing's. A mismatch deletes the file and stops.
5. **Unpack** to `staging/<id>/` in-process. Refuse absolute paths, `..`, links that point outside, and files not in
   `manifest.json`'s `files`.
6. **Journal**, then **move** each part into place (same file system, so each move is a rename). The previous version, if
   any, is kept as `<path>.prev` until step 8.
7. **Register**: entries in `documents/` appear by themselves; the launcher reloads its apps (`set_apps`) and its KUAL
   extensions.
8. **Hooks** (if any): run `post-install.sh` with a time limit. Failure rolls back.
9. **Record** in `installed.json`; delete `.prev` copies, the staging folder and the zip; clear the journal.

### 6.2 Update

The same as install, with the old files kept as `.prev` until the new version is recorded. Files the new version no
longer has are removed after the record. **Update all** runs updates one at a time, requirements first.

### 6.3 Remove

Run `pre-uninstall.sh` if present, delete exactly the files in `installed.json` (and their folders if empty), and
reload the launcher's apps. Files the app created at run time inside its own folder go with the folder; user data
outside it stays. The store refuses to remove an app that another installed app requires, and never removes the launcher.

### 6.4 Hooks

The current Store installs file-copy packages. It rejects hook files before extracting the payload. The future hook
contract requires a `pre-uninstall.sh` alongside `post-install.sh` so the review can check how the system change is undone.

Hooks are shell scripts inside the package, for steps a file copy cannot do (for example writing an upstart job). They
are reviewed in the catalog pull request, run as root with `/` as the working directory and a 60 s limit, and are
declared in `changes`. A hook must be idempotent and must not download anything.

### 6.5 The launcher's own update

The launcher cannot replace itself while it runs. Its update: download and verify as usual, unpack to staging, write a
marker, and restart the launcher through its supervisor (exit code for restart). The supervisor's start copies the
new files into place before starting the launcher, then the launcher's setup step refreshes the boot copy on
`/var/local` (`setup-boot.sh`). If the new launcher fails to start three times, the boot guard's existing fallback
starts the Kindle UI, and the next library start puts `.prev` back.

## 7. Catalog pipeline (CI in `kindle-primitive-catalog`)

On a pull request:

1. Validate every changed `app.json` against the JSON schema (`schema/app.schema.json`).
2. For each new version and architecture: download the asset, check the sha256 and size, open the zip, compare its
   `manifest.json` with the listing, check the file list and the allowed roots, look for hooks.
3. Check the licence: `hosted` needs a licence that allows redistribution (allow list: AGPL, GPL, LGPL, MPL, MIT, BSD,
   Apache, ISC, Unlicense), or an app published by Primitive itself (PolyForm Noncommercial 1.0.0, our licence; we
   hold the copyright). Others must be `upstream` or `link`.
4. Check images: icon 256 × 256 grayscale PNG; screenshots 632 × 840 grayscale PNG; size limits.
5. Post a summary on the pull request: what changed, sizes, flags, hooks to review.

On merge to `main`: build `site/v1/` (index, collections, app files, images) and publish it to GitHub Pages.
A nightly job re-checks that every asset URL still answers with the same sha256 and opens an issue if not.

## 8. Requirements

### 8.1 Functional

| Id | Requirement | Priority |
|---|---|---|
| FR-1 | Show the Today tab with collections from the catalog. | M |
| FR-2 | Show categories and the apps in each. | M |
| FR-3 | Search apps by name, subtitle, developer and category, with the shared keyboard. | M |
| FR-4 | Show an app page with icon, subtitle, action, screenshots, description, What's New, version history, What this app changes, and Information. | M |
| FR-5 | Install a hosted or upstream app: resolve, check space, download, verify sha256, unpack safely, move into place, register, record. | M |
| FR-6 | Refuse an app whose architecture or firmware range does not include the device, and say why. | M |
| FR-7 | Install required apps first, after asking. | M |
| FR-8 | Show installed apps and their versions; remove an app exactly. | M |
| FR-9 | Find updates when the store opens (Wi-Fi on) and show them in Updates; update one or all. | M |
| FR-10 | Roll back an install or update that fails at any step; finish or undo a cut install at the next start (journal). | M |
| FR-11 | Work from the cache without Wi-Fi: browse, read app pages already opened, remove apps. | M |
| FR-12 | Show `link` apps with instructions and their link, without an install button. | M |
| FR-13 | Show a warning and ask twice for `system` apps and apps that start at boot or change system files. | M |
| FR-14 | Update the launcher itself (§6.5). | S |
| FR-15 | A badge on the Store tile when updates are available. | S |
| FR-16 | Check for updates once a day when Wi-Fi is on (Settings > Store, default on). | S |
| FR-17 | Import entries from KindleForge's `registry.json` as `upstream` or `link` listings (a catalog script, reviewed by hand). | L |
| FR-18 | Signatures on packages and on the index (D7, later). | L |
| FR-19 | Install `upstream` listings whose files are not in our package format, from a file layout declared in the listing (which file of the author's zip goes where), pinned by sha256. Not needed by the KindleForge review, which migrates nothing ([store-migration-kindleforge.md](store-migration-kindleforge.md)); kept for a future outside app. | L |

### 8.2 Non-functional

| Id | Requirement | Priority |
|---|---|---|
| NFR-1 | Follows the `primitive-ui` skill: tokens, components, refresh rules, dark mode, rotation. | M |
| NFR-2 | HTTPS only, to an allow list: `github.com`, `objects.githubusercontent.com`, `raw.githubusercontent.com`, `doannguyentrong.github.io`, and the hosts named by `upstream` listings. | M |
| NFR-3 | Every downloaded package is checked by sha256 before it is opened. | M |
| NFR-4 | No secrets in any repo, listing or log: no SSH password, no Wi-Fi keys, no tokens. | M |
| NFR-5 | The store never holds `/mnt/us` open while idle, so USB drive mode keeps working (the launcher's rule). | M |
| NFR-6 | Power loss at any step leaves either the old version or the new one working (journal, staging, renames). | M |
| NFR-7 | Memory: the store adds at most 20 MB to the launcher while open, and nothing while closed. | S |
| NFR-8 | The index loads and shows in under 3 s on Wi-Fi; a cached index in under 1 s. | S |
| NFR-9 | The catalog is static: GitHub Pages and Releases only, no server of ours. | M |
| NFR-10 | Network and unzip code is shared: HTTPS from the browser's `kb-net` moved to `doannt-kindle-tools` (`primitive-net`), zip in-process. No dependency on `curl` or `unzip` on the device. | S |
| NFR-11 | Desktop target renders every store screen to PNG for review. | M |
| NFR-12 | Tests: fixture catalog and packages for install, update, remove, sha mismatch, bad paths, rollback, journal recovery. | M |

## 9. Repos

| Repo (GitHub) | Local folder | Role |
|---|---|---|
| `kindle-primitive` | `doannt-kindle/` | Umbrella: docs, skills, the plan. |
| `kindle-primitive-catalog` | `doannt-kindle-catalog/` | Listings, schema, CI, Pages site. |
| `kindle-primitive-build` | `doannt-kindle-build/` | Reusable release workflow for publishers. |
| `kindle-primitive-launcher` | `doannt-kindle-launcher/` | Store client (`kl-store` crate) and host. |
| `kindle-primtitive-tools` | `doannt-kindle-tools/` | Shared crates, plus `primitive-net` and the store's UI parts when shared. |
| `kindle-primitive-browser`, `kindle-primitive-terminal` | as today | First publishers. |

## 10. Risks specific to the store

- **Self-update of the launcher** can leave a Kindle without its host. Mitigation: §6.5, the boot guard, and a test on the
  Kindle before each launcher release through the store.
- **Soft-float Kindles** need `armel` builds that we do not make yet; until then our apps list `armhf` only and the store
  says so on older Kindles.
- **Upstream links rot** or change their files. Mitigation: pinned sha256, the nightly check, and `link` as the fallback.
- **Licences**: hosting is limited to the allow list (§7); KindleTweaks' Repository is CC BY-NC-SA, so its packages are
  `upstream` or `link` only. Primitive's own apps are under PolyForm Noncommercial 1.0.0 (code) and CC BY-NC-SA 4.0
  (docs and pictures); the store's listings text, icons and screenshots in the catalog are under CC BY-NC-SA 4.0 unless
  a publisher's own licence says otherwise.
- **Hooks run as root**. Mitigation: reviewed in pull requests, declared on the app page, time-limited, no downloads.

## 11. Build checklist

- [ ] Catalog repo with schema, `apps/` for the three apps, CI checks, Pages publishing (FR-1–4 data, NFR-9).
- [ ] Shared release workflow producing `<id>-<version>-<arch>.zip`, `.sha256` and `manifest.json` (plan S2).
- [ ] `primitive-net` in tools (NFR-10).
- [ ] `kl-store` crate: catalog cache, resolver, installer, journal, `installed.json` (FR-5–11, NFR-3, NFR-6).
- [ ] Store screens and desktop screenshots, reviewed by the owner (FR-1–4, FR-12–13, NFR-1, NFR-11).
- [ ] Tests (NFR-12).
- [ ] Device test with the owner watching: install, update, remove the browser; refuse a wrong-architecture package;
      recover from a cut install.
- [ ] Launcher self-update (FR-14) and its device test.
