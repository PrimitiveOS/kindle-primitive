# System upgrade plan: making the launcher the system layer

Status date: 2026-11-21. Design: [system architecture](system-architecture.md). Each phase ends with a device check
on the Kindle Oasis 3 with the owner present.

## Phase 1: the supervisor keeps sleep and wake (launcher 0.6.0)

- [x] Clear `preventScreenSaver` at supervisor start.
- [x] Opening an app or the Store keeps the launcher's sleep picture (no stock screensaver hand-back).
- [x] Sleep picture while an app is open (`kl-launcher --sleep-screen`).
- [x] Wake: redraw signal for apps with `# Wake: redraw`, restart for the others.
- [x] Apps start in their own process group (`setsid`).
- [ ] Device check: in the browser, the power button sleeps and the lock screen is the sleep wallpaper; wake brings
  the browser back (restarted, until it supports the signal).

## Phase 2: one theme

- [x] Find why the icons look dark in light mode: the icon artwork. Nine bundled icons are black tiles and the rest
  white tiles, and icons are drawn as-is in both themes (screen captures in both themes, 2026-11-21).
- [ ] Icon forms: a light and a dark form for every bundled icon (design first, the owner approves the set), and the
  launcher picks the form for the theme (`icon.png`, `icon-dark.png`).
- [x] Theme contract (§4.2): apps read `dark_mode` from `launcher/settings.txt` at start and on `SIGUSR1` (browser
  `be41f3b`).
- [x] Browser: under the launcher the bars follow the system theme and Night darkens the page only; standalone,
  Night darkens everything as before (browser `be41f3b`).
- [ ] Browser: rename Night (for example "Dark pages") so it is not confused with dark mode (owner to choose the
  word).
- [ ] Browser release (owner's go-ahead).
- [ ] Device check: switch the theme in launcher Settings, open the browser, both match.

## Phase 3: the launcher stays running (the system layer)

- [x] The launcher no longer exits when an app opens (launcher 0.6.1, `ac5fa1b`): it sends SIGUSR1 to the
  supervisor, which runs the app while the launcher keeps running with its drawing paused. A trapped USR1 interrupts
  the supervisor's `wait` on the Kindle's busybox shell (tested).
- [ ] Memory: measure the launcher's resident size while an app runs (the browser uses about 40 MB).
- [x] Input routing: over an app the launcher acts only on the top-edge swipe and the power events; the app keeps the
  page buttons and every other touch.
- [x] The supervisor's Phase 1 power watch runs only when the launcher does not stay (one owner for sleep and wake).
- [ ] Crash safety: if the system layer crashes, the supervisor restarts it without stopping the app.
- [ ] Device check: open an app, sleep and wake from the power button, the lock picture is right, the app comes back.

## Phase 4: quick settings from every app

- [x] The system gesture opens quick settings over the app: the app is frozen (SIGSTOP to its group), touch is taken
  (EVIOCGRAB), the screen saved, the panel drawn over the app's picture; back at Home the screen is put back, touch
  released and the app resumed (launcher 0.6.1).
- [x] A theme change from the panel ends with the redraw signal, for apps that declare `# Wake: redraw`.
- [ ] Settings and Power from the panel over an app: they open full screen; check they return to the app.
- [ ] Device check in the browser and the Store: open, change the light and the theme, close, the app is intact.

## Phase 5: apps follow the contracts

- [x] Primitive Browser supports `# Wake: redraw` and the theme contract, and leaves the top-edge swipe to the
  launcher (`be41f3b`).
- [ ] Every other Primitive app supports `# Wake: redraw` and the theme contract.
- [ ] Apps drop their own sleep, screensaver and quick settings code.
- [ ] [Contracts](contracts.md) §1 gains the `Wake: redraw` header; the store's checks require it for new apps.
- [ ] Releases of each app.

## Risks

- Memory: a resident launcher competes with apps for RAM on the Oasis 3. Measure before Phase 3.
- Two drawers on one screen: only one process may draw at a time. The system layer draws only while the panel or the
  lock picture is up, and the app is told to redraw (or the saved screen is put back) afterwards.
- Input: the system gesture must not steal an app's own swipes. Use a reserved edge, the same as on the home screen.
