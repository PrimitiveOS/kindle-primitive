<div align="center">

# Primitive Redefined Kindle

**A clean, fast, open set of apps for jailbroken Kindle e-readers, and the store that installs them.**

Written in Rust, drawn for e-ink, hosted on GitHub.

</div>

Primitive replaces the Kindle's crowded home screen with a calm grid of the apps you use, and adds what the stock Kindle
lacks: a real web browser, a terminal, SSH, and simple settings for Wi-Fi, display and power. Every app shares one
design language, inspired by Apple's Liquid Glass and rebuilt for black-and-white e-ink. Primitive Store, now being
designed, will install and update them all from the Kindle itself.

This repository is the umbrella: it holds the plan, the store's design, the guides, and the skills shared by every
Primitive app. Each app has its own repository.

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/home.png" alt="Home screen" width="200"><br><sub>Home screen</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/quick-settings.png" alt="Quick settings" width="200"><br><sub>Quick settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/settings.png" alt="Settings" width="200"><br><sub>Settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/dark-home.png" alt="Dark mode" width="200"><br><sub>Dark mode</sub></td>
  </tr>
</table>

<sub>Screenshots from Primitive Launcher's desktop build, with demo values.</sub>

## Why Primitive

- **A clean screen.** One grid of your apps instead of shelves, banners and the store. E-ink redraws only what changed.
- **More memory for your apps.** With the stock interface stopped, apps get about 140 MB more memory on the Kindle Oasis 3.
- **Quick to start.** With the boot start on, the launcher opens as soon as the Kindle's start-up animation ends.
- **One design everywhere.** The same status bar, keyboard, quick settings and wording in every app.
- **Yours to change.** Open source, built on GitHub, installable by USB today and from the store tomorrow.

## The apps

| App | What it is | Repository | Latest | Licence |
|---|---|---|---|---|
| **Primitive Launcher** | The home screen and settings: app grid, quick settings, Wi-Fi, SSH and DNS, display, sleep, power, USB drive mode, start at boot. The host of every other app and of the store. | [kindle-primitive-launcher](https://github.com/DoanNguyenTrong/kindle-primitive-launcher) | [v0.3.20](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/releases) | PolyForm Noncommercial 1.0.0 from the next version (AGPL-3.0 up to v0.3.20) |
| **Primitive Browser** | A web browser made for e-ink, with its own engine, night mode and image switch. | [kindle-primitive-browser](https://github.com/DoanNguyenTrong/kindle-primitive-browser) | [v0.2.16](https://github.com/DoanNguyenTrong/kindle-primitive-browser/releases) | PolyForm Noncommercial 1.0.0 from the next version (AGPL-3.0 up to v0.2.16) |
| **Primitive Terminal** | A shell on the Kindle, with the shared keyboard, history and Ctrl. | [kindle-primitive-terminal](https://github.com/DoanNguyenTrong/kindle-primitive-terminal) | 0.1.8, not released yet | AGPL-3.0 (its engine is ported from KOReader's terminal); licence file to add |
| **Primitive Store** | Browse, install, update and remove apps on the Kindle, with every download checked. | inside the launcher (planned) | design | PolyForm Noncommercial 1.0.0 |

Shared code: [kindle-primtitive-tools](https://github.com/DoanNguyenTrong/kindle-primtitive-tools) holds the on-screen
keyboard (`primitive-keyboard`) and the quick settings figures and icons (`primitive-quick`), under AGPL-3.0 or PolyForm
Noncommercial 1.0.0 at the user's choice. Each app includes it as a git submodule under `tools/`.

The apps are tested on a **Kindle Oasis 3** (hard-float, firmware 5.18.2). The store is designed for every jailbroken
Kindle e-reader; each app says which Kindles it supports.

## How it fits together

```
                      GitHub
   ┌───────────────────────────────────────────────┐
   │ app repos ── Releases (zip + sha256)           │
   │ kindle-primitive-catalog ── Pages (index.json) │
   └───────────────────────┬───────────────────────┘
                           │ HTTPS, checked by sha256
   Kindle (jailbroken)     ▼
   ┌───────────────────────────────────────────────┐
   │ Primitive Launcher ── Store                    │
   │   ├─ Primitive Browser                         │
   │   ├─ Primitive Terminal                        │
   │   └─ other apps, KUAL extensions, scriptlets   │
   └───────────────────────────────────────────────┘
```

The launcher is the only part that starts with the Kindle. Every other app is a module with its own folder and a
library entry, so it shows on the launcher's grid and can be installed, updated and removed on its own.

## Install

Today, install each app by USB from its GitHub release:

1. Download the app's zip (and its `.sha256` to check it) from its releases page.
2. Connect the Kindle by USB while its own home screen shows, and copy the folders from the zip onto the Kindle drive.
3. Eject, unplug, and open the app from the Kindle library.

Start with Primitive Launcher; its `INSTALL.md` (inside the zip) has every step. A jailbroken Kindle is required; see the
[KindleModding wiki](https://kindlemodding.org/) for jailbreaking. When the store ships, installing anything else is a tap:
[docs/store-install-apps.md](docs/store-install-apps.md).

## Documentation

| Document | For |
|---|---|
| [docs/kindle-platform-plan.md](docs/kindle-platform-plan.md) | The plan: repos, architecture, decisions, phases and gates. |
| [docs/implementation-plan.md](docs/implementation-plan.md) | The tracking plan: every milestone and task with checklists and gates. |
| [docs/store-architecture.md](docs/store-architecture.md) | Primitive Store's system design and requirements. |
| [docs/store-submit-app.md](docs/store-submit-app.md) | Developers: how to add an app to the store. |
| [docs/store-install-apps.md](docs/store-install-apps.md) | Kindle owners: how to install, update and remove apps. |
| [docs/store-migration-kindleforge.md](docs/store-migration-kindleforge.md) | KindleForge's 28 packages reviewed against our quality bar: KOReader as a reference, the rest rebuilt natively or left out. |
| [.agents/skills/](.agents/skills) | Shared skills for AI coding agents: `primitive-ui` (the design language), `kindle-device` (working on the device), `kindle-eink` (drawing to e-ink). Linked as `.claude/skills`. |

## For developers

The apps live side by side inside this repository's folder; this repository ignores them, and each keeps its own history:

```sh
git clone https://github.com/DoanNguyenTrong/kindle-primitive.git doannt-kindle
cd doannt-kindle
git clone --recurse-submodules https://github.com/DoanNguyenTrong/kindle-primitive-launcher.git doannt-kindle-launcher
git clone --recurse-submodules https://github.com/DoanNguyenTrong/kindle-primitive-browser.git doannt-kindle-browser
git clone --recurse-submodules https://github.com/DoanNguyenTrong/kindle-primitive-terminal.git doannt-kindle-terminal
git clone https://github.com/DoanNguyenTrong/kindle-primtitive-tools.git doannt-kindle-tools
```

Each app builds for the Kindle with `cargo zigbuild` (target `armv7-unknown-linux-musleabihf`) and has a desktop build that
renders its screens to PNG. New screens follow the `primitive-ui` skill. Every device build bumps the patch version, a new
phase bumps the minor, and release tags are never moved.

## Roadmap

| Phase | What | State |
|---|---|---|
| S0 | Decisions (own store, GitHub hosting, licences, scope) | Done |
| S1 | Contracts, licences for the terminal and tools | Next |
| S2 | Every app packaged by a shared release workflow | Planned |
| S3 | The catalog on GitHub Pages | Planned |
| S4 | The store in the launcher | Planned |
| S5 | Launcher, Browser and Terminal installed from the store | Planned |
| S6 | Other Kindle projects listed by link | Planned |
| S7 | Hardening: architecture and firmware checks, recovery | Planned |

Details and checklists: [docs/kindle-platform-plan.md](docs/kindle-platform-plan.md).

## Thanks

Primitive learns from the Kindle community: [KOReader](https://koreader.rocks/), the
[KindleModding wiki](https://kindlemodding.org/), [Awesome-Kindle](https://github.com/KindleTweaks/Awesome-Kindle),
[KindleForge](https://github.com/KindleTweaks/KindleForge), [KPM](https://github.com/Gingrspacecadet/KPM), and KUAL.
Primitive is not affiliated with any of them.

## Licence and trademarks

Each app is under its own licence (see the table). The documents, skills and pictures in this repository are under
[CC BY-NC-SA 4.0](LICENSE): share and adapt them for non-commercial purposes, with credit, under the same licence.

Kindle is a trademark of Amazon.com, Inc. or its affiliates. Primitive is not affiliated with or endorsed by Amazon.
Jailbreaking and changing a Kindle's software is at your own risk.
