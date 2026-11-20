# PrimitiveOS implementation plan

Updated 20 November 2026. The public catalog contains **35 listings**, including **34 first-party apps** and the linked
KOReader entry. Its system releases are Primitive Launcher **0.5.5**, Store **0.1.7**, Primitive Browser **0.2.18**,
and Primitive Terminal **0.1.8**. These versions describe the public catalog. See the [latest device evidence](handoff/STATE.md)
for what has been confirmed on the Oasis 3. [Live catalog](https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json)

The platform decisions are in the [platform plan](kindle-platform-plan.md). See the [Store architecture](store-architecture.md),
[local verification guide](local-verification.md), and [education and productivity app designs](education-productivity-apps.md)
for design and test details.

Checklist status

- `[x]` records a completed item. Where an item requires a Kindle, it needs a dated device result.
- `[x] … (Mac)` records desktop or local package verification. `(Published)` records verified public deployment.
- `[ ]` records work or verification still due. Keep each hardware gate open until its checks pass on a Kindle.

For initial setup, manually copy Primitive Launcher onto the Kindle once. Open Store from the existing Launcher for other
apps. Leave an installed Launcher in place unless the owner requests a Launcher change. Device builds bump the patch
version, new phases start a minor version, and new apps start at 0.1.0. Tags `vX.Y.Z` are immutable. The owner approves
public releases and listings. Record device findings in the relevant repo's `docs/device-notes.md` or published test record.

## Overview

| Milestone | Track / repo | State |
|---|---|---|
| [A1 Umbrella repo](#a1-umbrella-repo) | A Foundations / `kindle-primitive` | **Done**. The directory and all first-party repositories are in the [PrimitiveOS organization](https://github.com/PrimitiveOS). |
| [A2 Contracts and schemas](#a2-contracts-and-schemas) | A / `kindle-primitive` | **Done** (contracts, three schemas, examples, tests); owner's read pending |
| [A3 Repo upkeep and licences](#a3-repo-upkeep-and-licences) | A / all repos | Project licence terms documented. Both licence files verified in all 11 study and work packages. |
| [A4 Device spikes](#a4-device-spikes) | A / device | Oasis 3 identity and storage recorded. HTTPS package transfer, keep-awake, Bluetooth, jailbreak status, and fast-refresh measurements remain. |
| [B1 Shared build workflow](#b1-shared-build-workflow) | B Packaging / `kindle-primitive-build` | Commit-pinned workflow publishes ZIPs and checksum sidecars on app version tags. |
| [B2 Our three apps packaged](#b2-our-three-apps-packaged) | B / launcher, browser, terminal | ARMHF releases are listed in Store. Package and installer fixtures passed on the Mac. |
| [B3 Soft-float builds](#b3-soft-float-builds) | B / launcher, browser, terminal | ARMEL release assets are available. Soft-float Kindle checks remain open. |
| [C1 Catalog repo and pipeline](#c1-catalog-repo-and-pipeline) | C Catalog / `kindle-primitive-catalog` | The organization’s [catalog](https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json) is live. The workflow validates archives and refreshes the download counts. |
| [C2 Public listings and collections](#c2-public-listings-and-collections) | C / `kindle-primitive-catalog` | 34 first-party apps and the linked KOReader listing are live. |
| [D1 Shared network crate](#d1-shared-network-crate) | D Store / tools | `primitive-net` on tools `main` (`241a527`), tested on the Mac |
| [D2 Store engine](#d2-store-engine) | D / shared Tools | The engine passes Mac tests for refresh, install, removal, recovery, and signed verification. |
| [D3 Store screens](#d3-store-screens) | D / standalone Store | Today, Apps, Updates, Search, and product pages are covered by desktop captures in `docs/store-screens/` and the simulation. |
| [D4 Store on the Kindle](#d4-store-on-the-kindle) | D / device | Store 0.1.7 launched on Oasis 3 and refreshed the organization catalog with zero listing or artwork failures. The full install, update, and removal gate remains open. |
| [D5 Our apps through the store](#d5-our-apps-through-the-store) | D / launcher, browser, terminal | Local package installs, Launcher update trial, and boot-copy recovery checks passed. |
| [E1 Device layer in the kit](#e1-device-layer-in-the-kit) | E App kit / tools | Three SDK crates share the Oasis 3 profile and cross-check on both ARM targets. |
| [E2 Interface components](#e2-interface-components) | E / tools | Shared components and Hello gallery render on the Mac. |
| [E3 Text editing](#e3-text-editing) | E / tools | Shared editable fields and multiline editor have host coverage. |
| [E4 App lifecycle](#e4-app-lifecycle) | E / tools | Host lifecycle coverage for input, sleep, wake, save, and app exit. |
| [E5 App template](#e5-app-template) | E / `kindle-primitive-app-template` | Hello 0.1.0 is live in Store. Its desktop driver verifies the lifecycle. |
| [F1–F13 Native apps](#f-native-apps-phase-s6) | F / one repo each | Published with desktop previews and ARMHF packages. Device gates remain. |
| [F14–F16 Study and work](#study-and-work-release) | F / apps and catalog | Seven new apps and four updates published and verified on the Mac. Oasis 3 release checks remain open. |
| [F17 Files and Viewer](#f17-files-and-viewer) | F / Files and Viewer | Viewer opens PDF, JPEG, and PNG offline with continuous PDF scrolling. Files can hand documents to Viewer or KOReader. |
| [G1–G3 Launcher features](#g-launcher-features) | G / launcher | Wi-Fi file transfer passes host loopback checks. G1 and G3 depend on device findings. |
| [G4–G8 Launcher settings](#g4-battery) | G / Launcher, Store, and Tools | Launcher 0.5.5 and Store 0.1.7 are published and installed on the Oasis 3. Display previews wallpaper and adjusts opacity for Home, Sleep, and Startup. Detailed device checks remain open. |
| [H1–H5 Hardening](#h-hardening-phase-s7) | H / all | Host coverage for install recovery, reviewed hooks, signed catalog and package verification, and package safety. Device and publication gates remain open. |

Open release verification starts with the [study and work device checks](#study-and-work-release), using the installed
Launcher. The broader device gates cover [Store](#d4-store-on-the-kindle), [Hello](#e5-app-template),
[additional Kindle models and recovery](#h-hardening-phase-s7), and the [device measurements](#a4-device-spikes).

---

## A. Foundations (phase S1)

### A1 Umbrella repo

- [x] Folder `doannt-kindle/` with the four app repos side by side; `git init` with the app repos ignored (Mac).
- [x] Documents: platform plan, store architecture, submission guide, install guide, migration review, this plan (Mac).
- [x] Skills in `.agents/skills` (`primitive-ui`, `kindle-device`, `kindle-eink`), linked as `.claude/skills` (Mac).
- [x] Umbrella README and the CC BY-NC-SA 4.0 `LICENSE` for docs and skills (Mac).
- [x] `.gitignore` ignores every app folder by pattern (`/doannt-kindle-*/`), so new app repos need no change.
- [x] First commit (`8be0056`); remote `https://github.com/PrimitiveOS/kindle-primitive.git` (public); pushed.

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

- [x] Launcher from 0.3.21 and Browser from 0.2.17 use PolyForm Noncommercial 1.0.0 for code and CC BY-NC-SA 4.0 for
      project documentation and artwork. Prior releases retain their published terms. [Licence audit](licence-audit.md)
- [x] Tools: AGPL-3.0 or PolyForm Noncommercial 1.0.0 (`1ed99a0`).
- [x] Terminal includes the AGPL-3.0 `LICENSE` file (its engine is ported from KOReader's terminal) and a README licence
      section. Its Tools submodule is pinned to the dual-licensed `1ed99a0` revision.
- [x] Terminal and Tools have local GitHub Actions workflows for `cargo test` and Clippy (Mac).
- [x] Terminal is published in Store as a developer tool. Its package remains under AGPL-3.0. (Published)
- [x] All 11 study and work ARMHF releases include `LICENSE` and `LICENSE-DOCS`. The latest public ZIPs match their
      repository licence files and published checksum sidecars. (Mac, Published)
- [x] The Launcher release jobs completed successfully for [v0.3.12](https://github.com/PrimitiveOS/kindle-primitive-launcher/actions/runs/44313351840)
      and [v0.3.20](https://github.com/PrimitiveOS/kindle-primitive-launcher/actions/runs/44438661847).
- [x] The Browser keeps `deploy/fix-hosts-truyendich.sh` outside the release package. Both ARM package inventories
      were checked locally (R4).
- [ ] Browser: the untracked `docs/tinhte/` folder is the owner's; commit it or leave it out.
- [ ] Tools: keep the remote name `kindle-primtitive-tools` or rename it (GitHub redirects the old name).

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
      `com.lab126.powerd preventScreenSaver`. The temporary session override was cleared on 20 November 2026 and
      read back as `0` on the Oasis 3. Focus-specific behaviour remains to be tested.
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
- [x] Publish GitHub Releases from app `v*` tags with ARM ZIPs and `.sha256` sidecars. (Published)
- [x] Secret scan step fails the job if a configured pattern appears in the package.
- [x] Apps pin the reusable workflow by commit SHA. The study and work releases use `9533d48`. (Published)

### B2 Our three apps packaged

- [x] Launcher release via `scripts/stage.sh` and the shared packager (`primitive-launcher-<v>/manifest.json`, `launcher/`, `documents/Launcher.sh`,
      `LICENSE`, `LICENSE-DOCS`, `INSTALL.md`); `changes`: network, stops the Kindle UI, starts at boot, system files
      (boot job). `release.yml` calls B1.
- [x] Browser release (`dir` = `browser`, with FBInk and its GPL-3.0 licence). Declares network access. (Published)
- [x] Terminal release (`dir` = `terminal`) and release workflow. (Published)
- [ ] Each app's zip unpacked and checked by the owner (**Gate B**).

### B3 Soft-float builds

- [x] Build the `armv7-unknown-linux-musleabi` target with Zig and stage complete Launcher, Browser, and Terminal ZIPs.
      Launcher includes static Dropbear with zlib and Browser includes static FBInk (Mac).
- [x] Checked the published ARMEL ZIPs for Launcher 0.4.10, Browser 0.2.18, and Terminal 0.1.8 in the
      [licence audit](licence-audit.md#release-package-review). (Mac, Published)
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
- [x] Build and publish `site/` to GitHub Pages on pushes to `main`. The 20 November workflow passed schema and
      deep release asset checks before deploying. (Published) [Catalog deployment](https://github.com/PrimitiveOS/kindle-primitive-catalog/actions/runs/44580696716)
- [x] `catalog-health.yml` schedules a nightly check of published asset size and SHA-256 and opens an issue on failure.
- [x] Pull request template with the submission checklist (store-submit-app §1).

### C2 Public listings and collections

- [x] Launcher, Store, Browser, Terminal, Hello, and the other first-party apps have hosted releases. KOReader is listed
      under Reading as a third-party link. (Published)
- [x] Start here, Made by Primitive, and Study and work are live. Study and work contains the 11 new or updated apps
      and Primitive Browser. (Published) [Live collections](https://primitiveos.github.io/kindle-primitive-catalog/v1/collections.json)
- [x] **Gate C**. The 33-entry live index matched the generated catalog. The 11 changed listings, their icons and
      screenshots, and the collections file matched the published assets byte for byte. (Published)

---

## D. Store (phases S4 and S5)

Store is a standalone app with its own version and release workflow. Primitive Launcher provides a single Store tile,
can bootstrap Store when it is absent, and refreshes its app grid after installation or removal.

### D1 Shared network crate

- [x] `primitive-net` in `doannt-kindle-tools` (branch `feature/primitive-net`, `241a527`): downloads with an allow list,
      HTTPS only, redirects checked by hand, size limits, progress, `.part` files (Mac).
- [x] Resume partial Store and bootstrap downloads only against the same expected size and SHA-256 (Mac).
- [x] Store bootstrapped and installed ARMHF packages over HTTPS on the Oasis 3 on 19 November 2026. The separate
      download-speed and memory measurement in A4.4 remains open.
- [x] Tests on a local HTTP server. (Mac)
- [ ] The browser uses `primitive-net` where it overlaps (later, no behaviour change).

### D2 Store engine

Crate `kl-store` in shared Tools, used by Store and Primitive Launcher.

- [x] Models for the index, listings, manifests, `installed.json`; parsers with tests (Mac).
- [x] Cache the catalog in `launcher/store/cache/`. Support Refresh, refresh on open, and a daily check over Wi-Fi.
      Keep the saved catalog available offline (Mac).
- [x] Store 0.1.4 opens from the cached first page, paginates lists, and preloads nearby artwork. Refresh checks listings
      concurrently and reuses unchanged revisions. **Done** can interrupt a refresh and exit. (Mac, Published)
- [x] Store 0.1.6 opens from the cached catalog and preloads icons around the visible list rows while scrolling. (Mac)
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
- [x] Show the cached GitHub package download total on each product page when the catalog provides it. (Mac)
- [x] Install sheet, changes and requirement review, confirmation, and download and install progress (Mac).
- [x] Update all, per-app updates, and removal confirmation (Mac).
- [x] Search with the shared keyboard and app-row results (Mac).
- [x] Scroll long lists vertically with the navigation tabs fixed at the bottom. Returning from a product page restores
      its list position. [Desktop previews](store-screens/README.md) (Mac)
- [x] Launcher Settings › Store and the Store gear share the daily check preference and provide cache clearing (Mac).
- [x] Dark mode and upside-down renders captured in [`docs/store-screens/`](store-screens/README.md) (Mac).

### D4 Store on the Kindle

- [x] Store 0.1.2 bootstrapped over Wi-Fi, refreshed 19 listings, installed apps, and opened Hello on the Oasis 3 on
      19 November 2026. [Store test record](https://github.com/PrimitiveOS/kindle-primitive-store#status)
- [x] Device logs for Store 0.1.4 recorded a faster first frame, a refresh that reused all 19 listings, and return to
      Launcher through **Done** during refresh. The owner confirmed startup was faster. See `build/store-performance/`
      in the local workspace for the run logs.
- [ ] Complete a Browser install, open, return, update, and removal sequence on the Oasis 3.
- [ ] Verify Store list scrolling, fixed tabs, and Back on the Oasis 3 in light and dark mode. Check a long Search
      result list with the keyboard open and after dismissing it.
- [ ] Check download totals after refreshing Store, including a first-party app while offline and a link listing
      that shows Unavailable.
- [ ] A package for the wrong architecture is refused with the reason.
- [ ] Power off during an install; the next start finishes or undoes it.
- [ ] USB drive mode while the store is idle on the Kindle. The Store and supervisor pass idle, write, cleanup, and
      handoff tests (Mac).
- [ ] Memory with the store open stays under the launcher's budget + 20 MB.
- [ ] **Gate D**: the owner installs, updates and removes an app from the store on the Kindle.

### D5 Our apps through the store

- [x] Browser 0.2.18 and Terminal 0.1.8 installed from the public catalog and returned to Launcher in the Oasis 3 smoke test
      on 19 November 2026. See `build/device-validation/README.md` in the local workspace.
- [ ] Complete Browser and Terminal update and removal checks on the Oasis 3.
- [x] Launcher self-update stages the candidate, restarts through the supervisor and retains the previous files during
      the trial. Boot-copy fixtures cover insufficient space and an interrupted write (Mac).
- [x] Launcher, Browser and Terminal installation guides explain Store updates and USB and SSH fallbacks (Mac).
- [x] A prior Launcher 0.4.10 supervisor trial was accepted on the Oasis 3. The installed, RAM, and boot copies matched.
      See `build/launcher-uninstall-warning/device-verification.log` in the local workspace.
- [ ] **Gate D5**: complete the remaining Store install, update, and removal checks on the Kindle using the existing Launcher.

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
- [x] Hello 0.1.0 ships from the template and is listed in Store. (Published)
- [x] The Oasis 3 smoke test installed Hello, opened it, and increased its counter by tapping **Say hello**.
- [ ] **Gate E**: confirm the full Hello lifecycle on the Kindle, including sleep, wake, return to Launcher, and removal.

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
- [x] Notes 0.1.1 adds checklist ordering and a reading journal template. See [F15](#f15-more-practice). (Mac, Published)
- [ ] Verify Notes across Kindle sleep, power loss, and USB eject.

### F2 Focus (productivity; like the Clock app's timer and Pomodoro apps)

- [x] Focus and break timer, presets 25/5 and 50/10, custom lengths; start, pause, reset.
- [x] Large minute-based countdown, end screen, and today's focus count and total.
- [x] Focus 0.1.1 adds reusable subjects and a weekly study log. See [F16](#f16-reference-and-routines). (Mac, Published)
- [ ] Verify keep-awake behavior while Focus runs on the Kindle (A4.5).

### F3 Words (game; like Wordle)

- [x] Six guesses for a five-letter word, shared keyboard with letter states, marks that read in black and white.
- [x] Daily word and free play with statistics and streaks.
- [x] English answer and guess banks ship from independent selections (Mac). The source credited by KWordle supplied
      its two datasets without a redistribution licence. The Words README records the provenance check.

### F4 Cards (productivity; like AnkiMobile, Quizlet)

- [x] Decks and cards, keyboard editing, SM-2 review, paged card faces, and per-deck statistics.
- [x] Import of Anki `.apkg` text fields and export to Documents. Media remains a later extension.
- [x] Cards 0.1.1 adds an independent Self-test and preview for two-column TSV imports. See
      [F14](#f14-daily-planning-and-reading) and [F15](#f15-more-practice). (Mac, Published)

### F5 Calculator (tool; like Calculator)

- [x] Standard calculator with large keys, history, result copy, and exact decimal arithmetic.
- [x] Calculator 0.1.3 adds unit conversions, exact worked steps, and plots for lines and quadratics. See
      [F16](#f16-reference-and-routines). (Mac, Published)

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

### F13 Cascade (falling-blocks game)

- [x] Cascade 0.1.0 is published with its own name and monochrome artwork. (Published)
- [ ] Measure the panel refresh and ghosting at each pace setting on the Oasis 3 (A4.9).
- [x] Touch actions for movement, rotation, and drops, with page buttons for movement.
- [ ] Confirm changed-cell refresh, full refresh at line clears, and pause on sleep on the Kindle.
- [x] Scoring, levels, next piece, hold, and best scores in the release.

### Study and work release

All three waves shipped on 20 November 2026. The published release links and shipped features are in the
[education and productivity release record](education-productivity-apps.md#released-apps). The seven new apps use the
approved icons. The first-party app directory links every current Store release. [PrimitiveOS app directory](../README.md#the-apps)

- [x] Core and desktop interaction checks passed across all 11 releases. Checks included persistence, import previews,
      retry flows where applicable, and light and dark screenshots. (Mac)
- [x] Downloaded and checked the 11 public ARMHF packages and checksum sidecars. Checked manifests and both licence
      files, and matched the seven approved icons against the launcher entries. (Mac, Published)
- [x] Refreshed an 11-listing fixture built from the released catalog entries. The Store engine installed and removed
      all 11 public packages and preserved a personal document. (Mac)
- [x] Verified public Pages after deployment. The 11 listings, catalog assets, and Study and work collection matched
      the reviewed output. (Published)
- [ ] **Study and work Kindle gate**. Use the existing Launcher and Store on the Oasis 3. Install the seven new apps and
      update the four existing apps without losing existing user data. Check touch targets, both portrait orientations,
      e-ink refresh, airplane mode, sleep and wake, USB eject, and return to Launcher. Record release-specific results
      before adding a Kindle model to `tested_on`.

#### F14 Daily planning and reading

- [x] Tasks 0.1.0 covers Today, lists, due dates, recurring tasks, and Undo. (Mac, Published)
- [x] Reading Practice 0.1.0 ships 12 passages and 36 questions, with saved progress and missed-answer review. (Mac, Published)
- [x] Cards 0.1.1 Self-test tracks retries separately from the scheduled review. (Mac, Published)
- [ ] On the Oasis 3, complete and undo a recurring task, resume a passage question after reopening the app, and retry
      missed cards after reboot in airplane mode. Verify that the existing Cards review schedule survives the update.

#### F15 More practice

- [x] Math Practice 0.1.0 ships worked examples and five-problem sets for arithmetic, fractions, and percentages.
      Equivalent fraction answers are accepted. (Mac, Published)
- [x] Language Practice 0.1.0 ships ten beginner English lessons for Vietnamese speakers with tap exercises and
      missed-answer review. (Mac, Published)
- [x] Notes 0.1.1 saves checklists and reading journals as plain text. Cards 0.1.1 previews two-column TSV imports and
      identifies duplicates. (Mac, Published)
- [ ] On the Oasis 3, check the number keypad, equivalent answers, Vietnamese diacritics, and TSV import errors.
      Verify that the Notes update preserves existing notes and that the Cards update preserves existing decks.

#### F16 Reference and routines

- [x] Dictionary 0.1.1 includes original starter definitions, accent-insensitive lookup, TSV import preview, and
      a Cards-compatible favorites export. (Mac, Published)
- [x] Habits 0.1.0 records editable daily and weekly check-ins and exports CSV. Agenda 0.1.0 lists local events and
      previews supported one-off `.ics` imports with all-day, local, or UTC start times. (Mac, Published)
- [x] Focus 0.1.1 adds subjects and a weekly study log. Calculator 0.1.3 adds conversions, exact steps, and static line
      and quadratic plots with a value table. (Mac, Published)
- [ ] On the Oasis 3, check date boundaries, duplicate and unsupported file handling, subject history, and plot redraws
      against known examples.

### F17 Files and Viewer

- [x] Build a standalone Files app that opens in Documents, scrolls vertically, searches filenames, and supports
      creating folders, renaming, copying, moving, and confirmed deletion. (Mac)
- [x] Preserve the existing Launcher setup and hand supported documents to KOReader when it is installed.
      Simulate the package and document handoff locally. (Mac)
- [x] Install Files and verify that it opens through the Launcher supervisor on the Oasis 3.
- [x] Open a sample PDF from Files in KOReader on the Oasis 3. The owner confirmed the page displayed.
- [ ] Verify the return from KOReader under both device orientations.
- [x] Implement one read-only Viewer for PDF, JPEG, and PNG. Scroll PDFs with swipes or Kindle page buttons,
      resume from Recent, and use compact zoom controls and a View menu. (Mac)
- [x] Add **Open in Viewer** to Files and keep **Open in KOReader** for its supported formats. (Mac)
- [x] Install Viewer and Files on the Oasis 3. Verify the Files handoff, swipe and physical-button scrolling, and
      returning to Launcher. Launch Viewer from its own tile and verify image zoom and physical-button navigation
      in the file picker.
- [ ] Check USB eject, both portrait orientations, and performance on larger documents on the Oasis 3.
- [x] Publish Viewer and the Files update to GitHub and list both releases in Store. [Viewer plan](viewer-plan.md)

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

### G4 Battery

- [x] Review current Launcher settings and device capabilities alongside Apple and Amazon guidance.
      [Launcher settings plan](launcher-settings-plan.md)
- [x] Add Settings › Battery with charge level and source-aware charging state. Reuse the existing alerts and awake
      refresh path. Link to Front light, Wi-Fi, and automatic Store checks. (Mac)
- [x] Add local 24-hour history and opt-in Low power mode. Host tests cover missing readings, observation gaps,
      leased writes, and the distinction between automatic and manual Store refresh. (Mac)
- [ ] On the Oasis 3, check unplugged and charging states, sleep and wake, USB and eject, light overrides, file transfer,
      and manual Store refresh in Low power mode. Measure battery use before claiming savings.

### G5 Display and accessibility

- [x] Share direct front-light and warmth selection and single-step buttons between Display and Quick Settings.
      Show controls supported by the active device profile. (Mac)
- [x] Add a Launcher text-size preview, stronger contrast, and the shared opening-animation preference. (Mac)
- [ ] On the Oasis 3, check front-light and warmth readback and touch targets in both portrait orientations.
      Check text legibility in light and dark mode and after sleep.

### G6 Storage and settings navigation

- [x] Add used and total storage, the device profile and read firmware version, and links to installed apps and
      Store settings. The mock supervisor opens Store's installed list only for the intended launch. (Mac)
- [x] Add per-app visibility, grid columns and rows, and updated startup and sleep descriptions. Scroll vertically
      through Settings and App visibility. The desktop driver checks swipes, opening a scrolled setting, and restoring
      the list position with Back. (Mac)
- [ ] Verify Settings and App visibility scrolling, the installed-app shortcut, USB status, and storage totals on the
      Oasis 3. Check Store updates and removal from that path and confirm that visibility and grid changes persist after
      reboot.

### G7 Date and time

- [x] Add the Kindle's date, local clock, and UTC offset under System in Settings. Refresh re-reads the firmware's
      configured time zone. (Mac)
- [x] Add an explicit Wi-Fi clock sync using the firmware's time tool where available. Desktop tests cover navigation,
      time-zone offsets, and timeout. (Mac)
- [ ] On the Oasis 3, verify network sync, a changed stock Kindle time zone, and error feedback while offline.

### G8 Wallpaper

- [x] Group the Home, Sleep, and Startup pickers under Display. Save each choice locally, support each screen's
      default, preserve the existing sleep rotation, and validate PNGs before use. (Mac)
- [x] Preview the Home layout and the fitted Sleep and Startup pictures before applying them. Adjust opacity
      independently for each screen. Cancel leaves the saved choices alone. (Mac)
- [x] Extend the Home wallpaper behind the status bar and page indicator. Check contrast in both themes. (Mac)
- [x] Verify the Launcher 0.5.5 in-place update and preservation of wallpaper preferences and PNGs on the Oasis 3.
- [x] Confirm the Oasis 3 saves the Sleep opacity independently of Home and Startup.
- [x] Confirm Home wallpaper preview, opacity, and coverage behind both bars on the Oasis 3. (20 November 2026)
- [ ] On the Oasis 3, verify legibility on both Home themes and after turning the device, sleep and wake with a fixed
      image and the Kindle screensaver, and the automatic Launcher startup picture after the firmware splash.
      Check that saved opacity survives restarting Launcher and that the gallery refreshes after USB eject.

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
| HTTPS on the Kindle | High | Store downloaded packages over Wi-Fi on the Oasis 3. Transfer profiling remains open (A4.4). |
| Launcher self-update | Medium | The Oasis 3 accepted a supervisor trial. Failed trials still need a device recovery check. |
| Soft-float compatibility | Medium | Release archives exist. A soft-float device is needed for validation. |
| App kit from existing code | High | The device layer and renderer exist in the launcher and browser. |
| Multi-line text editing on e-ink | Medium | Notes ships with the shared editor. Measure refresh cost while typing on the Kindle. |
| Turn-based games | High | Fit e-ink; logic is testable on the Mac. |
| Falling-blocks game (F13) | Medium | Needs fast partial updates; ghosting limits the speed (A4.9). |
| Chess engine with a fitting licence | High | Chess ships with the Cozy Chess move generator and its MIT notice. |
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
| Growing app catalog | High | Slow device coverage | Batch desktop checks by release, then record hardware evidence per app |
| GitHub limits (Pages, API, release sizes) | Low | Catalog or downloads slow | Static files, small images, releases per app |
| Secrets in public repos | Low | Exposure | Secret scan before every push and in CI |
