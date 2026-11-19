<div align="center">

# Primitive Redefined Kindle

**Your Kindle, set free.**

A calm, open operating layer for jailbroken Kindle e-readers: a home screen, settings, apps, and an app store of our own,
in place of Amazon's storefront.

Written in Rust, drawn for e-ink, hosted on GitHub.

</div>

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/home.png" alt="Home screen" width="200"><br><sub>Your apps, not a shop window</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/quick-settings.png" alt="Quick settings" width="200"><br><sub>Quick settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/settings.png" alt="Settings" width="200"><br><sub>Settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/DoanNguyenTrong/kindle-primitive-launcher/main/docs/images/dark-home.png" alt="Dark mode" width="200"><br><sub>Dark mode</sub></td>
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
- **Reading comes first, and so does the law.** Primitive does not remove DRM and does not help anyone get books they
  have not paid for.

## A true OS for the Kindle

Inside every Kindle is Linux, with Amazon's interface running on top of it. Primitive keeps the Linux and replaces the
interface:

| | Amazon's interface | Primitive |
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

What we keep from Amazon, on purpose: the Linux kernel and its drivers. That is what keeps Primitive safe and
reversible. Amazon's own interface is one tap away, it comes back by itself if Primitive fails to start, and removing
Primitive's folders returns the Kindle to Amazon's interface.

## Inspiration

- **Apple** for the design language and the quality bar: few controls, clear words, and nothing that needs a manual.
- **Android and the custom ROM community** for the belief that hardware should keep living after its maker loses
  interest, and that you should be able to install what you want.
- **The Kindle community**: [KOReader](https://koreader.rocks/) proved how much a Kindle can do, and the
  [KindleModding wiki](https://kindlemodding.org/), [Awesome-Kindle](https://github.com/KindleTweaks/Awesome-Kindle),
  [KindleForge](https://github.com/KindleTweaks/KindleForge), [KPM](https://github.com/Gingrspacecadet/KPM) and KUAL
  opened the door. Primitive is not affiliated with any of them.

## The apps

| App | What it is | Repository | Latest | Licence |
|---|---|---|---|---|
| **Primitive Launcher** | The home screen and settings: app grid, quick settings, Wi-Fi, SSH and DNS, display, sleep, power, USB drive mode, start at boot. The host of every other app and of the store. | [kindle-primitive-launcher](https://github.com/DoanNguyenTrong/kindle-primitive-launcher) | 0.3.21 | PolyForm Noncommercial 1.0.0 (AGPL-3.0 up to v0.3.20) |
| **Primitive Browser** | A web browser made for e-ink, with its own engine, night mode and an image switch. | [kindle-primitive-browser](https://github.com/DoanNguyenTrong/kindle-primitive-browser) | 0.2.17 | PolyForm Noncommercial 1.0.0 (AGPL-3.0 up to v0.2.16) |
| **Primitive Terminal** | A shell on the Kindle, with the shared keyboard, history and Ctrl. | [kindle-primitive-terminal](https://github.com/DoanNguyenTrong/kindle-primitive-terminal) | 0.1.8 | AGPL-3.0 (its engine is ported from KOReader's terminal) |
| **Store** | Standalone app to browse, install, update and remove Kindle apps. Launcher opens it from one Store tile. | [kindle-primitive-store](https://github.com/DoanNguyenTrong/kindle-primitive-store) | 0.1.1 | PolyForm Noncommercial 1.0.0 |

Coming as native apps (see the [implementation plan](docs/implementation-plan.md)): Notes, Focus, Cards, Calculator,
Words, Sudoku, Chess, Minesweeper, Solitaire, Crossword, Blocks, Ships, and a falling-blocks game.

Shared code: [kindle-primtitive-tools](https://github.com/DoanNguyenTrong/kindle-primtitive-tools) holds the on-screen
keyboard and the quick settings figures and icons, under AGPL-3.0 or PolyForm Noncommercial 1.0.0 at your choice.

The apps are tested on a **Kindle Oasis 3**. The store is designed for every jailbroken Kindle e-reader, and each app says
which Kindles it supports.

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

## Install

A jailbroken Kindle is required; the [KindleModding wiki](https://kindlemodding.org/) explains how. Then install
Primitive Launcher by USB from its latest release:

1. Download `primitive-launcher-<version>.zip` (and its `.sha256` to check it) from the
   [releases page](https://github.com/DoanNguyenTrong/kindle-primitive-launcher/releases).
2. Connect the Kindle by USB while its own home screen shows, and copy the `launcher` and `documents` folders onto it.
3. Eject, unplug, and open **Launcher** in the Kindle library. The first time, it also sets itself up to start with the
   Kindle.

Other apps install the same way today. When the store ships, installing anything else is a tap:
[docs/store-install-apps.md](docs/store-install-apps.md).

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
| A | Foundations: this repo, contracts, licences, device checks | This repo done; the rest next |
| B | Every app packaged by a shared release workflow | Planned |
| C | The catalog on GitHub Pages | Planned |
| D | Standalone Store and its Launcher entry | See local verification |
| E | An app kit and template, so new apps are small | Planned |
| F | Native apps: productivity tools and games | Planned |
| G | Launcher features: jailbreak status, Wi-Fi file transfer, Bluetooth keyboard | Planned |
| H | Hardening: other Kindles, recovery, signatures | Planned |

Details and checklists: [docs/implementation-plan.md](docs/implementation-plan.md).

## Licence and trademarks

Each app is under its own licence (see the table). The documents, skills and pictures in this repository are under
[CC BY-NC-SA 4.0](LICENSE): share and adapt them for non-commercial purposes, with credit, under the same licence.

Kindle is a trademark of Amazon.com, Inc. or its affiliates. Primitive is not affiliated with or endorsed by Amazon.
Jailbreaking and changing a Kindle's software is at your own risk.
