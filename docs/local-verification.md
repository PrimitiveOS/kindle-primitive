# Kindle platform verification on a Mac

Run these commands from the umbrella checkout with the sibling repositories present. The local run uses desktop devices,
temporary user-storage fixtures, and cross-compiled packages.

```sh
sh scripts/simulate.sh build/simulation
sh scripts/simulate.sh build/simulation --packages
```

Use the Rust toolchain and schema-checking Python environment described in [the handoff](handoff/ENVIRONMENT.md).
The package run also requires Zig, cargo-zigbuild, and the installed Rust target
`armv7-unknown-linux-musleabihf`. Fetch dependencies for the app workspaces with `cargo fetch --locked` if their
locked crates are missing from the local cache.

The output contains the test and build logs, PNG captures at the Oasis 3 dimensions, and per-app installer archives
with SHA-256 sidecars. The archive verifier compares the ZIP file list with its manifest, checks executable modes and
the ARM floating-point ABI, and passes each archive to the Store's Rust unpacker. The launcher bootstrap test
installs the actual locally staged Store package into a temporary Kindle filesystem and verifies the Store entry and
install record. Catalog tests build a static Pages tree and verify the installable app contract separately.

| Track | Local coverage | Device or release gate |
| --- | --- | --- |
| Foundations and contracts | Schema examples, local fixtures, and current device profiles. | Owner review of the contracts. Older hardware, Bluetooth, active hotfix status, keep-awake, and fast panel measurements need devices. |
| Packaging and catalog | Local ARMHF archives, checksums, package validation, CI workflows, catalog collections, and release asset verification. Launcher, Browser, and Terminal also have soft-float build coverage. | Releases, public Store/Launcher/Terminal and native listings, icons, and GitHub merges require approval. Complete Browser and Launcher soft-float archives need ARMEL versions of bundled native helpers. |
| Store and launcher | Refresh, offline cache, browsing and Search, install confirmation and progress, update/remove, bootstrap, refusal and interrupted transaction recovery. | Open the Store on the Kindle. Install, open, update, and remove Browser. Check Wi-Fi, USB idle mode, sleep and wake, display orientation, and memory. Then exercise the Store bootstrap from a launcher build with a published Store asset. |
| SDK and native apps | Shared event loop, touch, rotation, bitmap rendering, keyboard and multiline editing. Hello plus the thirteen F-track app candidates have desktop drivers and package entry scripts. | Review previews and artwork, then install/open/sleep/wake/remove Hello and each app. Confirm Focus can keep the panel awake and measure the cadence and ghosting for the falling-piece game. |
| Wi-Fi file transfer | Host loopback verifies the displayed session code, upload limits and path validation, conflict handling, and incomplete transfer cleanup. | On a Kindle, check LAN access on the chosen Wi-Fi network and confirm transfer ends when the Settings page closes or USB drive mode starts. |
| Hardening | Host verifies architecture/firmware refusal, declared files, checksums, cache and network policy, journal recovery, and catalog asset checks. | The second hardware profile, the launcher update under power loss, and boot fallback need Kindle testing. The platform plan keeps signatures for a later signing decision. |

Prototype app listing JSON files are drafts. The catalog should receive actual release URL, SHA-256, byte count,
approved art and copy, and observed `tested_on` models when an owner-approved release reaches that step. The package
stage and simulation do not need those claims.

The installer accepts the schema-1 file-copy format with catalog SHA-256 checks. Packages that declare root hooks
are refused. Signature trust policy and resumable downloads remain open. The complete ARMEL Terminal candidate can
be checked separately from `doannt-kindle-terminal/dist/`. Launcher and Browser need soft-float builds of their bundled
helpers before offering equivalent ARMEL packages.

## Device-review sequence

1. Review [the Store captures](store-screens/README.md) plus the generated native app previews.
2. Use the standalone Store archive for the Store device gate in [the handoff](handoff/PIPELINE.md#d1-device-gate-the-store-works-on-the-kindle-owner-present-a-stop-point). Check Search, install and removal confirmation, recovery, sleep, rotation, and Wi-Fi errors.
3. After the device gate and the Store release, test the launcher's existing-Store and clean bootstrap paths. Exercise
   a launcher update from a known healthy version and confirm the device returns to the previous launcher after a failed
   trial.
4. Verify a file transfer on the Kindle, and run the native app device checklists. Record panel timing, memory, USB
   and firmware behavior in the corresponding repository before publishing.

## Local feature branches

| Checkout | Branch | Commit |
| --- | --- | --- |
| Shared Tools and Store engine | `feature/store-device` | `9f8c0d5` |
| Primitive Store | `feature/store-device` | `5ea2b7c` |
| Primitive Launcher | `feature/bootstrap` | `07ab754` |
| Primitive Browser | `feature/armel-build` | `66213ee` |
| Primitive Terminal | `feature/terminal-package` | `0e24d9b` |
| Catalog | `feature/catalog-validation` | `336437c` |
| Shared packaging | `feature/package-validation` | `c805f61` |
| Hello template | `feature/app-template` | `cee94c9` |
| Notes, Focus, Words | `feature/notes`, `feature/focus`, `feature/words` | `2cecf1d`, `03aab9d`, `f4f0615` |
| Cards, Calculator, Sudoku | `feature/cards`, `feature/calculator`, `feature/sudoku` | `a8323f2`, `ec5b5c1`, `cc570b5` |
| Chess, Minesweeper, Solitaire | `feature/chess`, `feature/minesweeper`, `feature/solitaire` | `b992abf`, `b7000df`, `fbaac67` |
| Crossword, Blocks, Ships, Cascade | `feature/crossword`, `feature/blocks`, `feature/ships`, `feature/cascade` | `0dad7ba`, `7e94cdf`, `5a80d74`, `1fcc2ae` |

The Launcher and Store share the Tools pin. For GitHub CI, make the pinned Tools commit available to both consumers
before publishing their branches. The new app checkouts use the adjacent Tools checkout for local builds and the
reusable package workflow for releases once its version tag is approved.

## Primitive Store listing proposal

- Name **Primitive Store**, offered by **Primitive AI**
- Subtitle **Find apps for your Kindle**
- Primary category **System**
- Description **Browse apps, see what they change and install them over Wi-Fi. Use Updates to keep your apps current or remove apps you no longer want.**
- Change notice **Uses the internet to check the catalog and download packages. Installs and removes app files in user storage.**

The Store icon and the native app icons in the simulation's `proposals/` directory are artwork for review.
