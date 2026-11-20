# The store app: every function, and the design of what is not built

This describes the original standalone Store implementation on 19 November 2026. See the [Store architecture](../store-architecture.md)
and [current handoff](STATE.md) for released behaviour.

Repository: `doannt-kindle-store` (folder `/Users/doannguyen/Documents/GitHub/prai-workspace/doannt-kindle/doannt-kindle-store`).
Shared code: `doannt-kindle-tools` (folder `doannt-kindle-tools`, the store's submodule at `tools/`). Line numbers change; the
names are the reference.

## 1. The program: `crates/store-app/src/main.rs`

- `env_dir(name, default) -> PathBuf`: an environment variable as a path, or the default. Used for `KL_DIR` (default
  `/mnt/us/launcher`, the data folder shared with the launcher) and `KL_RUN` (default `/var/tmp/kl-store`, where the program
  copies its fonts and runs from).
- `font_paths(dir, run) -> Vec<String>`: the two Noto Sans files (`NotoSans-Regular.ttf`, `NotoSans-Bold.ttf`), from `run/fonts`
  if present, else `dir/fonts`.
- `main()`:
  1. `dir`, `run`, `root = dir.parent()` (`/mnt/us`). Logs `store v<version> dir <dir>`.
  2. `kl_store::install::recover(Paths::under(root))`: finishes or undoes an install a power cut interrupted; logs the result.
  3. `Settings::parse(dir/settings.txt)`; `input::TURN` set from `settings.rotation.turn()`.
  4. `Renderer::new(W, H, font_paths)`; on error logs and exits 2.
  5. `Ui::new(Vec::new(), Layout::new(W, H, 4, 5))`, `ui.version = <crate version>`, `ui.set_store(store::load_store(dir))`,
     `kl_render::load_store_pictures(renderer, dir/store/cache)`, `ui.open_store()`.
  6. `Display::open()`; `device::status(&settings)`; a channel `(tx, rx)`.
  7. Threads: touch (`input::find(profile::ACTIVE.touch_name)` → `input::touch_loop`), buttons (`input::find("gpio-keys")` →
     `input::button_loop`), a tick every second (`Ev::Tick`; stops when the receiver is gone).
  8. `display.show(renderer.draw(&ui, &status), &settings, true)` (a full refresh for the first frame).
  9. The loop, `while let Ok(ev) = rx.recv()`:
     - `Ev::Input(input)` → `ui.handle(input)`.
     - `Ev::Tick` → `device::status` again; `Redraw` only if `status.clock` changed.
     - `Ev::StoreRefreshed{entries, message}` → reload pictures; `ui.set_store(entries)`; `store_busy = false`; from a product
       page back to the list; `notice = message`; `Redraw`.
     - `Ev::StoreInstalled{entries, message}` → `set_store`; `store_installing = None`; back to the list if on a product
       page; `notice = message`; `Redraw`.
     - Anything else: nothing.
     - If `ui.screen == Screen::Home` (Done was tapped): log `store: done` and break (the program ends; the supervisor restarts
       the launcher, which takes the screen).
     - `Action::Redraw{full}` → `display.show`; `Action::Device(cmd)` → `device_command(...)` then `display.show`; other actions
       are not used by the store.
- `device_command(cmd, ui, dir, root, tx, status)`: the store's commands.
  - `StoreRefresh`: logs `store: refresh requested (wifi on: …, state: …)`. If connected (`status.wifi_on && wifi_state ==
    "connected"`): `store::start_store_refresh(tx, dir)`, notice `Updating the store...`. Else: `store_busy = false`, notice
    `Connect to Wi-Fi to update the store.`.
  - `StoreInstall(index)`: the entry's id and name from `ui.store[index]`. Connected: `store::start_store_install(tx, dir, id)`,
    notice `Installing <name>...`. Not connected: `store_installing = None`, notice `Connect to Wi-Fi to install from the
    store.`. No entry: `store_installing = None`.
  - `StoreRemove(index)`: `kl_store::install::remove(Paths::under(root), id)`. Ok: `set_store(store::load_store(dir))`,
    `screen = Store`, notice `Removed <name> from this Kindle.`, logs `store: removed <id>`. Err: notice `Could not remove …`.
  - Others: nothing.

## 2. The network and install work: `crates/store-app/src/store.rs`

- `STORE_CATALOG = "https://primitiveos.github.io/kindle-primitive-catalog/v1"`: the catalog's published site.
- `NetSource` (implements `kl_store::refresh::Source`): `text(url)` → `primitive_net::fetch_text(url, Policy::store(MAX_INDEX))`;
  `bytes(url, max)` → `primitive_net::fetch_bytes(url, Policy::store(max))`. Errors become strings.
- `start_store_refresh(tx, dir)`: a thread. Logs `store: refresh started`. Runs
  `kl_store::refresh::refresh(STORE_CATALOG, dir/store/cache, &NetSource)` under `catch_unwind` (a panic becomes the error
  `an internal error`). Message: `Store updated: N apps.` (plus `M could not be updated.` when some failed), or
  `The store could not be updated: <error>`. Then `load_store(dir)` and `Ev::StoreRefreshed{entries, message}`. Logs the result.
- `start_store_install(tx, dir, id)`: a thread. Logs `store: install of <id> started`. Runs `store_install_app(dir, id)` under
  `catch_unwind`. Message `Installed <id> <version>.` or `Could not install <id>: <error>`. Then `load_store` and
  `Ev::StoreInstalled{entries, message}`.
- `store_install_app(dir, id) -> Result<String, String>`:
  1. Reads `dir/store/cache/apps/<id>.json` (the listing); error `the app is not in the catalog the store has`.
  2. `device::store_device()` (architecture and firmware of this Kindle); error `the Kindle's firmware version cannot be read`.
  3. `kl_store::resolve::pick_version(&listing, &device)` (the newest version that runs here).
  4. `version.assets[device.arch]` (the package URL, SHA-256, size); error `no package for this Kindle`.
  5. `root = dir.parent()`; `paths = Paths::under(root)`; `downloads = dir/store/downloads` created.
  6. `zip = downloads/<id>-<version>-<arch>.zip`; `primitive_net::download(asset.url, zip, Policy::store(asset.size + 1), |_,_| {})`.
  7. `installed_at` from `date +%Y-%m-%d`.
  8. `kl_store::pipeline::install_downloaded(paths, listing, device, zip, asset.url, installed_at)` → the installed version.
- `load_store(dir) -> Vec<StoreEntry>`: reads the record `dir/store/installed.json` (default if missing); reads every
  `dir/store/cache/apps/*.json` as a `Listing` (bad files are skipped); one `StoreEntry::from_listing(listing, record.apps[id])`
  per listing; sorted by name.

The device facts (`device::store_device`) live in the shared kit: architecture `armhf` if `/lib/ld-linux-armhf.so.3` exists,
else `armel`; firmware from `/etc/prettyversion.txt`, else `/etc/version.txt` (`kl_store::version::firmware_from_text`).

## 3. The shared store model: `tools/crates/kl-core/src/store.rs`

- `enum StoreTab { Today, Apps, Updates }`.
- `enum Status { NotInstalled, Installed(String), Update { installed, latest } }`.
- `enum Kind { Install, Link }`: Link for a listing with `source: link` (KOReader). Never installed by the store.
- `struct StoreEntry`: `id, name, subtitle, developer, description, categories, licence, repo, kind, latest, status,
  changes (lines), size (armhf asset size of the newest version), firmware_min, tested_on, screenshots (count, at most 2)`.
- `StoreEntry::from_listing(listing, installed)`: the newest non-withdrawn version (`newest_live_entry`), the status (update
  when the newest version is newer than the installed one), the change lines, the size, firmware and tested-on facts.
- `StoreEntry::page_rows() -> Vec<(label, value)>`: `info_rows()`, plus a last row `("Remove from this Kindle", "")` when
  `can_remove()`.
- `StoreEntry::info_rows()`: Developer, Licence, Category (capitalised, comma-separated), Kindle firmware (`<min> or later`),
  Tested on (joined, or `Not yet`), Repository (without `https://`), then one `Change` row per change line.
- `can_remove()`: `kind == Install` and status Installed or Update.
- `status_line()`: Link → `Listed by link: the store does not install it.`; NotInstalled → `Version <latest>`; Installed →
  `Installed: version <v>`; Update → `Update ready: <installed> to <latest>`.
- `action_label()`: Link → `View`; NotInstalled → `Get`; Update → `Update`; Installed → `Installed`.
- `newest_live_entry(listing)`, `newest_live(listing)`: the newest version that is not withdrawn (by version order).
- `change_lines(changes)`: `Uses the internet.`, `Stops the Kindle's own screen while it runs.`, `Starts when the Kindle
  starts.`, `Changes the Kindle's system files.`, `Runs its own install steps.`, or `Changes nothing outside its own
  folder.`; the listing's notes appended.
- `format_size(bytes)`: `N bytes`, `N KB`, `N.N MB`.

## 4. The screens and their input: `tools/crates/kl-core/src/ui.rs` (store part) and `layout.rs` (store geometry)

State in `Ui`: `store: Vec<StoreEntry>`, `store_page`, `store_open: Option<usize>`, `store_tab`, `store_scroll`, `store_busy`
(a refresh runs), `store_installing: Option<id>`, `store_remove_armed: Option<id>`, `notice`, `version`.

- `set_store(entries)`: replaces the entries; resets the page, the open entry, the scroll (keeps the tab).
- `store_featured()`: `Some(0)` when there are entries. `store_today_rows()`: indices 1..min(3, len). `store_apps()`: all
  indices. `store_updates()`: entries whose status is not NotInstalled.
- `store_pages()`: pages of the current tab's list (rows per page from the layout).
- `open_store()`: tab Today, page 0, screen Store.
- `store_list(input)` (the tabs):
  - `PageForward`/`PageBack` → `store_page_key(±1)`: a list with more than one page turns the page; otherwise (and on Today)
    the tab changes (Today → Apps → Updates, no wrap).
  - Horizontal swipe → `store_turn(±1)` (the list page).
  - Tap on Done (`store_done`) → `screen = Home`.
  - Tap on Refresh (`store_refresh`) → if busy: nothing; else `store_busy = true` and `Action::Device(StoreRefresh)`.
  - Tap on a tab → `set_store_tab(tab)` (the page resets). The same tab: nothing.
  - Today: the featured card → `store_open_entry(0)`; See All → Apps tab; a row → `store_open_entry(index)`.
  - Apps/Updates: the page label's left half turns back, the right half forward; a row → `store_open_entry(index)`.
- `store_app(input)` (the product page):
  - `PageForward`/`PageBack`: scroll one screen (`height − 200`); `PageBack` at the top → back to the store.
  - Vertical swipe: scroll by the swipe, clamped to `store_scroll_max()`.
  - Tap on Back (`store_back`) → `Screen::Store`.
  - Tap on the action pill (`store_action(scroll)`): Link → notice `<name> is on its own website: <repo>`; installing (any) →
    nothing; Installed → nothing (no open action yet); otherwise `store_installing = id` and `Action::Device(StoreInstall(index))`.
  - Tap on the last row when `can_remove()`: the first tap arms `store_remove_armed` and sets notice `Tap Remove again to
    remove <name> from this Kindle.`; the second tap returns `Action::Device(StoreRemove(index))` and disarms.
- `store_open_entry(index)`: `store_open = Some(index)`, scroll 0, `Screen::StoreApp`.
- `store_scroll_max()`: `page_height(rows, shots) − height`, at least 0.
- `store_info_count(index) -> (rows, shots)`.

The geometry (`layout.rs`): `store_tabs` (the floating tab bar, 130 px at the bottom), `store_tab(i)`, `store_tab_at`,
`store_title` (top 50..160), `store_body_bottom`, `store_feature` (200..670, the featured card), `store_see_all`,
`store_today_row(i)`, `store_list_row(i)` (from y 200, 170 px rows), `store_rows_per_page`, `store_pages(n)`,
`store_page_label`, `store_row_at`, `store_done` (top right, 200 × 84), `store_refresh` (left of Done, 240 × 84), `store_back`
(top left), `store_hero(scroll)` (340 px icon, centred, from 190), `store_name` (570), `store_subtitle` (650), `store_action(scroll)`
(320 × 100 at 770), `store_developer` (895), `store_info_cells(scroll)` (three cells at 980, 150 high), `store_shot(i, scroll)`
(406 × 540 at 1190), `store_about(scroll, shots)` (1874 with screenshots, 1290 without), `store_info_row(i, scroll, shots)`
(from about top + 426, 100 px rows), `store_page_height(rows, shots)`. Constants: `STORE_TAB_BAR_H = 130`, `STORE_ROW_H = 170`,
`STORE_INFO_ROW_H = 100`.

## 5. The drawing: `tools/crates/kl-render/src/lib.rs` (store part)

- `store_list(ui)`: the large title (`Today`/`Apps`/`Updates`, 84 px bold), the Refresh capsule (outline; reads `Updating`
  while busy), the Done capsule (filled), the active tab's content, the tab bar, the notice (`store_notice`) above the bar.
- `store_today(ui)`: the featured card (black, 48 px corners): `FEATURED`, the name (68 px, two lines), the subtitle, the icon
  tile at the right (200 px), the action pill (white with a black label). Then `See All` and the `Apps` heading, then the two
  rows (`store_row`). With no entries: `store_empty` (a message).
- `store_rows(ui, indices, empty)`: the rows of one page (`store_row`) and the page label (`N of M`); `store_empty` when none.
- `store_row(entry, rect)`: the icon tile (132 px, `store_tile`), the name (40 px bold), the subtitle (28 px, grey), the action
  pill (`store_capsule`, filled for Get/Update), a hairline.
- `store_capsule(rect, label, primary, outline_ink)`: a filled pill (primary) or an outlined pill (3 px border), centred label
  (30 px bold).
- `store_tile(tile, entry, bg, ink)`: the app's picture when the cache has it at this size (key `store-icon:<id>:<px>`; the
  picture is skipped when its top is under the header), else a rounded tile in `bg` with the first letter in `ink`.
- `initial(tile, name, ink)`: the first letter, centred.
- `store_tab_bar(l, active)`: the bar (rounded frame), the three tabs (the active one filled), each with a glyph (`tab_glyph`)
  and a label.
- `tab_glyph(i, cx, cy, s, ink)`: a star (Today), four squares (Apps), a tray with an arrow (Updates).
- `store_notice(ui, y)`: the notice text (30 px bold, two lines) at `y`.
- `store_app(ui)`: the header band (white, 170 px, covers scrolled content, with a rule when scrolled), `‹ Store`, the hero
  tile, the name and subtitle (centred), the action pill, `Offered by <developer>`, the information strip (VERSION, SIZE,
  FIRMWARE with hairlines), the screenshots (`store-shot:<id>:<n>`, when present and below the header), `About` and the
  description (7 lines), `Information` and the rows (`page_rows`; the Remove row in bold), and the bottom notice band.
- `load_store_pictures(renderer, cache)`: `cache/icons/<id>.png` → `set_store_icon` (three sizes), `cache/shots/<id>-<n>.png`
  → `set_store_shot`.
- `Renderer::set_store_icon(id, png)`: `icon_tile` at 132, 200 and 340 px (rounded, dithered, outlined).
- `Renderer::set_store_shot(id, index, png)`: `picture_tile` at 406 × 540.
- Constants: `STORE_ICON_SIZES = [132, 200, 340]`, `STORE_SHOT_W = 406`, `STORE_SHOT_H = 540`.

## 6. The engine: `tools/crates/kl-store/`

- `catalog.rs`: the types. `Index { schema, generated_at, categories, apps: Vec<Card> }`; `Card { id, dir, name, subtitle, categories,
  icon, source, latest_version, arch, updated_at, listing }`; `Listing` (the app's full listing: `versions: Vec<VersionEntry>`
  with `assets: BTreeMap<arch, Asset{url, sha256, size}>`, `firmware {min, max}`, `requires`, `tested_on`, `withdrawn`);
  `Manifest { schema, id, dir, version, arch, firmware, requires, files, hooks }`; `Source { Hosted, Upstream, Link }`;
  `Listing::dir()` (the folder: `dir` or the id).
- `version.rs`: `Version { nums, packaging }`, `parse("1.2.3" | "2026.10" | "2.6-p1")`, total order (numbers, then packaging),
  equality from order; `firmware_from_text(text)` (the first dotted version of at least two numbers).
- `resolve.rs`: `Device { arch, firmware }`; `pick_version(listing, device)` → the newest version that has the architecture,
  runs on the firmware (`min` ≤ device ≤ `max`), is not withdrawn; errors `NotInstallable` (link), `NoArch`, `NoFirmware{need}`,
  `AllWithdrawn`. `missing_requirements(requires, installed_fn)` → the unmet `(id, range, installed)`.
- `verify.rs`: `sha256_file(path) -> (hex, size)` (streamed); `verify_file(path, sha, size)` (size first, then hash; the hash is
  compared in lower case).
- `unpack.rs`: `Limits { max_total_bytes: 200 MB, max_files: 5000 }`; `is_safe_relative(name)` (no absolute path, no `\`, no NUL,
  no empty part, no `.` or `..`); `is_allowed_place(name, dir)` (`documents/…`, `extensions/<dir>/…`, `<dir>/…`, never the
  reserved folders `documents extensions system fonts screensaver koreader`); `is_package_only(name)` (manifest, INSTALL.md,
  LICENSE*, hooks); `unpack(zip, dest, manifest, limits)`: pass 1 checks every name, the single top folder, links (symlink mode
  refused), sizes; pass 2 writes each installed file and keeps the zip's permission bits; the written list must equal the
  manifest's `files` exactly, both ways. `read_manifest(zip)`: the `<top>/manifest.json` entry.
- `record.rs`: `Record { schema, apps: BTreeMap<id, Installed> }`, `Installed { id, dir, version, arch, installed_at, source_url,
  sha256, files, requires }`; `load(path)` (missing → empty; damaged → error); `save(path, record)` (temp file, sync, rename);
  `dependents_of(id)`.
- `install.rs`: `Paths { root, staging, record, journal }` with `Paths::under(root)` (`root/launcher/store/…`); `Source { manifest,
  source_url, sha256, installed_at }`; `install(paths, source, fail_after)`: writes the journal (`Moving`), moves each file from
  `staging/<id>/<file>` into `root/<file>` (the old file kept as `<file>.prev`), journals each move, saves the record, then
  journal `Recorded`, then `finish`: removes the old-only files, the `.prev` copies, the journal, the staging folder. A failure
  undoes the logged moves (`undo`) and clears the journal. `recover(paths)`: `Recorded` → finish; `Moving` → undo and restore the
  record to its previous entry. `remove(paths, id)`: refused if another installed app requires it; deletes exactly the recorded
  files and the empty folders above them (never the root); saves the record without the app.
- `pipeline.rs`: `install_downloaded(paths, listing, device, zip, source_url, installed_at)`: `pick_version`; the asset for the
  architecture; `verify_file`; `read_manifest`; checks the id, the version and the architecture; `missing_requirements` against
  the record (error `needs <id> <range>…`); staging cleared and `unpack`; `install`. The zip is removed in every case.
- `refresh.rs`: `trait Source { text(url), bytes(url, max) }`; `MAX_INDEX = 1 MB`, `MAX_LISTING = 256 KB`, `MAX_PICTURE = 1 MB`,
  `SHOTS_PER_APP = 2`; `refresh(base, cache, source) -> Report { refreshed, failed: Vec<(id, reason)>, removed }`:
  reads `base/index.json` (must be schema 1); for each card: the listing `base/apps/<id>.json` (id must match), the icon
  `base/icons/<id>.png` (must be a PNG), the screenshots `base/shots/<id>-<n>.png` (PNG) for n below
  `min(listing.screenshots, 2)`; writes the files atomically; a failed app keeps its cache; removes cached files of apps no
  longer listed; writes `index.json` last.
- `primitive-net` (`tools/crates/primitive-net/src/lib.rs`): `Policy::store(max)`: hosts `github.com`,
  `objects.githubusercontent.com`, `release-assets.githubusercontent.com`, `raw.githubusercontent.com`,
  `doannguyentrong.github.io`; HTTPS only; 120 s timeout; 5 redirects. `host_of(url)`, `allowed(url, policy)`. `open` follows
  redirects by hand (each target must be allowed; relative `Location` resolved). `download(url, dest, policy, progress)`:
  streams to `dest.part`, renames when complete, removes the part on error, refuses a larger announced length.
  `fetch_text`, `fetch_bytes`: the same, in memory, with the size limit.

## 7. The device layer: `tools/crates/kl-kindle/src/`

- `lib.rs`: `enum Ev` (all events: `Input`, `Tick`, `Usb`, `UsbRedraw`, `Turn`, `Background`, `Wifi`, `WifiResult`, `Notice`,
  `StoreRefreshed`, `StoreInstalled`); `log(msg)` (stderr, `[kl] …`).
- `display.rs`: `Display::open()` (the panel, or none with a log line); `show(upright, settings, full)` (a GC16 full
  update when asked or when the size changed; otherwise the changed rectangle, DU when black and white, AUTO otherwise);
  `show_region(upright, area, settings)` (a pop-up area only).
- `input.rs`: `find(name_hint)` (the input device by its name); `touch_loop(path, tx)` (touch events → `Ev::Input`, taps and
  swipes); `button_loop(path, tx)` (the page buttons and the power key); `gesture(start, end, held)`; `turn_point(turn, x, y)`
  (touch mapped to the screen's turn); `TURN` (the current turn, an atomic).
- `device.rs`: `status(settings) -> Status` (clock, date, Wi-Fi on and state, battery, USB, storage, memory, CPU); `wifi_info()`;
  `store_device()`; `power_loop(tx)` and `power_event(line)` (the power key → sleep and wake); `orientation_loop(tx, start)` and
  `accelerometer_turn()` (auto rotation); `system_command(cmd)` (`sync; /sbin/<cmd>`, detached); `set_wifi`, `join_network`,
  `forget_network`, `set_light`, `set_warmth`, `set_ssh`, `set_public_dns`, `set_autostart`, `unload_stock_screensaver`,
  `free_storage`, `restart_launcher`.
- `eink.rs`: the panel driver (MXCFB ioctl, waveform constants `WAVE_GC16`, `WAVE_DU`, `WAVE_AUTO`).
- `profile.rs`: `Profile` (names, screen size 1264 × 1680, touch device name, page key codes, the battery and charger paths),
  `ACTIVE` = the Oasis 3.

## 8. Features not built yet: the design (in the order the pipeline takes them)

Each design names its inputs, outputs, and the steps. Where a launcher function does the same job, copy it and note the source.

### 8.1 Sleep and wake in the store app (T1)

- The events: `device::power_loop(tx)` runs `lipc-wait-event` for `goingToScreenSaver`, `outOfScreenSaver` and
  `exitingScreenSaver` and sends `Ev::Input(Input::Sleep)` or `Ev::Input(Input::Wake)` (through `device::power_event`).
  The store does not start `power_loop` yet (it is missing from `main`).
- The UI already handles them (`tools/crates/kl-core/src/ui.rs`, `Ui::handle`): `Sleep` remembers the screen (`before_sleep`),
  sets `Screen::Sleep` and returns `Action::Redraw{full: true}`; `Wake` restores `before_sleep` and returns `Redraw{full: true}`
  (a second wake event is ignored).
- The store's loop must NOT draw while asleep: the launcher skips `Redraw` when `ui.screen == Screen::Sleep` and there is no
  battery message and no sleep picture (its `main.rs`, the arm `Action::Redraw { .. } if ui.screen == Screen::Sleep ...`).
  Copy that arm into the store's loop (the store has no sleep picture: skip every redraw while `Screen::Sleep`).
- Design: in `main`, start `device::power_loop(tx.clone())` in a thread; in the loop, `Action::Redraw` is skipped while
  `ui.screen == Screen::Sleep`. A wake redraws full. The clock thread keeps ticking; a tick while asleep changes nothing.
- Test (Mac): `Ui` tests for `Sleep` and `Wake` exist in `kl-core` (`ui.rs` tests). Add a store-loop test when T7 moves the
  device command logic into a testable function.

### 8.2 Auto rotation in the store app (T2)

- Source: `device::orientation_loop(tx, start)` and `Ev::Turn(Rotation)` (the launcher's loop handles `Ev::Turn`).
- Design: start `orientation_loop(tx, settings.rotation)`. On `Ev::Turn(r)`: `settings.rotation = r`, `input::TURN` updated,
  the orientation file written as the launcher does, redraw full. Only when `settings.auto_rotation` is on.

### 8.3 Crash log (T3)

- Source: the launcher's `install_crash_log()` and `on_fatal` (`main.rs`): a signal handler that writes to `log` and
  restores the default handler.
- Design: copy it into the store as `install_crash_log()`, writing `dir/log-store.txt`. The threads already catch panics.

### 8.4 Refresh on open and the daily check (T4)

- Design: on start, if Wi-Fi is connected and the cache's `index.json` is older than 24 hours (file mtime), start
  `start_store_refresh`. Setting `store_daily_check` (default on) in `settings.txt` (the store reads it; the launcher's settings
  page can show it later). A tick check once per hour while awake.

### 8.5 The Search tab (T5)

- Design: a fourth tab (`StoreTab::Search`) with a field at the top (the shared keyboard: copy the launcher's
  `Screen::Password` / `NetworkName` keyboard pattern from `ui.rs` and `layout.rs keyboard_*`). Results: the entries whose
  name, subtitle, developer or categories contain the text (case-insensitive), as rows (`store_row`). The tab bar becomes four
  items (the glyph: a magnifier, a circle and a handle, drawn with the existing path helpers).

### 8.6 The install sheet (T6a)

- Design: `Get` opens a pop-up over the product page (the launcher's `confirm_box` pattern in `layout.rs`, 600 px high): the
  name, the size (`format_size`), `What this app changes` (the change lines), a warning line for `system` categories or for
  `starts_at_boot`/`root_filesystem` changes, and two buttons: Cancel and Install. Install starts `StoreInstall` as today.
  Progress steps (Downloading, Checking, Installing) replace the pop-up text, from `Ev` notices sent by `start_store_install`
  (add `Ev::Notice` sends at the three steps; the download's progress callback is not drawn).

### 8.7 Store tests (T6)

- The store app has no tests. Move the pure logic of `device_command` into a function returning the next `(notice, action)`
  and test it. Test `load_store` with a temporary folder (a listing and a record) and `store_install_app` with a fixture
  package (use `kl_store::unpack::fixtures` as `pipeline.rs` does).

### 8.8 Store desktop preview (T7)

- Design: the launcher's `kl-desktop` already renders every store screen (`store-today.png`, `store-apps.png`,
  `store-updates.png`, `store-app.png`, `store-app-scrolled.png`, `store-link.png`). Keep it; add the Search and install-sheet
  screens to it when they exist. The desktop build reads the catalog from `../doannt-kindle-catalog`.

### 8.9 Publish the store as a package (T8; needs the owner's go-ahead)

- Design: the store repo gets `scripts/stage.sh` (stages `store/bin/kl-store-app` and `documents/Store.sh` in `build/stage`),
  and `.github/workflows/release.yml` as in the browser (test; `cargo zigbuild -p store-app`; `stage.sh`; the build repo's
  `scripts/package.py --id primitive-store --dir store --version <tag> --arch armhf --stage build/stage --license LICENSE
  --install INSTALL.md --firmware-min 5.16.3 --out dist`; `softprops/action-gh-release` publishes `dist/*`). Tag `v0.1.0`.
  Then the catalog listing `apps/primitive-store/app.json` (developer Primitive AI, category `system`? (the owner decides), the
  description, `changes`: `network: true`, `starts_at_boot: false`, `root_filesystem: false`, notes: "Installs apps from the
  catalog into /mnt/us."), `icon.png` (256 px grayscale; design first and ask the owner), `asset` from the downloaded release
  file (size and SHA-256 from `curl` of the asset URL; the store's `check-assets.py` checks it). Then `sh scripts/test.sh` and
  push. The Pages site rebuilds.
- Remove guard: the store must not offer Remove for itself. Add to `StoreEntry::can_remove()`: `id != "primitive-store"`
  (keep the constant in one place).

### 8.10 The launcher's bootstrap (T9; a launcher deploy; the owner present)

- Current launcher: a built-in `Launch::Store` tile (`apps.rs` builtins: id `store`, order 9000) that opens `Screen::Store`
  inside the launcher (the old store code: `kl-core/src/store.rs`, `ui.rs` store functions, `kl-render` store functions,
  `kl-launcher/src/main.rs` store functions). Remove that code after the bootstrap works.
- Design: the built-in tile's tap: if `/mnt/us/store/bin/kl-store-app` exists → `Launch::Script` of `/mnt/us/documents/Store.sh`
  (the same as any library entry; the supervisor runs it). Else → the install path: refresh only the store's listing
  (`refresh::refresh` restricted to the `primitive-store` card, or a single-listing fetch), then `install_downloaded` for
  `primitive-store` (the same code the store uses), then `load_library` and `set_apps` (the launcher's reload), then open it.
  Show progress notices (`Ev::Notice`) and the Wi-Fi check (as the store does). Hide the built-in tile when `documents/Store.sh`
  exists (`apps.rs merge`: drop the builtin with id `store` when a discovered app has the name `Primitive Store`).
- After the bootstrap works: delete the launcher's store UI and engine code (kl-core `store.rs`, the store parts of `ui.rs`,
  `layout.rs`, `kl-render`, `kl-launcher/src/main.rs`) and the `kl-store` dependency; the store engine stays in tools for the
  store app. Bump the launcher to a new minor version (`--minor`) for this phase.

### 8.11 Hardening (T10)

- Download progress on the screen (the install sheet, 8.6), a timeout message, the storage check before a download (`statvfs`:
  three times the size of the package must fit on `/mnt/us`: `free_storage()` exists in `device.rs`).
- `kl-store::install::remove` for `dir` folders that the Kindle uses (refused reserved names are in `unpack.rs`).
- A package for a device that is not armhf: `armel` builds are not made yet; listings declare `armhf` only.
