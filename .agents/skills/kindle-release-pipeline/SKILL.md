---
name: kindle-release-pipeline
description: Use when a change to any PrimitiveOS Kindle repo (app, Terminal, Store, Browser, Launcher, tools, catalog) must go all the way out: commit on a feature branch, merge into main and resolve conflicts, push, test, build, tag a release, watch the Release workflow, list it in the Store catalog and install it on the Kindle. Covers versions, tools pins, the catalog rules and the approvals that stay with the user.
metadata:
  type: reference
---

# Kindle release pipeline

The full cycle for one change: **commit → merge to main → push → test and build → tag and release → Store listing → device**. Follow the steps in order. Stop at any failed check and fix it on `main` (or the feature branch) before going on. The reference doc with the release table is `docs/merge-and-release.md` in the umbrella repo; this skill is the working checklist.

## 0. Ground rules

- **Work in a fresh clone** for every merge, tag and release (`git clone <url> /tmp/<work>/<repo>`). Never merge or tag in a checkout that has the user's uncommitted work. The umbrella repo's working tree (`doannt-kindle/`) belongs to the user: write there only when asked, and then commit only the explicit paths you created.
- **Stage explicit paths only** (`git add <file> ...`), never `git add .` or a whole directory.
- **Never force-push `main`, never move or delete a tag.** A failed release publishes nothing: fix on `main`, bump the patch, tag the new version.
- **Outward-facing steps need the user's go-ahead** unless they already said this release is approved: pushing to `main`, creating tags, merging a catalog listing (it publishes to every Store user), and any device install. Say which step is next and wait when unsure.
- **Never store credentials** in a repo, a commit, a log or a chat. The Kindle's SSH password comes from the user for each session and goes into a temporary expect helper outside the repos, deleted when the session ends.
- Attribution on commits and PR text: end with the attribution line given in the session's system reminder.
- Tooling: `gh` is not installed. Use `git` for pushes and tags, and the public GitHub REST API (`api.github.com`) for run status. Unauthenticated calls are limited (about 60 an hour): if you get HTTP 403, use the direct release download URLs instead.

## 1. Commit on a feature branch

1. Branch from the current `origin/main`: `git checkout -b feature/<topic> origin/main`.
2. Make the change. Run the repo's checks **before** committing (section 3).
3. Commit only the explicit paths, with a message that says what changed and why. Push the branch: `git push -u origin feature/<topic>`. Pushing the branch first keeps the work even if the merge goes wrong.

## 2. Merge to main and resolve conflicts

1. `git fetch origin`; check how far the branch is from `main`: `git rev-list --count origin/main..feature/<topic>` and the reverse.
2. In the fresh clone: `git checkout main && git merge --no-ff feature/<topic> -m "Merge <topic> into main"`. Keep `--no-ff` so the feature history stays visible.
3. Conflicts, and how they were settled before:
   - `Cargo.toml` / `Cargo.lock` versions: keep the **higher** version, then refresh the lock with `cargo build --offline` (or `cargo metadata`) in a checkout that has tools present.
   - A `tools` submodule conflict: set the pointer with `git update-index --cacheinfo 160000,<commit>,tools`, then `git submodule update --init tools`.
   - Two hunks in the same function that both add something (two enum variants, two match arms): keep both. If only one side is complete, keep that side.
   - After any conflict: run every check in section 3 again. Do not push a merge you have not tested.
4. Do not push `main` until the merged result passes the checks. Then `git push origin main`.

## 3. Checks (run on the merged result)

Run them the way CI does: `--locked`, and with `KL_TEST_FONTS` **unset** (CI never sets it). An empty `KL_TEST_FONTS=` is not unset: the drawing tests then try to load fonts from an empty path and fail. Run the flaky-looking tests more than once before you call them flaky: the launcher's file-transfer test failed once in twelve runs on Linux, because the server closed with unread bytes (fixed in 0.6.18).

| Repo | Commands | Extra |
|---|---|---|
| App (kit app) | `cargo test --workspace --locked --offline` | `KL_TEST_FONTS=<launcher>/assets/fonts` for the drawing tests; the sibling `../doannt-kindle-tools` must be present (a symlink to the tools checkout is fine) |
| Tools | `cargo test --workspace --offline`; `cargo clippy --workspace --all-targets --offline -- -D warnings` | the same `KL_TEST_FONTS` |
| Terminal | `cargo test --workspace --locked --offline`; `cargo clippy --workspace --all-targets --locked --offline -- -D warnings` | the tools submodule is at the pinned commit |
| Launcher | `cargo test --locked --workspace --offline`; `cargo clippy --locked --workspace --all-targets --offline -- -D warnings`; `for t in tests/*-test.sh; do sh "$t"; done` | the tools submodule is at the pinned commit |

Clippy runs in CI only for tools, tools-apps, tools-store, the Terminal and the Launcher. App repos run only the tests. A failing check blocks the release: fix it first.

Delete a finished `target/` folder when you are done with it: each one is hundreds of megabytes, and the disk fills quickly.

## 4. Tools first, then the repos that use it

- The apps (and the Store, Launcher, Terminal) build against the **tools** commit they pin:
  - Apps: `sibling-tools-ref` in `.github/workflows/release.yml` (a 40-character commit).
  - Launcher, Terminal, Store: the `tools` submodule pointer. Move it with `git -C tools fetch origin && git -C tools checkout <commit>`, then `git add tools`.
- Order: merge and push **tools** `main` first, then move each dependent repo's pin to that commit, test, release.
- A pin change alone (no code change) still goes through the same checks, and the repo gets a release if its CI needs the new pin.

## 5. Version, changelog, tag and release

1. **Version**: the Cargo version of the app (`[workspace.package]` or `[package]`). Bump the patch for a release (`0.1.2` → `0.1.3`). If the tag for the current version exists, bump; never reuse a version. The device builds of the Launcher and Browser bump the patch themselves (`scripts/build-device.sh`, `--minor` for a new phase): the release version and the device version must match.
2. **Changelog**: add a `## <version>` entry at the top of the version list, with one line per user-visible change. Its file is `CHANGELOG.md` in most repos and `docs/CHANGELOG.md` in the Launcher. Look for it before you edit, and keep its existing heading style.
3. **Commit**: `Release <version>` with the version, changelog, `Cargo.lock` and pin changes. **The lock is part of the bump**: a release that bumps `Cargo.toml` but not `Cargo.lock` fails its CI with `cannot update the lock file` (the launcher's 0.6.17 run did, and was not published). Refresh it with `cargo build --offline --workspace` (no `--locked`), check that only the version lines moved, then commit it.
4. **Tag**: `git tag -a v<version> -m v<version>`; then `git push origin main` and `git push origin v<version>`. The tag must equal the version in the build files and in `manifest.json`.
5. **Watch the Release run** (the `release.yml` workflow runs on the tag). Check the run status from the API: `https://api.github.com/repos/PrimitiveOS/<repo>/actions/workflows/release.yml/runs?per_page=1`. A "Test failure" means the tests failed against the pinned tools: check the pin first.
6. **Assets**: the release has `<id>-<version>-<arch>.zip` and a `.sha256` per architecture. Download the zip directly from `https://github.com/PrimitiveOS/<repo>/releases/download/v<version>/<id>-<version>-<arch>.zip` and check its SHA-256 against the `.sha256` file before you use it anywhere.

Repos and their ids (the repo name is `kindle-primitive-<name>`, except the tools): `2048`, `agenda`, `app-template`, `blocks`, `calculator`, `cards`, `cascade`, `chess`, `crate-shift`, `crossword`, `dictionary`, `files`, `focus`, `habits`, `language-practice`, `math-practice`, `memory-match`, `minesweeper`, `nonogram`, `notes`, `reading-practice`, `ships`, `snake`, `solitaire`, `starship`, `sudoku`, `switchyard`, `tasks`, `viewer`, `words` (apps); `terminal`, `store`, `browser`, `launcher`, `catalog`; tools is `kindle-primtitive-tools` (sic). Some older releases (Reader, Tools, Catalog, umbrella docs) have no release workflow.

## 6. Store listing (the catalog)

Listings live in the catalog repo: `apps/primitive-<name>/app.json`, `icon.png`, `shots/`. Folder names are `primitive-<name>`, not the repo name.

1. Add the new version at the **top** of `versions`: `version`, `date` (today), `notes` (one to five lines, what's new), `firmware` and `requires` copied from the previous entry, `tested_on`, and `assets.armhf` (and `armel` only once armel is tested on a device): `url`, `sha256`, `size` from the verified zip.
2. `tested_on` lists only the Kindle models the version was actually run on. An untested version gets `[]`. Do not claim a test that did not happen.
3. Active listings use **armhf only** until armel has been tested on a device.
4. Check: `sh scripts/check-app.sh apps/primitive-<name>` and `sh scripts/test.sh` must pass. The write helper must keep the file's formatting (two-space JSON, trailing newline).
5. Branch, commit, push, merge into the catalog `main`, run `sh scripts/test.sh` on the merged result, then push `main`. Pushing `main` publishes: get the user's go-ahead first.
6. After publishing, check the public index (`https://primitiveos.github.io/kindle-primitive-catalog/v1/apps/<id>.json`) shows the new version.
7. System apps (the Launcher, anything that changes how the Kindle starts) are reviewed on a Kindle before they publish (`docs/store-submit-app.md` §4.5 and §5).

## 7. Install on the Kindle (optional, needs the user)

The device steps (SSH on port 2222, the storage checks, checksums, backups, the library entry, `# Wake: redraw`) are in the `kindle-device` skill. The short version:

1. Ask the user for the Kindle's SSH password for this session. Never reuse one from an earlier session without asking.
2. Back up what is on the device first (`cp -p <binary> <binary>.<old-version>.bak`), then upload to `<name>.new`, `sync`, and `mv` into place.
3. Verify the device checksum equals the local one: `sha256sum` on the device against `shasum -a 256` locally.
4. Start the app through its library entry, and read its log (`log-app.txt`, `log-terminal.txt`, `log-launcher.txt`).
5. Delete the expect helper that held the password when the session is done.

The Launcher's device build deploys through `scripts/build-device.sh`, which runs the installer with the password. Run it only with the user's go-ahead for that session.

## 8. Report back

State, per repo: the tag, the Release run result, the catalog publish result and the device result. Say which steps were not done and why (a missing password, a rate limit, a step waiting for approval). Do not call a release done until its Release run has finished green.
