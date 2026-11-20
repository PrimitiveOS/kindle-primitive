# Launcher settings plan

Reviewed 20 November 2026 against Primitive Launcher 0.4.10 and its pinned Tools revision. The first addition is
**Settings › Battery**. Follow it with controls that improve reading and make existing settings easier to find.
The initial device target is the Kindle Oasis 3 on firmware 5.18.2. [Implementation milestones](implementation-plan.md#g-launcher-features)

Launcher **0.5.3** and Store **0.1.6** are published and installed on the Oasis 3. Swipe vertically through the grouped Settings
list. **Back** returns to the previous position. **Apps › Manage installed apps** opens Store's installed list, and
**App visibility** is a scrollable list of individual home-screen switches. Grid settings reuse the existing
preferences in `apps.toml`. **Storage** links to the same installed list and to Store's saved catalog controls.
Older Store versions still open at Today.

**Date and time** under System shows the device clock and the UTC offset from the stock Kindle time zone.
**Sync** asks the firmware's clock tool to update the time over Wi-Fi. **Refresh** re-reads the configured time zone,
including a change made in the Kindle interface. The sync runs on request with a timeout. [Date and time milestone](implementation-plan.md#g7-date-and-time)

**Display › Wallpaper** groups the Home Screen, Sleep Screen, and Startup Screen. Each keeps its own choice and can
return to its default. The sleep picker also offers the existing rotation from `launcher/screensavers/`. Startup shows
the chosen image when Launcher takes over automatically after the Kindle startup screen. [Wallpaper milestone](implementation-plan.md#g8-wallpaper)

## What to take from Apple

| Reference | PrimitiveOS design |
|---|---|
| iPhone Battery leads with charge status, then shows battery history and links to settings that may help. [Apple Battery usage](https://support.apple.com/en-gb/102432) | Put current level and charging state at the top. Add direct rows for Front light, Wi-Fi, and automatic Store checks. Show a short history when enough observations exist. |
| iPhone has a manual Low Power Mode with defined effects. Adaptive Power is model-specific. [Apple Power Modes](https://support.apple.com/guide/iphone/save-battery-life-with-power-modes-on-iphone-iphcab9aecd1/27/ios/27) | Pilot an explicit **Low power mode** with a short list of changes and a visible state. Keep the user’s existing brightness and Store preferences recoverable when it turns off. |
| Apple separates current charge, battery health, and model-specific charging controls. [Battery usage and health](https://support.apple.com/en-au/guide/iphone/iphd453d043a/27/ios/27) · [Set a charge limit](https://support.apple.com/en-euro/guide/iphone/iph0777c60aa/27/ios/27) | Show measured charge now. Battery Health, cycle counts, time estimates, and a charge limit each need verified support for the Kindle model and firmware. |
| Apple provides quick brightness control, appearance settings, and dedicated legibility options. [Brightness and color](https://support.apple.com/en-ie/guide/iphone/iph60ba71065/27/ios/27) · [Display and text settings](https://support.apple.com/en-mide/guide/iphone/-iphd6804774e/ios) | Share front-light controls between Display and Quick Settings. Offer a simple reading preview for larger text and stronger contrast. Use Kindle warmth and rotation only on models that support them. |
| iPhone groups Lock Screen and Home Screen wallpaper in one place and allows separate choices. [Apple Wallpaper guide](https://support.apple.com/en-euro/guide/iphone/iph3d267104/27/ios/27) | Use one Wallpaper page inside Display, with an independent picker for each screen. Use grayscale composition so app icons and labels are legible on e-ink. |
| Apple shows available storage before actions for freeing space. [Apple Storage](https://support.apple.com/en-mide/guide/iphone/iph47c931112/ios) | Show user-storage capacity first. Route removal and cache actions through the Store flows that already own those files. |

Amazon identifies front-light level, avoiding unused network access, and letting the device sleep as practical
ways to conserve Kindle battery. Display appearance and front-light level are separate controls on our e-ink interface.
[Amazon battery guidance](https://digprjsurvey.amazon.com/csad/help/node/G4GMVBJTKV5K77V6) · [Amazon screen light guide](https://digprjsurvey.amazon.com/csad/help/node/GFF5L8YJ8D3SYLZA)

## Launcher settings today

| Area | Current controls | Gap to address |
|---|---|---|
| Network | Wi-Fi & network, SSH & DNS, Wi-Fi file transfer. Quick Settings repeats Wi-Fi and SSH. | Make technical connection controls easy to find under Network. The current Airplane shortcut toggles Wi-Fi through the same action as the Wi-Fi shortcut. Label it according to the radios the device actually controls. |
| Display | Frontlight and Warmth with step buttons, Dark mode, Opening animation, and Rotation. Quick Settings also offers direct level selection. | Reuse Quick Settings' direct selection in Display. Standardize the current two-step Settings buttons and one-step Quick Settings buttons on single-step adjustment. Keep rotation upright or upside down on Oasis 3. |
| Sleep | Chooses the Launcher sleep picture or Kindle screensaver. | Label the existing choice **Sleep screen**. Explain when the stock picture resumes. An adjustable idle timeout or deep-sleep control needs a verified platform API and separate tests. |
| Apps and Store | Hidden apps, automatic catalog checks, and clear saved catalog. | Put grid options and a link to Store management alongside Hidden apps. Keep Store as the owner of app installation, updates, and removal. |
| Device and About | Startup, restart Launcher, open the stock Kindle UI, Launcher version, app count, memory, available storage, and Wi-Fi address. | Show firmware, the model when verified, and storage used and available. Update the old startup explanation to match the implemented switch. |
| Battery and accessibility | The status bar shows charge and a charging bolt. Launcher already warns at 10% and 5%. Dark mode and opening animation are under Display. | Add the Battery page and a dedicated **Accessibility** page. Start with Launcher text size, stronger contrast, and a shared setting for opening animation. |

The released Launcher 0.4.10 layout uses nine fixed-height rows. The current Settings overview and App visibility
scroll vertically as their content grows. Keep the title and navigation control visible during swipes, and keep tap
geometry and rendering in sync for partly visible rows, both portrait orientations, and larger text sizes.
[Settings layout at the released Tools pin](https://github.com/PrimitiveOS/kindle-primtitive-tools/blob/107f15a5cd893b66cdacdb406a3144342224b592/crates/kl-core/src/layout.rs#L51)

## First release

**Battery.** Use a single card for the percentage, monochrome meter, and state. Show **Charging**, **On battery**,
**Plugged in**, or **Fully charged** when the readings support that label. Use **Status unavailable** when the source
cannot distinguish states. Report **Plugged in** with **Not charging** when both facts are known. A tapped battery
indicator in Quick Settings can open the same page. Keep one set of low-battery alerts and link to the existing Wi-Fi,
front-light, and Store controls. Front-light adjustment stays available with just a few taps.

Reuse the Launcher’s existing `powerd` percentage and charging reads and the Oasis 3 supply paths. Read external
power directly from the charger. Use USB drive state for storage export.
Reject out-of-range levels and preserve unknown readings. Use the existing awake status refresh with a redraw of
the changed card only. The page adds no wake timer. The Oasis 3 log confirms the charger-online and charging flags
change on plug-in. [Device reads](https://github.com/PrimitiveOS/kindle-primtitive-tools/blob/107f15a5cd893b66cdacdb406a3144342224b592/crates/primitive-device/src/lib.rs#L118) · [Oasis 3 USB test](https://github.com/PrimitiveOS/kindle-primitive-launcher/blob/v0.4.10/docs/device-notes.md#usb-with-volumd-paused-s5-first-half-2026-11-18-0938)

**Display.** Keep the existing front-light and warmth levels and their shared values in Quick Settings. Use the same
tappable scale and single-step buttons in both places. A device capability check controls whether to
show warmth or auto-rotation. Add a simple high-contrast preview when Accessibility is ready. Manual values stay usable
with unreliable sensors. Offer a warmth schedule or ambient auto-brightness later if the relevant clock, sensor, and
stock Kindle handoff have been validated.

## Follow-up releases

1. **Battery history and Low power mode.** Add a local 24-hour chart of observed battery level, marked charging periods,
   and the last observed charge event. Sample on open, wake, state transitions, or the existing awake cadence with a
   bounded write rate. Label missing intervals and show **Collecting history** until observations are available. Keep
   history writes under the existing USB lease. Scope the opt-in Low power pilot to a disclosed front-light cap and
   deferral of automatic Store catalog checks. Keep manual Refresh, Wi-Fi file transfer, and in-progress transactions
   available. When the mode ends, restore only values still owned by the mode so later manual changes are respected.
2. **Accessibility.** Add larger Launcher text with a preview, stronger grayscale contrast, and a shared **Opening
   animation** preference. Keep the existing normal and dark themes. Expand text scaling to independent apps when
   they use the shared control and pass their own layout tests.
3. **Storage and device information.** Reuse Quick Settings' used and total storage reading for Kindle user storage.
   Add an **Installed apps** link
   to Store and the existing **Clear saved catalog** action. Show model and firmware when available, with Launcher
   version and USB status. Keep cleanup explicit. Test the storage page with a full drive and while USB owns the volume.
4. **App grid and settings navigation.** Make the existing grid layout controls easier to discover alongside Hidden apps.
   Keep related settings together in the scrolling overview. Preserve Back and Done behaviour.

Current evidence supports battery level and charger state on the Oasis 3. App use duration can be measured separately
if it becomes useful. Per-app battery percentages need energy attribution. Battery Health and runtime estimates require
reliable readings and drivers can omit those fields. Charge limiting and optimized charging need a documented,
model-specific charger control with physical verification, including behaviour across sleep and reboot. The first
release leaves charging management to the stock firmware. [Linux power supply attributes](https://cdn.kernel.org/doc/html/latest/power/power_supply_class.html)

## Verification gates

- **Desktop.** Cover charge status and missing or invalid readings, 10% and 5% alert behaviour, light and dark themes,
  both portrait orientations, and tap targets at the smallest supported layout. Exercise scrolling, taps after scrolling,
  Back, and Done.
  For later power mode work, verify manual overrides, pref migration, and the existing Store and USB state transitions.
- **Oasis 3.** Compare battery state while unplugged, charging, and plugged in without charging. Verify brightness,
  warmth, USB drive and eject, normal sleep and wake, and return to the stock Kindle UI. During the Low power pilot, run
  a manual Store refresh and a file transfer. Check that status updates produce no extra periodic wakeups and measure
  consumption over comparable sessions before publishing a savings claim.
- **Device setup.** Test in simulation first. Use the existing Launcher installation for any approved hardware work.
  The keep-awake override was cleared on 20 November. The Battery page and its planned power mode leave that control
  alone. [Current device state](handoff/STATE.md#kindle-oasis-3)
