# PrimitiveOS implementation plan

Status date: 2026-11-19. On the Kindle: Primitive Launcher **v0.3.21**, Primitive Browser **v0.2.17**, Primitive Terminal
**v0.1.8**. Decisions D1–D7 are taken ([kindle-platform-plan.md](kindle-platform-plan.md) §4). This is the tracking
document for all the work; the design behind it is in [store-architecture.md](store-architecture.md), and the app choices
in [store-migration-kindleforge.md](store-migration-kindleforge.md).

The [local verification guide](local-verification.md) records the current Mac simulation and ARM package workflow.
The milestone checkboxes below retain their device-tested meaning.

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
| [A3 Repo upkeep and licences](#a3-repo-upkeep-and-licences) | A / all repos | Launcher, Browser, Tools, and Terminal licences present. Historical Launcher releases checked. |
| [A4 Device spikes](#a4-device-spikes) | A / device | Oasis 3 identity and storage recorded. HTTPS package transfer, keep-awake, Bluetooth, jailbreak status, and fast-refresh measurements remain. |
| [B1 Shared build workflow](#b1-shared-build-workflow) | B Packaging / `kindle-primitive-build` | The GitHub repo exists. The feature branch is tested locally. Publishing the workflow tag requires approval. |
| [B2 Our three apps packaged](#b2-our-three-apps-packaged) | B / launcher, browser, terminal | Complete local ARMHF candidates verified by the packager and Store engine. |
| [B3 Soft-float builds](#b3-soft-float-builds) | B / launcher, browser, terminal | Complete local ARMEL candidates verified. Soft-float Kindle checks are pending. |
| [C1 Catalog repo and pipeline](#c1-catalog-repo-and-pipeline) | C Catalog / `kindle-primitive-catalog` | Pages is live. The feature branch's catalog and deep archive checks run locally. |
| [C2 First listings](#c2-first-listings) | C / `kindle-primitive-catalog` | Browser and KOReader are live. All current candidates have a private review catalog. |
| [D1 Shared network crate](#d1-shared-network-crate) | D Store / tools | `primitive-net` on tools `main` (`241a527`), tested on the Mac |
| [D2 Store engine](#d2-store-engine) | D / shared Tools | The engine passes Mac tests for refresh, install, removal, recovery, and signed verification. |
| [D3 Store screens](#d3-store-screens) | D / standalone Store | Today, Apps, Updates, Search, and product pages are covered by desktop captures in `docs/store-screens/` and the simulation. |
| [D4 Store on the Kindle](#d4-store-on-the-kindle) | D / device | The standalone ARMHF Store package and the bootstrap fixture pass on the Mac. The device gate needs the owner present. |
| [D5 Our apps through the store](#d5-our-apps-through-the-store) | D / launcher, browser, terminal | Local package installs, Launcher update trial, and boot-copy recovery checks passed. |
| [E1 Device layer in the kit](#e1-device-layer-in-the-kit) | E App kit / tools | Three SDK crates share the Oasis 3 profile and cross-check on both ARM targets. |
| [E2 Interface components](#e2-interface-components) | E / tools | Shared components and Hello gallery render on the Mac. |
| [E3 Text editing](#e3-text-editing) | E / tools | Shared editable fields and multiline editor have host coverage. |
| [E4 App lifecycle](#e4-app-lifecycle) | E / tools | Host lifecycle coverage for input, sleep, wake, save, and app exit. |
| [E5 App template](#e5-app-template) | E / `kindle-primitive-app-template` | Hello is packaged and its desktop driver verifies the lifecycle. |
| [F1–F13 Native apps](#f-native-apps-phase-s6) | F / one repo each | Desktop previews and verified ARMHF packages are available. Owner and device gates remain. |
| [G1–G3 Launcher features](#g-launcher-features) | G / launcher | Wi-Fi file transfer passes host loopback checks. G1 and G3 depend on device findings. |
| [H1–H5 Hardening](#h-hardening-phase-s7) | H / all | Host coverage for install recovery, reviewed hooks, signed catalog and package verification, and package safety. Device and publication gates remain open. |

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
- [x] Umbrella README and the CC BY-NC-SA 4.0 `LICENSE` for docs and skills (Mac).
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
- [x] Terminal includes the AGPL-3.0 `LICENSE` file (its engine is ported from KOReader's terminal) and a README licence
      section. Its Tools submodule is pinned to the dual-licensed `1ed99a0` revision.
- [x] Terminal and Tools have local GitHub Actions workflows for `cargo test` and Clippy (Mac).
- [ ] Decide whether to release Launcher `v0.3.21` with the new licence. Browser `v0.2.17` is already published.
- [x] The Launcher release jobs completed successfully for [v0.3.12](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/actions/runs/44313351840)
      and [v0.3.20](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/actions/runs/44438661847).
- [x] The Browser keeps `deploy/fix-hosts-truyendich.sh` outside the release package. Both ARM package inventories
      were checked locally (R4).
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
- [x] A4.4 HTTPS from the Kindle (2026-11-19, launcher 0.4.0): the store's Refresh read the catalog's index and
      KOReader's listing and icon from GitHub Pages and wrote them to `store/cache` (1 app, 0 failed). Still open:
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
- [ ] **Gate A**: owner review of the contracts and licences. Measure the full package download on Kindle for A4.4.

---

## B. Packaging (phase S2)

### B1 Shared build workflow

Repo `kindle-primitive-build` (local `doannt-kindle-build`).

- [x] Reusable workflow `package.yml`: inputs `id`, `dir`, `binary-crate`, `arches`; pins zig and cargo-zigbuild as the
      launcher's release workflow does; checks out submodules.
- [x] Steps: test, build per architecture (`armv7-unknown-linux-musleabihf`; `armel` target after B3), run the app's
      `scripts/package.sh`, write `manifest.json` (file list, sha256), zip as `<id>-<version>-<arch>.zip`, `.sha256`.
- [x] Tag check: the workflow checks the crate version before the packager writes the manifest.
- [ ] Publish the GitHub Release on a `v*` tag; attach zips and `.sha256`.
- [x] Secret scan step fails the job if a configured pattern appears in the package.
- [ ] Versioned with tags (`@v1`), so apps pin it.

### B2 Our three apps packaged

- [x] Launcher candidate via `scripts/stage.sh` and the shared packager (`primitive-launcher-<v>/manifest.json`, `launcher/`, `documents/Launcher.sh`,
      `LICENSE`, `LICENSE-DOCS`, `INSTALL.md`); `changes`: network, stops the Kindle UI, starts at boot, system files
      (boot job). `release.yml` calls B1.
- [x] Browser candidate (`dir` = `browser`, with FBInk and its GPL-3.0 licence). Declares network access.
- [x] Terminal candidate (`dir` = `terminal`) and release workflow.
- [ ] Each app's zip unpacked and checked by the owner (**Gate B**).

### B3 Soft-float builds

- [x] Build the `armv7-unknown-linux-musleabi` target with Zig and stage complete Launcher, Browser, and Terminal ZIPs.
      Launcher includes static Dropbear with zlib and Browser includes static FBInk (Mac).
- [ ] Confirm the GitHub CI result for the soft-float builds after the changes reach GitHub.
- [ ] Test on a soft-float Kindle (needs a device; until then listings declare `armhf` only).

---

## C. Catalog (phase S3)

### C1 Catalog repo and pipeline

Repo `kindle-primitive-catalog` (local `doannt-kindle-catalog`).

- [x] Layout: `apps/<id>/app.json`, `icon.png`, `shots/`; `collections.json`; `schema/`; `scripts/`.
- [x] `scripts/check-app.sh`: schema, ids, categories, text lengths, images (256 × 256 icon; 632 × 840 grayscale shots).
- [x] Pull request CI configuration: download each asset, check sha256 and size, open the zip, compare `manifest.json`, check
      allowed roots and paths, find hooks, check the licence against the allow list; post a summary comment.
- [x] `scripts/build-index.py` writes `site/v1/index.json`, `collections.json`, `apps/<id>.json`, icons, and shots.
- [ ] Publish `site/` to GitHub Pages on merge to `main` (`doannguyentrong.github.io/kindle-primitive-catalog/v1/`).
- [ ] Nightly job: every asset URL still answers with the same sha256; open an issue if not.
- [x] Pull request template with the submission checklist (store-submit-app §1).

### C2 First listings

- [ ] Approve the public Primitive Launcher listing and decide on Terminal. The private review catalog has
      candidate listings and captures. Primitive Browser 0.2.17 is published and its live asset passed validation.
- [x] KOReader is published as a link under Reading.
- [x] The private catalog builds the Start here and Made by Primitive collections (Mac).
- [x] **Gate C, current publication**. Pages served `index.json`. Its one hosted asset, Primitive Browser 0.2.17
      ARMHF, passed checksum, size, and archive validation on 2026-11-19 (Mac).

---

## D. Store (phases S4 and S5)

The store is a new phase of the launcher: its first device build starts a new minor version
(`scripts/build-device.sh --minor`).

### D1 Shared network crate

- [x] `primitive-net` in `doannt-kindle-tools` (branch `feature/primitive-net`, `241a527`): downloads with an allow list,
      HTTPS only, redirects checked by hand, size limits, progress, `.part` files (Mac).
- [x] Resume partial Store and bootstrap downloads only against the same expected size and SHA-256 (Mac).
- [ ] Check the bundled root certificates on the Kindle with a full package download (A4.4 device check).
- [x] Tests on a local HTTP server (Mac); HTTPS on the Kindle is still to check (A4.4).
- [ ] The browser uses `primitive-net` where it overlaps (later, no behaviour change).

### D2 Store engine

Crate `kl-store` in the launcher.

- [x] Models for the index, listings, manifests, `installed.json`; parsers with tests (Mac).
- [x] Cache the catalog in `launcher/store/cache/`. Support Refresh, refresh on open, and a daily check over Wi-Fi.
      Keep the saved catalog available offline (Mac).
- [x] The Store reads the device architecture, firmware and free space. The shared Oasis 3 build reports the
      `KindleOasis3` profile name. Additional device profiles need hardware evidence.
- [x] Resolver: newest version for the architecture and firmware; `requires` with `>=`; withdrawn versions skipped (Mac).
- [x] Installer (Mac): verify sha256 and size (`verify.rs`), unpack in-process to `staging/` with path checks and the
      manifest's file list (`unpack.rs`), journal, rename into place keeping `.prev`, record, clean up (`install.rs`).
- [x] Download through `primitive-net`, checks, install, and the library reload (apps and icons), done on the Mac (`083c9d8`).
- [x] Reviewed hook transactions with a 60 s runtime limit, exact root-owned approvals, and Mac fixtures for
      install, update, rollback, and removal. The device gate covers the Kindle runtime and its kernel isolation.
- [x] Update keeps the previous files until a new version is recorded. Update all processes requirements first (Mac).
- [x] Remove through the product page. The Store preserves packages another app requires and refuses to remove
      Launcher or Store through this flow (Mac).
- [x] Journal recovery: an unfinished install is undone, or finished when the record was saved (Mac; `recover`).
- [x] Tests (Mac, 30): install, update, remove, sha and size mismatch, bad paths, `//` in names, links, two top
      folders, size limits, rollback at each step, power-cut recovery in both states, dependency refusal, damaged record;
      and a test that reads a package made by the build packager (`KL_TEST_PACKAGE`).

### D3 Store screens

Following the `primitive-ui` skill; reviewed as desktop screenshots before any device build.

- [x] Store tile with a cached update badge (Mac).
- [x] Floating tab bar for Today, Apps, Updates, and Search. Refresh is at the top right (Mac).
- [x] Collections on Today, category selection in Apps, and install, update and Open actions on rows (Mac).
- [x] Product page with app details, capabilities, screenshots, release notes, version history, and information (Mac).
- [x] Install sheet, changes and requirement review, confirmation, and download and install progress (Mac).
- [x] Update all, per-app updates, and removal confirmation (Mac).
- [x] Search with the shared keyboard and app-row results (Mac).
- [x] Launcher Settings › Store and the Store gear share the daily check preference and provide cache clearing (Mac).
- [x] Dark mode and upside-down renders captured in [`docs/store-screens/`](store-screens/README.md) (Mac).

### D4 Store on the Kindle

- [ ] Install the browser from the store (from a test catalog first), open it, return, update it, remove it.
- [ ] A package for the wrong architecture is refused with the reason.
- [ ] Power off during an install; the next start finishes or undoes it.
- [ ] USB drive mode while the store is idle on the Kindle. The Store and supervisor pass idle, write, cleanup, and
      handoff tests (Mac).
- [ ] Memory with the store open stays under the launcher's budget + 20 MB.
- [ ] **Gate D**: the owner installs, updates and removes an app from the store on the Kindle.

### D5 Our apps through the store

- [ ] Browser and terminal (if listed) install and update from the public catalog.
- [x] Launcher self-update stages the candidate, restarts through the supervisor and retains the previous files during
      the trial. Boot-copy fixtures cover insufficient space and an interrupted write (Mac).
- [x] Launcher, Browser and Terminal installation guides explain Store updates and USB and SSH fallbacks (Mac).
- [ ] **Gate D5**: all our listed apps install, update and remove through the store; one launcher self-update on the
      Kindle.

---

## E. App kit (enables the native apps)

Shared crates in `doannt-kindle-tools`, taken from the launcher and the browser, so each new app is small. Dual-licensed
like the rest of tools.

### E1 Device layer in the kit

- [x] `primitive-eink` exposes the framebuffer driver, waveforms, rectangle and full refreshes (Mac).
- [x] `primitive-input` exposes touch, page buttons and rotation using the shared Oasis 3 profile (Mac).
- [x] `primitive-device` exposes the shared battery, Wi-Fi, rotation, sleep and wake, and idle refresh code (Mac).
- [ ] Device profiles beyond the Oasis 3 (screen size, rotation, input device), filled as devices are tested.

### E2 Interface components

- [x] `primitive-ui` uses the shared vello_cpu and parley renderer and the Primitive UI tokens.
- [x] Components include text, buttons, cards and rows, switches, chevrons, section headers, pop-ups with halo, sheets, tab
      bar, paged lists, status bar, block progress, full-screen message, icons (24-unit paths).
- [x] Dark mode preserves pictures. Native controls submit pressed feedback before dispatching the action, using
      the changed rectangle. Physical visibility and cadence remain part of the panel check.
- [x] The Hello desktop driver renders the component gallery and verifies localized feedback before dispatch.

### E3 Text editing

- [x] The shared single-line field tracks the caret, clips long text, and supports masking. Launcher Wi-Fi and SSH
      screens use it (Mac).
- [x] Notes uses the shared multiline editor with cursor placement by tap, insert/delete, wrapping and page scrolling.

### E4 App lifecycle

- [x] Event loop with app-supplied deadlines and redraws when the app reports a visible change.
- [x] Packages include library entries. The supervisor exercises the grid launch and return protocol in Mac fixtures.
- [x] Native lifecycle invokes save on sleep and exit and reads app settings and log paths from each app directory.
- [x] Native app entries run from RAM and let the supervised app reserve the user volume during file access (Mac).
- [ ] Confirm native apps let the Kindle drive mount while idle and resume after eject on an Oasis 3.

### E5 App template

Repo `kindle-primitive-app-template`.

- [x] Workspace: `<x>-core` (state, logic, tests), `<x>-render`, `<x>-kindle`, `<x>-desktop`, using E1–E4.
- [x] `scripts/stage.sh`, `release.yml` calling B1, `app.json` draft, icon, README (licences: PolyForm Noncommercial
      for code, CC BY-NC-SA 4.0 for docs), `CHANGELOG.md`, `docs/device-notes.md`.
- [x] A "Hello" app made from it.
- [ ] **Gate E**: the Hello app installs from the store, opens from the grid, sleeps and wakes, returns to the launcher,
      and is removed.

---

## F. Native apps (phase S6)

Each app is its own repo (`kindle-primitive-<name>`, local `doannt-kindle-<name>`), made from the template (E5), with
its own versions from 0.1.0. Every app milestone includes the **definition of done** below, plus its own items.

**Definition of done for an app release**

- [ ] Desktop screenshots of every screen reviewed by the owner before the first device build.
- [ ] The `primitive-ui` review checklist passed (tokens, touch targets, way back, refresh, dark mode, upside down).
- [x] Core logic covered by tests on the Mac.
- [ ] Works with Primitive Launcher in front; leaving returns to the launcher; sleep and wake keep the state.
- [ ] Packaged by B1; listing in the catalog with icon, screenshots, `changes`, `tested_on`.
- [ ] Device gate: the owner installs it from the store, uses it for a day, and removes it.

### F1 Notes (productivity; like Apple Notes)

- [x] Notes list (newest first, pinned on top), new note, open, edit with the multi-line editor (E3), delete with Undo.
- [x] Search across notes. Plain text files in `/mnt/us/notes/` (copyable over USB), names from the first line.
- [x] Autosave and durable file handling pass Mac fixtures.
- [ ] Verify Notes across Kindle sleep, power loss, and USB eject.

### F2 Focus (productivity; like the Clock app's timer and Pomodoro apps)

- [x] Focus and break timer, presets 25/5 and 50/10, custom lengths; start, pause, reset.
- [x] Large minute-based countdown, end screen, and today's focus count and total.
- [ ] Verify keep-awake behavior while Focus runs on the Kindle (A4.5).

### F3 Words (game; like Wordle)

- [x] Six guesses for a five-letter word, shared keyboard with letter states, marks that read in black and white.
- [x] Daily word and free play with statistics and streaks.
- [x] English answer and guess banks ship from independent selections (Mac). The source credited by KWordle supplied
      its two datasets without a redistribution licence. The Words README records the provenance check.

### F4 Cards (productivity; like AnkiMobile, Quizlet)

- [x] Decks and cards, keyboard editing, SM-2 review, paged card faces, and per-deck statistics.
- [x] Import of Anki `.apkg` text fields and export to Documents. Media remains a later extension.

### F5 Calculator (tool; like Calculator)

- [x] Standard calculator with large keys, history, result copy, and exact decimal arithmetic.

### F6 Sudoku (game)

- [x] Puzzle generator with unique solutions and difficulty levels, notes mode, mistakes check, and Undo.

### F7 Chess (game; play against the Kindle)

- [x] Board with tap-to-move, legal moves shown, Undo, and difficulty levels.
- [x] Local search with the licensed Cozy Chess move generator.
- [x] Save and resume a game and export standard PGN.

### F8 Minesweeper (game)

- [x] Classic board sizes, tap to reveal, hold to flag, safe first tap, timer, and best times.

### F9 Solitaire (game; Klondike)

- [x] Tap-to-move, draw one or three, persistent Undo, auto-finish, and card faces for e-ink.

### F10 Crossword (game; like crossword apps)

- [x] Grid and clue list, shared keyboard, check, and reveal.
- [x] Bundled original puzzles and import of standard unlocked `.puz` files.

### F11 Blocks (game; like 1010! and Woodoku)

- [x] Place three pieces per turn on a 9 × 9 grid, clear rows, columns and boxes, and track scores.
- [x] Original visual design in the local candidate.

### F12 Ships (game; Battleship)

- [x] Place ships manually or randomly, play against the Kindle at three levels, and play two-person hot-seat.

### F13 Falling-blocks game (game; like Tetris) (owner, 2026-11-19)

- [ ] Name and look of our own: not called "Tetris" (The Tetris Company's trademark), and no copy of its look (its
      colours, piece textures, screens); a working name until the owner picks one. The owner checks the name and look
      before the first public listing.
- [ ] A4.9 answered first; the game's speed levels follow what the panel can show (pieces move in clear steps, not
      smooth motion).
- [x] Touch actions for movement, rotation, and drops, with page buttons for movement.
- [ ] Only the changed cells are redrawn with a fast waveform; a full refresh at line clears or every few seconds to
      clear ghosting; pause on sleep.
- [x] Scoring, levels, next piece, hold, and best scores in the Cascade candidate.

---

## G. Launcher features

### G1 Jailbreak status in Settings › About

- [ ] After A4.7: show whether the hotfix is installed and updates are blocked, with a link to the KindleModding wiki.

### G2 Wi-Fi file transfer

- [x] A Settings page starts a small web server while it is open, shows an address and a code, and accepts files
      from a phone or computer on the same network into `documents/`.
- [x] Host fixtures cover session closure, code checks, transfer limits, and restricting writes to `documents/`.

### G3 Bluetooth keyboard

- [ ] Only if A4.6 finds a working radio: pair a keyboard in Settings; typing in the shared text fields.

---

## H. Hardening (phase S7)

- [x] H1 Local Ed25519 signing and opt-in verification of the index, listings, and packages in Store and Launcher.
      Production key provisioning and publication require owner approval. See [Store signatures](store-signatures.md).
- [ ] H2 Other Kindles: architecture and firmware checks on a soft-float Kindle and a second hard-float model.
- [ ] H3 Recovery: bad packages (wrong sha, wrong device, missing file, bad paths) refused; the launcher still starts;
      the boot guard after a failed self-update.
- [ ] H4 Catalog health: the nightly check's issues are answered; withdrawn versions handled.
- [x] H5 Review of install paths, archive limits, hook declarations and approvals, and the network allow list (Mac).
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
