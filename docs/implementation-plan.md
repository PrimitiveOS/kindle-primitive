# Implementation plan: Primitive Store, our apps, and the native apps

Status date: 2026-11-19. On the Kindle: Primitive Launcher **v0.3.21**, Primitive Browser **v0.2.17**, Primitive Terminal
**v0.1.8**. Decisions D1–D7 are taken ([kindle-platform-plan.md](kindle-platform-plan.md) §4). This is the tracking
document for all the work; the design behind it is in [store-architecture.md](store-architecture.md), and the app choices
in [store-migration-kindleforge.md](store-migration-kindleforge.md).

How to read the checklists (the same as the launcher's plan):

- `[x]` done and confirmed on the Kindle by the owner.
- `[x] … (Mac)` done and tested on the Mac, not yet confirmed on the Kindle.
- `[ ]` not done.

A milestone is finished when every item is `[x]` without "(Mac)". A track ends with a gate that the owner checks on the
Kindle. Every device build bumps the patch version; a new phase of an app starts a new minor version; new apps start at
0.1.0; tags `vX.Y.Z` are never moved. Nothing is tagged, released, listed or pushed to a public catalog without the
owner's go-ahead. Device findings go into each repo's `docs/device-notes.md`.

## Overview

| Milestone | Track / repo | State |
|---|---|---|
| [A1 Umbrella repo](#a1-umbrella-repo) | A Foundations / `kindle-primitive` | **Done**, on GitHub (`8be0056`) |
| [A2 Contracts and schemas](#a2-contracts-and-schemas) | A / `kindle-primitive` | **Done** (contracts, three schemas, examples, tests); owner's read pending |
| [A3 Repo upkeep and licences](#a3-repo-upkeep-and-licences) | A / all repos | Licences done for launcher, browser, tools |
| [A4 Device spikes](#a4-device-spikes) | A / device | 5 of 9 answered (2026-11-19); A4.4 HTTPS, A4.5 keep awake, A4.6 Bluetooth, A4.7 jailbreak status, A4.9 fast updates open |
| [B1 Shared build workflow](#b1-shared-build-workflow) | B Packaging / `kindle-primitive-build` | Packager and workflow written and tested locally; repo not on GitHub yet |
| [B2 Our three apps packaged](#b2-our-three-apps-packaged) | B / launcher, browser, terminal | Launcher zip exists (old format) |
| [B3 Soft-float builds](#b3-soft-float-builds) | B / all apps | Not started |
| [C1 Catalog repo and pipeline](#c1-catalog-repo-and-pipeline) | C Catalog / `kindle-primitive-catalog` | Built and tested locally (commit `c83704c`); repo not on GitHub yet |
| [C2 First listings](#c2-first-listings) | C / `kindle-primitive-catalog` | Not started |
| [D1 Shared network crate](#d1-shared-network-crate) | D Store / tools | `primitive-net` on tools `main` (`241a527`), tested on the Mac |
| [D2 Store engine](#d2-store-engine) | D / launcher (`kl-store`) | On launcher `main`: catalog refresh (`0f9154b`) and install (`083c9d8`), 40 store tests; not deployed |
| [D3 Store screens](#d3-store-screens) | D / launcher | On launcher `main`: App Store layout (Today, Apps, Updates, product page), icons and screenshots; reviewed screens in `docs/store-screens/` |
| [D4 Store on the Kindle](#d4-store-on-the-kindle) | D / device | Code on `main`, tested on the Mac; the device test waits for the 0.4.0 build |
| [D5 Our apps through the store](#d5-our-apps-through-the-store) | D / launcher, browser, terminal | Not started |
| [E1 Device layer in the kit](#e1-device-layer-in-the-kit) | E App kit / tools | Not started |
| [E2 Interface components](#e2-interface-components) | E / tools | Not started |
| [E3 Text editing](#e3-text-editing) | E / tools | Not started |
| [E4 App lifecycle](#e4-app-lifecycle) | E / tools | Not started |
| [E5 App template](#e5-app-template) | E / `kindle-primitive-app-template` | Not started |
| [F1–F13 Native apps](#f-native-apps-phase-s6) | F / one repo each | Not started |
| [G1–G3 Launcher features](#g-launcher-features) | G / launcher | Not started |
| [H1–H5 Hardening](#h-hardening-phase-s7) | H / all | Not started |

Order of work:

1. **A1–A3** now (Mac and GitHub), **A4** when the Kindle is at hand.
2. **B1–B2** and **E1–E2** in parallel on the Mac.
3. **C1–C2**, then **D1–D4**: **Gate D**, the store installs an app on the Kindle.
4. **E3–E5**: **Gate E**, a new app from the template installs from the store and runs.
5. The first native apps: **F1 Notes**, **F2 Focus**, **F3 Words** (M-D7).
6. **D5** (our apps and the launcher's self-update through the store) and **G1**.
7. The other native apps and launcher features, in the owner's order.
8. **H** last, and whenever a second Kindle is available.

---

## A. Foundations (phase S1)

### A1 Umbrella repo

- [x] Folder `doannt-kindle/` with the four app repos side by side; `git init` with the app repos ignored (Mac).
- [x] Documents: platform plan, store architecture, submission guide, install guide, migration review, this plan (Mac).
- [x] Skills in `.agents/skills` (`primitive-ui`, `kindle-device`, `kindle-eink`), linked as `.claude/skills` (Mac).
- [x] README "Primitive Redefined Kindle" and the CC BY-NC-SA 4.0 `LICENSE` for docs and skills (Mac).
- [x] `.gitignore` ignores every app folder by pattern (`/doannt-kindle-*/`), so new app repos need no change.
- [x] First commit (`8be0056`); remote `https://github.com/DoanNguyenTrong/kindle-primitive.git` (public); pushed.

### A2 Contracts and schemas

- [x] `docs/contracts.md`: library entry header, module folder and `dir`, package layout, manifest, listing, catalog
      index, device choice of package, versions (Mac).
- [x] JSON schemas: `schema/app.schema.json`, `schema/manifest.schema.json`, `schema/index.schema.json` (Mac).
- [x] Examples that pass the schemas: `schema/examples/primitive-launcher.app.json` (hosted),
      `koreader.app.json` (link), `primitive-launcher.manifest.json` (Mac). Validated by `schema/scripts/validate.py`.
- [x] Negative tests: absolute paths, `..`, reserved folders, unknown architectures, missing or insecure assets,
      over-long subtitles, duplicate categories and link listings with assets are all refused (Mac).
      Found and fixed while testing: KOReader's date versions (`2026.10`) were refused, so the version pattern now allows
      them; `system/` was accepted in a manifest, so reserved folders are now excluded in the pattern.
- [ ] The owner reads the contracts (Gate A).

### A3 Repo upkeep and licences

- [x] Launcher: PolyForm Noncommercial 1.0.0 (code), CC BY-NC-SA 4.0 (docs, pictures); v0.3.21 on `main` (`cdc09c2`).
- [x] Browser: the same licences; v0.2.17 on `main` (`f3ae822`).
- [x] Tools: AGPL-3.0 or PolyForm Noncommercial 1.0.0 (`1ed99a0`).
- [ ] Terminal: add the AGPL-3.0 `LICENSE` file (its engine is ported from KOReader's terminal) and a README licence
      section; move its `tools` submodule to `1ed99a0`.
- [ ] Terminal and tools: CI (`cargo test`, clippy) on GitHub Actions, as the launcher and browser have.
- [ ] Release tags for launcher `v0.3.21` and browser `v0.2.17`, if the owner wants published releases with the new
      licences.
- [ ] Check the release CI result for launcher `v0.3.12` and `v0.3.20` (Actions tab; `gh` is not installed here).
- [ ] Browser: decide on `deploy/fix-hosts-truyendich.sh` (keep out of releases, or remove from the repo) (R4).
- [ ] Browser: the untracked `docs/tinhte/` folder is the owner's; commit it or leave it out.
- [ ] Tools: keep the remote name `kindle-primtitive-tools` or rename it (GitHub redirects the old name).
- [ ] Decide whether Primitive Terminal is a store app (it is a developer tool; the quality bar favours everyday apps).

### A4 Device spikes

Each answer goes into the launcher's `docs/device-notes.md` with the date.

- [x] A4.1 Architecture (2026-11-19): the Oasis 3 is `armv7l` with `/lib/ld-linux-armhf.so.3` present (hard-float). A
      soft-float Kindle is still needed to confirm the `armel` case.
- [x] A4.2 Firmware (2026-11-19): `/etc/prettyversion.txt` reads `Kindle 5.18.2 (…)`; `/etc/version.txt` reads
      `System Software Version: 025-juno_1802_stinger_zelda-…`. Both read with the stock UI running; reading with the
      framework stopped is still to check.
- [x] A4.3 Device identity (2026-11-19): there is no model code the store can read. The device type is "Kindle Oasis –
      10th Gen" in the stock help, which is the Oasis 3, so the store uses the name `KindleOasis3`. Wi-Fi MAC and serial
      number exist (`/sys/class/net/wlan0/address`, `androidboot.serialno`) and are never recorded. Details in the
      launcher's `docs/device-notes.md`.
- [ ] A4.4 HTTPS from a Rust binary on the Kindle: TLS with bundled root certificates (as the browser's `kb-net` does);
      download speed and memory for a 5 MB file.
- [ ] A4.5 Keep the screen awake with the framework stopped (for Focus): the launcher's own sleep handling, or
      `com.lab126.powerd preventScreenSaver`.
- [ ] A4.6 Bluetooth radio on the Oasis 3: from the stock UI first (the launcher plan's "Later" item); decides G3.
- [ ] A4.7 Jailbreak status signals: how to tell the hotfix is installed and updates are blocked; decides G1.
- [x] A4.8 Free space (2026-11-19): `/mnt/us` 4.9 GB free of 6.1 GB; `/var/local` 164 MB free of 240 MB. Write speed
      not measured yet. The installer needs about 3× the package size.
- [ ] A4.9 Fast e-ink updates for a falling-blocks game: how often a small rectangle can be redrawn with the fastest
      waveforms (DU, A2) on the Oasis 3, how much ghosting builds up, and how often a full refresh is needed; decides
      the speed levels of F13.
- [ ] **Gate A**: contracts read by the owner; licences complete; spikes A4.1–A4.4 answered (A4.1, A4.2 answered; A4.3,
      A4.4 open).

---

## B. Packaging (phase S2)

### B1 Shared build workflow

Repo `kindle-primitive-build` (local `doannt-kindle-build`).

- [ ] Reusable workflow `package.yml`: inputs `id`, `dir`, `binary-crate`, `arches`; pins zig and cargo-zigbuild as the
      launcher's release workflow does; checks out submodules.
- [ ] Steps: test, build per architecture (`armv7-unknown-linux-musleabihf`; `armel` target after B3), run the app's
      `scripts/package.sh`, write `manifest.json` (file list, sha256), zip as `<id>-<version>-<arch>.zip`, `.sha256`.
- [ ] Tag check: the tag equals the version in `Cargo.toml` and `manifest.json`.
- [ ] Publish the GitHub Release on a `v*` tag; attach zips and `.sha256`.
- [ ] Secret scan step (fails the job if a configured pattern appears in the package).
- [ ] Versioned with tags (`@v1`), so apps pin it.

### B2 Our three apps packaged

- [ ] Launcher: `scripts/package.sh` for the new layout (`launcher-<v>/manifest.json`, `launcher/`, `documents/Launcher.sh`,
      `LICENSE`, `LICENSE-DOCS`, `INSTALL.md`); `changes`: network, stops the Kindle UI, starts at boot, system files
      (boot job). `release.yml` calls B1.
- [ ] Browser: the same (`dir` = `browser`; FBInk and its GPL-3.0 licence inside); `changes`: network.
- [ ] Terminal: the same (`dir` = `terminal`); first release workflow; `changes`: none beyond its folder.
- [ ] Each app's zip unpacked and checked by the owner (**Gate B**).

### B3 Soft-float builds

- [ ] Choose the Rust target for `armel` (soft-float ARMv7 or ARMv6 musl) and check zig's support.
- [ ] Build launcher, browser and terminal for it in CI; note anything that does not build (vello's SIMD paths, QuickJS).
- [ ] Test on a soft-float Kindle (needs a device; until then listings declare `armhf` only).

---

## C. Catalog (phase S3)

### C1 Catalog repo and pipeline

Repo `kindle-primitive-catalog` (local `doannt-kindle-catalog`).

- [ ] Layout: `apps/<id>/app.json`, `icon.png`, `shots/`; `collections.json`; `schema/`; `scripts/`.
- [ ] `scripts/check-app.sh`: schema, ids, categories, text lengths, images (256 × 256 icon; 632 × 840 grayscale shots).
- [ ] Pull request CI: download each new asset, check sha256 and size, open the zip, compare `manifest.json`, check
      allowed roots and paths, find hooks, check the licence against the allow list; post a summary comment.
- [ ] `scripts/build-index.sh`: `site/v1/index.json`, `collections.json`, `apps/<id>.json`, icons, shots.
- [ ] Publish `site/` to GitHub Pages on merge to `main` (`doannguyentrong.github.io/kindle-primitive-catalog/v1/`).
- [ ] Nightly job: every asset URL still answers with the same sha256; open an issue if not.
- [ ] Pull request template with the submission checklist (store-submit-app §1).

### C2 First listings

- [ ] Primitive Launcher, Primitive Browser (and Primitive Terminal if A3 says so): `app.json`, icon, 2–5 screenshots
      from the desktop targets, What's New from the changelog.
- [ ] KOReader as a `link` listing (category `reading`, links to `koreader.rocks` and its releases).
- [ ] Collections: "Start here" (launcher, browser, KOReader), "Made by Primitive".
- [ ] **Gate C**: Pages serves `index.json`; each listed asset's sha256 matches its release.

---

## D. Store (phases S4 and S5)

The store is a new phase of the launcher: its first device build starts a new minor version
(`scripts/build-device.sh --minor`).

### D1 Shared network crate

- [x] `primitive-net` in `doannt-kindle-tools` (branch `feature/primitive-net`, `241a527`): downloads with an allow list,
      HTTPS only, redirects checked by hand, size limits, progress, `.part` files (Mac).
- [ ] Not done: resume of partial downloads; bundled root certificates on the Kindle (A4.4 device check).
- [x] Tests on a local HTTP server (Mac); HTTPS on the Kindle is still to check (A4.4).
- [ ] The browser uses `primitive-net` where it overlaps (later, no behaviour change).

### D2 Store engine

Crate `kl-store` in the launcher.

- [x] Models for the index, listings, manifests, `installed.json`; parsers with tests (Mac).
- [x] Catalog cache in `launcher/store/cache/` (index, listings, icons, screenshots); refresh by the Refresh button, on a thread, refused without Wi-Fi (Mac tests; the catalog's own build output is checked by a test). Not yet: refresh on open and the daily check.
- [ ] Device facts (A4.1–A4.3): architecture, firmware, model; free space.
- [x] Resolver: newest version for the architecture and firmware; `requires` with `>=`; withdrawn versions skipped (Mac).
- [x] Installer (Mac): verify sha256 and size (`verify.rs`), unpack in-process to `staging/` with path checks and the
      manifest's file list (`unpack.rs`), journal, rename into place keeping `.prev`, record, clean up (`install.rs`).
- [x] Download through `primitive-net`, checks, install, and the library reload (apps and icons), done on the Mac (`083c9d8`).
- [ ] Installer, still to do: hooks with a 60 s limit, and Remove on the product page (the engine's remove exists).
- [ ] Update (old files kept until the new version is recorded) and Update all (requirements first).
- [x] Remove (exact files; refuses an app another app requires) (Mac). The launcher is refused by the caller, not yet wired.
- [x] Journal recovery: an unfinished install is undone, or finished when the record was saved (Mac; `recover`).
- [x] Tests (Mac, 30): install, update, remove, sha and size mismatch, bad paths, `//` in names, links, two top
      folders, size limits, rollback at each step, power-cut recovery in both states, dependency refusal, damaged record;
      and a test that reads a package made by the build packager (`KL_TEST_PACKAGE`).

### D3 Store screens

Following the `primitive-ui` skill; reviewed as desktop screenshots before any device build.

- [x] Store tile on the grid, after Settings (Mac, `a4e47f7`). The badge for updates is not done.
- [ ] Floating tab bar: Today, Apps, Updates, Search; Refresh at the top right of each tab.
- [ ] Today: collection cards. Apps: category cards, then app rows. App row: icon, name, subtitle, action capsule
      (Get, Update, Open, Link).
- [x] App page: icon, subtitle, developer and licence, status, description, what the app changes, action (Mac).
      Not yet: the information strip, screenshots with Previous and Next, What's New, Version history, Information.
- [x] The action on the page: Get asks the device for the download; until D2's download is wired the screen says it is
      not in this build (Mac). Not yet: the install sheet, its warnings and confirmation, the progress steps.
- [ ] Updates: Update all, per-app Update, installed list with Remove (confirmation pop-up).
- [ ] Search with the shared keyboard; results as app rows.
- [ ] Settings › Store page: daily update check (default on), clear the cache.
- [ ] Dark mode and upside-down checked; desktop screenshots in `docs/images/` (Mac).

### D4 Store on the Kindle

- [ ] Install the browser from the store (from a test catalog first), open it, return, update it, remove it.
- [ ] A package for the wrong architecture is refused with the reason.
- [ ] Power off during an install; the next start finishes or undoes it.
- [ ] USB drive mode while the store is idle (the store holds nothing open on `/mnt/us`).
- [ ] Memory with the store open stays under the launcher's budget + 20 MB.
- [ ] **Gate D**: the owner installs, updates and removes an app from the store on the Kindle.

### D5 Our apps through the store

- [ ] Browser and terminal (if listed) install and update from the public catalog.
- [ ] Launcher self-update: unpack to staging, marker, restart through the supervisor, files moved before the start,
      `setup-boot.sh` refreshes `/var/local`, `.prev` restored after three failed starts.
- [ ] Each app's `INSTALL.md` puts the store first and keeps USB and SSH as fallbacks.
- [ ] **Gate D5**: all our listed apps install, update and remove through the store; one launcher self-update on the
      Kindle.

---

## E. App kit (enables the native apps)

Shared crates in `doannt-kindle-tools`, taken from the launcher and the browser, so each new app is small. Dual-licensed
like the rest of tools.

### E1 Device layer in the kit

- [ ] `primitive-eink`: framebuffer, the Oasis 3 update call, waveforms, rectangle and full refreshes (from
      `kl-kindle/eink.rs`).
- [ ] `primitive-input`: touch (tap, long press, swipe), buttons, rotation of touch points (from `kl-kindle/input.rs`).
- [ ] `primitive-device`: battery, Wi-Fi state, accelerometer turn, sleep and wake, keep awake (A4.5).
- [ ] Device profiles beyond the Oasis 3 (screen size, rotation, input device), filled as devices are tested.

### E2 Interface components

- [ ] `primitive-ui` crate: the renderer (vello_cpu and parley, as `kl-render`), tokens from the skill as constants.
- [ ] Components: text, buttons, cards and rows, switches, chevrons, section headers, pop-ups with halo, sheets, tab
      bar, paged lists, status bar, block progress, full-screen message, icons (24-unit paths).
- [ ] Dark mode inversion that keeps pictures; pressed state; rectangle refresh hints.
- [ ] Desktop output to PNG for every component (a gallery page for review).

### E3 Text editing

- [ ] Single-line field (exists in the launcher for Wi-Fi; moved to the kit).
- [ ] Multi-line editor: cursor, insert and delete, line wrap, scrolling by page, cursor moves by tap; tuned for e-ink
      (redraw only the changed lines). Needed by Notes.

### E4 App lifecycle

- [ ] Event loop with timers that only fire when something changes on screen.
- [ ] Start from the library entry and from the launcher's grid; leaving returns to the launcher (supervisor exit codes).
- [ ] State saved on sleep and exit; settings file per app in its folder; log file.
- [ ] Runs from a copy in `/var/tmp`, so `/mnt/us` stays free for USB drive mode (the launcher's rule).

### E5 App template

Repo `kindle-primitive-app-template`.

- [ ] Workspace: `<x>-core` (state, logic, tests), `<x>-render`, `<x>-kindle`, `<x>-desktop`, using E1–E4.
- [ ] `scripts/package.sh`, `release.yml` calling B1, `app.json` stub, icon, README (licences: PolyForm Noncommercial
      for code, CC BY-NC-SA 4.0 for docs), `CHANGELOG.md`, `docs/device-notes.md`.
- [ ] A "Hello" app made from it.
- [ ] **Gate E**: the Hello app installs from the store, opens from the grid, sleeps and wakes, returns to the launcher,
      and is removed.

---

## F. Native apps (phase S6)

Each app is its own repo (`kindle-primitive-<name>`, local `doannt-kindle-<name>`), made from the template (E5), with
its own versions from 0.1.0. Every app milestone includes the **definition of done** below, plus its own items.

**Definition of done for an app release**

- [ ] Desktop screenshots of every screen reviewed by the owner before the first device build.
- [ ] The `primitive-ui` review checklist passed (tokens, touch targets, way back, refresh, dark mode, upside down).
- [ ] Core logic covered by tests on the Mac.
- [ ] Works with Primitive Launcher in front; leaving returns to the launcher; sleep and wake keep the state.
- [ ] Packaged by B1; listing in the catalog with icon, screenshots, `changes`, `tested_on`.
- [ ] Device gate: the owner installs it from the store, uses it for a day, and removes it.

### F1 Primitive Notes (productivity; like Apple Notes)

- [ ] Notes list (newest first, pinned on top), new note, open, edit with the multi-line editor (E3), delete with Undo.
- [ ] Search across notes. Plain text files in `/mnt/us/notes/` (copyable over USB), names from the first line.
- [ ] Autosave; nothing lost on sleep, power off, or leaving.

### F2 Primitive Focus (productivity; like the Clock app's timer and Pomodoro apps)

- [ ] Focus and break timer, presets 25/5 and 50/10, custom lengths; start, pause, reset.
- [ ] Large countdown redrawn once a minute (calm e-ink); keep awake while running (A4.5); a clear end screen.
- [ ] Today's focus count and total.

### F3 Primitive Words (game; like Wordle)

- [ ] Six guesses for a five-letter word, shared keyboard with letter states, marks that read in black and white.
- [ ] Daily word and free play; statistics and streak.
- [ ] Word lists: from KWordle's MIT lists (credited), English first; the answer and guess lists' licences checked.

### F4 Primitive Cards (productivity; like AnkiMobile, Quizlet)

- [ ] Decks and cards; create cards with the keyboard; review with spaced repetition (a published algorithm, for
      example SM-2), large card faces.
- [ ] Import of Anki decks (`.apkg`: text fields first; media later); export.
- [ ] Statistics per deck.

### F5 Primitive Calculator (tool; like Calculator)

- [ ] Standard calculator with large keys, history, copy of the result; exact decimal arithmetic.

### F6 Primitive Sudoku (game)

- [ ] Puzzle generator with unique solutions and difficulty levels; notes mode; mistakes check; undo.

### F7 Primitive Chess (game; play against the Kindle)

- [ ] Board with tap-to-move, legal moves shown, undo, levels.
- [ ] Engine: our own search, or a move generator and engine with a licence that fits PolyForm (MIT, Apache, BSD);
      GPL engines such as Stockfish are excluded. Licence checked before use.
- [ ] Save and resume a game; PGN export.

### F8 Primitive Minesweeper (game)

- [ ] Classic board sizes; tap to reveal, long press to flag; first tap is safe; timer and best times.

### F9 Primitive Solitaire (game; Klondike)

- [ ] Tap-to-move (no dragging needed), draw one or three, undo, auto-finish; card faces drawn for e-ink.

### F10 Primitive Crossword (game; like crossword apps)

- [ ] Grid and clue list; type with the shared keyboard; check and reveal.
- [ ] Puzzles: bundled free or self-made puzzles (licence recorded for each), and opening `.puz` files the user has.

### F11 Primitive Blocks (game; like 1010! and Woodoku)

- [ ] Place three pieces per turn on a 9 × 9 grid; clear rows, columns and boxes; score and best score.
- [ ] Our own visual design (no copy of other games' look).

### F12 Primitive Ships (game; Battleship)

- [ ] Place ships (manual or random), play against the Kindle at three levels, hot-seat for two.

### F13 Falling-blocks game (game; like Tetris) (owner, 2026-11-19)

- [ ] Name and look of our own: not called "Tetris" (The Tetris Company's trademark), and no copy of its look (its
      colours, piece textures, screens); a working name until the owner picks one. The owner checks the name and look
      before the first public listing.
- [ ] A4.9 answered first; the game's speed levels follow what the panel can show (pieces move in clear steps, not
      smooth motion).
- [ ] Controls for touch and the page buttons: left, right, rotate, soft drop, hard drop; large touch zones.
- [ ] Only the changed cells are redrawn with a fast waveform; a full refresh at line clears or every few seconds to
      clear ghosting; pause on sleep.
- [ ] Scoring, levels, next piece, hold, best scores.

---

## G. Launcher features

### G1 Jailbreak status in Settings › About

- [ ] After A4.7: show whether the hotfix is installed and updates are blocked, with a link to the KindleModding wiki.

### G2 Wi-Fi file transfer

- [ ] A Settings page that starts a small web server while it is open, shows an address and a code, and accepts files
      from a phone or computer on the same network into `documents/`.
- [ ] Stops when the page closes; refuses everything without the code; size limit; no path outside `documents/`.

### G3 Bluetooth keyboard

- [ ] Only if A4.6 finds a working radio: pair a keyboard in Settings; typing in the shared text fields.

---

## H. Hardening (phase S7)

- [ ] H1 Signatures on packages and the index (D7, later): key handling, verification in the store.
- [ ] H2 Other Kindles: architecture and firmware checks on a soft-float Kindle and a second hard-float model.
- [ ] H3 Recovery: bad packages (wrong sha, wrong device, missing file, bad paths) refused; the launcher still starts;
      the boot guard after a failed self-update.
- [ ] H4 Catalog health: the nightly check's issues are answered; withdrawn versions handled.
- [ ] H5 Review of the installer's security (paths, archive limits, hooks, network allow list).
- [ ] **Gate H**: a bad package is refused on the Kindle and the launcher still starts.

---

## Later

Not scheduled. Each item is picked up when the owner asks for it.

- [ ] Primitive Sketch (drawing with real finger drags), after the kit has a fast drawing path.
- [ ] More collections and categories as apps arrive.
- [ ] Apps and listings in other languages.
- [ ] A full-screen terminal mode in Primitive Terminal (would let terminal programs run; kTerm is not planned).

---

## Feasibility

| Part | Feasibility | Why |
|---|---|---|
| Catalog on GitHub Pages and Releases | High | Static files; CI does the checks. |
| Shared build workflow | High | The launcher's release workflow already builds and packages. |
| Store engine (download, verify, install) | High | Rust in-process; the launcher already reloads apps after changes. |
| HTTPS on the Kindle | Medium-high | The browser does HTTPS today; to confirm for downloads (A4.4). |
| Launcher self-update | Medium | Replacing the running host needs the supervisor's help and a tested rollback. |
| Soft-float builds | Medium | Toolchain support and a test device both needed. |
| App kit from existing code | High | The device layer and renderer exist in the launcher and browser. |
| Multi-line text editing on e-ink | Medium | New component; refresh cost while typing. |
| Turn-based games | High | Fit e-ink; logic is testable on the Mac. |
| Falling-blocks game (F13) | Medium | Needs fast partial updates; ghosting limits the speed (A4.9). |
| Chess engine with a fitting licence | Medium | Must be our own or permissively licensed. |
| Bluetooth keyboard | Unknown | The Oasis 3's radio is unconfirmed (A4.6). |

## Test strategy

| Level | What | Where |
|---|---|---|
| Unit | Parsers, resolver, installer steps, game and app logic, keyboard and editor | Mac, `cargo test` |
| Fixtures | Catalog and package fixtures for the store engine; bad packages | Mac |
| Screenshots | Desktop targets render every screen to PNG for the owner's review | Mac |
| CI | Build, tests, packaging, catalog checks, nightly asset check | GitHub Actions |
| Device | Milestone checklists and gates, with the owner watching; logs per app | Kindle |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| A failed launcher self-update | Low | Kindle falls back to the stock UI | Staging, `.prev`, boot guard, device test before each release |
| Only one test Kindle (Oasis 3) | High | Other models untested | `tested_on` per app; H2 when devices are available; listings say what was tested |
| Packages hold `/mnt/us` open | Medium | USB drive mode breaks | Run from `/var/tmp`; the store holds nothing open while idle |
| Licence mix-ups in new apps | Medium | Cannot publish | Licence checks before using any outside code; tools dual-licensed |
| Falling-blocks game looks like Tetris | Medium | Takedown of the listing | Own name and look; owner's check before listing |
| Scope: 13 apps and a store | High | Slow progress | Gates per track; first set of three apps; everything else on the owner's order |
| GitHub limits (Pages, API, release sizes) | Low | Catalog or downloads slow | Static files, small images, releases per app |
| Secrets in public repos | Low | Exposure | Secret scan before every push and in CI |
