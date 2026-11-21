---
name: kindle-device
description: Use for any work on the user's jailbroken Kindle Oasis 3 (SSH access, deploying a binary, the library launcher, storage limits, safe install, crash debugging, device tools, Wi-Fi and USB, and the system layer that owns the power button, sleep, the lock screen and the stock screensaver while apps run). Read this before building, deploying or testing on the Kindle.
metadata:
  type: reference
---

# Kindle Oasis 3: device access, install and debugging

Learned on the user's Oasis 3 (Zelda platform, firmware 5.18.2, jailbroken, with KOReader and KPM installed).
Reference implementation: `/Users/doannguyen/Documents/GitHub/prai-workspace/doannt-kindle-browser` (Primitive Browser).
Its files: `deploy/install-ssh.sh` (installer), `deploy/Browser.sh` (launcher), `scripts/package-release.sh`,
`docs/DEVICES.md`, `docs/INSTALL.md`. Paths may move; check them before relying on them.

## Device facts

- Target: `armv7-unknown-linux-musleabihf`, static binary. Cross-build with `cargo zigbuild`, using the rustup
  toolchain on PATH (`$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin`) and `--offline` (the
  network to crates.io is often unreachable and `--offline` avoids timeouts).
- Shell is busybox. Verified: `ls -l`, `ps -o pid,args`, `pidof`, `pgrep`, `tr`, `od`, `hexdump`, `ldd`,
  `base64`, `grep`, `sha256sum`, `sync`. Not supported: `ls --time-style`, `sleep 0.1` (integers only), `scp`
  (not installed; see upload below), `file`, `readelf`, and `strace` (not checked; assume absent).
- Kernel: `/dev/fb0` is the e-ink framebuffer (see the `kindle-eink` skill). Input: touch `/dev/input/event8`
  (`cyttsp5_mt`), page buttons `/dev/input/event3` (`gpio-keys`). Find devices by name in
  `/sys/class/input/event*/device/name`; the event numbers can change.
- Device clock and log timestamps follow the device's own setting, which can differ from the Mac's.

## Storage: check before every test

- `/var` is a **64 MB tmpfs in RAM**. It filled up from test frames (2 MB each), copies of the 18 MB binary and
  kernel-log captures. When it is full, writes fail silently ("No space left on device"), and tests look broken.
  Keep large test files on `/mnt/us` and delete them after each test.
- `/` is ext3, about 24 MB free of 494 MB. Do not write there.
- `/mnt/us` is the user storage: an `fsp` FAT volume, about 5 GB free. Application data and installed binaries
  live here. Files on FAT show `rwxrwxrwx`, which is normal.
- `df -h /var /mnt/us /` shows the state. Run it first when something writes nothing.

## Access over SSH

- SSH server: dropbear on port 2222 (`ssh -p 2222 root@<ip>`). Find the IP with `ifconfig wlan0`. The server is
  the launcher's: it is started from the launcher's Settings > SSH & DNS (or its quick settings), with the launcher's
  own Dropbear in `/mnt/us/launcher/ssh/`. KOReader can also start one. Two servers on one port is a common mistake: the
  second fails with "Address family not supported" or "Address already in use", and a stop that only checks
  its own pid file does nothing. Check the port: `grep -i ':08AE ' /proc/net/tcp` (0x08AE = 2222, state `0A`).
- **Firewall**: the Kindle drops incoming connections by default (ping gets no reply, and a TCP connect times
  out even though the server is listening and the device browses fine). Open the port in the server's start
  command: `iptables -I INPUT -p tcp --dport 2222 -j ACCEPT` and `iptables -I OUTPUT -p tcp --sport 2222 -j
  ACCEPT` (delete first with `-D` so starting twice does not add it twice). KOReader's SSH plugin does the same.
  The rules last until the Kindle restarts, so a rule left by KOReader can make SSH work until the next restart.
  Check with `iptables -L INPUT -n | grep 2222`.
- Host key: `/mnt/us/launcher/ssh/dropbear_ed25519_host_key`. The launcher's install copies it from the browser's or
  KOReader's copy if the launcher has none,
  so the Mac's known-hosts entry stays valid. Fingerprint check: `ssh-keyscan -p 2222 <ip> | ssh-keygen -lf -`.
- **Password**: the user supplies it. Never write it into the repository, code, commit messages, logs or chat
  output. Keep it in an expect helper outside the repo (for example `/tmp/*.exp`), reading it from the user.
  The Kindle's default root password was public in pushed git history for this project; the user accepted that,
  but the rule still holds.
- expect helper pattern (password prompt, then run a command):
  ```
  set timeout 120
  spawn ssh -o StrictHostKeyChecking=accept-new -p 2222 root@<ip> <command>
  expect { -re {[Pp]assword:} { send -- "<password>\r"; exp_continue } eof }
  ```
  Put shell with brackets, quotes or `$` into a file and run it with `expect -f`, or base64 it. Inline Tcl
  quoting breaks.
- Upload a file: `ssh ... "cat > /path.new && sync && mv /path.new /path" < local`. No scp.
- Upload a script: base64-encode it locally, then `echo <b64> | base64 -d > /var/tmp/x.sh`. Keep it in `/mnt/us`
  or `/var/tmp` (remember `/var` is small).
- Long jobs: `nohup sh /var/tmp/job.sh > /var/tmp/job.log 2>&1 &`, then read the log in later calls. Do not
  sleep in the foreground for minutes. Use a background wait loop that polls the log and reports when it ends.
- Kill loops over `/proc/[0-9]*`: skip your own shell (`[ "$pid" = "$$" ] && continue`) and do not match a
  pattern the shell's own command line contains. Otherwise the loop kills the command that runs it.

## The system layer: who owns power, sleep and the screen

Read `docs/system-architecture.md` (umbrella repo) first. Primitive Launcher is the system layer over every app, and
the supervisor (`deploy/supervisor.sh`) keeps it in charge while an app is open. Apps never handle these:

- **Power button sleep needs two things.** `com.lab126.kaf frameworkStarted = 1` (held by `holder.lua` while the
  framework is stopped) and `com.lab126.powerd preventScreenSaver = 0`. With the flag at 1 the power button does
  nothing (seen 2026-11-21 in the browser); the supervisor sets it to 0 at start. Check:
  `lipc-get-prop com.lab126.powerd status` (`prevent_screen_saver:`).
- **The stock screensaver** is a blanket module: `lipc-get-prop com.lab126.blanket load` lists it,
  `lipc-set-prop com.lab126.blanket unload screensaver` removes it. The launcher unloads it to show its own sleep
  picture, and loads it back only when the user picks the Kindle UI. Never load it when an app opens: the user then
  sees the stock lock screen, not their wallpaper.
- **When the launcher does not stay over the app** (an older launcher, or after too many launcher crashes) the
  supervisor follows `lipc-wait-event -m com.lab126.powerd goingToScreenSaver,outOfScreenSaver`: on sleep it runs
  `kl-launcher --sleep-screen` (draws the sleep wallpaper); on wake it sends `SIGUSR1` to the app's process group
  when the app's entry has `# Wake: redraw` in its first ten lines (exact line, plain file, not a link), and
  restarts the app otherwise. Apps start under `setsid`, so the group is the app's own. When the launcher stays (the
  normal case), it handles sleep and wake itself (next bullets).
- **An app under the launcher** (`PRIMITIVE_LAUNCHER=1`) must not stop or start the framework, touch the screensaver,
  or put the Kindle to sleep. It redraws its whole screen on `SIGUSR1` and follows the system theme
  (`dark_mode` in `/mnt/us/launcher/settings.txt`).
- **Boot copy**: `/var/local/primitive-launcher` is what the boot job starts. Opening Launcher from the library runs
  `setup-boot.sh`, which replaces the whole copy when it differs from `/mnt/us/launcher` (built beside, checked, then
  swapped; the SSH host key is kept). Check it after an install:
  `sha256sum /mnt/us/launcher/kl-launcher /var/local/primitive-launcher/kl-launcher`.

- **The launcher stays running while an app is open** (0.6.1 and later). It asks the supervisor for the app with
  SIGUSR1, pauses its own drawing, and over the app it owns only the top-edge swipe (quick settings) and the power
  events: it freezes the app (SIGSTOP to its group), saves the screen, draws its panel over the app's picture
  (`Renderer::set_backdrop`), and on close puts the screen back and resumes the app. Log lines: `system layer: ...`.
  It sends `SIGUSR1` only to an app whose entry declares `# Wake: redraw` (the supervisor marks it with
  `run/app-redraws`): after a theme or rotation change while its screen was up (then it does not put the old screen
  back first), when it had no saved screen, and after the launcher started again over the app. On wake it puts the
  saved screen back; the app draws nothing.
- **The power menu** (from Power in quick settings, over the home screen or an app) is Cancel, Kindle UI, Restart,
  Power off (launcher 0.6.8). There is no Kindle UI tile on the home screen any more. Kindle UI over an app: the
  supervisor ends the app (TERM to its group) before the Kindle UI starts; the dialog is drawn on a plain page.
- **Only the theme switch flashes.** Pop-ups over an app open and close without a flash (only the changed box is
  updated). The app's redraw after the launcher's request must not flash: a GC16 flash shows the inverse of the
  screen for a moment, and the inverse of the new theme is the old one. The kit draws it with `Display::show_calm`
  (GC16 in partial mode); the browser with `redraw_all_calm` (the page waveform).
- **Native apps (the `primitive-app` kit, `primitive_app::run`)**: under the launcher the kit turns SIGUSR1 into a
  full redraw that reads the theme again (drawn with `show_calm`), and on wake it redraws only if a redraw was asked
  for while it slept. It drops the swipe down from the top edge (the system's), so the app never sees it. The
  contract is in the module docs of `crates/primitive-app/src/lib.rs` and in `docs/contracts.md` §1.1. An app
  built with that kit may declare `# Wake: redraw`. Never add the header to an app whose binary does not handle
  SIGUSR1: the signal ends it.
- **Library entry scripts** under the launcher: put `# Wake: redraw` in the first ten lines (after the other header
  lines), and `[ "${PRIMITIVE_LAUNCHER:-0}" = 1 ] && trap '' USR1` before the app starts. The signal goes to the
  whole process group; a shell that runs the app as a child (not `exec`) ends on it otherwise. An ignored signal is
  inherited through `exec`, and the app's own handler replaces it.
- **Apps build against the kit by path** (`../doannt-kindle-tools/crates/...`), so a local build uses whatever the tools
  working tree holds. To build against a kit branch without touching that tree: a worktree of the kit, a folder with a
  `doannt-kindle-tools` symlink to it, and a worktree of the app beside it (`/tmp/apppilot/` was used).

Lessons from the system layer (each cost a device round):

- A background shell pipeline (`lipc-wait-event | while read`) survives `kill` of its subshell: stop the children too
  (`kill_tree` in the supervisor), and make a watcher check it still serves the current app. Stale watchers set the
  restart flag on every wake and reopened the browser when the user left it.
- A trapped SIGUSR1 interrupts the shell's `wait` (busybox returns 138): loop `wait` until `kill -0` says the process
  is gone, or the supervisor treats the app as ended while it still runs.
- Child processes such as `lipc-wait-event` outlive the program that started them unless it sets
  `PR_SET_PDEATHSIG`; count them with `ps -o pid,ppid,args | grep lipc-wait-event` (parent 1 means orphaned).
- A new `supervisor.sh` only runs after Launcher is opened again from the Kindle library (or a restart); the
  installer's restart reloads the launcher binary only.
- An app frozen under quick settings has input queued behind the freeze. If it draws that input before it takes the
  redraw request, it flashes the old theme (seen in 2048): take the request first, the moment the loop wakes.
- The app's redraw after a theme switch was a second GC16 flash and showed the old theme for a moment (2048 and the
  browser): use a non-flashing whole-screen update for the launcher's redraw.

## Launcher and the library

- An app appears in the Kindle library through a script in `/mnt/us/documents/<Name>.sh`, with header lines
  `# Name:` and `# Icon: data:image/png;base64,...`. The library shows the icon as a book cover. Make the icon
  portrait, about 2:3 (the browser uses 600x920; KOReader's is 938x1432). A square icon looks wrong.
- Standalone pattern, only when the app is opened from the stock library without Primitive Launcher
  (`deploy/Browser.sh`): hide the status bar (or stop the framework), start the app in the
  background, wait for it, and on TERM restore the UI and open the library. A watchdog process stops the app if
  the launcher is killed. **Any non-zero exit restarts the app** (up to a limit, then "too many crashes; giving
  up"), so a plain kill looks like a crash. Stop the launcher with TERM first, then the app.
- Restore the Kindle UI when the app exits; the framework must come back.

## Installing safely

- **Stop the running app before replacing its files.** The app reads its program from the disk as it runs. On
  the FAT storage an overwritten file can give the running program other data, and it crashes with SIGBUS
  (exit 135, `[crash] fatal signal 07 at address ...`, at addresses inside the binary). The browser crashed this
  way several times. The mechanism is likely, not proven. The installer now stops the launcher (TERM), then any
  leftover app process, and only then copies.
- Copy by checksum: send a file only when its SHA-256 differs from the device's. Check after every install:
  `sha256sum <file>` on the device equals the local `shasum -a 256`.
- Ship every runtime file the app needs: fonts, device tools, their shared libraries and their licence texts.
  The release package and the installer must carry the same set. A missing library fails silently.
- Device builds get a new patch version every time (the user's rule); a new phase starts a new minor version with `scripts/build-device.sh --minor`. Tags `vX.Y.Z` are never moved.
- **Check the binary is the new build.** The launcher's build once compiled the shared library (`-p kl-kindle`)
  instead of the launcher, so the install copied a stale binary and reported success (0.5.6 ran 0.4.10). The build
  now fails unless the binary contains the version. After any install, confirm on the device:
  `grep -a "start v" /mnt/us/launcher/log-launcher.txt | tail -n 1` after the next start.

## Network and USB

- **Wi-Fi is 2.4 GHz only** on the Oasis 3. An iPhone hotspot shows up only with "Maximize Compatibility" on.
- **Saving a Wi-Fi network** (`lipc-hash-prop com.lab126.wifid createProfile`, the profile on standard input) accepts
  only the one-line form `[{ essid = "Name", secured = "yes", psk = "..." }]`. A `store_nw_user_pref` field or a
  multi-line profile is a parse error and nothing is saved. Test with a throwaway name and delete it after
  (`lipc-set-prop -i com.lab126.wifid deleteProfile <netid>`); never use the user's real password in a test.
- **USB**: the cable gives storage only (Amazon vendor `0x1949`, "Internal Storage", mounted at `/Volumes/Kindle`),
  no network. Read logs there when Wi-Fi is down; SSH needs Wi-Fi.
- **Finding the Kindle**: its Wi-Fi MAC starts `f4:03:2a`; `arp -a -n` after a ping sweep of the subnet shows its
  address. A port check can miss on the first try; retry before concluding SSH is down.

## Debugging

- App log: keep it on `/mnt/us` (e.g. `/mnt/us/<app>/log-<app>.txt`). Launcher lines are `[launcher HH:MM:SS]`,
  app lines are `[<tag>]`, and crashes are `[crash] fatal signal NN at address ...`. Tail it after each test.
- Exit codes: 135 = SIGBUS (signal 7), 139 = SIGSEGV, 143 = SIGTERM. `rc` in the launcher line is the process exit
  status.
- A pipe hides the exit code of the command before it: `cmd | tail` reports `tail`'s status. Redirect to a file
  and check `$?` (this caused a false "fbink works" report).
- Kernel log: `dmesg` (ring buffer, `dmesg -c` clears it). E-ink driver messages need dynamic debug:
  `echo "module mxc_epdc_v2_fb +p" > /sys/kernel/debug/dynamic_debug/control`. A capture loop writes to a file;
  put it on `/mnt/us` and stop it when done (it filled `/var`).
- Framework properties: `lipc-get-prop com.lab126.winmgr accelerometer` (U/D upright or upside down),
  `lipc-get-prop com.lab126.winmgr epdcMode` (Y8), `lipc-probe <service>` lists properties. Setting
  `com.lab126.kaf currentDisplayMode` did not change the screen in tests.
- Use `ps -o pid,stat,args` for process state. State `T` means stopped (SIGSTOP), `S` sleeping.

## Working with the user

- The user looks at the Kindle; you cannot. Do not claim a visual fix works until the user confirms it on the
  device. Give the user a precise test ("turn 4 pages with the buttons, then tell me which flash") and wait.
- Stage and commit only explicit paths; the working tree is shared with the user's own edits. Do not commit or
  push unless asked. Releases follow `docs/VERSIONING.md` in the reference repo.
- Report failures with the real output; do not summarise a failed step as success.
