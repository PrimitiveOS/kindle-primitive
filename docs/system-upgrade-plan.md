# System upgrade plan: making the launcher the system layer

Status date: 2026-11-21. Design: [system architecture](system-architecture.md). Each phase ends with a device check
on the Kindle Oasis 3 with the owner present.

## Phase 1: the supervisor keeps sleep and wake (launcher 0.6.0)

- [x] Clear `preventScreenSaver` at supervisor start.
- [x] Opening an app or the Store keeps the launcher's sleep picture (no stock screensaver hand-back).
- [x] Sleep picture while an app is open (`kl-launcher --sleep-screen`).
- [x] Wake: redraw signal for apps with `# Wake: redraw`, restart for the others.
- [x] Apps start in their own process group (`setsid`).
- [x] Device check: in the browser, the power button sleeps and the lock screen is the sleep wallpaper; wake brings
  the browser back (restarted, until it supports the signal). Passed on the Kindle, 2026-11-21 (launcher 0.6.2,
  browser 0.2.20).

## Phase 2: one theme

- [x] Find why the icons look dark in light mode: the icon artwork. Nine bundled icons are black tiles and the rest
  white tiles, and icons are drawn as-is in both themes (screen captures in both themes, 2026-11-21).
- [x] Icon forms: a light and a dark form for every bundled icon (design first, the owner approves the set), and the Done 2026-11-21: the owner approved the set; the launcher picks the form for the theme.
  launcher picks the form for the theme (`icon.png`, `icon-dark.png`).
- [x] Theme contract (§4.2): apps read `dark_mode` from `launcher/settings.txt` at start and on `SIGUSR1` (browser
  `be41f3b`).
- [x] Browser: under the launcher the whole browser (bars and pages) follows dark mode, and the Display sheet has
  no Day and Night; standalone, Night works as before (owner's choice; browser `016fdc0`).
- [x] Theme switch over an app: two updates, not three (the app shown inverted under the panel at the switch; no
  old-screen restore before the app redraws).
- [x] Browser release (owner's go-ahead). Done: its theme commits are in v0.2.21.
- [x] Device check: switch the theme in launcher Settings, open the browser, both match. Passed from quick settings over the browser,
  2026-11-21.

## Phase 3: the launcher stays running (the system layer)

- [x] The launcher no longer exits when an app opens (launcher 0.6.1, `ac5fa1b`): it sends SIGUSR1 to the
  supervisor, which runs the app while the launcher keeps running with its drawing paused. A trapped USR1 interrupts
  the supervisor's `wait` on the Kindle's busybox shell (tested).
- [x] Memory: the launcher uses about 22 MB while the browser (about 43 MB) runs (measured on the Kindle,
  2026-11-21).
- [x] Input routing: over an app the launcher acts only on the top-edge swipe and the power events; the app keeps the
  page buttons and every other touch.
- [x] The supervisor's Phase 1 power watch runs only when the launcher does not stay (one owner for sleep and wake).
- [x] Crash safety (launcher 0.6.6 and 0.6.7): the supervisor starts the launcher in a wrapper that reports its end
  (USR2). A crash while an app runs resumes the app (it may be frozen under quick settings), asks it to redraw, and
  starts the launcher again with `KL_ATTACH_APP=1`, following the app without drawing over it. Too many crashes leave
  sleep and wake to the supervisor until the app ends. Checked in both supervisor loops (the wait for the app, and
  the storage watch of an app with a storage lease). Device check passed in 2048, 2026-11-21: a crash with 2048 in
  front, and a crash with quick settings open over it.
- [x] Kindle UI over an app (0.6.6, 0.6.9): the supervisor closes the app before the Kindle UI starts, and the
  "Opening the Kindle UI" dialog is drawn on a plain page.
- [x] Device check: open an app, sleep and wake from the power button, the lock picture is right, the app comes back. Passed in the browser, 2026-11-21.

## Phase 4: quick settings from every app

- [x] The system gesture opens quick settings over the app: the app is frozen (SIGSTOP to its group), touch is taken
  (EVIOCGRAB), the screen saved, the panel drawn over the app's picture; back at Home the screen is put back, touch
  released and the app resumed (launcher 0.6.1).
- [x] A theme change from the panel ends with the redraw signal, for apps that declare `# Wake: redraw`.
- [x] Settings from the panel over an app: it opens full screen; check it returns to the app. Done 2026-11-21: the owner confirmed it returns to the app.
- [x] Power from the panel over an app: the power menu (Cancel, Kindle UI, Restart, Power off; launcher 0.6.8) is
  drawn over the app's screen; Cancel returns to the app.
- [x] Quick settings opens and closes over an app without a full flash (launcher 0.6.5); the app's redraw after a
  theme switch does not flash (kit `7cdc39b`, browser 0.2.21). Device check passed in the browser and 2048.
- [x] Device check in the browser: light, Airplane, Power then Cancel, and the theme from quick settings; the browser
  stays behind the panel and comes back intact (2026-11-21, launcher 0.6.2, browser 0.2.20).
- [x] Device check in the Store (it does not declare `# Wake: redraw` yet). Done 2026-11-21: the owner confirmed the Store 0.1.9 check (it declares `# Wake: redraw`).

## Phase 5: apps follow the contracts

- [x] Primitive Browser supports `# Wake: redraw` and the theme contract, and leaves the top-edge swipe to the
  launcher (`be41f3b`).
- [x] Pilot: 2048 on the app kit branch (`feature/app-contracts`): wake, theme and quick settings pass on the Kindle.
- [x] Every other Primitive app supports `# Wake: redraw` and the theme contract. Done: all 30 kit apps, the Terminal, the Store and the Reader declare it, and handle USR1.
- [x] Apps drop their own sleep, screensaver and quick settings code. Done: a search of the app repos finds no power, screensaver or quick-settings code.
- [x] [Contracts](contracts.md) §1 gains the `Wake: redraw` header (`a660aa8`).
- [x] The Store's checks require it for new apps. Done: the catalog check requires it for apps listed after 2026-11-21.
- [x] Kit: under the launcher, ignore an app's own `dark_mode` and `preferred_dark_mode`, and read the rotation again Done: the kit ignores an app's own dark mode under the launcher, and re-reads the rotation on the redraw request when auto-rotation is off.
  on the redraw request.
- [x] Docs and sample code: the app template, the browser docs, the kit's module docs and the skills describe the
  contracts (2026-11-21).
- [x] Releases of each app. Done: the Reader 0.1.4 is released; the other apps are released, or have only README and CI changes since their tag.

## Risks

- Memory: a resident launcher competes with apps for RAM on the Oasis 3. Measure before Phase 3.
- Two drawers on one screen: only one process may draw at a time. The system layer draws only while the panel or the
  lock picture is up, and the app is told to redraw (or the saved screen is put back) afterwards.
- Input: the system gesture must not steal an app's own swipes. Use a reserved edge, the same as on the home screen.
