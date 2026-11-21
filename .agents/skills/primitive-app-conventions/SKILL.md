---
name: primitive-app-conventions
description: Use when writing or reviewing a PrimitiveOS Kindle app (a new app, a change to an existing one, or a review before release). Sets the coding standard: build on the app kit (primitive-app and primitive-ui) instead of device code, the tap-feedback rule (every tappable control reverses black and white while it is held), dark mode and the system layer left to the kit, crate layout, tests, icons, versions and the changelog.
metadata:
  type: reference
---

# PrimitiveOS app conventions

Every native app is built on the **app kit** (`primitive-app`, `primitive-ui`) from the tools repo, and follows the look of Primitive Launcher (`primitive-ui` skill). The app template (`kindle-primitive-app-template`) is the starting point: copy it, then change the names. Primitive Browser is the one known exception (umbrella README, "Known exceptions to the app kit"); new apps do not copy it.

## 1. Build on the kit, not on the device

- The app implements the kit's `App` trait and is started with `primitive_app::run(app, &dir)`. The kit owns the e-ink screen, touch, the page buttons, rotation, sleep and wake, the USB drive mode, storage, the system layer and the theme. **An app has no device code**: no framebuffer, no `/dev/input`, no accelerometer, no `lipc`, no power or sleep calls, no SIGUSR1 handler, no lock screen, no quick settings, no dark-mode switch of its own.
- Draw with the kit's `Canvas` (`primitive_ui`): `header(canvas, title, exit)`, `screen_rect(width, x, y, w, h)` for layout (the 1264 × 1680 reference, scaled), `TITLE`, `BODY`, `CAPTION` text styles, `canvas.text`, `canvas.button`, `canvas.key`, `canvas.keyboard(layer, go_label, None)`, `canvas.card`, `canvas.panel`, `canvas.fill`, `canvas.icon`, `canvas.popup`, and the widgets `Rows`/`Row`, `TabBar`, `Sheet`, `Pager`, `switch`, `progress`, `full_screen_message`. Reuse them before writing a new one.
- Keep the layers separate in the crates:
  - `<app>-core`: the state and the rules. No drawing, no device, no files outside the app's own folder.
  - `<app>-render`: `App` drawing and the tap mapping (`input`, `swipe`). Draws only through `Canvas`.
  - `<app>-kindle`: the library entry point (`primitive_app::run`).
  - `<app>-desktop`: a driver that runs the same `App` on the Mac through `Lifecycle` and `frame`, for screenshots and tests.
- The library entry script (`deploy/<Name>.sh`) has `# Wake: redraw` in its first ten lines and `[ "${PRIMITIVE_LAUNCHER:-0}" = 1 ] && trap '' USR1` before the app starts. Without them the app ends on the launcher's redraw signal.

## 2. Tap feedback: every tappable control reverses (required)

The standard: when a control is tapped, it turns **black while it is white, and white while it is black**, for as long as the finger is on it. Not gray. The kit does this for its own controls automatically (`header`, `button`, `key`, `keyboard`, `Rows`, `TabBar`, `Sheet`, `Pager`), because they register themselves as tap targets while they are drawn.

For a control you draw yourself:

1. Register it while drawing: `let pressed = canvas.control_pressed(rect, false);`. The rectangle you register is the tap target: it must be the same rectangle the input code hit-tests (`rect.contains(x, y)`).
2. Draw the pressed state in black and white: a black fill with white ink when pressed, a white fill with black ink otherwise. Text, icons, carets and check marks inside it change ink too.
3. For a toggle (a check box, a switch, a selected card), invert the state rather than the look: `let on = state != pressed;`. A checked box then turns white while it is held, and an empty one turns black.
4. Never use a gray for the pressed state (`226`, `224`, `220`, `211`, `85` as a fill). Those are the old look, and the audit of 2026-11-21 found and removed them in ten apps.
5. A control that does nothing when tapped (disabled, or already the current choice with no action) does not need a reversal. A control that does something must reverse.
6. Taps on text, empty space or decoration are not controls: do not register them.

Check it: the kit's pattern (`primitive-ui` and the Terminal's `kt-render` test) draws the screen once, calls `canvas.press_at(x, y)` on the control's point, draws again, and asserts that only pixels inside the control's rectangle changed. Add one such test per new control. Also look at the pressed frame in the desktop driver (`lifecycle.press_feedback`).

## 3. Dark mode and the theme

- The kit draws the page in the system's theme: never invert colours yourself, and never write a light/dark switch into the app. An app's own `settings.txt` `dark_mode` is ignored under the Launcher.
- Pictures (photos, book pages, icons) keep their own shades: the kit inverts only what you draw with the ink values.
- Icons come as two files in `assets/icons/apps/`: `<name>.png` (black glyph on a white tile, 256 px) and `<name>-dark.png` (white glyph on black). Make the light file, then run `python3 -I scripts/icon-forms.py <dir>`, which makes the dark file and checks the pair. A test in the launcher checks that every bundled icon has both forms.

## 4. State, storage and the lifecycle

- Save the app's data with `primitive_app::save` (it runs under the USB lease) and save at sleep and exit (`App::save`). The kit calls `save` for you at those times.
- Keep the app's files in its own folder (`/mnt/us/<dir>/`). Do not write outside it.
- Long work (a network call, a big file) must not block the event loop for long: use `App::tick` and `App::deadline` to pick it up in steps.
- Never start or stop the Kindle's framework, the stock screensaver or the Kindle UI from an app. The Launcher owns them.

## 5. Tests, the desktop driver and the drawing checks

- `cargo test --workspace --locked`. Drawing tests need the Noto Sans fonts: set `KL_TEST_FONTS` to the launcher's `assets/fonts` and let the test skip without it (the Terminal and the kit do this).
- Every new screen gets a desktop screenshot in its `<app>-desktop` driver, and each changed control gets a pressed-frame check (section 2).
- Clippy: write code that passes `cargo clippy --workspace --all-targets -- -D warnings`. It is a CI check for the Terminal and the Launcher, and it is good practice everywhere.

## 6. Versions, changelog, README

- The version is the Cargo version (`[workspace.package]`). Each release bumps the patch (or the minor for a new phase) and has a `## <version>` entry at the top of `CHANGELOG.md`, one line per user-visible change. Tags are `v<version>` and never move.
- The README follows the umbrella's standard header (logo, title, one-line summary, the badges in order: CI, release, tag, licence, stars, Store downloads, then the links row), a status table with the tested Kindle, and the current version. The template shows it.
- The licence file is the one the repo states (`PolyForm-Noncommercial-1.0.0` for first-party apps unless the repo says otherwise).

## 7. Store listing

Each release gets a listing in the catalog (`apps/primitive-<name>/app.json`), see the `kindle-release-pipeline` skill, section 6. Set `changes` honestly: `network`, `stops_kindle_ui`, `starts_at_boot`, `root_filesystem`, `hooks`. `tested_on` is the models the app was really run on.

## 8. Review checklist (before a release)

- [ ] No device code in the app; the kit provides the screen, input, sleep, theme and storage.
- [ ] Every tappable control registers and reverses black and white (no gray pressed state); toggles reverse by state.
- [ ] Each changed control has a pressed-frame test.
- [ ] No own light or dark switch; icons have a light and a dark file.
- [ ] Library entry has `# Wake: redraw` and the USR1 trap.
- [ ] Tests pass with `KL_TEST_FONTS`; clippy is clean for the repos that run it.
- [ ] Version, changelog, README header and status are updated.
- [ ] Tools pin is the commit you tested with.
