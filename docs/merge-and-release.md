# Merging and releasing the Kindle repos

Written for: the maintainers who merge feature branches into `main` and publish releases.

This is what we did on 2026-11-21 and what to do next time. The order matters: tools first, then the apps and the
launcher that pin it.

## 1. The repos

- Every repo's default branch is `main`. Work happens on feature branches. Never push to `main` without a merge
  that has been tested.
- `kindle-primtitive-tools` is the shared code: the app kit (`primitive-app`, `primitive-ui`, `primitive-device`),
  the launcher's screens (`kl-core`, `kl-render`, `kl-kindle`) and the Store's pieces. The launcher and the Store pin a
  tools commit as a submodule. Native apps read it from a sibling folder, `../doannt-kindle-tools`, and their
  `release.yml` names the revision with `sibling-tools-ref`.
- Each app's `release.yml` calls the reusable workflow `package.yml` in `kindle-primitive-build`, pinned by commit.
  That workflow runs on a `v*` tag: it tests the app, builds it, packages it with `LICENSE`, `INSTALL.md` and
  `CHANGELOG.md`, and publishes the GitHub release.

## 2. Before you merge

1. Make sure the feature branch builds and its tests pass:
   - tools: `cargo test --workspace`
   - apps: `cargo test --workspace`, and the device build for the Kindle
   - launcher: `cargo test -p kl-launcher` and `sh tests/supervisor-test.sh`
2. Check how far each side is from the other:
   `git rev-list --count origin/main..origin/<feature>` and `git rev-list --count origin/<feature>..origin/main`.
3. Merge in a fresh clone, not in a checkout that has someone else's uncommitted work. That keeps their work out of
   the merge.
4. If the repo depends on tools (apps, launcher, Store), merge tools `main` first. Then point the repo at the new tools
   commit.

## 3. Merge into main

```sh
git clone <repo-url> merge-<name> && cd merge-<name>
git checkout main
git merge --no-ff origin/<feature> -m "Merge <feature> into main"
# resolve any conflicts, then run the tests again
git push origin main
```

Rules:

- Use `--no-ff`, so the feature history stays visible.
- Never force-push `main`. Never rewrite its history.
- Conflicts we met, and how they were settled:
  - `Cargo.toml` and `Cargo.lock` versions: keep the higher version, then refresh the lock with `cargo metadata`
    inside a checkout that has tools present.
  - A submodule (`tools`) conflict: set the pointer with
    `git update-index --cacheinfo 160000,<commit>,tools`, then `git submodule update --init tools`.
  - Duplicate hunks in the same function: keep both sides when both add something (for example two enum variants),
    otherwise keep the side that is complete. Test after every merge.

## 4. Versions

- The version is the Cargo version of the app (`[workspace.package]` or `[package]`). The tag is `v` plus that version.
- If the tag for the current version already exists, bump the patch (`0.1.3` to `0.1.4`). Never move or delete an
  existing tag. A tag that points at old code is history.
- The launcher and browser device builds bump the patch by themselves (`scripts/build-device.sh`). Keep the release
  version and the device version the same.

## 5. Release

1. Update `sibling-tools-ref` in the app's `.github/workflows/release.yml` to the tools `main` commit you shipped.
2. Commit `Release <version>` on `main`.
3. `git tag -a v<version> -m v<version>`, then `git push origin main` and `git push origin v<version>`.
4. Open the repo's Actions tab and watch the **Release** run. A "Test failure" means the tests failed against the
   pinned tools; check the pin first.
5. A failed release publishes nothing. Fix it on `main`, bump the patch and tag the new version.

### Architectures

`release.yml` builds and packages each architecture named in its `arches` input (default `armhf`, the Oasis 3). An app
stays `armhf` only until its `armel` build has been checked on a device. Then add `armel` to `arches`; the listing gets an
`armel` asset. The zip's manifest `arch` must equal its listing asset key; `check-assets.py` checks it.

## 6. Which repos publish a release

State after the merge-and-release run on 2026-11-21. "Release" is the GitHub release made by the Release workflow.

| Repo | Version released | Release run |
|---|---|---|
| Launcher | `v0.6.18` | succeeded (installed on the owner's Kindle Oasis 3; the 0.6.17 run failed on a stale `Cargo.lock`, not published) |
| Primitive Browser | `v0.2.21` | succeeded (from `feature/system-layer`; same content as `main`) |
| Store | `v0.1.8` | succeeded (from `feature/system-layer`; same content as `main`) |
| Terminal | `v0.2.0` | succeeded (app kit; tested on a Kindle Oasis 3) |
| 2048 | `v0.1.4` | succeeded |
| Agenda | `v0.1.2` | succeeded |
| Blocks | `v0.1.1` | succeeded |
| Calculator | `v0.1.5` | succeeded |
| Cards | `v0.1.3` | succeeded |
| Cascade | `v0.1.1` | succeeded |
| Chess | `v0.1.1` | succeeded |
| Crate Shift | `v0.1.3` | succeeded |
| Crossword | `v0.1.1` | succeeded |
| Dictionary | `v0.1.3` | succeeded |
| Files | `v0.1.5` | succeeded (see below) |
| Focus | `v0.1.2` | succeeded |
| Habits | `v0.1.2` | succeeded |
| Language Practice | `v0.1.1` | succeeded |
| Reading Practice | `v0.1.1` | succeeded (added after the first pass; see below) |
| Math Practice | `v0.1.1` | succeeded |
| Memory Match | `v0.1.2` | succeeded |
| Minesweeper | `v0.1.1` | succeeded |
| Nonogram | `v0.1.2` | succeeded |
| Notes | `v0.1.3` | succeeded |
| Ships | `v0.1.1` | succeeded |
| Snake | `v0.1.2` | succeeded |
| Solitaire | `v0.1.2` | succeeded |
| Starship | `v0.1.2` | succeeded |
| Sudoku | `v0.1.1` | succeeded |
| Switchyard | `v0.1.1` | succeeded |
| Tasks | `v0.1.2` | succeeded |
| Viewer | `v0.1.2` | succeeded |
| Words | `v0.1.1` | succeeded |
| Reader | `v0.1.4` | succeeded (0.1.3 failed on the workflow's package name; published nothing) |
| Tools | not released (no release workflow) | merged to `main` |
| Catalog | not released (no release workflow, no `CHANGELOG.md`) | merged to `main` |
| Umbrella docs | not released | merged to `main` |

Failed releases publish nothing. Fix them on `main`, then bump the patch and tag the new version. Never move a tag.

**Tap-feedback pass (2026-11-21).** Ten apps (agenda, habits, tasks, notes, cards, files, calculator, dictionary, snake, solitaire) and the Terminal were released with taps that reverse black and white, as the kit's controls do. The tools commit c1e758b (the kl-render test casts) lets `clippy --workspace --all-targets -D warnings` pass. The Terminal and the launcher pin it; the apps don't run clippy in CI. The launcher's pin moved on `main` without a release.

**Files `v0.1.3` failure, and its fix (`v0.1.4`).** The test
`reader::tests::stages_the_installed_viewer_and_passes_one_literal_document_argument` starts a script that it has just
written. On Linux that can fail with `Text file busy` (error 26) while another test forks. The test now retries the
start for a moment. The application code did not change.

## 7. Checks after a release

- Each repo's Actions run shows "Release" with a green check.
- The GitHub release has the zip and its `.sha256` for each architecture.
- The Kindle device build matches the release version (the device build bumps the same number).
- If a Kindle is on an older build than its release, say so in the release notes.

## 8. Store listings

Each release is added to its Store listing (`apps/<id>/app.json` in the catalog) through a pull request. The listing
takes the zip's URL, sha256 and size from the release, and `tested_on` lists the Kindle the app was run on. The
catalog's own checks (`sh scripts/test.sh` and `sh scripts/check-app.sh apps/<id>`) must pass. Merging the pull request
publishes to every Store user, so it waits for a maintainer's approval.

**Gap found after the first pass.** Reading Practice was merged but missing from the release list, so it stayed at
`v0.1.0`. It was released as `v0.1.1` afterwards and added to the Store catalog. Check every repo on `main` against its
latest tag before calling a release pass finished.
