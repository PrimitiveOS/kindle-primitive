# Add an app to Store

Use this guide to list a Kindle app in Store for PrimitiveOS. Open Store from the Primitive Launcher grid. Listings
live in the shared catalog, and hosted packages are published as GitHub release assets. [Store architecture](store-architecture.md)

## 1. Before you start

Your app can be listed when:

- [ ] It runs on a **jailbroken Kindle e-reader** and you know which architectures it supports: `armhf` (hard-float,
      newer firmware) and/or `armel` (soft-float, older firmware).
- [ ] Its source is in a **public GitHub repo** with a **licence file**.
- [ ] It installs into its own places only: `/mnt/us/<dir>/`, `/mnt/us/extensions/<dir>/`, and its own entry files in
      `/mnt/us/documents/`. Anything else (system files, boot jobs) is done by a reviewed hook and declared (§4.5).
- [ ] It downloads nothing during installation. Everything it installs is in the package.
- [ ] It contains no secrets (passwords, keys, tokens), no tracking, and nothing that targets a specific website or
      service in a way the reviewers cannot explain on the app page.
- [ ] It has been run on at least one Kindle model, which you will list in `tested_on`.
- [ ] It meets the **quality bar**: a real touch interface (nothing to type in a terminal and no configuration files to
      edit to use it); simple for someone who has never jailbroken a device; a kind of app that is popular on iOS or
      Android (productivity, games, everyday tools); and it works with **Primitive Launcher in front**, the Kindle's own
      interface stopped. Apps that run inside the Kindle's own interface (Illusion and other HTML booklets) do not.

First-party PrimitiveOS apps must also follow the `primitive-ui` skill and pass its review checklist.

## 2. Choose how the store gets your app

| Your licence and wishes | `source` | What the store does |
|---|---|---|
| A licence that allows redistribution (AGPL, GPL, LGPL, MPL, MIT, BSD, Apache, ISC, Unlicense), and you publish packages in our format; or a first-party PrimitiveOS app (PolyForm Noncommercial 1.0.0) | `hosted` | Downloads your release asset, checks it, installs it. |
| Any licence; you publish your own release files and do not want them re-hosted, or the licence does not allow it (for example CC BY-NC-SA) | `upstream` | Downloads from **your** release URL, pinned by sha256; we host nothing. Your files must still be in our package format, or installable by the file list and hooks you declare. |
| The app cannot be installed by file copy and reviewed hooks (it needs manual steps, a different jailbreak, or a firmware change) | `link` | Shows the app page with your instructions and a link. No install button. |

When in doubt, start with `link`: it needs no package and can be upgraded later.

## 3. Package your app

### 3.1 Layout

Make one zip per architecture, named `<id>-<version>-<arch>.zip`, holding one folder:

```
<id>-<version>/
  manifest.json
  LICENSE
  LICENSE-DOCS                  when documentation has its own licence
  INSTALL.md
  documents/<Name>.sh           optional: library entry
  <dir>/...                     your app's files, installed to /mnt/us/<dir>/
  extensions/<dir>/...          optional: a KUAL extension
  hooks/post-install.sh         optional
  hooks/pre-uninstall.sh        optional
```

- `id`: lower case letters, digits and `-`, unique in the store, never changed (for example `primitive-browser`).
- `dir`: your folder's name under `/mnt/us/`; it defaults to `id`. Pick it once: it never changes. Folders the Kindle or
  other tools use (`documents`, `extensions`, `system`, `koreader`, `fonts`, `screensaver`) are refused.
- `INSTALL.md`: how to install the zip by hand over USB, for people without the store.
- Library entry: a `.sh` file whose first lines are `# Name: <Name>`, `# Author: <You>`, optionally
  `# Icon: data:image/png;base64,...`, and `# DontUseFBInk`. Primitive Launcher shows it on the grid.

### 3.2 `manifest.json`

The version's entry from your listing (§4) plus the list of files the package installs:

```json
{
  "schema": 1,
  "id": "primitive-browser",
  "dir": "browser",
  "version": "0.2.16",
  "arch": "armhf",
  "firmware": { "min": "5.16.3", "max": null },
  "requires": { "primitive-launcher": ">=0.3.0" },
  "files": [
    "documents/Browser.sh",
    "browser/kb-kindle",
    "browser/fonts/NotoSans-Regular.ttf"
  ],
  "hooks": []
}
```

`files` lists every file in the zip except `manifest.json`, `LICENSE`, `LICENSE-DOCS`, `INSTALL.md` and `hooks/`. The store installs
exactly these and removes exactly these.

### 3.3 Build it in CI

The shared workflow in `kindle-primitive-build` tests and builds the app, packages each selected architecture, writes
the `.sha256` files, and publishes on a version tag. Pin an approved workflow revision in `.github/workflows/release.yml`:

```yaml
on:
  push:
    tags: ["v*"]
jobs:
  release:
    uses: DoanNguyenTrong/kindle-primitive-build/.github/workflows/package.yml@9533d481058f4d67b29568f40b30017ddcb32c8e
    permissions:
      contents: write
    with:
      id: primitive-browser
      dir: browser
      binary-crate: kb-kindle
      arches: armhf
      install-file: docs/INSTALL.md
      changelog-file: docs/CHANGELOG.md
      docs-licence-file: LICENSE-DOCS
```

To package locally, use the shared packager with your staged files. [Build guide](https://github.com/DoanNguyenTrong/kindle-primitive-build)

### 3.4 Release

- Tag `v<version>`, and the tag must equal the version in your build files and `manifest.json`.
- Attach `<id>-<version>-<arch>.zip` and `<id>-<version>-<arch>.zip.sha256` for each architecture.
- Never replace a published asset. A fix is a new version.

## 4. Write the listing

### 4.1 Files

In a fork of `kindle-primitive-catalog`, add a folder `apps/<id>/`:

```
apps/<id>/
  app.json
  icon.png
  shots/1.png
  shots/2.png
```

### 4.2 `app.json`

The full schema and an example are in [store-architecture.md](store-architecture.md) §4.4. Fill in:

| Field | Write |
|---|---|
| `name` | The app's display name, as on the Kindle's grid. Keep its existing package ID when changing this label. |
| `subtitle` | One line, at most 40 characters, that says what it is for. |
| `developer` | Your name and a link (your GitHub profile). |
| `categories` | One primary category from the store's list, and at most one more (§4.3). |
| `description` | Two to five short paragraphs in plain text. What it does, what it does not, how to start it. |
| `repo`, `licence` | Your repo URL and the SPDX id of your licence. |
| `source` | `hosted`, `upstream` or `link` (§2). |
| `changes` | The facts for "What this app changes" (§4.5). |
| `versions` | Newest first: version, date, What's New (one to five lines), firmware range, requirements, `tested_on`, and for each architecture the asset URL, sha256 and size. |

For a `link` app, `versions` holds the current version without `assets`, and `description` ends with the steps to
install it by hand.

### 4.3 Categories

`reading`, `productivity`, `internet`, `games`, `audio`, `creativity`, `developer`, `utilities`, `system`. What belongs
in each is in [store-architecture.md](store-architecture.md) §4.1. Use `system` for anything that changes how the Kindle
starts or runs; the store shows those apps with a warning.

### 4.4 Icon and screenshots

- `icon.png`: 256 × 256, grayscale, square, no rounded corners (the store rounds them), readable at 64 px.
- `shots/<n>.png`: 632 × 840 (half of the 1264 × 1680 screen), grayscale, portrait, one to five of them. Take them from
  the device or from the app's desktop target. No device frames, no text over the picture.

### 4.5 What this app changes

Set each flag that is true. Reviewers check them against the package.

| Flag | Set it when the app |
|---|---|
| `network` | Uses the internet at any time. |
| `stops_kindle_ui` | Stops the Kindle's own interface while it runs (as Primitive Launcher does). |
| `starts_at_boot` | Starts when the Kindle starts (an upstart job or similar). |
| `root_filesystem` | Writes to the Kindle's system files (anything outside `/mnt/us` and `/var/tmp`). |
| `hooks` | Declares both `post-install.sh` and `pre-uninstall.sh`. |

Use `notes` for one sentence of detail, for example "Writes /etc/upstart/primitive-launcher.conf".

Hooks are shell scripts of up to 64 KiB each. They run as root with a 60-second limit, must complete in the
foreground, and must avoid network access. Both scripts must be idempotent. The uninstall script must undo what
the install script did, including after a partial failure.

The manifest and archive require the exact pair when either hook is declared. The Kindle runtime requires a
root-owned approval for the exact release and both script digests. The Mac Store fixtures exercise the transaction
without executing package scripts. [Runtime approval format](store-architecture.md#64-hooks)

## 5. Check and open the pull request

1. Run `sh scripts/check-app.sh apps/<id>` from the catalog repository.
2. Commit only your app's folder and open a pull request titled `Add <name> <version>` or `Update <name> to <version>`.
3. The pull request template asks you to confirm the checklist in §1 and to say on which Kindle you tested.
4. CI posts a summary: sizes, flags, hooks, licence result. Fix anything it reports.
5. A reviewer reads the summary, the hooks, and the app page text, and installs the app on a Kindle for `system` apps and
   apps with hooks.
6. On merge, the catalog site is rebuilt and the app appears in the store at its next refresh.

## 6. What the checks and reviewers look at

Automatic (CI):

- `app.json` matches the schema; `id` is new (or the folder's), categories are known, text lengths are within limits.
- Each new asset downloads, its sha256 and size match, the zip opens, `manifest.json` matches the listing, every file is
  listed and inside the allowed roots, no absolute paths, no `..`, no links outside the package.
- The licence allows `hosted`, or `source` is `upstream` or `link`.
- The icon and screenshots have the right size and are grayscale.

By a reviewer:

- The description says plainly what the app does; the `changes` flags are true and complete.
- Hooks do only what `notes` says and can be undone.
- Nothing in the package targets a specific site or service without a reason stated on the app page, and nothing breaks
  the law or the Kindle owner's own interests.
- For `system` apps: an install, a restart, and a removal on a Kindle.

## 7. Update, withdraw, or remove an app

- **Update**: release the new version (§3.4), then add it at the **top** of `versions` in `app.json` and open a pull
  request `Update <name> to <version>`. Preserve earlier published releases.
- **Rename a repository**. Follow the [listing contract](contracts.md#5-the-listing-appsidappjson-in-the-catalog)
  to move repository and asset links while preserving the package identity. Verify the package at each new URL before publishing.
- **Withdraw a broken version**: add `"withdrawn": "<reason>"` to that version. The store stops offering it and offers
  the next older one. Installed copies are not removed; the Updates tab offers the next good version when there is one.
- **Remove the app**: open a pull request that deletes `apps/<id>/` and says why. Installed copies stay on Kindles and can
  be removed from the store's Updates tab; the `id` stays reserved.

## 8. Extra steps for first-party PrimitiveOS apps

- Version rules: every device build bumps the patch version; a new phase bumps the minor; tags `vX.Y.Z` are never moved.
- Before a release: tests pass, the desktop screenshots are reviewed by the owner, and the owner has tested the device
  build on the Kindle.
- The app's `CHANGELOG.md` entry becomes the version's What's New, shortened to five lines at most.
- Scan the staged files for secrets before every push (the SSH password and Wi-Fi keys must never appear).

The owner approved publication of the 20 November 2026 **Study and work** release. The eleven releases went live
after desktop and package checks with empty `tested_on` fields. Their Kindle verification remains open.
[Study and work release verification](local-verification.md#study-and-work-release-verification)
