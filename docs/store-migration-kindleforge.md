# KindleForge's packages and Primitive Store: review and migration plan

Status date: 2026-11-19 (third review, after the owner's feedback). Status: decided; nothing to migrate. Belongs to
phase S6 of [kindle-platform-plan.md](kindle-platform-plan.md); builds on [store-architecture.md](store-architecture.md)
and [store-submit-app.md](store-submit-app.md).

Result: **no KindleForge package is migrated.** KOReader is listed in the store as a **reference** (a `link` listing to
KOReader's own site and releases; we package nothing). Every other package is removed, skipped or excluded. What people
expect from a store (notes, flashcards, a focus timer, word and puzzle games) comes from **native Primitive apps** that
we build (§5).

## 1. Starting point

| Fact | Source | Checked |
|---|---|---|
| KindleForge's catalog lists **28 packages** (`registry.json` at `kf.penguins184.xyz`). | the registry file | 2026-11-19 |
| `KindleTweaks/KindleForge` (GPL-3.0) and `KindleTweaks/Repository` (package scripts, CC BY-NC-SA 4.0) are **archived**. | GitHub repo pages | 2026-11-19 |
| Many packages are **Illusion apps**: HTML and ES5 JavaScript that the Kindle's own interface runs (the start script copies the app to `/var/local/mesquite/` and registers it in `/var/local/appreg.db`). Seen in KShips, KWordle, KNotes, KPomo, KAnki, Kreate. | the apps' scripts and READMEs | 2026-11-19 |
| Others are **GTK apps** drawn through the Kindle's X server (RAnki, kTerm, Gambatte-K2, KinAMP, LARKPlayer, Gnome Games), **terminal programs**, or **background services** with no interface. | READMEs | 2026-11-19 |

Primitive Launcher stops the Kindle's own interface to free memory and take the screen. Illusion apps need that
interface, so they are not expected to run under our launcher as they are. Whether GTK apps run with it stopped was
not checked: no GTK app is kept, so the question no longer matters for the store.

## 2. What the store accepts

The owner's bar, applied to every app, ours or not:

1. **A real interface for touch.** No terminal, no command line, no editing of configuration files to use it.
2. **Simple for everyone.** Usable by someone who has never jailbroken a device: one tap to start, clear words, a way
   back. Quality in the spirit of Apple's apps.
3. **Familiar.** A kind of app that is popular on iOS or Android: productivity tools, games, everyday tools. Niche tools
   for developers or tinkerers are not store apps.
4. **Works with Primitive Launcher**, the Kindle's own interface stopped.
5. **Licence and content** as before: the licence allows it (D3), and it passes the content review.

## 3. Review of all 28 packages

Verdicts: **Reference** (listed as a link, nothing packaged), **Rebuild** (not migrated; the kind of app is
wanted, so we build our own, §5), **Skip for now**, **Remove**, **Excluded**.

| # | Package | What it is | Built with | Licence | Verdict | Why |
|---|---|---|---|---|---|---|
| 1 | KOReader | E-book and document reader | Native (Lua, own UI) | AGPL-3.0 | **Reference** (owner) | The reader most jailbroken Kindles use, with a full interface, and it already starts from our launcher. The store links to KOReader's own site and releases; we do not repackage it. |
| 2 | RAnki | Anki flashcards with AnkiWeb sync | GTK2, WebKitGTK | GPL-3.0 | **Remove** (owner) | Below the owner's quality bar (beta, the author warns of data loss). Flashcards come from our own app, Primitive Cards (§5). |
| 3 | KWordle | Wordle | Illusion (HTML) | MIT | **Rebuild** | The game is wanted, but it needs the Kindle's own interface and its UI is basic. Its MIT word lists (9 languages) can seed our game, with credit. |
| 4 | KShips | Battleship | Illusion (HTML) | GPL-3.0 | **Rebuild** (later) | A classic; needs the Kindle's own interface; not updated lately. |
| 5 | KNotes | Notes and a kanban board | Illusion (HTML) | none | **Rebuild** | Notes are essential; this one needs the Kindle's own interface and has no licence. |
| 6 | KPomo | Pomodoro timer | Illusion (HTML) | none | **Rebuild** | A focus timer is wanted; same limits as KNotes. |
| 7 | KAnki | Flashcards from a config file | Illusion (HTML) | none | **Remove** | Decks are edited on another site and copied as a file; RAnki or our own app covers flashcards. |
| 8 | Kreate | Drawing | Illusion (HTML) | GPL-3.0 | **Remove** | Its author notes you cannot draw by dragging, only by taps. A drawing app may come later as our own. |
| 9 | Gnome Games Suite | Chess, Minesweeper | GTK (GNOME) | GPL-2.0 | **Remove** (owner) | The owner wants native games, not GNOME ports. Chess and Minesweeper are in §5. |
| 10 | Gambatte-K2 | Game Boy emulator | GTK2, FBInk | GPL-3.0 | **Remove** | Users must supply game ROMs; known freezes; not a mainstream app. |
| 11 | KindleCraft (bareiron) | Minecraft server | Server, no UI | GPL-3.0 | **Remove** | Runs a server for other computers; nothing to use on the Kindle. |
| 12 | Textadept | Text editor | Terminal or GTK | MIT | **Remove** (owner) | Not needed. |
| 13 | Wordgrinder | Word processor | Terminal (curses) | fork: none detected | **Skip for now** (owner) | Not designed for general users. |
| 14 | JarLauncher | Java runtime and app launcher | Terminal | none | **Skip for now** (owner) | Unclear that it can work; a developer tool. |
| 15 | Alpine Linux | Linux environment | Terminal, system | GPL-3.0 | **Remove** (owner) | Developer tool. |
| 16 | KinAMP | Music player | GTK | GPL-3.0 | **Remove** (owner) | — |
| 17 | LARKPlayer | Audiobook player | GTK | none | **Remove** | Same family as KinAMP; firmware below 5.19 only; Bluetooth audio models only; no licence. |
| 18 | SOX Media Player | Audio player | Terminal | unknown | **Remove** | No interface; forum download. |
| 19 | Gargoyle | Text adventure interpreter | GTK | unknown | **Remove** | Niche; forum download. |
| 20 | kTerm | Terminal emulator | GTK | GPL-3.0 | **Remove** | Primitive Terminal is our terminal. kTerm was needed only by Textadept, Wordgrinder, JarLauncher and KindleFetch, which are all out (M-D6 closed). |
| 21 | Kindle HID Passthrough | Bluetooth keyboards and gamepads | Background service | GPL-3.0 | **Remove** | No interface; its own README says another tool must map the buttons. Bluetooth keyboards may become a launcher feature (§5). |
| 22 | Kindle Button Mapper | Button mapping | Background service, config files | GPL-3.0 | **Remove** | No interface. |
| 23 | KPM | Package manager | Terminal | MIT | **Remove** | Primitive Store does this job. |
| 24 | KUAL (PEKI) | Menu of extensions | Kindle's own interface | KindleTweaks terms | **Remove** | Primitive Launcher already shows KUAL extensions behind its Extensions tile. |
| 25 | HotfixUpdater | Jailbreak hotfix updater | Scriptlet | CC BY-NC-SA 4.0 | **Remove** from the store | Jailbreak upkeep, not an app. The install guide links the KindleModding wiki for the hotfix. |
| 26 | UpdateBlock Status | Checks that updates are blocked | Scriptlet | unknown | **Remove** | Jailbreak upkeep; could become a line in the launcher's Settings › About (§5). |
| 27 | Toggle ADs | Turns off the ads | Scriptlet | unknown | **Remove** | A jailbreak tweak; risk with Amazon's terms (was M-D3). |
| 28 | KindleFetch | Book downloader (Anna's Archive) | Terminal | MIT | **Excluded** | Content: it downloads copyrighted books without permission (M-D1). |

Totals: **1 reference** (KOReader), **4 rebuild** as our own (with Chess, Minesweeper, Crossword and Blocks added, §5), **2 skipped for now**, **20 removed**, **1 excluded**.

## 4. KOReader as a reference listing

KOReader is listed, not migrated (owner, 2026-11-19). Its listing in the catalog:

- `source: "link"`, category `reading`, developer "KOReader contributors", licence AGPL-3.0, links to
  `https://koreader.rocks/` and `https://github.com/koreader/koreader/releases`.
- The app page explains how to install it by hand and that Primitive Launcher shows it on the grid once it is installed
  (the launcher already finds `KOReader.sh` and starts it through its wrapper, so leaving KOReader returns to the
  launcher).
- No package repository, no re-hosting, no install button. Featured in Today › Start here as the reader to pair with the
  launcher.

No package repositories are needed for this migration. If an outside app later meets the bar in §2 and its author agrees,
the repackage approach (type B in store-architecture §4.5) can be used then.

## 5. What we build ourselves instead

The kinds of apps people expect from a phone's store, made native for e-ink with the `primitive-ui` skill. Each is its
own repository and its own small project. Names and first scopes are proposals; the owner chooses which and in what
order (M-D7).

**Productivity**

| App | Like | First scope | Replaces |
|---|---|---|---|
| Primitive Notes | Apple Notes, Google Keep | A list of notes, writing with the shared keyboard, search, pin, delete with Undo. Plain text files in `/mnt/us/notes/`, so they can be copied over USB. | KNotes |
| Primitive Focus | the Clock app's timer, Pomodoro apps | Focus and break timer with presets (25/5, 50/10), a large calm countdown refreshed once a minute, the screen kept awake while it runs. | KPomo |
| Primitive Cards | AnkiMobile, Quizlet | Flashcard decks with spaced repetition, import of Anki decks, review on large cards. | KAnki, RAnki |
| Primitive Calculator | Calculator | A standard calculator with history. | — |

**Games** (turn-based, which e-ink suits)

| App | Like | Replaces |
|---|---|---|
| Primitive Words | Wordle | KWordle (its MIT word lists reused, credited) |
| Primitive Sudoku | Sudoku apps | — |
| Primitive Chess | Chess against the device | Gnome Chess |
| Primitive Minesweeper | Minesweeper | Gnome Mines |
| Primitive Solitaire | Klondike solitaire | — |
| Primitive Ships | Battleship | KShips |
| Primitive Crossword | NYT Crossword, crossword apps | `crossword.koplugin` (KOReader plugin, on Awesome-Kindle) |
| Primitive Blocks | 1010!, Woodoku (turn-based block puzzles) | — |
| Falling-blocks game (name to choose) | Tetris | Tetris (terminal, on Awesome-Kindle) |

Also seen on Awesome-Kindle, not in KindleForge's catalog: **IllusionChess** (an Illusion app, so it needs the Kindle's own
interface; Primitive Chess replaces it), **Tetris** (runs in a terminal) and **Crossword** (a KOReader plugin, so only
inside KOReader).

Not built, with reasons:

- **Tetris** (not migrated; **built as our own falling-blocks game**, owner's decision 2026-11-19): it gets its own name
  and look, since "Tetris" is The Tetris Company's trademark and clones that copy its look have lost in court, and its
  speed follows what e-ink can show (a device spike first). See implementation plan F13. Primitive Blocks (turn-based)
  stays as well.
- **KindleCraft (bareiron).** It is a Minecraft server: people join it from a computer, and the Kindle shows nothing. The
  name also leans on Minecraft's trademark.
- **Crossword puzzles from newspapers** are copyrighted. Primitive Crossword ships free or self-made puzzles and opens
  standard `.puz` files the user already has.

**Everyday tools as launcher features** (not separate apps)

- Bluetooth keyboard pairing in Settings, on models with Bluetooth (replaces HID Passthrough for typing).
- Settings › About: jailbreak status (hotfix present, updates blocked), replacing UpdateBlock Status.
- Wi-Fi file transfer: send books and files from a phone or computer to the Kindle on the same network.

## 6. Steps

- [ ] The KOReader reference listing in the catalog, once the catalog exists (platform plan S3).
- [ ] The native apps the owner picks from §5, each its own project with its own gate on the Kindle.

## 7. Decisions

- **M-D1 — KindleFetch**: excluded (content), and it fails the quality bar as well.
- **M-D2 — Package repos**: none needed; KOReader is a reference listing.
- **M-D3 — Toggle ADs**: removed.
- **M-D4 — KUAL**: removed (the launcher shows KUAL extensions itself).
- **M-D5 — RAnki**: removed (owner); Primitive Cards instead.
- **M-D6 — kTerm**: removed; no remaining app needs it.
- **M-D7 — Which native apps first** (§5): the owner's choice. A suggested first set: Notes, Focus, Words.
