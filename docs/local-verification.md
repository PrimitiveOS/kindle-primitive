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
Store archive. The [private catalog review](local-catalog-review.md) feeds the actual ARMHF candidates through
the catalog's validation and the Store's cache and installer.

| Track | Local coverage | Device or release gate |
| --- | --- | --- |
| Foundations and contracts | Schema examples, local fixtures, and current device profiles. | Owner review of the contracts. Older hardware, Bluetooth, active hotfix status, keep-awake, and fast panel measurements need devices. |
| Packaging and catalog | Local ARMHF archives, checksums, package validation, CI workflows, catalog collections, and release asset verification. Complete ARMEL archives for Launcher, Browser, and Terminal also pass validation and Store unpacking. | Approve public listings, artwork, releases, and merges. Verify the ARMEL archives on a soft-float Kindle before advertising soft-float compatibility. |
| Store and launcher | Refresh, offline cache, Search, install confirmation and progress, Open, update and removal, resumable downloads, bootstrap, Launcher Store preferences, Store idle/write USB transitions, and interrupted transaction recovery. | Open the Store on the Kindle. Install, open, update, and remove Browser. Check Wi-Fi, USB drive mode and flash writes, sleep and wake, display orientation, and memory. Then exercise the Store bootstrap from a launcher build with a published Store asset. |
| SDK and native apps | Shared `primitive-device`, `primitive-eink`, and `primitive-input` crates. Hello plus the thirteen native apps have desktop drivers and opt in to Launcher idle USB support. Host fixtures cover USB pauses, scoped file access, and Notes edits across eject. | Review previews and artwork. Install, open, sleep, wake, and remove each app. Check native app USB remounts, Focus idle behavior, and Cascade refresh cadence and ghosting. |
| Wi-Fi file transfer | Host loopback verifies the displayed session code, upload limits and path validation, conflict handling, and incomplete transfer cleanup. | On a Kindle, check LAN access on the chosen Wi-Fi network and confirm transfer ends when the Settings page closes or USB drive mode starts. |
| Hardening | Host verifies architecture/firmware refusal, file ownership, archive limits, checksums, cache and network policy, journal recovery, and catalog asset checks. | The second hardware profile, the launcher update under power loss, and boot fallback need Kindle testing. The platform plan keeps signatures for a later signing decision. |

Prototype app listing JSON files are drafts. The catalog should receive actual release URL, SHA-256, byte count,
approved art and copy, and observed `tested_on` models when an owner-approved release reaches that step. The package
stage and simulation do not need those claims.

The installer accepts schema-1 file-copy packages with catalog SHA-256 checks and resumes an interrupted package
transfer against the same catalog size and checksum. It refuses root hooks. The platform plan keeps signing after
the current phase. The ARMEL archives use static Dropbear with zlib for Launcher and static FBInk for Browser.
The installer checks archive contents against the manifest before extraction. It recognizes specific unmodified
legacy Launcher, Browser, Store, and Terminal entries. A path already
holding a customized script or another unrecorded file in `documents/` or `extensions/` stays protected.

The public catalog index was reachable on 2026-11-19. Primitive Browser 0.2.17 ARMHF passed live size, checksum,
and archive-content checks. The larger local catalog has `.invalid` package URLs and no device compatibility claims.
[Public catalog index](https://doannguyentrong.github.io/kindle-primitive-catalog/v1/index.json)

Primitive Words uses independently selected English banks. KWordle's English answer and guess lists trace to
datasets copied from the original game without an upstream redistribution license, as recorded in the Words README.

## Device-review sequence

1. Review [the Store captures](store-screens/README.md) plus the generated native app previews.
2. Use the standalone Store archive for the Store device gate in [the handoff](handoff/PIPELINE.md#d1-device-gate-the-store-works-on-the-kindle-owner-present-a-stop-point). Check Search, install and removal confirmation, recovery, sleep, rotation, and Wi-Fi errors.
3. After the device gate and the Store release, test the launcher's existing-Store and clean bootstrap paths. Test the
   Store's Open and idle USB behavior with the matching Launcher and Store candidates. Exercise a launcher update
   from a known healthy version and confirm the device returns to the previous launcher after a failed trial.
4. Verify a file transfer on the Kindle. In Notes, connect the idle app to a computer, edit a saved note, eject the
   drive and verify both the app and note can be reopened. Run the native app device checklists and record panel timing,
   memory, USB and firmware behavior in the corresponding repository before publishing.

## Local feature branches

| Checkout | Branch | Commit |
| --- | --- | --- |
| Shared Tools and Store engine | `feature/store-device` | `ab62ec5` |
| Primitive Store | `feature/store-device` | `3836ff2` |
| Primitive Launcher | `feature/bootstrap` | `3b88740` |
| Primitive Browser | `feature/armel-build` | `4af7987` |
| Primitive Terminal | `feature/terminal-package` | `5680e46` |
| Catalog | `feature/catalog-validation` | `c8d2309` |
| Shared packaging | `feature/package-validation` | `f9b0cd5` |
| Hello template | `feature/app-template` | `c7e66d2` |
| Notes, Focus, Words | `feature/notes`, `feature/focus`, `feature/words` | `21e4169`, `3318999`, `a355f53` |
| Cards, Calculator, Sudoku | `feature/cards`, `feature/calculator`, `feature/sudoku` | `80b08a4`, `37c26cf`, `1683a52` |
| Chess, Minesweeper, Solitaire | `feature/chess`, `feature/minesweeper`, `feature/solitaire` | `36c2d54`, `2c36a31`, `b458c26` |
| Crossword, Blocks, Ships, Cascade | `feature/crossword`, `feature/blocks`, `feature/ships`, `feature/cascade` | `7b349ce`, `452c92f`, `7f53111`, `bfe1626` |

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
