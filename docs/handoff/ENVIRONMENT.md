# Environment: build, test, reach the Kindle

## The Mac

- Rust: the toolchain is `$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin`. Put it first on PATH in every shell:
  `export PATH=$HOME/.rustup/toolchains/stable-aarch64-apple-darwin/bin:/opt/homebrew/bin:/usr/bin:/bin`
  The shell in this environment sometimes loses `/usr/bin` from PATH (`curl: command not found`). Then call `/usr/bin/curl`,
  `/usr/bin/python3`, `/usr/bin/sips`, `/usr/bin/shasum`, `/usr/bin/file` by full path.
- Always build offline first (`--offline`): the crate cache is populated. New crates need network (crates.io works).
- Device binary: `cargo zigbuild --offline --release -p <crate> --target armv7-unknown-linux-musleabihf` (zig and
  cargo-zigbuild are installed at `/opt/homebrew/bin`). The output is `target/armv7-unknown-linux-musleabihf/release/<bin>`.
- Python with the schema checker (needed by the catalog scripts and the packager): use
  `/Users/doannguyen/Documents/GitHub/prai-workspace/prai-bldc-servo-drive/.venv/bin/python3` (it has `jsonschema` 3.x), or
  `/opt/homebrew/bin/python3` after `pip install jsonschema==4.26.0`. `/usr/bin/python3` has no `jsonschema`. Scripts that
  call `python3` pick whatever is first on PATH: put that venv first when running the catalog checks.
- Screenshots: `cargo run --offline -q -p kl-desktop -- --documents <empty folder> --out <folder>` (from the launcher folder,
  with the catalog folder beside it: it reads `../doannt-kindle-catalog/apps` and `drafts`). Look at PNGs with the Read tool;
  `/usr/bin/sips -Z 700 in.png --out small.png` makes them small.
- Tests: `cargo test --offline --workspace` in each of: tools, launcher, store. Expect 14 `test result: ok` lines in tools,
  about 6 in the launcher. The store's own tests: none yet (STORE-APP.md, task T6).
- Clippy: `cargo clippy --offline -p kl-core -p kl-render -p kl-store -- -D warnings` (in tools; these are the crates the
  owner's standard keeps clean).

## The device helper (SSH) without writing the password

- The SSH helper is an `expect` script at `/tmp/kbssh.exp` that contains the owner's password. It is NOT in any repo. It
  may be gone (`/tmp` is cleared at reboot). If it is missing, ask the owner for the password at the start of the device
  work and create the helper in `/tmp` only. Never write the password to a file in a repo, a log, a commit, or the chat.
- Run a command on the Kindle:
  `timeout 90 expect -f /tmp/kbssh.exp '<command>' 2>&1 | grep -v -i 'password\|spawn' | tail -n 20`
- The Kindle's own commands: `lipc-get-prop com.lab126.wifid cmState` (CONNECTED), `uptime`, `df -h /mnt/us /var/local`.
- Do not print `androidboot.serialno` values or the Wi-Fi MAC address (`/sys/class/net/wlan0/address`). Their presence is
  enough.
- Reboot without losing the SSH session: `nohup sh -c "sleep 2; sync; /sbin/reboot" >/dev/null 2>&1 &` as a separate
  command (a backgrounded reboot inside `&&` gets killed).
- Power off: `sync; /sbin/halt -f -p` (the launcher's Power menu uses this; `/sbin/poweroff` shows the stock "restarting"
  cover).

## Deploy wrappers (outside the repos, in `/tmp/kl-spikes/`; recreate them if missing)

Each wrapper is an `expect` script: it runs a shell command on the Mac, and answers the `Password:` prompt from
`/tmp/kbssh.exp`. Pattern (`deploy.exp`):

```
set timeout 900
set f [open /tmp/kbssh.exp]
set txt [read $f]
close $f
regexp {send -- "([^"]*)\\r"} $txt -> pw
cd /Users/doannguyen/Documents/GitHub/prai-workspace/doannt-kindle/doannt-kindle-launcher
spawn sh scripts/build-device.sh
expect {
    -re {[Pp]assword:} { send -- "$pw\r"; exp_continue }
    eof
}
catch wait result
exit [lindex $result 3]
```

- Launcher, patch build (0.4.x -> 0.4.x+1): `spawn sh scripts/build-device.sh` (the script bumps the patch, runs
  `cargo test`, runs `tests/supervisor-test.sh`, `tests/setup-boot-test.sh`, cross-builds, and installs over SSH with
  `deploy/install-ssh.sh`). Expect `deployed Primitive Launcher v0.x.y`. The install restarts a running launcher.
- Launcher, new phase: `spawn sh scripts/build-device.sh --minor`.
- Store: `spawn sh deploy/install-ssh.sh target/armv7-unknown-linux-musleabihf/release/store-app` in the store folder (after
  `cargo zigbuild ... -p store-app`). Expect `installed Primitive Store (<bytes> bytes, sha256 …)`.
- Browser: `spawn sh scripts/build-device.sh` in the browser folder (its own patch bump; deploys to `/mnt/us/browser`).
- The launcher deploy logs go to `/tmp/kl-spikes/deploy-launcher-<version>.log` (the wrapper's output).

## Reading the device's logs

- Launcher log: `/mnt/us/launcher/log-launcher.txt` (the device's `[kl]` lines and the supervisor's `[launcher …]` lines).
  Store lines: `grep -E "store|\[kl\] start" /mnt/us/launcher/log-launcher.txt | tail -n 20`.
- The store app prints its own lines through `kl_kindle::log` (stderr); the supervisor keeps stderr in the log file. Panics
  are not visible (stderr to `/dev/null` under the supervisor): the store's background threads catch panics and report them
  as an error message instead.
- Crash logs: none in the store app yet (task T3).

## Known traps (each one cost time in this session)

- A new `tools` commit is not seen by the launcher until the launcher's `tools` submodule is moved: `git -C tools fetch -q
  origin && git -C tools checkout -q <commit>`, then commit the submodule pointer in the launcher.
- Cargo inheritance: the shared crates use `version.workspace = true` and `libc.workspace = true`. A workspace that consumes
  them must define the same `[workspace.package]` and `[workspace.dependencies]` (tools defines them; the store copies
  nothing: it uses the tools submodule).
- `include_bytes!` paths in `kl-core` and `kl-render` point at `../../../assets/` (the tools root's `assets/`). Keep the
  files there.
- The store's `cargo test` on the device-target crates needs the host toolchain; the launcher's `tests/*.sh` run on the Mac.
- Python string escapes: when a script writes Rust `\u{2039}` inside a Python `'''` string, Python fails. Use the literal
  character.
- `sed -i ''` (BSD sed) needs the empty argument on macOS.
- `git add` of a deleted path fails (`pathspec did not match`): stage deletions with `git add -A -- <file>` for files that
  still exist, and `git rm -- <file>` for removed ones. Check `git status --porcelain` after staging.
- GitHub Pages: the workflow cannot enable Pages itself; the owner sets Source to GitHub Actions once.
- GitHub release assets redirect to `release-assets.githubusercontent.com` (signed). The store's allow list includes it.
  Any new host a download goes through must be added to `primitive-net`'s `Policy::store` and to the store's documentation.
