# Primitive Kindle platform: repos, architecture, and execution plan

Status date: 2026-11-19.

This document covers three things: the repos we have and the ones we need to create, the architecture that connects
them (launcher as host, apps as modules, a GitHub-hosted app store), and the order of work with a gate per phase.
The reference for the wider Kindle ecosystem is [Awesome-Kindle](https://github.com/KindleTweaks/Awesome-Kindle)
(cloned to `/tmp/kl-research/Awesome-Kindle` at commit `ae2e041`, not kept in this workspace).

How to read the checklists (same as the launcher's plan):

- `[x]` done and confirmed on the Kindle by the owner.
- `[x] … (Mac)` done and tested on the Mac, not yet confirmed on the Kindle.
- `[ ]` not done.

A phase is finished when its gate passes. Device builds bump the patch version; a new phase starts a new minor version.
Tags `vX.Y.Z` are never moved.

## 1. What the ecosystem looks like

Awesome-Kindle is a curated list (85 lines, one README, no code) of about 40 community projects in seven groups:
Amazon alternatives, quality of life, productivity, games, development, audio, and miscellaneous. Each entry links to
its own GitHub repo, and most projects are standalone: a scriptlet folder, a KUAL extension, or a KOReader plugin.

Facts from the list and from the projects it links that shape our plan:

- **KindleForge** (`KindleTweaks/KindleForge`) is the existing on-device store. It is a GUI app (a Go binary, KFPM) that
  installs packages from `KindleTweaks/Repository`. Its README says it is in **maintenance mode** and will be rewritten
  to use **KPM** as its backend, with no ETA. Its licence is GPLv3 for KindleForge and CC BY-NC-SA 4.0 for the
  Repository packages. The non-commercial, share-alike licence limits how we can re-host those packages.
- **KPM** (`Gingrspacecadet/KPM`) is a shell package manager for Kindles. It needs `kterm`, `curl`, and `unzip` or `tar`.
  Its wiki (kpmwiki.vercel.app) documents the package format; we have not read it yet (see open item O3).
- **KUAL extensions** are folders under `/mnt/us/extensions/<name>/` with a `config.xml` and a `menu.json`. Our launcher
  already reads them (`crates/kl-core/src/kual.rs`), so a store can install them with no launcher change.
- **Library entries** are scriptlets in `/mnt/us/documents/*.sh` with a header (`# Name:`, `# Author:`, `# Icon:`). Our
  launcher and browser use them (see §3.2).
- **Jailbreak base**: the ecosystem depends on a jailbreak stack (AdBreak, WinterBreak, or LanguageBreak, a universal
  hotfix, and a minimum firmware). Our launcher is verified on the Oasis 3 with firmware 5.18.2 only. Every store
  install must respect that.

Conclusion: the ecosystem has no installer that we can rely on right now. KindleForge is being rewritten, and KPM is a
shell tool. A store we control, on GitHub, with a documented package contract, is a sound base. We do not need to wait
for either project, but we should keep the package format compatible with KPM where it costs little (open item O3).

## 2. Repo inventory

### 2.1 Existing repos

| Repo (local folder) | Remote | Role | Version and state (2026-11-19) | Licence | Gaps |
|---|---|---|---|---|---|
| `doannt-kindle-launcher` | `DoanNguyenTrong/kindle-primitive-launcher` | Primitive Launcher: the host (grid, settings, Wi-Fi, SSH, boot, USB). Crates `kl-core`, `kl-render`, `kl-kindle`, `kl-desktop`. | 0.3.20, tag `v0.3.20` on `main` (`55d034c`). Local branch `chore/move-kindle-skills` (skills removal, not pushed). | PolyForm Noncommercial 1.0.0 from the next version (docs and pictures CC BY-NC-SA 4.0); AGPL-3.0 up to v0.3.20 | Store is not built. Release CI state for `v0.3.12` unverified (no `gh`). |
| `doannt-kindle-browser` | `DoanNguyenTrong/kindle-primitive-browser` | Primitive Browser: a module app. Crates `kb-app`, `kb-engine`, `kb-js`, `kb-net`, `kb-kindle`, `kb-desktop`. | 0.2.16, tag `v0.2.16`. Current branch `feature/diagnostics-ssh` (not `main`). | PolyForm Noncommercial 1.0.0 from 0.2.17 (docs CC BY-NC-SA 4.0); AGPL-3.0 up to v0.2.16 | No store entry yet. `deploy/fix-hosts-truyendich.sh` is site-specific (see R4). Its own `tools/` submodule. |
| `doannt-kindle-terminal` | `DoanNguyenTrong/kindle-primitive-terminal` | Primitive Terminal: a module app. Crates `kt-core`, `kt-engine`, `kt-render`, `kt-kindle`, `kt-desktop`. | 0.1.8 on `main` (`5bd4f20`). No tags. | AGPL-3.0 (engine ported from KOReader); **no licence file yet** | No licence file. No CI or release workflow. No tags. |
| `doannt-kindle-tools` | `DoanNguyenTrong/kindle-primtitive-tools` (sic) | Shared Rust crates used by launcher and browser: `primitive-keyboard`, `primitive-quick`. Submodule `tools/` in each app. | `main` (`16b1223`). No tags. | AGPL-3.0 or PolyForm Noncommercial 1.0.0 (`1ed99a0`) | No CI, no tags. The remote name has a typo (`primtitive`). |
| `doannt-kindle` (umbrella) | none, not a git repo | Holds the four repos above, the shared skills (`.agents/skills`, linked as `.claude/skills`), and this plan. | n/a | n/a | Make it a git repo (or keep it a plain folder) and decide (see D6). |

Cross-repo facts:

- The launcher, browser, and terminal each include `tools` as a submodule. Every app must pin a commit of `tools`, so an
  update of `tools` is a change in three repos.
- Releases are built by GitHub Actions. The launcher's `release.yml` publishes `dist/primitive-launcher-<v>.zip` and a
  `.sha256` on `v*` tags, and the tag must match `Cargo.toml`. The browser has the same pattern. The terminal has none.
- Device builds are made with `scripts/build-device.sh` (cross-compile to `armv7-unknown-linux-musleabihf` with zig,
  then install over SSH). Deploys are run from outside the repos.
- The skills (`kindle-device`, `kindle-eink`) are in `doannt-kindle/.agents/skills`, linked from `.claude/skills`.

### 2.2 Repos to create

GitHub names follow `kindle-primitive-*`; local folders follow `doannt-kindle-*` inside `doannt-kindle/`.

| New repo (GitHub / local) | Purpose | Phase |
|---|---|---|
| `kindle-primitive` / `doannt-kindle` | The umbrella: README, docs (this plan, the store documents), and the shared skills. Git initialised locally; remote `https://github.com/DoanNguyenTrong/kindle-primitive.git` (D6). | now |
| `kindle-primitive-catalog` / `doannt-kindle-catalog` | The public catalog: one folder per app with `app.json`, icons and screenshots; the JSON schema; CI that checks every listing and publishes the static API to GitHub Pages. Hosts no binaries. | S3 |
| `kindle-primitive-build` / `doannt-kindle-build` | Shared CI: a reusable workflow that builds a device package (zip, `.sha256`, `manifest.json`) per architecture for any app, with the zig setup pinned as the launcher does now. Each app calls it on a `v*` tag. | S2 |

The store client is **not** a separate repo: it is a crate (`kl-store`) in the launcher, which owns the grid and the install
paths (see [store-architecture.md](store-architecture.md) §3). Packages we do not own are listed as `upstream` or `link`
entries in the catalog, so no repo of re-hosted packages is needed at first (D3).

Apps that will become store modules but already exist as repos (§2.1) need no new repo. Future apps need one repo each,
using the module contract in §3.

## 3. Architecture

### 3.1 Layers

```
GitHub (hosting)
  ├─ app releases: zip + .sha256 + manifest.json   (one repo per app, built by doannt-kindle-build)
  └─ catalog: index.json + manifests                (doannt-kindle-catalog, GitHub Pages)

Kindle (Oasis 3, jailbroken, Wi-Fi)
  ├─ base:    stock framework, jailbreak, hotfix (not ours; the store checks them)
  ├─ host:    Primitive Launcher (grid, settings, Wi-Fi, SSH, boot job, USB, store)
  ├─ apps:    Primitive Browser, Primitive Terminal, store-installed modules (KUAL, scriptlets)
  └─ shared:  primitive-keyboard, primitive-quick (compiled into each binary; not installed separately)
```

The launcher is the host and the only thing that starts at boot. Apps are modules: each one installs into its own folder
and gets a library entry or an `apps.toml` entry, so the launcher shows it on the grid. The store is a screen of the
launcher (decision D1), so one tile opens the catalog and installs what the user picks.

### 3.2 Contracts (to freeze in `doannt-kindle/docs/contracts.md` before S2)

**A. Library entry (scriptlet).** A `.sh` file in `/mnt/us/documents/` with these header lines, in this order:
`# Name:`, `# Author:`, optional `# Icon:` (a PNG as a data URI), `# DontUseFBInk`, and a marker line
`# PrimitiveLauncherEntry` for entries that the launcher itself runs. The launcher and browser already do this.

**B. Module folder.** `/mnt/us/<dir>/` holds the app's binary and data (`dir` defaults to the app's id; the existing
apps keep `launcher`, `browser`, `terminal`). The entry is a `.sh` in `documents/` that
runs the binary from the module folder (copying it to `/var/tmp` first if it must not hold `/mnt/us`, as the launcher
does now).

**C. KUAL extension.** `/mnt/us/extensions/<name>/` with `config.xml` and `menu.json` (already supported by the launcher).

**D. Package (zip).** One folder at the root named `<app-id>-<version>/`, containing `documents/` and/or `<app-id>/`
and/or `extensions/`, plus `INSTALL.md`, `LICENSE`, and `manifest.json`. The zip is paired with `<zip>.sha256`.

**E. Manifest (`manifest.json`, inside the zip and in the catalog).**

```json
{
  "id": "primitive-browser",
  "name": "Primitive Browser",
  "version": "0.2.16",
  "author": "Primitive AI",
  "licence": "AGPL-3.0-only",
  "repo": "https://github.com/DoanNguyenTrong/kindle-primitive-browser",
  "arch": ["armhf"],
  "firmware": { "min": "5.16.3" },
  "tested_on": ["KindleOasis3"],
  "requires": { "launcher": ">=0.3.0" },
  "files": [{ "from": "documents/Browser.sh", "to": "documents/Browser.sh" }],
  "install_dir": "/mnt/us/browser",
  "entry": "documents/Browser.sh",
  "icon": "icon.png",
  "sha256": "<zip sha256>",
  "size": 0
}
```

The `arch`, `firmware`, and `requires` fields let the store refuse what would not run (D5). The full schema is in
[store-architecture.md](store-architecture.md).

**F. Catalog index (`index.json`).** A list of `{ id, name, version, summary, category, manifest_url, icon_url }`, with a
`generated_at` date. The device fetches it over Wi-Fi and caches it in `launcher/cache/`.

**G. Versions.** Patch per device build, minor per phase, tag `v<version>` matching `Cargo.toml` (the launcher's rule).
A store update is offered when the catalog's version is newer than the installed one.

### 3.3 Install flow on the device

1. Store opens; it reads the cached index (or fetches it when Wi-Fi is on).
2. The user picks an app. The store checks `device`, `min_firmware`, `requires`, and free space (`/mnt/us` for modules,
   `/var/local` for the launcher's own copy; see §5 R1).
3. Download the zip to `/mnt/us/launcher/cache/` (staged name), verify `sha256` against the manifest, and refuse on a
   mismatch.
4. Unpack into a staging folder, check the file list against the manifest, then rename each part into place.
5. Register: write the library entry (or `apps.toml` entry) and tell the launcher to reload apps (`set_apps`, as the
   single-instance reload does now).
6. Record the install in `launcher/store/installed.json` (id, version, files), so update and uninstall know what to change.

Uninstall removes exactly the files in `installed.json`. Update replaces them in the same order, and keeps the previous
folder until the new one starts, so a failed update can be rolled back.

## 4. Execution strategy

Work runs in phases with a gate each. Every device step is run with the owner watching the Kindle, as before. Nothing is
published (tag, release, catalog entry) without the owner's go-ahead.

### Phase S0: decisions (answered 2026-11-19)

- [x] D1 — Store host: **our own store**, architected by us. KindleForge and KPM are references for knowledge only.
- [x] D2 — Hosting: **GitHub Releases** for binaries, **GitHub Pages** for the catalog index. No binaries in the catalog
      repo.
- [x] D3 — Licences: **re-host only** packages whose licence allows it; **link** the rest (for example CC BY-NC-SA).
- [x] D4 — First scope: **our three apps**, plus outside apps by link. Narrowed on 2026-11-19 by the owner's quality
      bar (store-submit-app §1): only outside apps with a real interface, familiar from iOS or Android, are linked
      (KOReader); KUAL extensions and scriptlets are not store listings.
- [x] D5 — Device scope: **all jailbroken Kindle e-readers**, not only the Oasis 3. Manifests declare the architecture
      (`armhf` hard-float, `armel` soft-float) and the firmware range; the store checks both on the device. Each app
      lists the models it was tested on.
- [x] D6 — Umbrella repo: **yes**, `https://github.com/DoanNguyenTrong/kindle-primitive.git` (git initialised locally on
      `main`, the four app repos ignored).
- [x] D7 — Deployed integrity uses SHA-256. The later H1 candidate adds opt-in Ed25519 verification for local
      review. Enabling production trust and publishing signed releases require owner approval. [Store signatures](store-signatures.md)
- [x] Gate S0: passed.

Documents to write before implementation (owner's order of request; written in this order):

- [x] `.agents/skills/primitive-ui/SKILL.md` — the UI and UX skill for every Primitive app.
- [x] `docs/store-architecture.md` — the store's system architecture and requirements.
- [x] `docs/store-submit-app.md` — how to add an app to the store.
- [x] `docs/store-install-apps.md` — how to install apps from the store.
- [x] `README.md` — the umbrella repo's README, "Primitive Redefined Kindle".

### Phase S1: fix the contracts and the missing basics

- [ ] Write `doannt-kindle/docs/contracts.md` with §3.2 (A–G) as the source of truth.
- [ ] Add `LICENSE` to `doannt-kindle-terminal` and `doannt-kindle-tools` (the owner chooses the licence; AGPL-3.0 to
      match the other two is the default).
- [ ] Fix the `tools` remote name (`kindle-primtitive-tools`) or document it, as the owner prefers.
- [ ] Release-check `v0.3.12` (launcher) and the browser's CI status. The owner checks the Actions tab (no `gh`).
- [ ] Gate S1: the contracts are written and the owner has read them.

### Phase S2: every app can be packaged

- [ ] Create `doannt-kindle-build` with a reusable workflow: zig setup pinned, build `armv7-unknown-linux-musleabihf`,
      run the tests, package the zip and `manifest.json`, write `.sha256`, publish on a `v*` tag.
- [ ] The launcher's `scripts/package-release.sh` becomes the first user of the build workflow.
- [ ] Add a package script to browser and terminal (none today; the browser ships by `deploy/install.sh` over USB).
- [ ] Terminal gets a release workflow and a tag (`v0.1.8` or the next version).
- [ ] Gate S2: one zip per app builds in CI, and the owner has unpacked each one and checked its files.

### Phase S3: the catalog

- [ ] Create `doannt-kindle-catalog`: `index.json` and `apps/<id>/<version>.json` manifests, a generator script
      (`scripts/build-index.sh`), GitHub Pages on.
- [ ] One entry each for the launcher, browser, and terminal, with the links from their releases.
- [ ] Gate S3: `index.json` is served by Pages, and each manifest's `sha256` matches its release asset.

### Phase S4: the store in the launcher

- [ ] Store screen: list (name, version, summary, installed or update), detail (repo, licence, device check), install,
      update, remove. Built from the existing UI (`primitive-keyboard` for text, `primitive-quick` for status).
- [ ] Installer (§3.3) with checks: device, firmware, requirements, free space, sha256, file list, rollback.
- [ ] `launcher/store/installed.json` written and read; uninstall removes exactly its files.
- [ ] Desktop screenshots of the store screens (as the launcher does for its screens).
- [ ] Tests: a fixture catalog and zip for the install, the sha mismatch, the rollback, and the uninstall.
- [ ] Device test (owner watching): install the browser from the store, open it from the launcher, update it, remove it.
- [ ] Gate S4: the install, update, and uninstall of one app work on the Kindle.

### Phase S5: migrate the existing apps to modules

- [ ] Browser: installable from the store; its USB installer stays for developers.
- [ ] Terminal: installable from the store; its SSH installer stays.
- [ ] Launcher: the store updates the launcher itself. This needs care: a launcher update replaces the running host, so
      the update runs from the launcher's boot-time copy on `/var/local` (`setup-boot.sh`), and the owner
      tests it on the Kindle before the next release.
- [ ] Each app's install docs point at the store first, with USB and SSH as the fallback.
- [ ] Gate S5: all three apps install, update, and remove from the store on the Kindle.

### Phase S6: list other projects

The detailed plan for KindleForge's 28 packages is [store-migration-kindleforge.md](store-migration-kindleforge.md)
(reviewed against the owner's quality bar: nothing is migrated; KOReader is a reference listing; notes, flashcards, a
focus timer and word and puzzle games are rebuilt as native Primitive apps).

- [ ] Add the KOReader reference listing (`link`, with its licence shown). We host nothing of it.
- [ ] Pick the native apps to build first (migration plan §5, M-D7). Each is its own repo and its own phase.
      All tasks are tracked in [implementation-plan.md](implementation-plan.md).
- [ ] Gate S6: the catalog lists KOReader with correct links, and the first native app is planned.

### Phase S7: hardening

- [ ] Production signature rollout, if approved. The H1 candidate has a local signing and verification fixture.
- [ ] Architecture and firmware checks against the manifest (`arch`, `firmware`), on hard-float and soft-float Kindles.
- [ ] A recovery path: the store never removes the launcher. The launcher's boot guard (`DISABLE`, `BOOT_KINDLE`) still
      works after a bad install.
- [ ] Gate S7: a bad package (wrong sha, wrong device, missing file) is refused on the Kindle, and the launcher still
      starts.

## 5. Risks

- **R1 — Storage.** The root filesystem has about 24 MB free and `/var/local` about 170 MB (from the device checks). Modules
  go on `/mnt/us`, which is the user storage, and the launcher's boot copy stays on `/var/local`. The store checks free
  space before install.
- **R2 — Drift.** A store update can change the launcher's boot copy. The launcher's setup step (0.3.18) rewrites the
  copy and the job from `/mnt/us/launcher` on each open, so a store update must leave those files consistent.
- **R3 — Jailbreak base and many models.** The store serves every jailbroken Kindle (D5), but our apps are tested on the
  Oasis 3 only. Manifests declare `arch` and `firmware`, and `tested_on` says where an app was checked. Soft-float
  Kindles (`armel`) need their own builds, which we do not make yet.
- **R4 — Site-specific content.** `doannt-kindle-browser/deploy/fix-hosts-truyendich.sh` removes a hosts-file override for
  one site. It must not be listed in any public catalog without the owner's review of its purpose and the legal position.
- **R5 — Licences.** The launcher (and the store in it) moves to PolyForm Noncommercial 1.0.0 for code and CC BY-NC-SA
  4.0 for docs and pictures (decided 2026-11-19); releases up to v0.3.20 stay AGPL-3.0. The browser moves with it (from 0.2.17). The tools
  crates are dual-licensed (AGPL-3.0 or PolyForm Noncommercial 1.0.0), so the terminal can stay AGPL-3.0: its engine is
  ported from KOReader's terminal (AGPL-3.0). KindleForge is GPLv3, the KindleTweaks Repository is CC BY-NC-SA 4.0, and two of our repos (terminal, tools)
  have no licence file. Re-hosting is limited to what D3 allows. The umbrella's docs and skills are CC BY-NC-SA 4.0.
- **R6 — KindleForge and KPM.** KindleForge is in maintenance and its rewrite on KPM has no date. The store does not
  depend on either. Compatibility with KPM's package format is nice to have (O3).
- **R7 — Security.** Installing over Wi-Fi from GitHub means the sha256 must be checked before anything runs. The SSH
  password is never stored in any repo or catalog. Wi-Fi keys are never logged.
- **R8 — Public repos.** The launcher and browser repos are public. Any new public repo (catalog, build, store) must be
  scanned for secrets before the first push, as the launcher's commits are.

## 6. Open items

- **O1** — Done: D1 to D7 answered (§4, S0).
- **O2** — The owner's choice of licence for `doannt-kindle-terminal` and `doannt-kindle-tools`.
- **O3** — Read the KPM wiki for its package format and decide whether our manifest should match it.
- **O4** — Confirm that the release CI for `v0.3.12` passed and that the browser's `feature/diagnostics-ssh` branch is
  merged or kept (the browser repo is not on `main`).
- **O5** — The launcher repo is on the local branch `chore/move-kindle-skills` (commit `234f7bd`, not pushed). Merge it to
  `main` or push it when ready.
- **O6** — Which external projects from Awesome-Kindle the store should list first (S6).

## 7. Summary of the first steps

1. Decide D1 to D7 (S0).
2. Freeze the contracts and fix the licence and remote gaps (S1).
3. Build the packaging workflow and package the three apps (S2).
4. Publish the catalog on GitHub Pages (S3).
5. Build the store screen and installer in the launcher, and test it on the Kindle (S4).
