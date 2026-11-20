# System architecture: the launcher is the system layer

Status date: 2026-11-21. Status: agreed direction (owner, 2026-11-21). The phases that get there are in the
[system upgrade plan](system-upgrade-plan.md).

## 1. The rule

Primitive Launcher is the umbrella over every app. It is not an app that steps aside: it stays in charge of the
Kindle while any app is open. Apps run underneath it and draw their own content, but the system controls belong to
the launcher only:

- the power button, sleep and wake, and the lock screen (the sleep picture);
- the boot screen (the wait screen) and the Kindle's stock screensaver module;
- the quick settings panel (Wi-Fi, light, warmth, rotation, light and dark mode, and the rest);
- the system theme (light or dark mode);
- Wi-Fi, SSH, DNS, USB drive mode, and the Store.

An app never puts the Kindle to sleep, never loads or unloads the stock screensaver, and never draws its own quick
settings. An app can ask the launcher to open quick settings, and it follows the system theme.

## 2. Layers

```text
Kindle
  Linux kernel and drivers (Amazon's, unchanged)
  powerd, blanket, lipc (Amazon's system services; the stock framework is stopped)
  Supervisor (shell, runs the whole time)  ── starts and stops everything below, survives crashes
    System layer (Primitive Launcher)      ── always running: power, sleep, lock screen, quick settings, theme
      Home screen and Settings             ── shown when no app is in front
      App in front (Browser, Store, ...)   ── draws its content; gets the page buttons and touch
```

The supervisor is the process owner: it starts the system layer and the app, restarts them if they crash, and
gives the Kindle UI back when the user asks. The system layer is the policy owner: it decides what the buttons,
the sleep and the theme do.

## 3. Who owns what

| Thing | Owner | Apps |
|---|---|---|
| Power button, sleep, wake | System layer | Never handle it. Redraw when asked (§4.1). |
| Lock screen picture | System layer (the sleep wallpaper in Settings) | Never draw it. |
| Stock screensaver module (`com.lab126.blanket`) | System layer: unloaded while Primitive runs; loaded back only when the user picks the Kindle UI | Never touch it. |
| `preventScreenSaver` (powerd) | System layer: 0 at start | Never set it. |
| Boot screen | Supervisor and system layer | None. |
| Quick settings panel | System layer, as an overlay on top of the app | Can ask for it (§4.3). Never draw their own. |
| Theme (light or dark) | System layer (`dark_mode` in `launcher/settings.txt`) | Follow it for their chrome (§4.2). |
| Page buttons and touch | The app in front | Theirs, except the system gesture for quick settings. |
| App content options (for example the browser's Night mode for pages) | The app | Allowed, for content only. |

## 4. Contracts between the system layer and apps

### 4.1 Wake: redraw

When the Kindle wakes, the screen shows the lock picture until something draws. The supervisor sends `SIGUSR1` to
the app's process group, and the app redraws its whole screen.

An app declares support with a line in the first ten lines of its library entry:

```sh
# Wake: redraw
```

An app without the line is restarted on wake, so the screen is never left blank. Apps start in their own process
group so the signal reaches the app itself, not only its launch script.

### 4.2 Theme

The system theme is `dark_mode=on|off` in `launcher/settings.txt`. An app reads it when it starts, and again when it
gets `SIGUSR1` (the same signal as a wake redraw). Its chrome (bars, buttons, keyboard, menus) follows the theme. An app
may keep a content option, for example the browser's Night mode for web pages, but that option changes page content
only, never the chrome, and it is shown as a content option, not as dark mode.

App icons follow the theme too. Today an icon is drawn exactly as its PNG, in both themes, and the icon set has two
styles: some icons are a white tile, others a black tile (Store, Cards, Cascade, Chess, Crossword, Minesweeper,
Solitaire, Sudoku, Terminal). So the grid looks half light and half dark in either theme (checked on the Kindle,
2026-11-21, in both themes). The rule: every icon has a light form (white tile, black glyph) and a dark form (black
tile, white glyph), and the launcher draws the form that matches the theme. An app ships `icon.png` (light) and
`icon-dark.png` (dark); without a dark form the light one is used in both themes.

### 4.3 Quick settings from any app

The system gesture (the same swipe that opens quick settings on the home screen) belongs to the system layer in every
app. The system layer saves the screen, draws the panel over the app, and on close puts the saved screen back, so the
app does not need to redraw. Changes that affect the app (the theme, the rotation) end with a redraw signal (§4.1).

## 5. What is built today, and what is not

Built (launcher 0.6.0, on the Kindle once installed):

- The supervisor clears `preventScreenSaver` at start.
- Opening an app or the Store no longer hands the stock screensaver back. Only the Kindle UI does.
- While an app is open, the supervisor follows the power events: on sleep it draws the sleep picture
  (`kl-launcher --sleep-screen`), and on wake it sends the redraw signal or restarts the app (§4.1).

Not built yet (see the upgrade plan):

- The launcher still exits when an app opens, so the quick settings panel and the system gesture are not available
  inside apps. The supervisor covers sleep and wake meanwhile.
- No app supports `# Wake: redraw` yet, so apps are restarted on wake.
- Icons do not follow the theme: the bundled icon set mixes white and black tiles (§4.2).
- Apps do not follow the system theme yet. The browser keeps its own Night mode, and its chrome does not follow the
  launcher's theme.
