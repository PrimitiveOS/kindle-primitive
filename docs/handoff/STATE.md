# State at handoff (2026-11-19)

All paths are under `/Users/doannguyen/Documents/GitHub/prai-workspace/doannt-kindle/` (the umbrella folder). Each folder
is its own git repository, ignored by the umbrella repo (`/doannt-kindle-*/` in its `.gitignore`).

## Repositories

| Folder | GitHub remote | Branch | Last commit | Role |
|---|---|---|---|---|
| `doannt-kindle` | `DoanNguyenTrong/kindle-primitive` | main | `582aea5`+ (see `git log`) | Umbrella: README, plans, store docs, skills (`.agents/skills`, linked `.claude/skills`), store screenshots (`docs/store-screens/`). |
| `doannt-kindle-launcher` | `DoanNguyenTrong/kindle-primitive-launcher` | main | `b7ae2d7` | Primitive Launcher 0.4.4 (on the Kindle). Its program only; uses the shared kit from tools. Release tags `v0.3.12`, `v0.3.20`. |
| `doannt-kindle-tools` | `DoanNguyenTrong/kindle-primtitive-tools` (sic) | main | `cdb95ae` | The shared kit: `kl-core` (screens, layout, store model), `kl-render` (renderer), `kl-kindle` (device layer, library), `kl-store` (store engine), `primitive-net` (downloads), `primitive-keyboard`, `primitive-quick`. Uncommitted: `Cargo.lock` (modified). |
| `doannt-kindle-store` | `DoanNguyenTrong/kindle-primitive-store` | main | `2aa7465` | **Primitive Store 0.1.0**: the store app (`crates/store-app`), `deploy/Store.sh`, `deploy/install-ssh.sh`. Submodule `tools/`. No tags yet. |
| `doannt-kindle-catalog` | `DoanNguyenTrong/kindle-primitive-catalog` | main | `b812933` | The public catalog: `apps/` (published), `drafts/` (not published), `schema/`, `scripts/`, CI `catalog.yml` (publishes GitHub Pages). |
| `doannt-kindle-build` | `DoanNguyenTrong/kindle-primitive-build` | main | `57a873a` | The shared packager (`scripts/package.py`) and the reusable release workflow (`.github/workflows/package.yml`). |
| `doannt-kindle-browser` | `DoanNguyenTrong/kindle-primitive-browser` | main | `bc66135` | Primitive Browser 0.2.17, tag `v0.2.17` (release published, store package asset). Uncommitted, not ours to commit: `docs/tinhte/` (owner's), `build/`, `dist-store/` (local leftovers: do not commit). |
| `doannt-kindle-terminal` | `DoanNguyenTrong/kindle-primitive-terminal` | main | `5bd4f20` | Primitive Terminal 0.1.8. No licence file, no CI, no tags. Not touched in this session. |
| `docs/handoff/` (inside the umbrella) | umbrella remote `DoanNguyenTrong/kindle-primitive` | main | see the umbrella's `git log` | These handoff documents. There is no separate handoff repo. |

Licences: launcher, browser, store code: PolyForm Noncommercial 1.0.0 (launcher and browser releases up to v0.3.20 and
v0.2.16 are AGPL-3.0). Docs and pictures: CC BY-NC-SA 4.0. Tools: AGPL-3.0 or PolyForm (dual). The KOReader icon in the
catalog is KOReader's own, AGPL-3.0, credited.

## Versions

- Launcher: `0.4.4` in `Cargo.toml` (Kindle runs 0.4.4). A device build bumps the patch version (see RULES.md).
- Store: `0.1.0` (not deployed as a package; installed by its own script onto the Kindle).
- Browser: `0.2.17` (on the Kindle from the USB install; the store package of 0.2.17 is published).
- Catalog listings: `koreader` (a link listing: the store shows it, installs nothing), `primitive-browser` (hosted, 0.2.17).

## Catalog and GitHub

- Pages: live. `https://doannguyentrong.github.io/kindle-primitive-catalog/v1/index.json` lists `koreader` and
  `primitive-browser`. Icons at `.../v1/icons/<id>.png`, listings at `.../v1/apps/<id>.json`, screenshots at
  `.../v1/shots/<id>-<n>.png`. The Pages source was set to GitHub Actions by the owner (a manual step; the workflow token
  cannot enable Pages).
- Browser release `v0.2.17`: `https://github.com/DoanNguyenTrong/kindle-primitive-browser/releases/download/v0.2.17/primitive-browser-0.2.17-armhf.zip`
  (9,504,649 bytes, SHA-256 `7be3aa25ef743affac5704dcaad7c8fccf5a0180467064631e061c5ba6b6928b`). Checked by download.
  The release also has the old USB zip (`primitive-browser`/`browser` layout from `scripts/package-release.sh`).
- No `gh` CLI on this Mac. The GitHub API is rate-limited from this network; read run status from the public pages only
  (or ask the owner). Actions runs: `https://github.com/DoanNguyenTrong/<repo>/actions`.

## The Kindle (Oasis 3, the only tested device)

- Address `192.168.1.28`, SSH port `2222`, root login. The password is the owner's; see ENVIRONMENT.md. Never write it down.
- Firmware `5.18.2` (`/etc/prettyversion.txt`). Hard-float (`/lib/ld-linux-armhf.so.3` present). Architecture `armhf`.
- Storage: `/mnt/us` (user storage, FUSE `fsp`, about 4.9 GB free); `/var/local` (240 MB, 164 MB free).
- Installed (as of this handoff; re-check with SSH): launcher `0.4.4` at `/mnt/us/launcher/kl-launcher` (deployed
  from the build before the kit move; the kit move changed no behaviour; see the deploy log of 0.4.4); store `0.1.0` at
  `/mnt/us/store/bin/kl-store-app` (sha256 `e3ddd257…`); library entries in `/mnt/us/documents/`: `Launcher.sh`,
  `Primitive Browser.sh`, `Terminal.sh`, `KOReader.sh` (+ `.sdr`), `Store.sh` (the store's entry).
- The launcher's data: `/mnt/us/launcher/` (settings, `apps.toml`, `cache/`, `store/` with `cache/`, `downloads/`,
  `installed.json` (the record), `journal.json`, `staging/`).
- The boot job `/etc/upstart/primitive-launcher.conf` is installed (launcher `setup-boot` writes it on open); `/var/local/
  primitive-launcher/` is the boot-time copy of the launcher.
- Not installed through the store yet: nothing. The browser on the Kindle came from the USB install, not the store. A store
  install of the browser would replace the same files and then show Remove.

## Store app on the Kindle: not yet tested by the owner

The store `0.1.0` was installed by `deploy/install-ssh.sh` (see ENVIRONMENT.md) on 2026-11-19. The owner has not opened it
yet. The launcher still has its own built-in Store tile (the old store inside the launcher, 0.4.4). Two Store icons therefore
appear until the bootstrap change (PIPELINE.md, step P5).

## Known open facts about the device

- A4.4 HTTPS from the Kindle: works for the catalog (refresh, 1 app, 0 failed on 0.4.0). Download speed and memory for a
  9.5 MB package: not measured.
- A4.3 device identity: the device type text is "Kindle Oasis – 10th Gen" (stock help files), i.e. the Oasis 3, mapped to
  the store name `KindleOasis3`. No model code file. Identifiers (serial, Wi-Fi MAC) exist and are never recorded.
- Wi-Fi state is read from `com.lab126.wifid` `cmState` (`CONNECTED`) and `enable`.
