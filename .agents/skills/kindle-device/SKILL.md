---
name: kindle-device
description: Use for any work on the user's jailbroken Kindle Oasis 3 (SSH access, deploying a binary, the library launcher, storage limits, safe install, crash debugging, device tools). Read this before building, deploying or testing on the Kindle.
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

## Launcher and the library

- An app appears in the Kindle library through a script in `/mnt/us/documents/<Name>.sh`, with header lines
  `# Name:` and `# Icon: data:image/png;base64,...`. The library shows the icon as a book cover. Make the icon
  portrait, about 2:3 (the browser uses 600x920; KOReader's is 938x1432). A square icon looks wrong.
- The launcher pattern (`deploy/Browser.sh`): hide the status bar (or stop the framework), start the app in the
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
