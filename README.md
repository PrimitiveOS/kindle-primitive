<div align="center">

# PrimitiveOS - Redefine Your Kindle

**Your Kindle, set free.**

PrimitiveOS is an open operating environment for jailbroken Kindle e-readers. It gives your Kindle a home screen for
your apps, device settings, and a Store for installing and updating apps over Wi-Fi.

Written in Rust, drawn for e-ink, hosted on GitHub.

</div>

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/PrimitiveOS/kindle-primitive-launcher/fdd81fd0a76fb596b3094f251e9a93a5e5c08070/docs/images/home.png" alt="Home screen" width="200"><br><sub>Home screen</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/PrimitiveOS/kindle-primitive-launcher/fdd81fd0a76fb596b3094f251e9a93a5e5c08070/docs/images/quick-settings.png" alt="Quick settings" width="200"><br><sub>Quick settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/PrimitiveOS/kindle-primitive-launcher/fdd81fd0a76fb596b3094f251e9a93a5e5c08070/docs/images/settings.png" alt="Settings" width="200"><br><sub>Settings</sub></td>
    <td align="center"><img src="https://raw.githubusercontent.com/PrimitiveOS/kindle-primitive-launcher/fdd81fd0a76fb596b3094f251e9a93a5e5c08070/docs/images/dark-home.png" alt="Dark mode" width="200"><br><sub>Dark mode</sub></td>
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
installation guide explains how to remove its files. [Launcher installation guide](https://github.com/PrimitiveOS/kindle-primitive-launcher/blob/main/docs/INSTALL.md)

## Inspiration

- **Apple** for the design language and the quality bar: few controls, clear words, and nothing that needs a manual.
- **Android and the custom ROM community** for the belief that hardware should keep living after its maker loses
  interest, and that you should be able to install what you want.
- **The Kindle community**: [KOReader](https://koreader.rocks/) proved how much a Kindle can do, and the
  [KindleModding wiki](https://kindlemodding.org/), [Awesome-Kindle](https://github.com/KindleTweaks/Awesome-Kindle),
  [KindleForge](https://github.com/KindleTweaks/KindleForge), [KPM](https://github.com/Gingrspacecadet/KPM) and KUAL
  opened the door. PrimitiveOS is an independent project.

## The apps

The tables cover every first-party app in Store. App names link to GitHub repositories, and version numbers link to
the releases currently listed in Store.
[Live Store catalog](https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json)

The catalog's daily report totals GitHub release ZIP downloads for each first-party app. Downloads through Store,
manual downloads, and automated checks all contribute. Store shows the total on each app page when available.
The Catalog workflow saves reports in Markdown, CSV, and JSON. [Download reports](https://github.com/PrimitiveOS/kindle-primitive-catalog/actions/workflows/catalog.yml)

### System

| App on GitHub | What it does | Store version |
|---|---|---|
| [Primitive Launcher](https://github.com/PrimitiveOS/kindle-primitive-launcher) | Home screen, wallpaper previews, quick settings, and device controls. Uninstall apps from Settings. | [0.5.9](https://github.com/PrimitiveOS/kindle-primitive-launcher/releases/tag/v0.5.9) |
| [Store](https://github.com/PrimitiveOS/kindle-primitive-store) | Browse a scrolling catalog, see app download totals, and install, update, or remove apps. | [0.1.8](https://github.com/PrimitiveOS/kindle-primitive-store/releases/tag/v0.1.8) |

### Internet

| App on GitHub | What it does | Store version |
|---|---|---|
| [Primitive Browser](https://github.com/PrimitiveOS/kindle-primitive-browser) | Browse the web with e-ink page controls, night mode, and an image switch. | [0.2.21](https://github.com/PrimitiveOS/kindle-primitive-browser/releases/tag/v0.2.21) |

### Reading

| App on GitHub | What it does | Store version |
|---|---|---|
| [Reader](https://github.com/PrimitiveOS/kindle-primitive-reader) | Read EPUB, compatible Kindle books, PDFs and comics offline. Read correctly positioned EPUB footnotes, see chapter and book time estimates, search PDFs by word boundaries and open high-resolution print images. | [0.1.17](https://github.com/PrimitiveOS/kindle-primitive-reader/releases/tag/v0.1.17) |

### Education and study

| App on GitHub | What it does | Store version |
|---|---|---|
| [Reading Practice](https://github.com/PrimitiveOS/kindle-primitive-reading-practice) | Read short passages, answer questions, and retry missed answers. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-reading-practice/releases/tag/v0.1.1) |
| [Math Practice](https://github.com/PrimitiveOS/kindle-primitive-math-practice) | Read examples and practice arithmetic, fractions, and percentages. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-math-practice/releases/tag/v0.1.1) |
| [Language Practice](https://github.com/PrimitiveOS/kindle-primitive-language-practice) | Practice beginner English using Vietnamese prompts and short tap exercises. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-language-practice/releases/tag/v0.1.1) |

### Productivity

| App on GitHub | What it does | Store version |
|---|---|---|
| [Cards](https://github.com/PrimitiveOS/kindle-primitive-cards) | Create or import flashcards, review on a schedule, and run short self-tests. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-cards/releases/tag/v0.1.2) |
| [Focus](https://github.com/PrimitiveOS/kindle-primitive-focus) | Run focus and break timers, label sessions, and review a weekly study log. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-focus/releases/tag/v0.1.2) |
| [Notes](https://github.com/PrimitiveOS/kindle-primitive-notes) | Write and search plain-text notes, check off lists, and keep a reading journal. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-notes/releases/tag/v0.1.2) |
| [Agenda](https://github.com/PrimitiveOS/kindle-primitive-agenda) | Read a chronological calendar and import supported events from an iCalendar file. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-agenda/releases/tag/v0.1.1) |
| [Habits](https://github.com/PrimitiveOS/kindle-primitive-habits) | Log check-ins and review daily or weekly habits. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-habits/releases/tag/v0.1.1) |
| [Tasks](https://github.com/PrimitiveOS/kindle-primitive-tasks) | Manage today’s tasks, due dates, lists, and repeating items. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-tasks/releases/tag/v0.1.1) |

### Utilities

| App on GitHub | What it does | Store version |
|---|---|---|
| [Calculator](https://github.com/PrimitiveOS/kindle-primitive-calculator) | Calculate and revisit history, convert units, see worked steps, and plot a graph. | [0.1.4](https://github.com/PrimitiveOS/kindle-primitive-calculator/releases/tag/v0.1.4) |
| [Files](https://github.com/PrimitiveOS/kindle-primitive-files) | Browse, find, and organise Kindle files. Open supported documents in Reader, Viewer, or KOReader. | [0.1.4](https://github.com/PrimitiveOS/kindle-primitive-files/releases/tag/v0.1.4) |
| [Hello](https://github.com/PrimitiveOS/kindle-primitive-app-template) | Try a small native example app and use its repository as an app template. | [0.1.0](https://github.com/PrimitiveOS/kindle-primitive-app-template/releases/tag/v0.1.0) |
| [Dictionary](https://github.com/PrimitiveOS/kindle-primitive-dictionary) | Look up definitions, import a glossary, and export favorites for Cards. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-dictionary/releases/tag/v0.1.2) |
| [Viewer](https://github.com/PrimitiveOS/kindle-primitive-viewer) | Read PDFs with continuous scrolling and open JPEGs and PNGs offline. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-viewer/releases/tag/v0.1.2) |

### Developer tools

| App on GitHub | What it does | Store version |
|---|---|---|
| [Primitive Terminal](https://github.com/PrimitiveOS/kindle-primitive-terminal) | Run shell commands with the shared on-screen keyboard and command history. | [0.1.9](https://github.com/PrimitiveOS/kindle-primitive-terminal/releases/tag/v0.1.9) |

### Games

#### Puzzles and word games

| App on GitHub | What it does | Store version |
|---|---|---|
| [2048](https://github.com/PrimitiveOS/kindle-primitive-2048) | Swipe the board, merge matching numbers, and beat your best score. | [0.1.4](https://github.com/PrimitiveOS/kindle-primitive-2048/releases/tag/v0.1.4) |
| [Blocks](https://github.com/PrimitiveOS/kindle-primitive-blocks) | Place pieces and clear full rows, columns, or 3 × 3 boxes. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-blocks/releases/tag/v0.1.1) |
| [Crate Shift](https://github.com/PrimitiveOS/kindle-primitive-crate-shift) | Swipe to move and push crates onto marked docks across eight puzzles. | [0.1.3](https://github.com/PrimitiveOS/kindle-primitive-crate-shift/releases/tag/v0.1.3) |
| [Crossword](https://github.com/PrimitiveOS/kindle-primitive-crossword) | Solve mini crosswords or open your own unlocked `.puz` files. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-crossword/releases/tag/v0.1.1) |
| [Memory Match](https://github.com/PrimitiveOS/kindle-primitive-memory-match) | Turn over cards and find every matching pair in as few attempts as possible. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-memory-match/releases/tag/v0.1.2) |
| [Minesweeper](https://github.com/PrimitiveOS/kindle-primitive-minesweeper) | Flag mines and beat your best time on three board sizes. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-minesweeper/releases/tag/v0.1.1) |
| [Nonogram](https://github.com/PrimitiveOS/kindle-primitive-nonogram) | Reveal pictures by solving row and column clues. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-nonogram/releases/tag/v0.1.2) |
| [Sudoku](https://github.com/PrimitiveOS/kindle-primitive-sudoku) | Solve generated puzzles with pencil marks, mistake checks, and undo. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-sudoku/releases/tag/v0.1.1) |
| [Switchyard](https://github.com/PrimitiveOS/kindle-primitive-switchyard) | Set track junctions and dispatch a train to the depot. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-switchyard/releases/tag/v0.1.1) |
| [Words](https://github.com/PrimitiveOS/kindle-primitive-words) | Solve a daily five-letter word puzzle or play a practice round. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-words/releases/tag/v0.1.1) |

#### Card and board games

| App on GitHub | What it does | Store version |
|---|---|---|
| [Chess](https://github.com/PrimitiveOS/kindle-primitive-chess) | Play against your Kindle at three levels, save games, and export PGN. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-chess/releases/tag/v0.1.1) |
| [Ships](https://github.com/PrimitiveOS/kindle-primitive-ships) | Place your ships and hunt the opposing fleet against your Kindle or a second player. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-ships/releases/tag/v0.1.1) |
| [Solitaire](https://github.com/PrimitiveOS/kindle-primitive-solitaire) | Play draw-one or draw-three Klondike with touch controls and undo. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-solitaire/releases/tag/v0.1.1) |

#### Arcade games

| App on GitHub | What it does | Store version |
|---|---|---|
| [Cascade](https://github.com/PrimitiveOS/kindle-primitive-cascade) | Guide falling pieces, clear rows, and choose from three speeds. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-cascade/releases/tag/v0.1.1) |
| [Snake](https://github.com/PrimitiveOS/kindle-primitive-snake) | Choose a speed, steer a continuously moving snake, and collect food to grow. | [0.1.1](https://github.com/PrimitiveOS/kindle-primitive-snake/releases/tag/v0.1.1) |
| [Starship](https://github.com/PrimitiveOS/kindle-primitive-starship) | Steer in real time, dodge incoming fire, and defeat the flagship. | [0.1.2](https://github.com/PrimitiveOS/kindle-primitive-starship/releases/tag/v0.1.2) |

Primitive Terminal uses AGPL-3.0-only. The other current app releases use PolyForm Noncommercial 1.0.0.

See the [gameplay references](docs/gameplay-reference.md) for the original rules and Kindle controls.

Shared code: [kindle-primtitive-tools](https://github.com/PrimitiveOS/kindle-primtitive-tools) holds the on-screen
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
   page. [Latest Launcher release](https://github.com/PrimitiveOS/kindle-primitive-launcher/releases/latest)
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
| [Education and productivity research](docs/education-productivity-apps.md) | App designs, benchmarks, and Kindle controls. |
| [docs/store-architecture.md](docs/store-architecture.md) | Store design and requirements. |
| [docs/store-submit-app.md](docs/store-submit-app.md) | Developers: how to add an app to the store. |
| [docs/store-install-apps.md](docs/store-install-apps.md) | Kindle owners: how to install, update and remove apps. |
| [docs/store-migration-kindleforge.md](docs/store-migration-kindleforge.md) | KindleForge's 28 packages reviewed against our quality bar: KOReader as a reference, the rest rebuilt natively or left out. |
| [.agents/skills/](.agents/skills) | Shared skills for AI coding agents: `primitive-ui` (the design language), `kindle-device` (working on the device), `kindle-eink` (drawing to e-ink). Linked as `.claude/skills`. |

## For developers

The apps live side by side inside this repository's folder; this repository ignores them, and each keeps its own history:

```sh
git clone https://github.com/PrimitiveOS/kindle-primitive.git doannt-kindle
cd doannt-kindle
git clone --recurse-submodules https://github.com/PrimitiveOS/kindle-primitive-launcher.git doannt-kindle-launcher
git clone --recurse-submodules https://github.com/PrimitiveOS/kindle-primitive-browser.git doannt-kindle-browser
git clone --recurse-submodules https://github.com/PrimitiveOS/kindle-primitive-terminal.git doannt-kindle-terminal
git clone https://github.com/PrimitiveOS/kindle-primtitive-tools.git doannt-kindle-tools
```

Each app builds for the Kindle with `cargo zigbuild` (target `armv7-unknown-linux-musleabihf`) and has a desktop build that
renders its screens to PNG. New screens follow the `primitive-ui` skill. Every device build bumps the patch version, a new
phase bumps the minor, and release tags are never moved.

## Known exceptions to the app kit

Every app is built on the shared app kit (`primitive-app`): the same run loop, redraw on wake, theme, press feedback and
system swipe. These are the exceptions, tracked here until they move:

| App | Why it is not on the kit yet | Plan |
|---|---|---|
| Primitive Browser | It has its own run loop and page engine. Kept as it is for now. | Move to the kit after the next browser release. |

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

See [The apps](#the-apps) for current app licences. The first-party software in `scripts/`, `schema/scripts/`,
and the three JSON schemas in `schema/` use the [PolyForm Noncommercial License 1.0.0](LICENSE-CODE).
Project-owned documentation, skills, artwork, screenshots, and other non-code resources use
[CC BY-NC-SA 4.0](LICENSE). Third-party components and material have their own terms.

The [licensing audit](docs/licence-audit.md) records the terms in each app and release package.

Kindle is a trademark of Amazon.com, Inc. or its affiliates. PrimitiveOS is not affiliated with or endorsed by Amazon.
Jailbreaking and changing a Kindle's software is at your own risk.
