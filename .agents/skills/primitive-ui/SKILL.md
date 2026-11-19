---
name: primitive-ui
description: Use when designing, building or reviewing any PrimitiveOS app on a Kindle (Launcher, Browser, Terminal, Store, or a new app). Defines the PrimitiveOS design language (Apple's Liquid Glass adapted to e-ink), its tokens (canvas, grays, type, radii, sizes), its components (status bar, icon grid, settings cards and rows, switches, buttons, pop-ups, quick settings, keyboard, icons), interaction and e-ink refresh rules, dark mode, wording, and a review checklist.
metadata:
  type: reference
---

# Primitive UI for PrimitiveOS

The reference implementation is Primitive Launcher (`doannt-kindle-launcher`): its home grid, Settings, and quick
settings are the look every app follows. The values below are taken from its code (`crates/kl-core/src/layout.rs`,
`crates/kl-render/src/lib.rs`) and from the shared crates in `doannt-kindle-tools` (`primitive-keyboard`,
`primitive-quick`). When the launcher changes a value, change it here too.

For how pixels reach the panel (waveforms, flashing, the update ioctl), read the `kindle-eink` skill. This skill is
about what to draw.

## 1. Principles: Liquid Glass on e-ink

Apple's Liquid Glass (iOS 26) is built on translucent layers, concentric shapes, controls that float above content, and
capsule-shaped buttons. E-ink has no colour, no translucency, and no smooth motion, so each idea is translated:

| Liquid Glass idea | PrimitiveOS on e-ink |
|---|---|
| Content first; chrome recedes | A thin status bar; no dock; controls grouped in cards and sheets, not spread over the screen. |
| Glass layers float over content | Pop-ups and sheets sit **over** the screen they came from, with a 6 px black border and a 10 px **white halo** that separates them from what is underneath. The screen behind stays visible. Never a full-screen page for a small question. |
| Concentric shapes | Every rounded shape inside another keeps the same centre of curvature: inner radius = outer radius − border width (`rounded_frame` does this). App icons are rounded squares with a radius of **22.5 % of their width**. |
| Capsules and circles for controls | Switches are pills (radius = half the height). Quick toggles are circles. Buttons are rounded rectangles (16 px). |
| Hierarchy without colour | Weight and size carry the hierarchy: bold black titles, regular gray secondary text. Two grays for text, no more. |
| Fluid motion | One-shot motion only: the optional opening zoom from an icon. Feedback is a pressed state on the touched element alone. |
| One system across apps | Same status bar, keyboard, quick settings icons and wording in every app, through the shared crates. |

Two rules that come from e-ink, not from Apple:

- **Draw only what changed.** Small changes refresh a rectangle; a new screen refreshes the whole panel once (§6).
- **Black and white first.** Every element must read in pure black and white. Grays are for secondary text, hairlines and
  idle states only.

## 2. Canvas

- Reference screen: **1264 × 1680 px, portrait**, 300 ppi (Kindle Oasis 3). The store serves every jailbroken Kindle, so
  lay out in proportion: compute sizes from the screen width (`size × width / 1264`) and keep the grid, margins and
  touch targets in the same ratios. Test on the smallest screen an app claims to support.
- Margins: **40 px** at the sides. Status bar: **120 px** high. Footer (page dots, Previous/Next): **90 px**.
- The screen turns with the Kindle (upright or upside down, read from the accelerometer). Apps follow the turn; there is
  **no turn button**. Landscape is not supported.

## 3. Tokens

### 3.1 Grays (0 = black, 255 = white)

| Value | Use |
|---|---|
| `0` | Ink: text, borders, filled buttons, "on" controls. |
| `0x11` (17) | Keyboard key text and the fill of a key that is on. |
| `60` | Section headers above cards. |
| `85` | Secondary text: a row's value, explanations in pop-ups. |
| `187` | Unlit parts of an indicator (Wi-Fi arcs above the signal). |
| `200` | Hairlines between rows in a card. |
| `0xbd` (189) | Key outlines. |
| `0xe2` (226) | The line above the keyboard. |
| `0xf7` (247) | Key fill. |
| `255` | Paper: backgrounds, the inside of cards and pop-ups, the halo. |

No gradients and no dithering in the interface. Dithering is for pictures only (icons from PNG, sleep pictures).

### 3.2 Type

Noto Sans, Regular and Bold (`assets/fonts`, shipped in each app's package). Sizes in px at the reference width:

| Size | Weight | Gray | Use |
|---|---|---|---|
| 64 | Bold | 0 | Page title ("Settings"). |
| 56 | Bold | 0 | Detail title (a network's name, "Password"). |
| 50 | Bold | 0 | Pop-up title ("Power", "Open the Kindle UI?"). |
| 48 | Bold | 0 | List heading (Extensions). |
| 38 | Bold | 0 | Row title in a card. |
| 36 | Bold / Regular | 0 | Button label (bold); pop-up body (regular). |
| 30 | Regular | 0 / 85 | Icon label on the grid; pop-up explanation (gray 85). |
| 28 | Regular | 85 | A row's value under its title. |
| 26 | Bold | 60 | Section header above a card. |
| 24 | Regular | 0 | Small print. |

Text wraps to its box and is cut with "…" after its line limit. Sentence case everywhere ("Power off", "Restart the
launcher"), except where the owner chose otherwise ("Powered Off").

### 3.3 Radii and borders

| Element | Radius | Border |
|---|---|---|
| App icon (rounded square) | 22.5 % of its width | 4 px (drawn icons) |
| Pop-up and sheet | 28 px | 6 px, plus a 10 px white halo |
| Card (grouped list) | 22 px | 2 px |
| Button | 16 px | 4 px |
| Keyboard key | 12 px | 1 px, gray `0xbd` |
| Progress and level bars | 13 px | 2 px |
| Switch | half its height (pill) | 3 px when off |
| Quick toggle | circle | 4 px when off |

### 3.4 Sizes

| Element | Size |
|---|---|
| Grid | 4 columns × 5 rows by default (3–5 × 3–6 allowed); icons up to 184 px; label 30 px, 12 px under the icon. |
| Quick toggle | 100 px circle; up to 7 in a row. |
| Quick settings level | 24 steps, with − and + buttons at the ends. |
| Switch | 112 × 64 px, 40 px from the row's right edge. |
| Button | 100 px high. |
| Row in a card | 120 px (130 on the Settings home, 104 for a Wi-Fi network). |
| Section header | 56 px band; 24 px gap between sections. |
| Pop-up menu | 600 px wide, rows of 100 px. |
| Keyboard area | 730 px at the bottom; keys up to 124 px high, 8 px apart. |
| Icon glyph | 24-unit SVG grid, strokes 2 units wide, drawn at 40 px in rows. |

**Touch targets**: at least 100 px (about 8.5 mm) in both directions. Small controls get a larger hit area than their
drawing (the launcher grows button hit areas by 12 px on each side).

## 4. Components

Use the shared crates first. Copy from the launcher when a component is not shared yet, and move it into
`doannt-kindle-tools` when a second app needs it.

- **Status bar** (120 px): clock (52 px bold) and date on the left; on the right the indicators (SSH, a running job),
  Wi-Fi (three arcs, or a slash when off), and the battery (with a bolt when charging). The same order in every app.
- **Home grid**: rounded-square icons of one size, the name under each, pages of 20 with dots in the footer. No dock.
  Tap darkens only the touched icon. Long press opens a menu **beside** the icon (move, change icon, hide).
- **Settings**: a page title (64 px) with a filled **Done** button at the top right. Rows are grouped in **cards** under
  small section headers. A row has a bold title, a gray value under it, and a **›** chevron when it opens a page, or a
  switch when it toggles. Hairlines (gray 200, 2 px) separate rows inside a card, indented 32 px.
- **Switch**: on = black pill with a white knob on the right; off = outlined pill with a black knob on the left.
- **Buttons**: primary = black fill with white bold text; secondary = white with a black border. In a row of buttons,
  the safe choice (Cancel) is on the left and outlined; the actions are on the right and filled.
- **Pop-up**: centred box over the current screen; title (50 px bold), explanation (30–36 px), buttons at the bottom.
  Tapping outside the box is the same as Cancel. Destructive or system actions (Power off, Restart, Remove) always go
  through a pop-up.
- **Quick settings**: a sheet pulled down from the status bar. Header like the status bar; a row of round toggles with
  labels under them (Airplane, Auto-rotate, Dark mode, Animation, SSH, Settings, Power); Brightness and Warmth levels
  with − and +; a System section (CPU, memory, storage) with an icon, a bar and the value; a handle with "Swipe up to
  close". On = black circle with a white glyph; off = outlined circle with a black glyph.
- **Lists** (Wi-Fi networks, extensions, store apps): rows of 104–120 px in a card, with Previous and Next in the footer
  when they do not fit. A lock glyph marks a secured network; a chevron marks a row that opens something.
- **Keyboard**: always `primitive-keyboard` (layers, keys, `style`, `look(def, pressed)`). Never a custom keyboard.
- **Icons**: SVG paths on a 24-unit grid (`primitive_quick::Icon { stroke, fill }`), strokes 2 units wide. App icons are
  PNGs, square, shown as rounded squares; a drawn icon is a black glyph on a white tile with a 4 px border.
- **Waiting**: a pop-up with a title, a sentence that says how long, and a row of 10 blocks that fill in turn. No
  spinners (they would refresh the panel constantly).
- **Full-screen message**: centred title (64 px bold) and body (38 px), for states that end the app (for example
  "Powered Off").

## 5. Interaction

- **Feedback first**: on touch, mark the touched element pressed (darken it) and refresh only its rectangle; run the action
  after the pressed look is on the screen.
- **Gestures**: swipe down from the top for quick settings; swipe left and right for pages; long press for an item's menu.
  Every action reachable by a gesture is also reachable by a visible control.
- **Leaving**: every screen other than home has a visible way back (Done, Back, or Cancel). Tapping outside a pop-up
  closes it.
- **Confirm what is hard to undo** (power, restart, remove, forget a network) in a pop-up that says what will happen and
  how to undo it.
- **No busy loops**: nothing redraws on a timer unless it shows something new (the clock, a level, a progress block).

## 6. E-ink refresh

- A changed control: refresh its rectangle with a fast, non-flashing update.
- A new screen (opening a page, a pop-up closing, dark mode or rotation changing): one **full** refresh that flashes, to
  clear ghosting.
- No continuous animation. The opening zoom is one short sequence and can be turned off in Settings.
- Keep the last picture meaningful: the panel keeps it when the app stops or the Kindle turns off (the launcher draws
  "Powered Off" before the halt for this reason).
- Details of waveforms and the update call: the `kindle-eink` skill.

## 7. Dark mode

Dark mode inverts the whole interface (white on black) and keeps **pictures** as they are (PNG icons, photos, the sleep
picture). Build every screen in light mode, then check it inverted. Grays invert too, so a gray that reads on white must
also read on black.

## 8. Words

- Plain words, short sentences, sentence case. Buttons are verbs ("Restart", "Install", "Remove").
- Say what will happen and how to undo it ("Power off turns it off until you press its power button.").
- Units with numbers ("180 of 512 MB", "1.1 GB of 6.1 GB", "12 %").
- One name per thing across apps (Wi-Fi, SSH, Quick settings, Kindle UI).

## 9. Screenshots and review

Each app has a desktop target (`*-desktop`) that renders its screens to PNG at 1264 × 1680, as `kl-desktop` does. Use it
to review a screen before any device build, and for the README and store screenshots.

Review checklist for a new or changed screen:

- [ ] Reads in pure black and white; grays only for secondary text, hairlines and idle states.
- [ ] Uses the tokens above (sizes, radii, grays, type); no new values without a reason written next to them.
- [ ] Touch targets ≥ 100 px; a visible way back; destructive actions confirmed in a pop-up.
- [ ] Pop-ups float over the screen with border and halo; concentric radii.
- [ ] Shared components from `primitive-keyboard` and `primitive-quick` where they exist.
- [ ] Refreshes only what changed; one full refresh per new screen; no timer redraws without new content.
- [ ] Checked in dark mode and upside down.
- [ ] Desktop screenshot reviewed by the owner before the device build.
