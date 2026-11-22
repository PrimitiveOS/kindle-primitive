# Current release state

Updated 22 November 2026. Each `doannt-kindle-*` checkout is an independent Git repository in the umbrella workspace.
The [app directory](../../README.md#the-apps) links all first-party repositories and their published versions.

## Platform and catalog

| Component | Published state | Source |
|---|---|---|
| PrimitiveOS umbrella | App directory and implementation plan under the PrimitiveOS GitHub organization. | [Umbrella repository](https://github.com/PrimitiveOS/kindle-primitive) |
| Primitive Launcher | 0.5.9. Adds offline uninstall under Apps and Storage. The licensed ARMHF, ARMEL, and first-install ZIPs passed package checks. | [Launcher release](https://github.com/PrimitiveOS/kindle-primitive-launcher/releases/tag/v0.5.9) |
| Store | 0.1.7. Refreshes from the organization catalog. Scrolls vertically, preloads nearby artwork, and shows the cached download total on app pages. | [Store release](https://github.com/PrimitiveOS/kindle-primitive-store/releases/tag/v0.1.7) |
| Primitive Browser | 0.2.18. | [Browser release](https://github.com/PrimitiveOS/kindle-primitive-browser/releases/tag/v0.2.18) |
| Primitive Terminal | 0.1.8. Listed under Developer Tools. | [Terminal release](https://github.com/PrimitiveOS/kindle-primitive-terminal/releases/tag/v0.1.8) |
| Files | 0.1.2. Browse and organise Kindle files and open supported documents in Reader, Viewer, or KOReader. | [Files release](https://github.com/PrimitiveOS/kindle-primitive-files/releases/tag/v0.1.2) |
| Reader | 0.1.22 in GitHub and Store, installed in place on Oasis 3. All 26 package files matched and existing state checksums were preserved. The current original-file sweep has 37 end-prompt comparisons awaiting a corrected replay. | [Reader release](https://github.com/PrimitiveOS/kindle-primitive-reader/releases/tag/v0.1.22) · [Earlier complete original-file acceptance](https://github.com/PrimitiveOS/kindle-primitive-reader/blob/v0.1.18/docs/real-document-verification.md) |
| Viewer | 0.1.1. Opens PDFs, JPEGs and PNGs offline. Kindle page buttons scroll PDFs and navigate the file picker. | [Viewer release](https://github.com/PrimitiveOS/kindle-primitive-viewer/releases/tag/v0.1.1) |
| Store catalog | 36 listings, including 35 hosted first-party apps and one KOReader link. The catalog includes a daily snapshot of package download totals. | [Public catalog](https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json) · [Collections](https://primitiveos.github.io/kindle-primitive-catalog/v1/collections.json) |
| Tools and Build | Shared app kit, packager, and reusable release workflow. Apps pin Tools by commit. The Launcher and Store releases allow the organization catalog host. | [Tools repo](https://github.com/PrimitiveOS/kindle-primtitive-tools) · [Build repo](https://github.com/PrimitiveOS/kindle-primitive-build) |

The migration moved 38 existing project repositories to the PrimitiveOS organization. The transfer preserved 70 existing GitHub releases
and all 176 release assets, including the package ZIPs and their checksum files. [Organization profile](https://github.com/PrimitiveOS)

Reader development is currently desktop-only because the owner is taking the Kindle offline. Preserve that instruction until the owner reconnects it. The newer candidate is on `feature/reader-workflow-simulation`; its aggregate hardware acceptance and release remain pending. The previous prepared 0.1.23 delivery scripts must not publish or install without checking the final accepted source and current device gates.

The combined `31612701` candidate adds global document defaults, full local reading-data backup and independent content DPI controls. It passes 724 library, 14 package and four system tests, plus actual-process catalog acquisition, two-profile sync, highlight, Japanese/Latin lookup and original-file cross-feature checks. Original document hashes remain unchanged. [Aggregate CI](https://github.com/PrimitiveOS/kindle-primitive-reader/actions/runs/45000388767) passes at that exact source. Style tweaks and CSS display/visibility projection remain separate work; full reading parity is not complete.

The earlier `b8ab53a6` source has a fresh 48-edition Mac replay: 1,509 sections, 28,075 painted frames, 28,065 exact page anchors and 33,405 resolved fragments. It maps all 26,592,055 tested non-whitespace characters without modifying originals. The supplied font stack leaves 134 undeclared private-use symbols unresolved. Do not relabel that full replay as the newer combined source; the DPI slice separately checks default-scale arithmetic across all 48 editions and exact first-frame pixels in three originals.

The exact `31612701` production and five native test targets compile as static ARM32 hard-float binaries. Its private 20,614,502-byte draft package has SHA-256 `7df50ff74f640f09cfa6890727cf2116210dd0be3f30b0cb4fc28f3d77d96108`; all 26 files, both project licences and 325 dependency notices validate. These are Mac compiler/package checks. No candidate native binary has executed on the disconnected Kindle, and no new public release or Store package has replaced 0.1.22. A pinned, isolated KOReader Mac reference is being prepared for new SDL UI comparisons, distinct from the historical Oasis captures.

Storage cleanup archived 7,932 device QA receipts on the Mac and removed obsolete temporary builds and transfer chunks. The last measurement before disconnect showed 33% used and 4,270,976 KiB available on `/mnt/us`. Installed applications, original documents and saved data were retained. Future checksum-verified uploads remove their transfer chunks after assembly.

## Study and work releases

| App | Version | Published changes |
|---|---|---|
| [Tasks](https://github.com/PrimitiveOS/kindle-primitive-tasks) | 0.1.0 | Today, upcoming items, named lists, repeating tasks, and completion with undo. |
| [Reading Practice](https://github.com/PrimitiveOS/kindle-primitive-reading-practice) | 0.1.0 | Twelve original passages at two levels, saved progress, and a retry for missed questions. |
| [Math Practice](https://github.com/PrimitiveOS/kindle-primitive-math-practice) | 0.1.0 | Worked examples and five-problem sessions for arithmetic, fractions, and percentages. |
| [Language Practice](https://github.com/PrimitiveOS/kindle-primitive-language-practice) | 0.1.0 | Ten beginner English lessons for Vietnamese speakers and review of missed exercises. |
| [Dictionary](https://github.com/PrimitiveOS/kindle-primitive-dictionary) | 0.1.1 | Offline lookup with an original starter glossary, favorites, previewed TSV import, and export for Cards. |
| [Habits](https://github.com/PrimitiveOS/kindle-primitive-habits) | 0.1.0 | Daily and weekly check-ins, editable history, and CSV export. |
| [Agenda](https://github.com/PrimitiveOS/kindle-primitive-agenda) | 0.1.0 | Upcoming appointments and one-way `.ics` import for one-off all-day events and events with local or UTC time. |
| [Cards](https://github.com/PrimitiveOS/kindle-primitive-cards) | 0.1.1 | Self-test with retry and previewed two-column TSV import. Existing scheduled reviews keep their progress. |
| [Notes](https://github.com/PrimitiveOS/kindle-primitive-notes) | 0.1.1 | Plain-text checklists and a reading journal template. |
| [Focus](https://github.com/PrimitiveOS/kindle-primitive-focus) | 0.1.1 | Optional subject labels and a weekly study log. |
| [Calculator](https://github.com/PrimitiveOS/kindle-primitive-calculator) | 0.1.3 | Unit conversions, worked fraction and linear-equation steps, and line and quadratic plots. |

All eleven published ARMHF ZIPs passed SHA-256, manifest, and licence-file checks against the app sources. The seven
new packages carry their approved Launcher icons, which match the public Store artwork. Desktop app checks and the
Store integration run passed. The integration run refreshed the fixture catalog, installed and removed each public
package, and preserved a seeded personal document. GitHub Pages served the updated catalog, collection, icons, and
screenshots. [Catalog publication run](https://github.com/PrimitiveOS/kindle-primitive-catalog/actions/runs/44580696716)

Each package carries `LICENSE` and `LICENSE-DOCS`. Project-owned code uses PolyForm Noncommercial 1.0.0.
Project-owned documentation, artwork, and bundled content use CC BY-NC-SA 4.0 where declared. The policy and the
terms for Terminal, Tools, and earlier releases are recorded in the [licensing audit](../licence-audit.md).

## Kindle Oasis 3

- The known hardware baseline is firmware 5.18.2 and ARMHF. The Store records this model as `KindleOasis3`.
  The 19 November device run installed and smoke-tested the 18 hosted packages then available. Store 0.1.2
  bootstrapped from Launcher, refreshed the catalog, installed apps, and opened Hello. The checks for Notes,
  Cards, Focus, and Calculator covered their 0.1.0 builds. Local evidence is in `build/device-validation/`.
- Subsequent device checks verified Launcher 0.4.10 in the installed, running, and boot copies after its
  supervisor trial. They also verified Store 0.1.4 startup, cached catalog reuse, and **Done** cancelling a
  refresh and returning to Launcher. Local evidence is in `build/launcher-uninstall-warning/device-verification.log`
  and `build/store-performance/`.
- On 20 November 2026, the keep-awake override was cleared. A readback of `com.lab126.powerd` returned
  `preventScreenSaver=0`.
- Launcher 0.5.3 and Store 0.1.6 updated in place on 20 November. The Launcher trial passed and the boot
  copy refreshed. Existing library scripts and Launcher preferences matched their pre-update hashes.
- On 20 November, Launcher 0.5.4 and Store 0.1.7 updated in place for the organization catalog migration.
  The Launcher trial passed, and the installed, running, and boot binaries matched the published ARMHF
  package. Store's installed binary matched its release. Both library scripts, Launcher settings, and
  the normal sleep configuration matched their pre-update state.
- On the same device, Store 0.1.7 fetched the new public index and showed all 34 listings. It refreshed 33
  listings and reused one with zero listing or artwork failures. The saved index matched the live index
  byte for byte. [Catalog publication run](https://github.com/PrimitiveOS/kindle-primitive-catalog/actions/runs/44656500321)
- Launcher 0.5.5 passed its in-place startup trial on 20 November. The running binary and boot copy matched the
  verified ARMHF package. Library entry contents, wallpaper settings, and the PNG galleries matched their
  pre-update hashes. The desktop simulator exercised preview, opacity changes, Back, and Apply. Captures show
  full-screen Home in both themes. Device readback confirmed Sleep opacity saved at 80% while Home and Startup
  were each saved at 100%. The owner confirmed Home wallpaper preview, opacity, and coverage behind the
  status and bottom bars on the Oasis 3.
- Launcher 0.5.9 passed its supervised update from 0.5.8 on 20 November. The user-storage, running, and boot copies
  matched the GitHub ARMHF release. The existing library entry, boot job, preferences, and wallpaper galleries
  matched their pre-update checksums. On Oasis 3 firmware 5.18.2, automated Settings taps verified that Cancel kept the
  test package installed and Uninstall removed its payload and receipt while preserving its untracked data.
- Files 0.1.0 installed and opened through the Launcher supervisor on 20 November. Desktop tests covered file
  operations. The owner opened a sample PDF from Files and confirmed that KOReader displayed the test page.
- On 20 November, Files 0.1.1 opened a PDF through Viewer 0.1.0 on firmware 5.18.2. The owner confirmed
  that swipes and the physical forward button scrolled the document. Viewer saved the scroll position and
  returned to Launcher. The handoff kept the foreground process ID and advanced the USB lease sequence.
  The sampled peak with the test PDF was about 29 MiB. From Viewer’s home-screen tile, the owner opened
  a sample image and confirmed zoom in and out. After updating to Viewer 0.1.1, the owner confirmed that
  both physical page buttons move through the file picker. USB eject and larger documents remain to be tested.
- On 20 November, Reader 0.1.0 and Files 0.1.2 passed installed package checksum checks on firmware 5.18.2.
  Automation verified Files opening Markdown and DOCX in Reader, forward and back input, reading position restore,
  and return to Launcher via Done or Exit Reader. All 249 native Reader tests, 15 EPUB profiles, and an English OCR
  smoke test passed. Store refreshed the live catalog and cached both checked releases.
  [Catalog deployment](https://github.com/PrimitiveOS/kindle-primitive-catalog/actions/runs/44744121098)
- Reader 0.1.1 passed 258 desktop tests and is live on GitHub and in Store. Desktop checks covered nested folder
  browsing, reading bars that leave the document layout in place, and the EPUB and PDF selection popup. On the Oasis 3,
  the in-place update verified all 23 installed files and preserved Reader state checksums. An on-device offscreen
  smoke rendered the picker and EPUB and PDF controls and selection actions. It checked that opening controls left
  the middle of the page intact and that Done issued an exit. Interactive device checks remain open.
  [Reader 0.1.1 release](https://github.com/PrimitiveOS/kindle-primitive-reader/releases/tag/v0.1.1)
- Reader 0.1.2 passed 280 desktop tests. Oasis 3 installation preserved Reader state and verified all 23 files.
  Its offscreen EPUB and PDF previews matched six macOS menu images byte for byte. Live gestures and page-button
  checks remain open. [Reader 0.1.2 release](https://github.com/PrimitiveOS/kindle-primitive-reader/releases/tag/v0.1.2)
- The physical-device checks for the eleven Study and work releases remain open. Check Store install or update,
  app launch and exit, touch targets, both portrait orientations, sleep and wake, USB eject, and data persistence.
  Record passing hardware results per release before adding a model to `tested_on`.
- Keep the installed Launcher in place. Use the existing Store tile to open standalone Store. Reserve the manual
  copy of `launcher/` and `documents/Launcher.sh` for first-time setup.
- The [environment guide](ENVIRONMENT.md) has device access and log locations. The last known Store cache and
  installed-app records are under `/mnt/us/launcher/store/`.
