---
name: kindle-eink
description: Use for drawing to the e-ink screen of a Kindle Oasis 3 (framebuffer, the Zelda update ioctl, waveform choice, flashing versus calm page turns, dithering and gray levels, FBInk, and how to test a waveform on the device). Read before writing or tuning any e-ink output.
metadata:
  type: reference
---

# Kindle Oasis 3: e-ink drawing

Measured on the user's Oasis 3 in the Primitive Browser project. The reference code is
`crates/kb-kindle/src/eink.rs` and `crates/kb-kindle/src/main.rs` in
`/Users/doannguyen/Documents/GitHub/prai-workspace/doannt-kindle-browser`. Device access (SSH, install, storage)
is in the `kindle-device` skill.

## Framebuffer

- `/dev/fb0`, 8 bits per pixel, pixel format Y8 (gray). Visible 1264 x 1680, line length 1280 bytes,
  `smem_len` 4587520. Upright rotation is 0. FBInk reports `viewVertOffset=8` on this device.
- Open read/write, `FBIOGET_FSCREENINFO` (0x4602) and `FBIOGET_VSCREENINFO` (0x4600), mmap `smem_len` bytes
  `MAP_SHARED`. Check `bits_per_pixel == 8`, `rotate == 0`, `xoffset == 0` before drawing in-process.
- Row `y` starts at `yoffset * line_length + y * line_length`. Copy the changed rows, then send the update.
- **Upside down**: the framebuffer's `rotate` becomes 2 (`/sys/class/graphics/fb0/rotate`) when the device is
  held upside down. Measured on the Oasis 3: the panel shows memory as it is. Upright text drawn in memory
  (FBInk, `pan` 0,0) reads upright to the user at rotation 2, so the app must NOT turn its frames. A rotation
  check that only accepted 0 sent every update to FBInk, which cannot show images, so the screen went blank.
  Accept rotation 2 for in-process drawing. Rotations 1 and 3 (landscape) are not supported.
- **Screen capture** (to see what the user sees): `cat /dev/fb0 > /var/tmp/fb.raw` on the device, copy it to the Mac
  (ssh `cat`), then take 1680 rows of 1264 pixels from row `yoffset`, with 1280 bytes per row. The memory holds two
  pages (3584 rows); the visible one starts at `yoffset` (0 in every capture so far). Write it as an 8-bit gray PNG and
  look at it. Delete the raw file on the device after (it is 4.5 MB in the small `/var`).

## Update ioctl (Zelda platform)

- `struct mxcfb_update_data_zelda`, 88 bytes: region (rect: top, left, width, height, 4 u32), `waveform_mode`,
  `update_mode`, `update_marker`, `temp` (i32), `flags`, `dither_mode` (i32), `quant_bit` (i32), `alt_buffer`
  (phys_addr, width, height, region rect), `hist_bw_waveform_mode`, `hist_gray_waveform_mode`, `ts_pxp`, `ts_epdc`.
- `MXCFB_SEND_UPDATE_ZELDA = _IOW('F', 0x2E, 88) = 0x4058462E`. `struct fb_var_screeninfo` is 160 bytes.
  Keep unit tests on both sizes (`size_of::<UpdateZelda>() == 88`, `size_of::<VarInfo>() == 160`): a wrong
  layout sends the ioctl with garbage fields.
- Waveform codes: DU 1, GC16 2, GL16 3, REAGL 4, AUTO 257, ZELDA_A2 6, ZELDA_GCK16 8.
- `update_mode`: PARTIAL 0, FULL 1. `temp`: `TEMP_USE_AMBIENT` = 0x1000 (the log shows `temp=4096`).
- For AUTO, FBInk sets `hist_bw` = DU and `hist_gray` = GC16. GC16 is the flashing waveform, so AUTO with any
  gray content flashes. Setting the gray histogram to REAGL (as the in-process path does) did not remove
  the flash by itself. The flash came from gray text (below).
- Each update returns a marker; the driver processes updates through the LUTs. One page turn of the full
  screen as partial AUTO took about 320 ms in the kernel log (`LUT N completed`), and in-process drawing
  took about 45 ms of CPU to reach the panel.

## What flashes (measured, not guessed)

- A full update (`update_mode` FULL) always flashes.
- Partial updates of pure black and pure white pixels (letters 0, paper 255) do not flash, in AUTO, GL16,
  REAGL, GC16 partial or DU.
- **Gray text flashes on every turn.** Text in a dark gray (for example #111 on white, or 238 when the page
  is inverted for night) makes each letter a gray transition. The panel reaches a gray by passing through the
  opposite extreme, so every old and new letter flashes. Fix: draw near-black pixels as 0 and near-white as 255
  (the two panel steps nearest each), keeping the anti-aliased edges. The browser's SOLID TEXT option does this.
- Quantise page content to the panel's 16 gray steps (multiples of 17). This lowers the driver's transition
  count. The driver runs its own flash pass when the transition count is high (about 2900 in the log: "SW
  mitigation"), so keep counts low.
- Waveform choice mattered less than content. A test with real browser frames flashed the same way in every
  waveform until the gray text was fixed.
- Ordered dithering (8x8 Bayer, 16 steps) can be done in the app. FBInk's `dither` option needs image support,
  which the KOReader FBInk build lacks.

## Page turns

- A page turn that scrolls a fixed share of the screen puts every text line a few rows off its old position,
  so nearly every pixel changes and the turn reads as a flash. Lines that land on the same rows as before change
  calmly. The browser's BOOK LINES and the line-aligned turn (`crates/kb-app/src/browser/lines.rs`) do this:
  forward, the next text line starts at the top; no overlap, nothing skipped.
- Paragraph spacing must be a whole number of lines, or the lines drift.
- Prefetch the neighbouring screens while idle, but not while a panel update is still running (the render uses
  300 to 650 ms of CPU and memory on this device). Wait about 450 ms after an update before prefetching.

## FBInk on this device

- Use the KOReader build of FBInk (git `92e1270`, reports "1.25.0 for Kindle" in strings). `fbink -e` prints
  the state (`currentRota=0` upright).
- The FBInk 1.25.0 build in `/mnt/us/libkh/bin` segfaulted on `fbink -e` (exit 139). KOReader's build runs.
- The KOReader build has **no image support** (`-g file=...` fails with "Image support is disabled"), and it
  cannot dither images. Do not put dithering or image display on a path that depends on FBInk.
- FBInk startup costs about 170 ms per call (process start, device detection), so use it only as a fallback.

## Testing a waveform (the method that worked)

1. Prepare pages as 1264 x 1530 gray images (the top 150 rows are the label band). Use the same font size, line
   spacing and gray levels as the real content. Text size mattered: pages at the browser's own size and layout
   gave the same result as the browser.
2. Write a shell script that, for each test, does a full clear, shows page 1, writes a label band at the top
   ("TEST n: name"), then turns 4 to 8 pages with a fixed delay or waits for button presses (read
   `/dev/input/event3`, 16-byte `input_event`, type EV_KEY=1, code 109 forward / 104 back, value 1 = press).
3. Run it in the background; record which tests flashed (the user watches). Keep the kernel-log capture on
   `/mnt/us`.
4. Compare the kernel log: `send_single_update:UPDATE_MODE_x waveform_mode=N`, `transition=`, `SW mitigation`,
   `coord left,top,width,height`, `LUT N completed`. Awk on these lines gives a per-update table.
5. Confirm on the device with the user before claiming a fix.

## Gotchas

- Do not add `dither` flags to FBInk calls without checking the build supports them.
- A screen that goes blank after a failed update is normal: the panel keeps the last good content. Check the
  framebuffer (`dd if=/dev/fb0 ...`, then count pixel values) to see what is on the panel.
- The browser's night view inverts the page; compute the gray levels after the inversion, because that is what
  the panel sees.
