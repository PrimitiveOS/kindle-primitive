# The owner's rules (from the whole session; follow them exactly)

## Secrets and privacy

- The SSH password is the owner's. It lives only in the `/tmp` helper (ENVIRONMENT.md). Never in a repo, a file, a log, a
  commit message, a diff, or the chat. Scan staged diffs for it before every commit:
  `pw=$(grep -o 'send -- "[^"]*\\r"' /tmp/kbssh.exp | head -n 1 | sed 's/send -- "//; s/\\r"$//'); git diff --cached | grep -q -F -- "$pw" && echo SECRET FOUND`
  (A digit-only password false-matches hex tables: check any hit by hand before reacting.)
- Wi-Fi keys (PSK values) are never printed or logged. Serial numbers and MAC addresses are never recorded.
- The repos are public. Scan for personal data (emails, LAN addresses other than the Kindle's own, identifiers) too.
- Credentials for GitHub: the agent does not create releases, tags, or repos without the owner (see "Releases").

## Git

- Stage explicit paths only. Never `git add` a whole directory (the owner's own work shares the trees). Use
  `git add -- <file>` per file, and check `git status --porcelain` before committing. Deleted files: `git rm -- <file>`.
- Never commit build leftovers: `build/`, `dist-store/`, `target/`, the owner's `docs/tinhte/` (browser).
- Commit along the way (the owner asked this for the handoff in `docs/handoff/`). Use short, factual messages that say what changed
  and why, and end each commit message with the attribution line:
  the attribution line the current system reminder specifies (at handoff: `Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>`).
- Feature branches for each piece of work (`feature/<name>`, `fix/<name>`). Pushes: push feature branches freely. Merge to
  `main` and push `main` only when the owner has said so in the conversation (for example "merge them to main now"). The
  handoff's PIPELINE.md does not approve merges to `main`; report the branch ready and wait.
- Tags and GitHub releases: only with the owner's go-ahead ("push and release" was given for the launcher; the browser's
  `v0.2.17` was approved as "publish primitive browser as a store package").

## Device work

- Set up PrimitiveOS by manually installing Primitive Launcher once. Copy `launcher/` to the Kindle drive root and
  `documents/Launcher.sh` to the existing `documents/` folder. Use Store for subsequent app installs.
- Leave an installed Launcher in place unless the owner directly requests a Launcher change. Use the existing Launcher
  to open and verify Store and other apps.
- Every device build bumps the patch version (`scripts/build-device.sh`); a new phase starts a minor version
  (`--minor`). The store app has its own version (`0.1.0` now), bumped by hand in its `Cargo.toml` and CHANGELOG.
- A device deploy changes what the owner tests. The owner asked: do not deploy until the owner has said so; the owner
  reviews screens on the Mac first (desktop screenshots). When the owner is present, a deploy is fine.
- The owner asked for fewer launcher deploys: the store must deploy by itself (its own install script), and the launcher
  must not need a rebuild for store changes.
- The owner is the test. For a step on the Kindle, prepare it on the Mac first, then ask the owner for the one hand action.
  Report what the log shows (grep the launcher log) and what the owner reports on screen.

## Design and UX

- The store follows the App Store's structure (Today, Apps, Updates, a product page with an information strip, screenshots,
  About, Information) with the e-ink rules of the `primitive-ui` skill (`doannt-kindle/.agents/skills/primitive-ui`). The
  owner rejected a settings-style list design.
- Icons: design first, show the owner the design (a PNG or a desktop screenshot), and ask permission before applying it.
  The KOReader icon is KOReader's stock icon (the owner decided this).
- Every visible string: plain words, sentence case, no jargon ("Installed", "Get", "Update", "Remove from this Kindle").
- Any action that cannot be undone (remove, power off) asks twice (the store's Remove needs two taps).
- A notice must appear on the screen for each outcome (the owner could not see a failed install before).

## Products and licences

- Our code is PolyForm Noncommercial 1.0.0; our docs and pictures are CC BY-NC-SA 4.0. Do not copy third-party code or
  pictures into our repos without the owner's decision. KindleForge's packages are CC BY-NC-SA: link, do not re-host.
- Each store listing names its licence and its developer. Our apps are credited "Primitive AI" (developer) and "Packaged by
  Primitive" where it applies.
- Documents for other people start with a one-line audience statement in the chat message that hands them over (never in
  the file).

## How to decide

- The owner said: act without asking for requested actions; pause only when a real decision or a hand action on the device is
  needed. Make the best reasoned decision otherwise, and list the decisions made in the final report.
- Name the reading you took when a request is ambiguous (for example: "the test was taken as: do not test on hardware now").
