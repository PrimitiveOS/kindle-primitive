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
| App content options (text size, page width) | The app | Allowed. No app has its own light or dark switch under the launcher. |

## 4. Contracts between the system layer and apps

### 4.1 Wake: redraw

An app declares that it can draw its whole screen again on request with a line in the first ten lines of its library
entry. The line must match exactly, and the entry must be a plain file (not a link); the script ignores the signal
itself, as a shell ends on it otherwise ([contracts](contracts.md) §1.1):

```sh
# Wake: redraw
[ "${PRIMITIVE_LAUNCHER:-0}" = 1 ] && trap '' USR1
```

The request is `SIGUSR1` to the app's process group (apps start in their own group, so the signal reaches the app,
not only its script). While the launcher runs over the app (the normal case), it saves the app's screen when the sleep
picture or quick settings goes up and puts it back after, so on wake the app usually does not redraw. The launcher
sends the request only when the saved screen no longer fits or is missing: after a theme or rotation change while its
screen was up, when it could not save the screen, and after it starts again over the app following a crash. An app
without the line gets its saved screen back and keeps the old theme until it starts again; SIGUSR1 would end it, so
it is never sent.

When the launcher is not running over the app (the fallback), the supervisor keeps sleep and wake: it draws the sleep
picture, and on wake sends `SIGUSR1` to an app with the line and restarts an app without it, so the screen is never
left blank.

### 4.2 Theme

The system theme is `dark_mode=on|off` in `launcher/settings.txt`. An app reads it when it starts, and again when it
gets `SIGUSR1` (the same signal as a wake redraw). The whole app follows the theme: its chrome and its content (the
owner's decision, 2026-11-21: in dark mode the browser's pages are dark too). Under the launcher an app has no light
or dark switch of its own; the browser shows Day and Night only when it is opened from the Kindle library without
the launcher.

Switching the theme over an app costs two screen updates, not three. When the switch is made in quick settings over
an app that redraws, the launcher shows the app's saved screen inverted under the panel (dark mode is the screen
inverted), so the one full update shows the whole screen as it will be. When the panel closes, the launcher does not
put the old screen back: it resumes the app and sends the redraw signal, and the app draws itself in the new theme.
An app that cannot redraw gets its saved screen back and keeps the old theme until it starts again.

Only the theme switch itself flashes the screen. The app's redraw after it must not flash: a GC16 flash shows the
inverse of what is on the screen for a moment, and the inverse of the new theme is the old one. The app kit
(`Display::show_calm`) and the browser (`redraw_all_calm`) draw the whole screen with a non-flashing waveform for the
launcher's redraw request.

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
Every system pop-up over an app (quick settings, the power menu, confirmations) is drawn over the app's saved screen,
never over the home screen: the renderer takes the app's screen as the backdrop (`Renderer::set_backdrop`).

Opening and closing a pop-up over an app does not flash. When the launcher's display resumes over an app it keeps what
is on the panel as its last frame, so opening quick settings updates only the panel's box; putting the app's screen
back updates only the box that changed, with a non-flashing waveform. Only a change over most of the screen (the sleep
picture going on wake) gets one full update, as a calm update there leaves a ghost.

## 5. What is built today, and what is not

Built (launcher 0.6.0 and 0.6.x, browser 0.2.19 and later):

- The supervisor clears `preventScreenSaver` at start.
- Opening an app or the Store no longer hands the stock screensaver back. Only the Kindle UI does.
- The launcher stays running while an app is open (0.6.1): it owns the top-edge swipe and the power events over the
  app, freezes the app while quick settings or the sleep picture is up, and puts the app's screen back after.
- A launcher crash while an app is open starts the launcher again over the app (0.6.6), and Kindle UI from the power
  menu closes the app first. Kindle UI is in the power menu, not on the home screen (0.6.8).
- The browser follows the contracts: `# Wake: redraw`, the whole browser follows the theme under the launcher, and
  it leaves the top-edge swipe to the launcher.
- The app kit follows them for every app built on it (tools branch `feature/app-contracts`); the 2048 pilot and the
  app template declare `# Wake: redraw`.

Not built yet (see the upgrade plan):

- Icons do not follow the theme: the bundled icon set mixes white and black tiles (§4.2).
- The other apps declare `# Wake: redraw` only on their rollout branches, not in a release; Reader, Solitaire,
  Terminal and the Store need their own changes (see the upgrade plan, Phase 5).
- Under the launcher the kit still lets an app's own `dark_mode` setting or `preferred_dark_mode` override the system
  theme, and its redraw request does not read the rotation again.
