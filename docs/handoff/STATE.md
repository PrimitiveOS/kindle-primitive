# Current release state

Updated 20 November 2026. Each `doannt-kindle-*` checkout is an independent Git repository in the umbrella workspace.
The [app directory](../../README.md#the-apps) links all first-party repositories and their published versions.

## Platform and catalog

| Component | Published state | Source |
|---|---|---|
| PrimitiveOS umbrella | App directory and education and productivity design. | [Umbrella release update `9c6fa84`](https://github.com/DoanNguyenTrong/kindle-primitive/commit/9c6fa84) |
| Primitive Launcher | 0.5.3. Includes vertical Settings, expanded device and app controls, clock sync, and wallpapers. | [Launcher release](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/releases/tag/v0.5.3) |
| Store | 0.1.6. Scrolls vertically, preloads nearby artwork, and shows the cached download total on app pages. | [Store release](https://github.com/DoanNguyenTrong/kindle-primitive-store/releases/tag/v0.1.6) |
| Primitive Browser | 0.2.18. | [Browser release](https://github.com/DoanNguyenTrong/kindle-primitive-browser/releases/tag/v0.2.18) |
| Primitive Terminal | 0.1.8. Listed under Developer Tools. | [Terminal release](https://github.com/DoanNguyenTrong/kindle-primitive-terminal/releases/tag/v0.1.8) |
| Files | 0.1.0. Browse and organise Kindle files and hand supported documents to KOReader. | [Files release](https://github.com/DoanNguyenTrong/kindle-primitive-files/releases/tag/v0.1.0) |
| Store catalog | 34 listings, including 33 hosted first-party apps and one KOReader link. The catalog includes a daily snapshot of package download totals. | [Public catalog](https://doannguyentrong.github.io/kindle-primitive-catalog/v1/index.json) · [Collections](https://doannguyentrong.github.io/kindle-primitive-catalog/v1/collections.json) |
| Tools and Build | Shared app kit, packager, and reusable release workflow. The eleven release builds use the Tools pin at `3d9026c`. | [Tools commit](https://github.com/DoanNguyenTrong/kindle-primtitive-tools/commit/3d9026c) · [Build repo](https://github.com/DoanNguyenTrong/kindle-primitive-build) |

## Study and work releases

| App | Version | Published changes |
|---|---|---|
| [Tasks](https://github.com/DoanNguyenTrong/kindle-primitive-tasks) | 0.1.0 | Today, upcoming items, named lists, repeating tasks, and completion with undo. |
| [Reading Practice](https://github.com/DoanNguyenTrong/kindle-primitive-reading-practice) | 0.1.0 | Twelve original passages at two levels, saved progress, and a retry for missed questions. |
| [Math Practice](https://github.com/DoanNguyenTrong/kindle-primitive-math-practice) | 0.1.0 | Worked examples and five-problem sessions for arithmetic, fractions, and percentages. |
| [Language Practice](https://github.com/DoanNguyenTrong/kindle-primitive-language-practice) | 0.1.0 | Ten beginner English lessons for Vietnamese speakers and review of missed exercises. |
| [Dictionary](https://github.com/DoanNguyenTrong/kindle-primitive-dictionary) | 0.1.1 | Offline lookup with an original starter glossary, favorites, previewed TSV import, and export for Cards. |
| [Habits](https://github.com/DoanNguyenTrong/kindle-primitive-habits) | 0.1.0 | Daily and weekly check-ins, editable history, and CSV export. |
| [Agenda](https://github.com/DoanNguyenTrong/kindle-primitive-agenda) | 0.1.0 | Upcoming appointments and one-way `.ics` import for one-off all-day events and events with local or UTC time. |
| [Cards](https://github.com/DoanNguyenTrong/kindle-primitive-cards) | 0.1.1 | Self-test with retry and previewed two-column TSV import. Existing scheduled reviews keep their progress. |
| [Notes](https://github.com/DoanNguyenTrong/kindle-primitive-notes) | 0.1.1 | Plain-text checklists and a reading journal template. |
| [Focus](https://github.com/DoanNguyenTrong/kindle-primitive-focus) | 0.1.1 | Optional subject labels and a weekly study log. |
| [Calculator](https://github.com/DoanNguyenTrong/kindle-primitive-calculator) | 0.1.3 | Unit conversions, worked fraction and linear-equation steps, and line and quadratic plots. |

All eleven published ARMHF ZIPs passed SHA-256, manifest, and licence-file checks against the app sources. The seven
new packages carry their approved Launcher icons, which match the public Store artwork. Desktop app checks and the
Store integration run passed. The integration run refreshed the fixture catalog, installed and removed each public
package, and preserved a seeded personal document. GitHub Pages served the updated catalog, collection, icons, and
screenshots. [Catalog publication run](https://github.com/DoanNguyenTrong/kindle-primitive-catalog/actions/runs/44580696716)

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
- Files 0.1.0 installed and opened through the Launcher supervisor on 20 November. Desktop tests covered file
  operations. The owner opened a sample PDF from Files and confirmed that KOReader displayed the test page.
- The physical-device checks for the eleven Study and work releases remain open. Check Store install or update,
  app launch and exit, touch targets, both portrait orientations, sleep and wake, USB eject, and data persistence.
  Record passing hardware results per release before adding a model to `tested_on`.
- Keep the installed Launcher in place. Use the existing Store tile to open standalone Store. Reserve the manual
  copy of `launcher/` and `documents/Launcher.sh` for first-time setup.
- The [environment guide](ENVIRONMENT.md) has device access and log locations. The last known Store cache and
  installed-app records are under `/mnt/us/launcher/store/`.
