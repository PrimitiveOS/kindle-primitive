# Architecture: how the pieces fit

This is the 19 November 2026 handoff snapshot. For the released system, see the [platform plan](../kindle-platform-plan.md)
and [Store architecture](../store-architecture.md).

## The idea

PrimitiveOS is an operating environment for jailbroken Kindle e-readers. The **launcher** is the home screen and starts
with the Kindle. Every other app is a separate program with its own repository, installed into the Kindle's storage, and
opened from the launcher's grid. The **store** is one of those apps. The launcher only needs to know how to start an app and
how to install one; it does not need the store's code to build.

```
                 GitHub
  app repos ── Releases (zip + sha256)           catalog (Pages): index.json, apps/*.json, icons, shots
       │                                                    │
       │  one shared packager (build repo)                  │  Refresh (HTTPS, store hosts only)
       ▼                                                    ▼
  ┌──────────── Kindle (Oasis 3, armhf, 5.18.2) ───────────────────────────────────────────┐
  │ launcher (kl-launcher)      the home screen; built-in Store tile = bootstrap (todo)    │
  │   │ opens an app: writes `next`, exits 10; the supervisor runs it                       │
  │   ├─ Primitive Browser      /mnt/us/browser/…   documents/Primitive Browser.sh           │
  │   ├─ Primitive Terminal     /mnt/us/terminal/…  documents/Terminal.sh                   │
  │   ├─ Store                  /mnt/us/store/bin/kl-store-app   documents/Store.sh          │
  │   └─ KOReader (stock UI path, library)                                                  │
  │ store data (shared with the launcher): /mnt/us/launcher/store/{cache,downloads,         │
  │   staging,installed.json,journal.json}                                                  │
  └──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Repositories and what each one is for

| Repo | Contains | Builds |
|---|---|---|
| `kindle-primitive-tools` (the **shared kit**) | `kl-core` (screens, layout, the store model, the UI state machine), `kl-render` (the renderer: text, pictures, pop-ups, the store's screens), `kl-kindle` (the device layer as a library: `device`, `display`, `eink`, `input`, `profile`, `Ev`, `log`), `kl-store` (the store engine: catalog, record, resolver, verify, unpack, install, refresh, pipeline), `primitive-net` (HTTPS with an allow list), `primitive-keyboard`, `primitive-quick` | `cargo test --workspace` (14 suites) |
| `kindle-primitive-launcher` | `crates/kl-launcher` (the launcher's program, `main.rs`), `crates/kl-desktop` (the desktop preview: PNG renders of the screens) | `scripts/build-device.sh` (tests, supervisor test, cross build, install) |
| `kindle-primitive-store` | `crates/store-app` (the store's program: `main.rs` event loop, `store.rs` network and install work), `deploy/Store.sh`, `deploy/install-ssh.sh` | `cargo zigbuild --release -p store-app --target armv7-unknown-linux-musleabihf` |
| `kindle-primitive-browser` | Primitive Browser (its own engine, `kb-*` crates), `scripts/stage.sh`, `scripts/package-release.sh`, `.github/workflows/release.yml` | `scripts/build-device.sh`; the release workflow publishes the store package |
| `kindle-primitive-catalog` | `apps/<id>/` (published listings with `icon.png` and `shots/`), `drafts/`, `schema/`, `scripts/build-index.py`, `scripts/check-app.sh`, `scripts/check-assets.py`, `scripts/test.sh`, `.github/workflows/catalog.yml` (Pages) | `sh scripts/test.sh`; CI on push to `main` |
| `kindle-primitive-build` | `scripts/package.py` (the packager: zip, manifest, `.sha256`), `.github/workflows/package.yml` (reusable release workflow), `schema/manifest.schema.json` | used by each app's release |
| `doannt-kindle` (umbrella) | README, plans, store docs, the skills (`.agents/skills/primitive-ui`, `kindle-device`, `kindle-eink`) | none |

## How an app gets onto the Kindle

1. **USB (the first install, and the launcher's only path until the bootstrap):** the zip from a release is copied onto
   the Kindle drive (`launcher/`, `documents/`), then the launcher is opened from the library. The launcher's first open runs
   `setup-boot.sh`, which copies its boot files to `/var/local` and writes the boot job.
2. **The store (every other app):** the store's catalog lists an app with a hosted asset (URL, SHA-256, size). A tap on Get:
   the device checks the Kindle (architecture `armhf` from `/lib/ld-linux-armhf.so.3`; firmware from `/etc/prettyversion.txt`),
   picks the newest version that runs there, downloads the zip (HTTPS, allow list, size limit), verifies size and SHA-256,
   checks the manifest (id, version, architecture, requirements), unpacks it safely into `staging/`, and installs it: each
   file is moved into `/mnt/us/<dir>/…` with the old copy kept as `.prev`; the record `installed.json` is written; the
   journal is cleared; `.prev` copies and the old-only files are removed. A failure restores the old files.
3. **The launcher's library:** `documents/*.sh` entries appear on the grid by themselves (the launcher reads the library at
   start and after an eject). A new store app therefore appears after the launcher reads the library again (a restart).

## The launcher's loop and the store's loop (the same pattern)

Both programs are one `main()` with one `loop { rx.recv() }` over `Ev` events from threads:

- `Ev::Input(Input)` from `input::touch_loop` and `input::button_loop` (touch, page buttons, power button).
- `Ev::Tick` from a thread every second (the clock; redraw only when the clock text changes).
- `Ev::StoreRefreshed{entries, message}` and `Ev::StoreInstalled{entries, message}` from the store's threads.
- `Ev::Turn(Rotation)` from `device::orientation_loop` (launcher only; the store does not read it yet).
- The screen: `ui.handle(input) -> Action`; `Action::Redraw{full}` redraws (`Display::show`); `Action::Device(cmd)` runs a
  command (`device_command` in the store, `run_device` in the launcher).
- Done (the store's `Screen::Home`) ends the program: the store's `main` breaks out of the loop and returns; the supervisor then
  starts the launcher again, which takes the screen.

## The data on the Kindle (paths, owned by whom)

| Path | Written by | Read by |
|---|---|---|
| `/mnt/us/launcher/settings.txt`, `apps.toml`, `icons/`, `screensavers/`, `fonts/` | the launcher | the launcher, the store (fonts and rotation) |
| `/mnt/us/launcher/store/cache/index.json`, `apps/<id>.json`, `icons/<id>.png`, `shots/<id>-<n>.png` | the store's refresh | the store (`load_store`, `load_store_pictures`) |
| `/mnt/us/launcher/store/downloads/<id>-<version>-<arch>.zip` | the install (deleted after the install) | the install |
| `/mnt/us/launcher/store/staging/<id>/…` | the install (deleted after) | the install |
| `/mnt/us/launcher/store/installed.json` | the install and remove (`record::save`, atomic) | the store (status), the launcher (later) |
| `/mnt/us/launcher/store/journal.json` | the install (cleared at the end) | startup `recover` |
| `/mnt/us/<dir>/…` (`browser`, `terminal`, `store`, …) | the install | the app |
| `/mnt/us/documents/*.sh` | the install (library entries) and USB installs | the launcher's grid |
| `/var/tmp/kl-store/` | the store's library entry (copies the binary here, runs it from there) | — |
| `/var/local/primitive-launcher/` | the launcher's setup (boot copy) | the boot job |
