# PrimitiveOS licensing audit

Reviewed 19 November 2026. This audit covers the umbrella repository and all 29 component repositories in the workspace. It records the terms found in source and release packages and the project policy confirmed after the review. The inventory reflects the state at the time of the audit.

## Findings

- **First-party apps.** Twenty-four current Store packages identify their own code as PolyForm Noncommercial 1.0.0. They ship that licence. It permits noncommercial use, modification, and redistribution subject to its terms. It also explicitly permits use by certain institutions and organizations, including educational institutions and government agencies, regardless of their funding. Public source remains readable, and the terms govern the permissions granted to recipients. [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)
- **Images.** The first-party app READMEs and umbrella describe pictures, screenshots, or artwork as CC BY-NC-SA 4.0, as do the Catalog README and the dedicated licence under `Tools/assets/icons/apps/`. That published wording grants conditional reuse and applies the noncommercial requirement to those images to the extent the licensor holds the relevant rights. The existing grants continue on their published terms. The policy confirmed below keeps those noncommercial terms in place. [CC BY-NC-SA 4.0 legal code](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en)
- **Image provenance.** The set includes app-rendered screenshots, icon renderers in the Crate Shift and Memory Match source, stock Amazon and KOReader marks, and Browser screenshots of external web pages. Some delivered images are mirrored between repositories or encoded in `documents/*.sh` or compiled assets. A rights decision needs to identify the actual images and their copies. The U.S. Copyright Office distinguishes generated content from copyrightable human contributions such as creative arrangement or modification. [U.S. Copyright Office report on copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)
- **Shared code and earlier releases.** Terminal uses AGPL-3.0-only for a KOReader-derived engine. Tools offers recipients a choice of AGPL-3.0 or PolyForm Noncommercial. The AGPL option includes commercial use under its terms. Launcher tags through 0.3.20 use AGPL. Browser used MIT through 0.1.18 and AGPL for 0.1.19 through 0.2.16. Git tags at these boundaries confirm the stated terms. A licence for future versions leaves the grants for these published versions available. [GNU AGPL text, sections 5, 6 and 10](https://opensource.org/license/agpl-3.0) · [MIT licence text](https://opensource.org/license/mit)

## Repository inventory

| Repository or app | Own code | Documentation, images, and exceptions |
|---|---|---|
| Blocks, Calculator, Cascade, Focus, Minesweeper, Notes, Ships, Solitaire, Sudoku | PolyForm NC | README applies CC BY-NC-SA to documentation and imagery. Store distributes icons and screenshots separately. |
| Cards | PolyForm NC | Same image terms. The ZIP stages six SQLite and Zstandard licence or attribution files separately. |
| Chess | PolyForm NC | Same image terms. The ZIP carries the MIT notice for cozy-chess. |
| Crossword | PolyForm NC | CC BY-NC-SA also covers original puzzle text. Puzzle content needs its own scope in any image-policy change. |
| Words | PolyForm NC | CC BY-NC-SA covers documentation and imagery. The README documents how the included word banks were selected independently of referenced datasets. Record word-bank terms separately from image terms. |
| 2048, Crate Shift, Memory Match, Nonogram, Snake, Starship, Switchyard | PolyForm NC | CC BY-NC-SA covers documentation and imagery. Checked the game icons in the packaged launcher scripts against the corresponding Store PNGs. |
| Primitive Launcher | PolyForm NC from 0.3.21 | CC BY-NC-SA for original documentation and pictures, with an explicit Amazon Kindle UI icon exception. Preserve the bundled Noto, Dropbear, zlib, and applicable musl notices. |
| Primitive Browser | PolyForm NC from 0.2.17 | CC BY-NC-SA for documentation and project imagery. External webpages appear in some screenshots. Preserve upstream terms for Noto, FBInk, Stylo, QuickJS, and other vendor or native helper code. The Browser ZIP includes Noto and FBInk notices. Compare its linked MIT QuickJS and MPL-2.0 Stylo components and vendored trees with the exact upstream notices and source obligations. |
| Primitive Terminal | AGPL-3.0-only | CC BY-NC-SA for documentation and pictures. Preserve Noto font notices and confirm recipients can obtain corresponding source for the exact distributed version, including its build inputs. |
| Store | PolyForm NC | CC BY-NC-SA for documentation and pictures. Catalog media and third-party listings need their own review. |
| Hello and app template | PolyForm NC | CC BY-NC-SA for documentation and pictures. Align the PolyForm required-notice URL with the app-template repository when updating its terms. The template also needs the chosen policy for future apps. |
| Tools | AGPL-3.0-only OR PolyForm NC | Its app icon directory has its own CC BY-NC-SA notice for first-party icons. Some icons are embedded in compiled code. Terminal uses the AGPL choice, while PolyForm apps use the PolyForm choice. |
| Build | No express first-party software licence found | The reusable packager includes licences from app repositories. Its own code needs an explicit grant if the owner wants others to reuse it on noncommercial terms. |
| Catalog | No express software grant found for its scripts or site code | README applies CC BY-NC-SA to project listings, icons, and screenshots. It identifies the stock KOReader icon as upstream material. KOReader is a linked third-party listing. |
| Umbrella | No express software grant found for its scripts or schemas | The root licence and README apply CC BY-NC-SA to docs, skills, and pictures. Shared schemas and code should have a stated scope. |

**Evidence.** I compared each app's root `LICENSE`, `LICENSE-DOCS`, README, Cargo metadata, and Store metadata where present. The 21 standalone app and game repositories have PolyForm NC across their 28 local release tags. The repository inventory includes one retired title. The current catalog has 25 first-party apps and one linked KOReader listing.

## Release package review

- Inspected all **36 ARMHF ZIPs** referenced by first-party Store listings. The cached ZIP bytes matched catalog size and SHA-256, and the embedded manifest matched the app ID, version, and architecture. Each software licence matched its listing. All 25 latest releases include both `LICENSE` and `LICENSE-DOCS`. Across the Store history checked, Browser 0.2.17 is the sole documentation-licence omission. Browser 0.2.18 includes it.
- Checked **five additional ARMEL ZIPs** from Launcher, Browser, and Terminal, plus **three additional ARMHF ZIPs** from GitHub for Crate Shift 0.1.1 and 2048 under its former Tidefork title at 0.1.1. The ARMEL sample includes the current versions of all three apps.
- The archives have selected notices for native binaries, fonts, and app-specific components. I found no consolidated Rust dependency notice bundle in the inspected ZIPs. The current ARMHF normal dependency graphs expose components under terms such as MIT, Apache-2.0, and Unicode-3.0, including ICU data. Inspect the code and data included in the actual release builds and carry the applicable upstream notices with them. A Cargo dependency graph alone does not identify which code survives linking. [MIT licence](https://opensource.org/license/mit) · [Apache License 2.0, section 4](https://apache.org/licenses/LICENSE-2.0.html) · [Unicode licence](https://www.unicode.org/license.txt) · [SIL font bundling guidance](https://software.sil.org/oflt/)
- Build's `scripts/package.py` adds `LICENSE`, `INSTALL.md`, and the optional `LICENSE-DOCS` as archive metadata. Store checks these separately from installed files in Tools' `crates/kl-store/src/unpack.rs`. A new root metadata filename would need coordinated packager, catalog, and Store support. An image notice or dependency notice can be included as a manifest-owned file under the app's existing install directory.

## Study and work package check, 20 November 2026

All 11 published ARMHF packages for this release contained `LICENSE` and `LICENSE-DOCS` matching their source
repositories. Their listings identify PolyForm Noncommercial 1.0.0 for project code. The documentation licences
cover project-owned artwork and screenshots, plus original starter content where declared. The seven new packages
carry the same approved icons as Store. Tasks, Habits, and Agenda also carry the upstream Chrono notice in their
installed file inventories. [Release list](education-productivity-apps.md#released-apps) · [Verification record](local-verification.md#study-and-work-release-verification)

## Confirmed policy

Viewer follows the project’s code and artwork licences. Its ARMHF package also includes the notices for Hayro,
the embedded PDF fonts and Adobe CMaps, and the linked dependencies under `viewer/licenses/`.
[Viewer notices](https://github.com/PrimitiveOS/kindle-primitive-viewer/tree/main/docs/licenses)

| Material | Licence and scope |
|---|---|
| Project-owned software and its compiled distributions | PolyForm Noncommercial 1.0.0 where the project grants it. The umbrella, Build, and Catalog now explicitly state the terms for their own software. |
| Project-owned documentation, artwork, screenshots, and non-code resources | CC BY-NC-SA 4.0 to the extent the project holds the relevant rights. This covers original puzzle content where stated and the original selection and arrangement in Words’ bundled word banks. [CC BY-NC-SA 4.0 legal code](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en) |
| Third-party software, fonts, stock icons, and other sourced material | The applicable upstream terms and notices accompany each component. Brand identifiers are subject to their applicable trademark rights. |
| Terminal, shared Tools, and earlier published software | Terminal’s AGPL terms, the AGPL option for shared Tools, and the terms of already published versions continue to apply. |

The games’ puzzle and level definitions in Rust source are covered by their software licences. The current Store packages already include their software and documentation licences. The audit's findings about dependency notices concern packaging and are separate from the project’s licence scope.
