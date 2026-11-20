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

- [ ] Find why the launcher's icons show dark while the theme is light (device check of `settings.txt` and the
  drawn screen).
- [ ] Theme contract (§4.2): apps read `dark_mode` from `launcher/settings.txt` at start and on `SIGUSR1`.
- [ ] Browser: chrome follows the system theme; Night stays a page-content option, renamed so it is not confused
  with dark mode. Browser release.
- [ ] Device check: switch the theme in launcher Settings, open the browser, both match.

## Phase 3: the launcher stays running (the system layer)

- [ ] The launcher no longer exits when an app opens. The supervisor starts the app as a child of the session and the
  launcher keeps running in a system mode: power, sleep, wake, the lock screen, and the system gesture. Memory budget on
  the Oasis 3: measure the launcher's resident size in system mode first; the browser uses about 40 MB.
- [ ] Input routing: the launcher reads the power button and watches touch for the system gesture only; the app keeps
  the page buttons and every other touch.
- [ ] The supervisor's Phase 1 power watch moves into the launcher (one owner for sleep and wake).
- [ ] Crash safety: if the system layer crashes, the supervisor restarts it without stopping the app.
- [ ] Device check: open an app, sleep and wake from the power button, the lock picture is right, the app comes back.

## Phase 4: quick settings from every app

- [ ] The system gesture opens quick settings over the app: save the screen, draw the panel, put the screen back on
  close (§4.3).
- [ ] Theme and rotation changes from the panel end with the redraw signal.
- [ ] Device check in the browser and the Store: open, change the light and the theme, close, the app is intact.

## Phase 5: apps follow the contracts

- [ ] Every Primitive app supports `# Wake: redraw` and the theme contract.
- [ ] Apps drop their own sleep, screensaver and quick settings code.
- [ ] [Contracts](contracts.md) §1 gains the `Wake: redraw` header; the store's checks require it for new apps.
- [ ] Releases of each app.

## Risks

- Memory: a resident launcher competes with apps for RAM on the Oasis 3. Measure before Phase 3.
- Two drawers on one screen: only one process may draw at a time. The system layer draws only while the panel or the
  lock picture is up, and the app is told to redraw (or the saved screen is put back) afterwards.
- Input: the system gesture must not steal an app's own swipes. Use a reserved edge, the same as on the home screen.
