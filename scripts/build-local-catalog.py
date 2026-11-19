#!/usr/bin/env python3
"""Build and validate a private ARMHF catalog from Mac simulation output."""

import argparse
import hashlib
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from jsonschema import Draft202012Validator
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "doannt-kindle-catalog"
SITE = "https://catalog.invalid/v1"
NATIVE_SCREENS = {
    "blocks": ("blocks.png", "blocks-playing-dark.png"),
    "calculator": ("calculator.png", "calculator-history.png"),
    "cards": ("cards-decks.png", "cards-question.png"),
    "cascade": ("cascade-paused.png", "cascade-pace.png"),
    "chess": ("chess-moves.png", "chess-dark.png"),
    "crossword": ("crossword.png", "crossword-clues.png"),
    "focus": ("focus.png", "focus-running-dark.png"),
    "hello": ("hello.png", "hello-dark.png"),
    "minesweeper": ("minesweeper.png", "minesweeper-game-dark.png"),
    "notes": ("notes-list.png", "notes-edit.png"),
    "ships": ("ships.png", "ships-fleet.png"),
    "solitaire": ("solitaire.png", "solitaire-dark.png"),
    "sudoku": ("sudoku.png", "sudoku-notes-dark.png"),
    "words": ("words-daily.png", "words-dark.png"),
}
SYSTEM_SCREENS = {
    "browser": ("browser/home.png",),
    "launcher": ("launcher/home-1.png", "launcher/quick-settings.png"),
    "store": ("launcher/store-today.png", "launcher/store-search-keyboard.png"),
    "terminal": ("terminal/terminal.png",),
}
REVIEW_README = """# Private catalog review

These listings use locally built ARMHF archives and desktop captures. Asset URLs use the reserved `catalog.invalid`
domain. Candidate device-test lists are empty. Native app and Store icons are proposals or local letter placeholders.
Terminal is included for private review of its package and listing.

- `apps/` contains each listing and its images in the catalog's source layout.
- `site/v1/` contains the generated index, collections, and assets for the Store cache test.
- `receipts.json` records actual ZIP sizes and hashes, with archive paths relative to the simulation directory.
"""


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def system_draft(module):
    if module == "launcher":
        return load(CATALOG / "drafts/primitive-launcher/app.json")
    if module == "browser":
        return load(CATALOG / "apps/primitive-browser/app.json")

    is_store = module == "store"
    return {
        "schema": 1,
        "id": f"primitive-{module}",
        "dir": module,
        "name": "Store" if is_store else f"Primitive {module.title()}",
        "subtitle": "Find apps for your Kindle" if is_store else "Run shell commands on Kindle",
        "developer": {"name": "Primitive AI", "url": "https://github.com/DoanNguyenTrong"},
        "categories": ["system" if is_store else "developer"],
        "description": (
            "Browse apps, see what they change and install them over Wi-Fi. "
            "Use Updates to keep your apps current or remove apps you no longer want."
            if is_store else
            "Type a shell command on the on-screen keyboard and read its output. "
            "Primitive Terminal opens from the Kindle library and can also run from Primitive Launcher."
        ),
        "repo": f"https://github.com/DoanNguyenTrong/kindle-primitive-{module}",
        "licence": "PolyForm-Noncommercial-1.0.0" if is_store else "AGPL-3.0-only",
        "source": "hosted",
        "icon": "icon.png",
        "changes": {
            "network": is_store,
            "stops_kindle_ui": False,
            "starts_at_boot": False,
            "root_filesystem": False,
            "hooks": False,
            "notes": ("Checks the catalog and installs or removes app files in user storage."
                      if is_store else "Runs shell commands you enter."),
        },
        "versions": [],
    }


def release_notes(changelog, version, draft):
    for previous in draft["versions"]:
        if previous["version"] == version and previous["notes"]:
            return previous["notes"]
    text = changelog.read_text(encoding="utf-8")
    heading = re.escape(version)
    match = re.search(rf"^## \[?{heading}\]?(?:[ \t].*)?$", text, re.MULTILINE)
    if match is None:
        return "Local build for package and desktop review."
    section = re.split(r"^## ", text[match.end():], maxsplit=1, flags=re.MULTILINE)[0]
    lines = re.findall(r"^- (.+(?:\n  [^\n]+)*)", section, re.MULTILINE)
    notes = "\n".join(" ".join(line.split()) for line in lines[:5])[:500].rstrip()
    return notes or "Local build for package and desktop review."


def archive_version(simulation, app_id, review_date, changelog, draft, checks, validator):
    archives = sorted((simulation / "packages" / app_id).glob("*-armhf.zip"))
    if len(archives) != 1:
        raise ValueError(f"{app_id}: expected exactly one ARMHF archive, found {len(archives)}")
    archive = archives[0]
    receipt = archive.with_suffix(".zip.sha256").read_text(encoding="utf-8").split()
    size = archive.stat().st_size
    if not 0 < size <= checks["MAX_BYTES"]:
        raise ValueError(f"{archive}: exceeds the catalog's ZIP size limit")
    with archive.open("rb") as source:
        checksum = hashlib.file_digest(source, "sha256").hexdigest()
    if receipt != [checksum, archive.name]:
        raise ValueError(f"{archive}: SHA-256 sidecar does not match the archive")
    top = archive.name.removesuffix("-armhf.zip")
    with zipfile.ZipFile(archive) as zipped:
        member = zipped.getinfo(f"{top}/manifest.json")
        if member.file_size > checks["MAX_MANIFEST"]:
            raise ValueError(f"{archive}: manifest exceeds the catalog's size limit")
        manifest = json.loads(zipped.read(member))
    asset = {"url": f"{SITE}/packages/{app_id}/{archive.name}", "sha256": checksum, "size": size}
    version = {
        "version": manifest["version"],
        "date": review_date,
        "notes": release_notes(changelog, manifest["version"], draft),
        "firmware": manifest["firmware"],
        "requires": manifest.get("requires", {}),
        "tested_on": [],
        "assets": {"armhf": asset},
    }
    checks["validate_package"](archive, draft, version, "armhf", validator)
    return version, {"archive": archive.relative_to(simulation).as_posix(), **asset}


def image_for_review(source, target, size):
    with Image.open(source, formats=["PNG"]) as image:
        if image.width * size[1] != image.height * size[0]:
            raise ValueError(f"{source}: unexpected aspect ratio for {size[0]} × {size[1]} output")
        foreground = image.convert("RGBA")
        background = Image.new("RGBA", foreground.size, "white")
        background.alpha_composite(foreground)
        gray = background.convert("L").resize(size, Image.Resampling.LANCZOS)
        gray.save(target, optimize=True)


def icon_for_review(module, simulation, target):
    own_icons = {
        "browser": CATALOG / "apps/primitive-browser/icon.png",
        "launcher": CATALOG / "drafts/primitive-launcher/icon.png",
        "terminal": ROOT / "doannt-kindle-terminal/assets/terminal-icon.png",
    }
    icon = own_icons.get(module, simulation / "proposals" / f"{module}.png")
    if icon.is_file():
        image_for_review(icon, target, (256, 256))
        return
    # Match the Store's letter tile when a fresh simulation has no icon proposals yet.
    image = Image.new("L", (256, 256), "white")
    font = ImageFont.truetype(ROOT / "doannt-kindle-launcher/assets/fonts/NotoSans-Bold.ttf", 136)
    ImageDraw.Draw(image).text((128, 124), module[0].upper(), fill="black", font=font, anchor="mm")
    image.save(target, optimize=True)


def build_review(simulation, staging, review_date):
    checks = runpy.run_path(str(CATALOG / "scripts/check-assets.py"))
    validator = Draft202012Validator(load(CATALOG / "schema/manifest.schema.json"))
    reference = staging / "apps/koreader"
    shutil.copytree(CATALOG / "apps/koreader", reference)
    listing = load(reference / "app.json")
    for version in listing["versions"]:
        version["tested_on"] = []
    dump(reference / "app.json", listing)
    receipts = {}
    for module in sorted(NATIVE_SCREENS.keys() | SYSTEM_SCREENS.keys()):
        repo = ROOT / f"doannt-kindle-{'app-template' if module == 'hello' else module}"
        if module in NATIVE_SCREENS:
            draft = load(repo / "app.json")
            screens = [f"{module}/{name}" for name in NATIVE_SCREENS[module]]
        else:
            draft = system_draft(module)
            screens = SYSTEM_SCREENS[module]

        app_id = f"primitive-{module}"
        if draft["id"] != app_id:
            raise ValueError(f"{app_id}: draft id disagrees with its package directory")
        changelog = repo / ("docs/CHANGELOG.md" if module in ("browser", "launcher") else "CHANGELOG.md")
        version, receipts[app_id] = archive_version(
            simulation, app_id, review_date, changelog, draft, checks, validator
        )
        draft["versions"] = [version]
        folder = staging / "apps" / app_id
        (folder / "shots").mkdir(parents=True)
        icon_for_review(module, simulation, folder / "icon.png")
        shots = [simulation / "previews" / name for name in screens]
        if module == "browser":
            shots.append(repo / "docs/images/real_reading_view.png")
        draft["screenshots"] = []
        for index, shot in enumerate(shots, 1):
            name = f"shots/{index}.png"
            image_for_review(shot, folder / name, (632, 840))
            draft["screenshots"].append(name)
        dump(folder / "app.json", draft)
        print(f"ok   {app_id} {version['version']} armhf", flush=True)

    collections = load(CATALOG / "collections.json")
    for collection in collections["collections"]:
        if collection["id"] == "start-here":
            collection["apps"] = ["primitive-launcher", "primitive-browser", "koreader"]
        if collection["id"] == "made-by-primitive":
            collection["apps"] = [app for app in sorted(receipts) if app != "primitive-terminal"]
    dump(staging / "collections.json", collections)
    dump(staging / "receipts.json", receipts)
    (staging / "README.md").write_text(REVIEW_README, encoding="utf-8")

    scripts = staging / "scripts"
    scripts.mkdir()
    builder = scripts / "build-index.py"
    shutil.copyfile(CATALOG / "scripts/build-index.py", builder)
    shutil.copytree(CATALOG / "schema", staging / "schema")
    subprocess.run([
        sys.executable, "-I", str(builder), "--out", str(staging / "site/v1"),
        "--base-url", SITE, "--now", f"{review_date}T00:00:00Z",
    ], check=True)
    shutil.rmtree(scripts)
    shutil.rmtree(staging / "schema")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulation", type=Path, help="output directory from simulate.sh --packages")
    parser.add_argument("--date", type=date.fromisoformat, default=date.today(), help="review date (YYYY-MM-DD)")
    args = parser.parse_args()
    simulation = args.simulation.resolve(strict=True)
    output = simulation / "catalog-review"
    try:
        with tempfile.TemporaryDirectory(prefix=".catalog-review-", dir=simulation) as work:
            staging = Path(work) / "catalog-review"
            previous = Path(work) / "previous-review"
            build_review(simulation, staging, args.date.isoformat())
            if output.exists() or output.is_symlink():
                if output.is_symlink() or not (output / "README.md").read_text(encoding="utf-8").startswith("# Private catalog review\n"):
                    raise ValueError(f"{output}: expected a previously generated catalog review")
                if {entry.name for entry in output.iterdir()} != {entry.name for entry in staging.iterdir()}:
                    raise ValueError(f"{output}: contains files outside the generated catalog review")
                output.rename(previous)
            try:
                staging.rename(output)
            except OSError:
                if previous.is_dir() and not output.exists():
                    previous.rename(output)
                raise
    except (KeyError, OSError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        raise SystemExit(str(error)) from None
    print(f"Private catalog review: {output}")


if __name__ == "__main__":
    main()
