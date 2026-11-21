# Device profile and install rules: the design

Status date: 2026-11-21. Written for: the people who change the launcher, the Store, the app kit and the release process.
Owner decision (2026-11-21): the Store does not limit installs by firmware. The only install rule is the chip
architecture (`armhf` now; `armel` later). The launcher reports what it knows about the Kindle and the owner
can choose the model where it cannot tell.

## 1. What the device can tell us (checked on the Kindle Oasis 3, read-only)

| Fact | Where | Value on the Oasis 3 | Use |
|---|---|---|---|
| Platform codename | `/etc/version.txt` (`System Software Version: …_stinger_<codename>-…`) | `zelda` | identifies the model |
| Firmware | `/etc/prettyversion.txt` | `5.18.2` | shown; not a gate |
| Architecture | `uname -m` (`armv7l`) and the loader (`/lib/ld-linux-armhf.so.3`) | `armhf` | the install gate |
| CPU | `/proc/cpuinfo` | `Freescale i.MX7 Dual` | shown |
| Serial | `/proc/usid` | `G000…` | **not stored or sent anywhere** (personal) |

Not usable: `/etc/prod` does not exist; `lipc-get-prop com.lab126.system devicetype` has no such property.
The codename is the only reliable model signal we found. The mapping codename → model is ours to keep; a
codename we do not know is shown as "unknown model" and the owner chooses the model.

## 2. Where the rules live

- **The launcher** detects the profile at start and writes `launcher/device.txt` (plain `key=value`):
  `model`, `model_source` (`detected` or `selected`), `firmware`, `arch`, `codename`. The file never holds the serial.
- **Settings › Device** (launcher): shows the detected values. If the model is unknown it lists the supported
  devices (the launcher's model table, `kl-core/src/models.rs`) for the owner to pick. The pick is saved in
  `settings.txt` as `device_model=<id>`, and it wins over detection only when detection failed.
- **The Store** reads the model from `launcher/device.txt`. It takes the architecture and firmware from the same files
  the launcher reads (`/lib/ld-linux-armhf.so.3`, `/etc/prettyversion.txt`), so the two agree.
- **The app kit** does not decide installs. It reads the same profile when it starts (section 4).

## 3. Install rules (what the Store does)

1. Only the architecture gates an install: a version is installable when the listing has an asset for the
   device's `arch`. The newest such version is offered.
2. Firmware: `firmware.min` and `firmware.max` are informational. They are shown on the app page
   ("Tested on firmware 5.18.2 and later"), not enforced.
3. `tested_on` is the list of Kindle models the app was verified on, by catalog name (the schema checks the names). An
   app page for a model not in `tested_on` says "Not tested on your Kindle yet" and the install button still works.
4. A listing with no asset for the device's arch is hidden from the list (proposal; see decision D2).
5. Withdrawn versions are still skipped, as today.

## 4. What the apps need (and why "install allowed" is not "works")

The screen size, the touch device name, the page-turn keys and the battery and charger paths are compiled into the
kit as one `Profile` (`crates/primitive-device/src/profile.rs`: `ACTIVE = OASIS_3`). A binary built for the Oasis 3
on another Kindle draws at 1264 × 1680 on a different panel, reads the wrong touch device and battery node, and
may do nothing useful. So the Store may let any armhf Kindle install an app, but the app works only where its
profile matches. Two steps make other models work:

- **A profile per model**, read by the kit at start from the launcher's `device.txt` (the codename), instead of
  the compile-time `ACTIVE`. Values per model come from reading that model (screen size from the framebuffer
  geometry, touch name from `/proc/bus/input/devices`, the keys and the battery nodes). Until a model's profile is
  added, its apps run with the Oasis 3 values and the launcher warns "Untested model: some screens may not fit".
- **Release builds record the arch**: each package manifest carries `arch` (already true) and the listing has one
  asset per arch (already true). `release.yml` takes `arches` (today `armhf`); an `armel` build is added when it is
  needed, and nothing else changes.

Apps need no install rule of their own. The conventions skill gets one line: an app reads the screen size and the
device values from the kit, never from constants.

## 5. Phases

Status (2026-11-22): phases 1–4, 6 and 7 are done. Phase 5 is deferred: the owner has no second Kindle to test a
model on, so it is not built. The kit still uses the Oasis 3's screen, touch and battery values for every model, and
the Store says "Not tested on your Kindle yet" for other models. Phase 5 starts when a second Kindle is available.

- [x] 1. Design (decisions D1–D4 recorded).
- [x] 2. Store rules: installs by architecture only (`tools` `kl-store`, `e65cb98`); firmware and `tested_on` are information.
- [x] 3. Launcher: model detected from the platform codename, or chosen from the supported list (`tools` `fe476aa`, launcher 0.6.20); `device.txt` written without the serial.
- [x] 4. Store UI: apps with no package for the device's arch are hidden; the app page says "Not tested on your Kindle yet" (`tools` `9d76c67`, Store 0.1.10).
- [-] 5. Kit: per-model screen, touch and battery values from `device.txt`. Deferred 2026-11-22: no second Kindle to test on (see the status above).
- [x] 6. Release: the arch is recorded per asset and per package (the existing manifest and listing format). An `armel` build is added when needed. `check-assets.py` checks each manifest's arch against its listing asset; the schema checks the `tested_on` names.
- [x] 7. Docs and skills: `store-submit-app.md` and `store-architecture.md` say firmware and `tested_on` never block an install; the conventions skill has the "device values come from the kit" line.

1. **Design (this document).** Decisions D1–D4 below.
2. **Store rules** (`tools` `kl-store`): arch-only `pick_version`; firmware and `tested_on` informational; a test
   per rule. Reads the profile from `device.txt` when present.
3. **Launcher** (`tools` `kl-kindle` profile detection, `kl-core` Settings › Device page, `kl-render` drawing, the
   `device.txt` writer, the model table in `kl-core/src/models.rs`); tests for detection, the unknown-model path and the saved choice.
4. **Store UI** (`store-app`): reads `device.txt`; shows the device line; hides arch mismatches (per D2); the
   "Not tested on your Kindle yet" note.
5. **Kit** (`tools` `primitive-device`): a runtime profile chosen from `device.txt`, Oasis 3 as the built-in default;
   the warning for untested models. Per-model values added one model at a time, each tested on its device.
6. **Release and catalog**: `arches` documented in the umbrella's `merge-and-release.md`; listings keep one asset per
   arch; `check-assets.py` checks the arch of each asset against its manifest.
7. **Docs and skills**: `store-submit-app.md` (firmware informational, arch gating), the conventions skill (no
   device constants), `device-profile-plan.md` ticked as done per phase.

Each phase ends with a device check on the Oasis 3 (the owner present). Phase 5 needs a second Kindle to test a
second model; until one is available it stays deferred and that model stays "untested".

## 6. Decisions needed

- **D1 — installs on untested models.** Allow with the warning (the owner's rule), or require a profile first?
  Recommendation: allow, with the warning, and say which models have a profile.
- **D2 — listings for the other arch.** Hide them, or show them disabled ("no armel build yet")? Recommendation: hide.
- **D3 — the supported list.** Which models go in the launcher's model table now? Only the Oasis 3 (`zelda`) is
  confirmed. The owner should name the other jailbreakable models; their codenames and values are read on the
  device when available.
- **D4 — the serial.** Keep it out of every file and every request (recommendation), so no device identity leaves
  the Kindle.
