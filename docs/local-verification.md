# Kindle platform verification on a Mac

Run these commands from the umbrella checkout with the sibling repositories present. The local run uses desktop devices,
temporary user-storage fixtures, and cross-compiled packages.

```sh
sh scripts/simulate.sh build/simulation
sh scripts/simulate.sh build/simulation --packages
sh scripts/simulate.sh build/simulation-armel --armel-packages
```

Use the Rust toolchain and schema-checking Python environment described in [the handoff](handoff/ENVIRONMENT.md).
The package run also requires Zig, cargo-zigbuild, and the installed Rust target
`armv7-unknown-linux-musleabihf`. Fetch dependencies for the app workspaces with `cargo fetch --locked` if their
locked crates are missing from the local cache. For the ARMEL run, install `armv7-unknown-linux-musleabi` and build
the pinned helper sources with `sh doannt-kindle-launcher/scripts/build-armel-ssh.sh` and
`sh doannt-kindle-browser/scripts/build-armel-fbink.sh`. The helpers are staged only in their platform's packages.

The output contains the test and build logs, PNG captures at the Oasis 3 dimensions, and per-app installer archives
with SHA-256 sidecars. The archive verifier compares the ZIP file list with its manifest, checks executable modes and
the ARM floating-point ABI, and passes each archive to the Store's Rust unpacker. Each package run also installs
the staged set into a temporary Kindle filesystem, makes the Launcher pass through its update trial, and removes
the removable apps while preserving a personal document. The ARMHF run tests Launcher bootstrap with the actual
Store archive. Catalog tests build a static Pages tree and verify the installable app contract separately.

| Track | Local coverage | Device or release gate |
| --- | --- | --- |
| Foundations and contracts | Schema examples, local fixtures, and current device profiles. | Owner review of the contracts. Older hardware, Bluetooth, active hotfix status, keep-awake, and fast panel measurements need devices. |
| Packaging and catalog | Local ARMHF archives, checksums, package validation, CI workflows, catalog collections, and release asset verification. Complete ARMEL archives for Launcher, Browser, and Terminal also pass validation and Store unpacking. | Approve public listings, artwork, releases, and merges. Verify the ARMEL archives on a soft-float Kindle before advertising soft-float compatibility. |
| Store and launcher | Refresh, offline cache, Search, install confirmation and progress, Open, update and removal, resumable downloads, bootstrap, Launcher Store preferences, Store idle/write USB transitions, and interrupted transaction recovery. | Open the Store on the Kindle. Install, open, update, and remove Browser. Check Wi-Fi, USB drive mode and flash writes, sleep and wake, display orientation, and memory. Then exercise the Store bootstrap from a launcher build with a published Store asset. |
| SDK and native apps | Shared event loop, lifecycle and settings, touch, rotation, bitmap rendering, keyboard, and single- and multiline editing. Hello plus the thirteen F-track app candidates have desktop drivers and package entry scripts. Focus has a running-timer idle refresh path. | Review previews and artwork, then install/open/sleep/wake/remove Hello and each app. Confirm Focus can keep the panel awake and measure the cadence and ghosting for the falling-piece game. |
| Wi-Fi file transfer | Host loopback verifies the displayed session code, upload limits and path validation, conflict handling, and incomplete transfer cleanup. | On a Kindle, check LAN access on the chosen Wi-Fi network and confirm transfer ends when the Settings page closes or USB drive mode starts. |
| Hardening | Host verifies architecture/firmware refusal, file ownership, archive limits, checksums, cache and network policy, journal recovery, and catalog asset checks. | The second hardware profile, the launcher update under power loss, and boot fallback need Kindle testing. The platform plan keeps signatures for a later signing decision. |

Prototype app listing JSON files are drafts. The catalog should receive actual release URL, SHA-256, byte count,
approved art and copy, and observed `tested_on` models when an owner-approved release reaches that step. The package
stage and simulation do not need those claims.

The installer accepts schema-1 file-copy packages with catalog SHA-256 checks and resumes an interrupted package
transfer against the same catalog size and checksum. It refuses root hooks. The platform plan keeps signing after
the current phase. The ARMEL archives use static Dropbear with zlib for Launcher and static FBInk for Browser.
The installer recognizes specific unmodified legacy Launcher, Browser, Store, and Terminal entries. A path already
holding a customized script or another unrecorded file in `documents/` or `extensions/` stays protected.

Primitive Words uses independently selected English banks. KWordle's English answer and guess lists trace to
datasets copied from the original game without an upstream redistribution license, as recorded in the Words README.

## Device-review sequence

1. Review [the Store captures](store-screens/README.md) plus the generated native app previews.
2. Use the standalone Store archive for the Store device gate in [the handoff](handoff/PIPELINE.md#d1-device-gate-the-store-works-on-the-kindle-owner-present-a-stop-point). Check Search, install and removal confirmation, recovery, sleep, rotation, and Wi-Fi errors.
3. After the device gate and the Store release, test the launcher's existing-Store and clean bootstrap paths. Test the
   Store's Open and idle USB behavior with the matching Launcher and Store candidates. Exercise a launcher update
   from a known healthy version and confirm the device returns to the previous launcher after a failed trial.
4. Verify a file transfer on the Kindle, and run the native app device checklists. Record panel timing, memory, USB
   and firmware behavior in the corresponding repository before publishing.

## Local feature branches

| Checkout | Branch | Commit |
| --- | --- | --- |
| Shared Tools and Store engine | `feature/store-device` | `ead19b0` |
| Primitive Store | `feature/store-device` | `f511431` |
| Primitive Launcher | `feature/bootstrap` | `b409c29` |
| Primitive Browser | `feature/armel-build` | `3179d67` |
| Primitive Terminal | `feature/terminal-package` | `0e24d9b` |
| Catalog | `feature/catalog-validation` | `336437c` |
| Shared packaging | `feature/package-validation` | `c805f61` |
| Hello template | `feature/app-template` | `1f00f59` |
| Notes, Focus, Words | `feature/notes`, `feature/focus`, `feature/words` | `2cecf1d`, `447e20b`, `3796421` |
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
