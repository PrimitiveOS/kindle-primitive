# PrimitiveOS platform plan

Status date 2026-11-20. Primitive Launcher hosts independently packaged apps and opens Store, which uses a
GitHub-hosted catalog. The [implementation plan](implementation-plan.md) tracks milestones and device gates.
The [app directory](../README.md#the-apps) links first-party repositories and their published releases.

## 1. What the ecosystem looks like

The original ecosystem review used [Awesome-Kindle](https://github.com/KindleTweaks/Awesome-Kindle) at commit
`ae2e041`. It identified scriptlets, KUAL extensions, and KOReader plugins as common ways to extend a Kindle.

- The review found KindleForge in maintenance mode, with KPM proposed as its next backend. KindleForge and its package
  repository use different licences, so PrimitiveOS reviews the terms of each upstream package before distribution.
  [KindleForge migration review](store-migration-kindleforge.md)
- KPM is a shell package manager. PrimitiveOS has its own package contract and a touch interface for installation.
  The KPM format remains a possible compatibility project. [Open items](#6-open-items)
- Primitive Launcher discovers KUAL extensions and Kindle library scriptlets. Store applies its own listing criteria.
- PrimitiveOS runs on the Kindle's existing Linux system and requires a jailbreak. The Oasis 3 running firmware 5.18.2
  is the model used for platform hardware validation. Release-specific device evidence belongs in the implementation
  plan and the app repositories.

## 2. Repo inventory

Component folders are siblings inside the umbrella checkout. New apps have their own repo and release history.

| Local folder | GitHub repository | Role and published state |
|---|---|---|
| `doannt-kindle` | [kindle-primitive](https://github.com/PrimitiveOS/kindle-primitive) | Platform docs, schemas, shared skills, and app directory. |
| `doannt-kindle-launcher` | [kindle-primitive-launcher](https://github.com/PrimitiveOS/kindle-primitive-launcher) | Launcher 0.4.10. Home screen, settings, lifecycle, USB handoff, and Store bootstrap. |
| `doannt-kindle-store` | [kindle-primitive-store](https://github.com/PrimitiveOS/kindle-primitive-store) | Store 0.1.4. Standalone catalog browser and installer. |
| `doannt-kindle-browser` | [kindle-primitive-browser](https://github.com/PrimitiveOS/kindle-primitive-browser) | Primitive Browser 0.2.18. Standalone browsing and offline reading. |
| `doannt-kindle-terminal` | [kindle-primitive-terminal](https://github.com/PrimitiveOS/kindle-primitive-terminal) | Primitive Terminal 0.1.8. Developer tool. |
| `doannt-kindle-tools` | [kindle-primtitive-tools](https://github.com/PrimitiveOS/kindle-primtitive-tools) | Shared Rust device, e-ink, UI, network, and Store crates. Each app pins the Tools revision that it builds against. |
| `doannt-kindle-build` | [kindle-primitive-build](https://github.com/PrimitiveOS/kindle-primitive-build) | Reusable release workflow and package validation. Apps pin the workflow revision. |
| `doannt-kindle-catalog` | [kindle-primitive-catalog](https://github.com/PrimitiveOS/kindle-primitive-catalog) | Listings, collections, icons, and screenshots, published through GitHub Pages. |
| `doannt-kindle-app-template` | [kindle-primitive-app-template](https://github.com/PrimitiveOS/kindle-primitive-app-template) | Native app template and source for Hello 0.1.0. |

Versions above describe public releases. For licensing boundaries and older versions, see the [licensing audit](licence-audit.md).

## 3. Architecture

### 3.1 Layers

```text
GitHub
  Publisher repos ── versioned ZIPs and SHA-256 sidecars ── GitHub Releases
  Catalog repo    ── validated listings and artwork     ── GitHub Pages

Kindle
  Primitive Launcher ── opens or bootstraps Store from one home-screen tile
  Store              ── caches the catalog and manages package transactions
  Apps               ── install to their own folders and open from Launcher
```

Store runs as a standalone program. Launcher owns the home screen, Store bootstrap, and app supervision.
The launcher is the system layer over every app: it keeps the power button, sleep, the lock screen, quick settings
and the theme while an app is open ([system architecture](system-architecture.md),
[upgrade plan](system-upgrade-plan.md)).
Both share the Store engine (`kl-store`) from Tools. The other shared crates are compiled into app binaries.
The catalog publishes metadata and artwork. GitHub Releases serve package binaries.
[Store architecture](store-architecture.md)

### 3.2 Contracts

[App, package, and catalog contracts](contracts.md) define scriptlet headers, module folders, release archives,
and the three schema 1 documents. The machine-readable schemas are in [schema/](../schema/).

A release has one `<id>-<version>-<arch>.zip` per architecture, with an internal manifest and a matching
`.sha256` file. The manifest defines the allowed install paths, architecture, firmware range, and minimum versions
of dependencies. The catalog listing records each asset URL, size, and digest. Git tags match their package version
and remain immutable.

### 3.3 Install flow on the device

1. For initial setup, copy Launcher to the Kindle drive by USB and open it from the stock Kindle library. This is the
   one manual app install. On an existing setup, use the installed Launcher. [Installation guide](store-install-apps.md#2-install-primitive-launcher-once)
2. Open **Store** from Launcher. If needed, Launcher downloads and verifies a compatible Store package over Wi-Fi.
   Store opens from the local catalog cache and refreshes over Wi-Fi.
3. Choose an app. Store resolves architecture, firmware, and dependencies, checks available space, verifies the
   download against its expected size and SHA-256, then verifies the ZIP contents against the manifest.
4. Store stages the package, updates the installed record, and refreshes the library. Removal follows the recorded
   file list. Updates stage replacements and keep a recovery path. Launcher updates also go through a startup trial.
5. A linked listing directs the user to the upstream instructions. KOReader is currently listed this way.

See the [Store architecture](store-architecture.md) for cache paths, the install journal, and recovery behaviour.

## 4. Execution strategy

### Phase S0: decisions (answered 2026-11-19)

| Decision | Outcome |
|---|---|
| D1 Store host | PrimitiveOS owns the Store. Launcher opens it as a separate application. |
| D2 Hosting | GitHub Releases serves ZIPs and checksum sidecars. GitHub Pages serves the catalog. |
| D3 Upstream distribution | Respect each package's licence and the owner's curation decisions. KOReader is a linked listing. |
| D4 App scope | Start from the Launcher, Browser, and Terminal. The catalog now includes Store, native apps, and games. The listing bar still applies. |
| D5 Device scope | Jailbroken Kindle e-readers. Every package declares architecture and firmware compatibility. Record tested models per release from hardware evidence. |
| D6 Umbrella | Keep platform docs, schemas, and skills in the public umbrella with independent app repos. |
| D7 Integrity | Verify public downloads by SHA-256. Ed25519 verification is available for opt-in use under a separate production trust decision. [Signatures](store-signatures.md) |

### Delivery and validation phases

| Phase | Current state | Tracking |
|---|---|---|
| S1 Foundations | Contracts, schemas, and project licence policy are documented. | [Foundations](implementation-plan.md#a-foundations-phase-s1) |
| S2 Packaging | Tagged releases build through the shared workflow. Launcher, Browser, and Terminal have ARMEL builds that still need soft-float hardware validation. | [Packaging](implementation-plan.md#b-packaging-phase-s2) |
| S3 Catalog | Pages serves 34 listings, including 33 hosted ARMHF apps and the KOReader link. Scheduled catalog builds include per-app download totals. | [Catalog](implementation-plan.md#c-catalog-phase-s3), [live index](https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json) |
| S4–S5 Store and modules | Standalone Store is published. Earlier Oasis 3 checks covered bootstrap, catalog refresh, app install and open, and a Launcher update trial. Remaining device checks are listed in the implementation plan. | [Store](implementation-plan.md#d-store-phases-s4-and-s5) |
| S6 Native apps | The 2026-11-20 release added seven education and productivity apps and updated Cards, Notes, Focus, and Calculator. All 11 release packages passed desktop Store integration checks. Oasis 3 validation is pending for those versions. | [Release scope](education-productivity-apps.md), [Study and work collection](https://primitiveos.github.io/kindle-primitive-catalog/v1/collections.json) |
| S7 Hardening | Package recovery, optional signing, and catalog checks have local or CI coverage. Hardware recovery, broader model coverage, and any production signing rollout have their own gates. | [Hardening](implementation-plan.md#h-hardening-phase-s7) |

The release gate covers published artifacts and catalog checks. The device gate covers what was actually observed on a
Kindle. The [implementation plan](implementation-plan.md) records evidence for each.

## 5. Risks

- **R1 Storage.** Apps install to `/mnt/us`, and Launcher also maintains a boot copy in `/var/local`. Installation
  checks space for the download, unpacking, and replacement.
- **R2 Launcher updates.** The installed binary, running copy, and boot copy can drift. The startup trial verifies
  the candidate and can restore the previous version.
- **R3 Kindle models.** Package architecture and firmware checks gate installation. Validate on each model before
  reporting it as tested, including soft-float Kindles.
- **R4 Site-specific content.** Browser keeps the site-specific hosts override script outside its release package.
- **R5 Licences.** Follow the current [project policy](licence-audit.md#confirmed-policy) and retain third-party notices
  and the terms of already published releases.
- **R6 Package ecosystems.** The build and install pipeline uses the PrimitiveOS contract. See the
  [migration review](store-migration-kindleforge.md) for upstream compatibility and curation decisions.
- **R7 Integrity.** Verify release size, SHA-256, and paths before installation. Follow the
  [separate trust procedure](store-signatures.md) if production signatures are approved.
- **R8 Public repos.** Scan staged changes and release packages for secrets and device identifiers before publishing.

## 6. Open items

- **O3** Review KPM's package format if interoperability is requested.
- Validate more Kindle models, including ARMEL, and record results per release.
- Finish the device checks for the new Study and work releases.
- Keep production signature provisioning as a separate decision. [Store signatures](store-signatures.md)
