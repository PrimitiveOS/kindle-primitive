# The pipeline: the ordered work, the checks, and the stop points

This is the 19 November 2026 standalone Store delivery plan. Follow the [implementation plan](../implementation-plan.md)
for current work and the [current handoff](README.md) for setup and operating instructions.

## What this handoff approves (read first)

This handoff lives in the umbrella repo at `docs/handoff/` (there is no separate handoff repo). Every path in this file is
relative to the umbrella folder `doannt-kindle/`.

The owner is away and asked for one agent that does not stop. This handoff approves, without asking again:

- Commits on feature branches (`feature/<name>`) in every repo listed in STATE.md, and in the umbrella on `feature/handoff`,
  with explicit paths (RULES.md).
- Pushing feature branches.
- Writing code, tests, docs, and desktop screenshots (the owner reviews them later).
- Building the store for the Kindle (`cargo zigbuild`), and installing the store on the Kindle **only when the owner is
  present** (see the device gates).

This handoff does NOT approve, and the agent must stop and wait for the owner:

- Merging into `main` and pushing `main`, in any repo. Every "Merge" step below means: finish the branch, run its checks,
  and report it as ready to merge in the final message. The owner's go-ahead is needed to merge.
- Any device step that needs a hand (a tap, a restart, a power button). Prepare everything on the Mac first.
- Any launcher deploy (`scripts/build-device.sh`), any new launcher version.
- Releases, tags, GitHub release assets, and catalog listings that make an app public (T8).
- Creating GitHub repos, changing repo settings, enabling anything on GitHub.
- The icon for the store (design first, show the owner, ask permission before applying it).
- The store's catalog category and the listing text for the public catalog (propose; the owner decides).

Where a step is blocked on a stop item, do the next unblocked task. Report the stop items in the final message.

## Preconditions (check before T1)

Run from the umbrella folder `doannt-kindle/`; each line must pass.

1. `cd doannt-kindle-tools && cargo test --offline --workspace` → every `test result:` line is ok and none says FAILED (31 `#[test]` functions in 7 crates).
2. `cd doannt-kindle-launcher && cargo test --offline --workspace` → ok (one crate has tests: `kl-launcher`).
3. `cd doannt-kindle-store && cargo build --offline` → builds (the store has no tests yet). The `tools` submodule is at
   `cdb95ae` or later (`git -C tools log --oneline -1`).
4. `cd doannt-kindle-store && cargo zigbuild --offline --release -p store-app --target armv7-unknown-linux-musleabihf` →
   builds (about 30 to 60 s).
5. The store on the Kindle is `0.1.0` (`sha256sum /mnt/us/store/bin/kl-store-app` starts with `e3ddd257` if nothing changed).
   Check with SSH (ENVIRONMENT.md). If the Kindle is unreachable, skip the device checks and continue on the Mac.

## T1. Sleep and wake in the store (STORE-APP.md 8.1)

- Change: in `doannt-kindle-store/crates/store-app/src/main.rs`: start `device::power_loop(tx.clone())` in a thread; skip
  `Action::Redraw` while `ui.screen == Screen::Sleep` (copy the launcher's arm: launcher `crates/kl-launcher/src/main.rs`,
  search `Screen::Sleep` near `Action::Redraw`).
- Branch: `feature/store-sleep`. Commit with explicit paths.
- Check (Mac): `cargo build --offline`; a unit test is not required here (T7 adds the testable loop). The `Ui` side is tested
  in tools.
- Merge: report the branch ready to merge (see the approvals above); do not merge or push `main`.
- Device gate: none for T1 on its own (the owner's gate D1 covers the whole store).

## T2. Auto rotation in the store (STORE-APP.md 8.2)

- Change: `device::orientation_loop(tx, settings.rotation)` thread (only when `settings.auto_rotation`); on `Ev::Turn(r)`:
  set `settings.rotation = r`, `input::TURN.store(r.turn())`, write `run/orientation` (the launcher's `write_atomic` helper:
  copy it), and `Redraw{full: true}`. The `Ev::Turn` variant is in `kl-kindle/src/lib.rs`.
- Branch `feature/store-rotation`. Check: `cargo build --offline`. Merge and push as in T1.

## T3. Crash log (STORE-APP.md 8.3)

- Change: copy `install_crash_log()` and `on_fatal` from the launcher's `main.rs` into the store's `main.rs` (the file path:
  `dir/log-store.txt`). Keep the `libc` signal calls as in the launcher.
- Branch `feature/store-crash-log`. Check: `cargo build --offline`. Merge and push.

## T4. Refresh on open, and the daily check (STORE-APP.md 8.4)

- Change: on start, if `status.wifi_on && wifi_state == "connected"` and `dir/store/cache/index.json` is older than 24 h
  (use `fs::metadata(...).modified()`), call `store::start_store_refresh(tx.clone(), dir.clone())` and set `ui.store_busy = true`.
  A setting `store_daily_check` (default on) read from `settings.txt` (key `store_daily_check=0|1`; add the parser line in
  `kl-core/src/settings.rs` in tools: test it). An hourly check while awake (a thread that sends `Ev::Tick` already exists:
  count ticks).
- Branch `feature/store-daily-check` in both tools and the store (the settings parser is in tools). Check: `cargo test` in
  tools (the new settings test), `cargo build` in the store. Merge both into their `main`s and push.

## T5. The Search tab (STORE-APP.md 8.5)

- Change: `StoreTab::Search` in `kl-core/src/store.rs`; `Ui` search field (copy the `Screen::NetworkName` editor pattern in
  `kl-core/src/ui.rs`, `layout.rs` `keyboard_*`, `kl-render` network name screen); results = `store_apps()` filtered by the
  text (name, subtitle, developer, categories; case-insensitive); the tab bar with four tabs (`layout.rs store_tab`
  widths; `store_tab_at`; `kl-render store_tab_bar` names and glyph); the glyph for Search: a circle and a handle drawn with
  `tab_glyph`.
- Tests in tools: a filter test (`store_search(text) -> Vec<usize>`), a tab-switch test with four tabs.
- Branch `feature/store-search` in tools (and the store's `store_list` tab mapping). Check: tools tests; desktop render
  (`cargo run --offline -q -p kl-desktop -- --documents /tmp/empty --out /tmp/shots` in the launcher; the store's Search
  screen needs the screen added to the desktop preview: T7). Merge tools to main; the launcher's tools pin moves
  (`git -C tools fetch -q origin && git -C tools checkout -q <commit>`) and the launcher's `main` gets the pin: THIS IS A
  LAUNCHER MERGE: stop and ask the owner before merging the launcher (the pin alone changes the launcher's build).

## T6. The install sheet, progress, and the store's tests (STORE-APP.md 8.6, 8.7)

- Change (8.6): `Get` opens the sheet (a pop-up over the product page: name, size, change lines, the warning for system and
  boot changes, Cancel and Install). Install starts the install as today. Progress: `start_store_install` sends
  `Ev::Notice(String)` at `Downloading <name>`, `Checking <name>`, `Installing <name>` (`Ev::Notice(String)` already exists in `doannt-kindle-tools/crates/kl-kindle/src/lib.rs`; send it; the handler in
  the store's loop sets `ui.notice`). The sheet's layout: a new `Layout::store_sheet()` (copy `confirm_box`/`confirm_buttons`).
- Change (8.7): move the logic of `device_command` into a pure function `store_command(cmd, status, ui_entries) -> (notice,
  Effect)` in the store crate, and test it (connected and not connected, a missing index, a remove). Test `load_store` with a
  temporary folder (a listing file and a record file). Test `store_install_app` with a fixture zip (see
  `kl-store/src/pipeline.rs` tests: `package` and `listing_for`; move the helpers into a shared test module or copy them).
- Branch `feature/store-sheet` (store) and `feature/store-sheet` (tools, for the layout and the notice enum if shared).
  Check: `cargo test --offline` in the store (the new tests) and in tools. Merge both to `main`. Push.

## T7. Desktop preview and the store's own rendering check (STORE-APP.md 8.8)

- Change: the launcher's `kl-desktop` renders the store screens: add the Search screen and the install sheet (`ui.store_tab =
  StoreTab::Search`, the sheet state) to `crates/kl-desktop/src/main.rs` (the store block near `store-today.png`).
- This is a launcher change to a desktop tool, not a device behaviour: the launcher's `main` merge is NOT needed for a desktop
  file, but the commit is in the launcher repo: stop and ask before merging the launcher. Commit on a branch.
- Output: the screenshots in `docs/store-screens/` of the umbrella repo (copy the new PNGs, add rows to its README). Commit
  the umbrella change on a branch; merge only when the owner says so.

## D1. Device gate: the store works on the Kindle (OWNER PRESENT; a stop point)

Prepare first (Mac): `cargo zigbuild --offline --release -p store-app --target armv7-unknown-linux-musleabihf` in the store
folder; then the install (`deploy/install-ssh.sh`) through the expect wrapper (ENVIRONMENT.md). Then ask the owner to do:

1. Open the library entry **Primitive Store** (after a launcher restart: Settings › Device › Restart the launcher).
   Expected log: `store v0.1.0 dir /mnt/us/launcher`.
2. Tap **Refresh** with Wi-Fi on. Expected log: `store: refresh requested (wifi on: true, state: connected)`, `store:
   refresh started`, `store: refreshed 2 apps, 0 failed, 0 removed` (2 apps: KOReader and the browser, after the catalog
   publish). Check the cache: `ls /mnt/us/launcher/store/cache/apps` shows both JSON files.
3. Open **Primitive Browser**'s page, tap **Get**. Expected: the notice `Installing Primitive Browser...`, then
   `store: install of primitive-browser started`, then `Installed primitive-browser 0.2.17.` (the store overwrites the
   manual install's files; the record `installed.json` gets the entry). The browser then shows **Remove from this Kindle**.
   Check: `grep -E "store|install" /mnt/us/launcher/log-launcher.txt | tail`.
4. Tap Remove twice on the browser's page: expected `store: removed primitive-browser` and the browser gone from the
   record. (Only after 3 worked; the browser is then re-installed by USB or by Get again.)

Stop here: the owner reports what the screen shows. Fix what the logs show as errors before continuing.

## T8. Publish the store as a package (a stop point: needs the owner's go-ahead)

- Preconditions: D1 passed. The owner has said "publish the store".
- Change (store repo): `scripts/stage.sh` (copy of the browser's, for the store: `store/bin/kl-store-app` and
  `documents/Store.sh`), `.github/workflows/release.yml` (copy the browser's; `--id primitive-store --dir store`,
  `--license LICENSE`, `--install README.md`), `LICENSE` (PolyForm Noncommercial 1.0.0 text: copy from the launcher's
  `LICENSE`; the Required Notice line for the store), `INSTALL.md` (install by the store; by USB as a fallback).
- Commit, merge to the store's `main`, push, tag `v0.1.0` (the owner approves the tag at this point: stop before tagging).
- After the tag: the release page (public) lists `primitive-store-0.1.0-armhf.zip`. Download it with curl and record its
  size and SHA-256 (`/usr/bin/curl -sL -o x.zip <url>`; `shasum -a 256 x.zip`).
- Catalog (`doannt-kindle-catalog`): `apps/primitive-store/app.json` (copy `apps/primitive-browser/app.json`; `id`
  `primitive-store`, `dir` `store`, `source` `hosted`, `categories` `["system"]` (PROPOSE; the owner decides), the description,
  `changes` (`network: true`, `stops_kindle_ui: true`, `starts_at_boot: false`, `root_filesystem: false`, `hooks: false`,
  notes `Installs and removes apps in /mnt/us.`), `versions[0]` with the asset URL, SHA-256 and size, `firmware.min`
  `5.16.3`, `requires` `{}`, `tested_on` `["KindleOasis3"]`). The icon: design it (ask the owner: show the PNG, wait for
  permission). Screenshots: `shots/` from the store's desktop preview (T7), at 632 × 840.
- Check: `sh scripts/check-app.sh apps/primitive-store`, `sh scripts/test.sh` (with the venv python first on PATH),
  `python3 -I scripts/check-assets.py apps/primitive-store` (downloads the asset and checks it). Commit on a branch, merge to
  the catalog's `main` only with the owner's go-ahead (publishing), push. Pages rebuilds in a few minutes; check
  `https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json` lists `primitive-store`.

## T9. The launcher's bootstrap (a launcher deploy: a stop point with the owner present; STORE-APP.md 8.10)

- Change (launcher repo, branch `feature/bootstrap`): the built-in tile id `store` (kl-core `apps.rs builtins`, `Launch::Store`)
  becomes: if `/mnt/us/store/bin/kl-store-app` exists → open `documents/Store.sh` through `Launch::Script`; else → install
  the store (`kl_store::refresh` for the one `primitive-store` card, then `pipeline::install_downloaded`, then the launcher's
  library reload `load_library` + `ui.set_apps` + `set_extensions`, then open). The tile is hidden when a discovered app
  named `Primitive Store` exists (`apps.rs merge`).
- Remove after it works (same branch): the launcher's store code (kl-core `store.rs`, the store parts of `ui.rs`, `layout.rs`,
  `kl-render`, `kl-launcher/src/main.rs` store functions, `kl-store` dependency).
- Store side: `StoreEntry::can_remove()` returns false for `primitive-store` (the store cannot remove itself).
- The launcher's version: a new minor version (`--minor`) for this phase.
- Check (Mac): launcher tests; the desktop preview of the built-in tile; `cargo zigbuild` for the device.
- Device gate (owner present): install the launcher (`scripts/build-device.sh --minor`, expect wrapper), restart, tap the
  built-in icon on a Kindle where the store is absent (move the store folder away first, owner's OK), and on a Kindle where
  it is present. Expected: the store installs from the catalog (T8 must be published first), then opens.

## T10. Hardening (STORE-APP.md 8.11)

- Storage check before a download (`device::free_storage()`, three times the package size), the timeout message, the
  download progress in the sheet (T6), the `armel` listing rule (listings declare `armhf` only).
- Tests for every new function in tools and the store.

## Standing checks (run before every merge)

- `cargo test --offline --workspace` in tools, launcher, store (as far as the crates have tests).
- `cargo clippy --offline -p kl-core -p kl-render -p kl-store -- -D warnings` in tools.
- `git status --porcelain` shows only the intended files; `git diff --cached` has no password (RULES.md).
- No file in any repo mentions the password, a Wi-Fi key, a serial number, or a MAC address.

## Summary for the owner at the end of the run

Write one message: the tasks done (with commit hashes), the tests run, the device gates waiting for the owner (D1, T9),
the decisions made (for example the store's category, the listing text), and the stop items (publish, tag, launcher
merge, icon). Name the reading taken for any ambiguity.
