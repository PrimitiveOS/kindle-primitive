<div align="center">

# PrimitiveOS - Redefine Your Kindle

**Your Kindle, set free.**

PrimitiveOS is an open operating environment for jailbroken Kindle e-readers. It gives your Kindle a home screen for
your apps, device settings, and a Store for installing and updating apps over Wi-Fi.

Written in Rust, drawn for e-ink, hosted on GitHub.

</div>

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/6d1f2ed124bb48fbc2162d9ff7d513d6346f9f7d/docs/images/home.png" alt="Home screen" width="200"><br><sub>Home screen</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/6d1f2ed124bb48fbc2162d9ff7d513d6346f9f7d/docs/images/quick-settings.png" alt="Quick settings" width="200"><br><sub>Quick settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/6d1f2ed124bb48fbc2162d9ff7d513d6346f9f7d/docs/images/settings.png" alt="Settings" width="200"><br><sub>Settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/6d1f2ed124bb48fbc2162d9ff7d513d6346f9f7d/docs/images/dark-home.png" alt="Dark mode" width="200"><br><sub>Dark mode</sub></td>
  </tr>
</table>

<sub>Screenshots from Primitive Launcher's desktop build, with demo values.</sub>

## Why we started

A Kindle is a wonderful piece of hardware. Its screen reads like paper, its battery lasts for weeks, it weighs almost
nothing, and it never buzzes for attention. It could be the calmest computer you own.

Its software is built for something else: selling. The home screen is a shop window of recommendations. Ad-supported
models show ads until you pay to remove them. You cannot install an app. The browser is basic, the settings are few, and
the device does only what Amazon decides it should do, for as long as Amazon decides. Features can disappear: in
early 2025, Amazon removed the option to download purchased books from its website and copy them to a Kindle over USB.

We think a device you bought should work for you. So we started building the Kindle we wanted: one that opens on your own
apps, shows no ads, asks for no account, and can grow with apps that anyone can make and share.

## What we believe

- **Your device, your choices.** No ads, no account, no tracking. Nothing leaves the Kindle unless you ask it to.
- **Calm by design.** E-ink is for focus. The interface stays out of the way and redraws only what changed.
- **Quality for everyone.** Every app has a real touch interface and works without a terminal. We hold our apps to the
  standard of the best phone apps, and the store holds every listing to the same bar.
- **One design everywhere.** A single design language, inspired by Apple's Liquid Glass and rebuilt for black-and-white
  e-ink: the same status bar, keyboard, quick settings and words in every app.
- **Open and fair.** The source is on GitHub. Our licences keep the work non-commercial and shared, and we credit the
  community whose work made this possible.
- **Reading comes first, and so does the law.** PrimitiveOS does not remove DRM and does not help anyone get books they
  have not paid for.

## Built on Kindle's Linux

PrimitiveOS uses the Kindle's Linux kernel and drivers. Primitive Launcher provides the home screen and settings.

| | Amazon's interface | PrimitiveOS |
|---|---|---|
| Home screen | Shop shelves and recommendations | Your apps on a calm grid |
| Apps | Only what Amazon ships | Apps from Store, or your own |
| Web | A basic browser | Primitive Browser, made for e-ink |
| Settings | A few switches | Wi-Fi, SSH, DNS, display, warmth, sleep, power, start at boot |
| Memory for apps | The stock interface takes it | About 140 MB more, with the stock interface stopped (Oasis 3) |
| Ads | On ad-supported models, unless you pay | None |
| Start-up | Into Amazon's home | Into your home screen |

Primitive Launcher is the home screen and starts with the Kindle. It handles what the stock interface did: Wi-Fi,
sleep and wake, rotation, the battery, USB drive mode, power off and restart. Apps are modules that install, update and
uninstall on their own, and the standalone Store installs them from the Kindle itself.

Use the **Kindle UI** tile to return to Amazon's interface. Launcher can also restore it if startup fails. The Launcher
installation guide explains how to remove its files. [Launcher installation guide](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/blob/main/docs/INSTALL.md)

## Inspiration

- **Apple** for the design language and the quality bar: few controls, clear words, and nothing that needs a manual.
- **Android and the custom ROM community** for the belief that hardware should keep living after its maker loses
  interest, and that you should be able to install what you want.
- **The Kindle community**: [KOReader](https://koreader.rocks/) proved how much a Kindle can do, and the
  [KindleModding wiki](https://kindlemodding.org/), [Awesome-Kindle](https://github.com/KindleTweaks/Awesome-Kindle),
  [KindleForge](https://github.com/KindleTweaks/KindleForge), [KPM](https://github.com/Gingrspacecadet/KPM) and KUAL
  opened the door. PrimitiveOS is an independent project.

## The apps

| App | What it is | Repository | Latest | Licence |
|---|---|---|---|---|
| **Primitive Launcher** | The home screen and device settings for PrimitiveOS. Opens Store and the apps you install. | [kindle-primitive-launcher](https://github.com/DoanNguyenTrong/kindle-primitive-launcher) | [0.4.10](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/releases/tag/v0.4.10) | PolyForm Noncommercial 1.0.0 (AGPL-3.0 up to v0.3.20) |
| **Primitive Browser** | A web browser made for e-ink, with its own engine, night mode and an image switch. | [kindle-primitive-browser](https://github.com/DoanNguyenTrong/kindle-primitive-browser) | [0.2.18](https://github.com/DoanNguyenTrong/kindle-primitive-browser/releases/tag/v0.2.18) | PolyForm Noncommercial 1.0.0 (AGPL-3.0 up to v0.2.16) |
| **Primitive Terminal** | A shell on the Kindle, with the shared keyboard, history and Ctrl. | [kindle-primitive-terminal](https://github.com/DoanNguyenTrong/kindle-primitive-terminal) | 0.1.8 | AGPL-3.0 (its engine is ported from KOReader's terminal) |
| **Store** | Browse, install, update and remove Kindle apps. Open the Store tile in Launcher. | [kindle-primitive-store](https://github.com/DoanNguyenTrong/kindle-primitive-store) | [0.1.4](https://github.com/DoanNguyenTrong/kindle-primitive-store/releases/tag/v0.1.4) | PolyForm Noncommercial 1.0.0 |

First-party apps in Store include Notes, Focus, Cards, Calculator, Words, Sudoku, Chess, Minesweeper, Solitaire,
Crossword, Blocks, Ships, and Cascade. [Public catalog](https://doannguyentrong.github.io/kindle-primitive-catalog/v1/index.json)

### Games

| Game | How to play |
|---|---|
| [Starship](https://github.com/DoanNguyenTrong/kindle-primitive-starship) | Dodge incoming fire, time your shields, and clear four waves. |
| [Tidefork](https://github.com/DoanNguyenTrong/kindle-primitive-tidefork) | Slide a single line of tiles to merge numbers and solve short challenges. |
| [Trail Carrier](https://github.com/DoanNguyenTrong/kindle-primitive-trailcarrier) | Collect parcels and reach the exit as your trail grows. |
| [Picture Logic](https://github.com/DoanNguyenTrong/kindle-primitive-picturelogic) | Reveal pictures from row and column clues. |
| [Switchyard](https://github.com/DoanNguyenTrong/kindle-primitive-switchyard) | Set track junctions and dispatch a train to the depot. |
| [Crate Shift](https://github.com/DoanNguyenTrong/kindle-primitive-crateshift) | Push crates onto marked docks across eight puzzles. |
| [Memory Pairs](https://github.com/DoanNguyenTrong/kindle-primitive-memorypairs) | Match all the symbols in as few turns as possible. |

Shared code: [kindle-primtitive-tools](https://github.com/DoanNguyenTrong/kindle-primtitive-tools) holds the on-screen
keyboard and the quick settings figures and icons, under AGPL-3.0 or PolyForm Noncommercial 1.0.0 at your choice.

PrimitiveOS has been tested on a **Kindle Oasis 3**. Each Store listing shows its Kindle requirements and device test status.

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
   │ Primitive Launcher (home screen) ── Store      │
   │   ├─ Primitive Browser                         │
   │   ├─ Primitive Terminal                        │
   │   └─ native apps: Notes, Focus, Words, …       │
   ├───────────────────────────────────────────────┤
   │ Linux kernel and drivers (Amazon's, unchanged) │
   └───────────────────────────────────────────────┘
```

## Get started with PrimitiveOS

A jailbroken Kindle is required. [KindleModding wiki](https://kindlemodding.org/)

Primitive Launcher is the only app you install manually during initial setup. If Launcher is already installed,
open **Store** from the Launcher home screen and use **Updates** for newer releases.

1. Download and extract the Launcher ZIP for your Kindle. Compare its SHA-256 with the `.sha256` file on the release
   page. [Latest Launcher release](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/releases/latest)
2. Connect the Kindle by USB while Amazon's Kindle interface is open. Copy `launcher/` to the root of the Kindle drive
   and `documents/Launcher.sh` into the Kindle's existing `documents/` folder.
3. Eject the Kindle drive, unplug the cable, and open **Launcher** in the Kindle library.
4. Connect to Wi-Fi and tap **Store** on the Launcher home screen. Launcher installs Store when needed.
   Use Store to install and update your apps. [Store guide](docs/store-install-apps.md)

## Documentation

| Document | For |
|---|---|
| [docs/kindle-platform-plan.md](docs/kindle-platform-plan.md) | The plan: repos, architecture, decisions, phases and gates. |
| [docs/implementation-plan.md](docs/implementation-plan.md) | The tracking plan: every milestone and task with checklists and gates. |
| [docs/store-architecture.md](docs/store-architecture.md) | Store design and requirements. |
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

| Track | What | State |
|---|---|---|
| A | Foundations: this repo, contracts, licences, device checks | Repo, contracts and licences in place |
| B | Every app packaged by a shared release workflow | Release packages published |
| C | The catalog on GitHub Pages | Live |
| D | Standalone Store and its Launcher entry | Released and tested on Kindle Oasis 3 |
| E | An app kit and template, so new apps are small | Shared kit and template available |
| F | Native apps: productivity tools and games | Available in Store |
| G | Launcher features: jailbreak status, Wi-Fi file transfer, Bluetooth keyboard | Planned |
| H | Hardening: other Kindles, recovery, signatures | Planned |

Details and checklists: [docs/implementation-plan.md](docs/implementation-plan.md).

## Licence and trademarks

Each app is under its own licence (see the table). The documents, skills and pictures in this repository are under
[CC BY-NC-SA 4.0](LICENSE): share and adapt them for non-commercial purposes, with credit, under the same licence.

Kindle is a trademark of Amazon.com, Inc. or its affiliates. PrimitiveOS is not affiliated with or endorsed by Amazon.
Jailbreaking and changing a Kindle's software is at your own risk.
