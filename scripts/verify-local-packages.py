#!/usr/bin/env python3
"""Verify the local packages and the executable architecture they declare."""

import hashlib
import json
import stat
import struct
import sys
import zipfile
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema/manifest.schema.json").read_text())
MAIN_BINARIES = {"primitive-launcher": "kl-launcher", "primitive-store": "kl-store-app",
                 "primitive-browser": "kb-kindle", "primitive-terminal": "kt-terminal"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(archive):
    checksum = archive.with_suffix(".zip.sha256").read_text().split()
    require(len(checksum) == 2 and checksum[1] == archive.name, "invalid checksum sidecar")
    with archive.open("rb") as data:
        actual = hashlib.file_digest(data, "sha256").hexdigest()
    require(checksum[0] == actual, "checksum mismatch")
    with zipfile.ZipFile(archive) as package:
        require(package.testzip() is None, "bad ZIP entry")
        manifests = [info for info in package.namelist() if info.count("/") == 1 and info.endswith("/manifest.json")]
        require(len(manifests) == 1, "expected one top-level manifest")
        manifest = json.loads(package.read(manifests[0]))
        Draft202012Validator(SCHEMA).validate(manifest)
        base = f'{manifest["id"]}-{manifest["version"]}'
        arch = manifest["arch"]
        require(archive.name == f"{base}-{arch}.zip" and manifests[0] == f"{base}/manifest.json", "ZIP name and manifest disagree")
        members = package.infolist()
        paths = set()
        installed = set()
        for member in members:
            name = member.filename.removesuffix("/")
            parts = PurePosixPath(name).parts
            require(name not in paths, f"duplicate path {name}")
            paths.add(name)
            require(parts and parts[0] == base and "/".join(parts) == name and ".." not in parts and "\\" not in name, f"invalid path {name}")
            if member.is_dir():
                continue
            mode = member.external_attr >> 16
            require(stat.S_ISREG(mode), f"not a regular file: {name}")
            rel = "/".join(parts[1:])
            if rel == "manifest.json" or rel == "INSTALL.md" or rel.startswith("LICENSE") or rel.startswith("hooks/"):
                continue
            installed.add(rel)
        require(installed == set(manifest["files"]), "ZIP entries and manifest file list differ")
        app_id = manifest["id"]
        binary_name = MAIN_BINARIES.get(app_id, manifest["dir"] + "-kindle")
        binaries = [name for name in installed if name.rsplit("/", 1)[-1] == binary_name]
        require(len(binaries) == 1, f"missing executable {binary_name}")
        entry = package.getinfo(f"{base}/{binaries[0]}")
        require(entry.external_attr >> 16 & stat.S_IXUSR, "executable bit is missing")
        with package.open(entry) as source:
            elf = source.read(52)
        require(elf.startswith(b"\x7fELF\x01\x01") and struct.unpack_from("<H", elf, 18)[0] == 40, "executable is not little-endian 32-bit ARM ELF")
        flags = struct.unpack_from("<I", elf, 36)[0]
        require(flags & 0x600 == (0x400 if arch == "armhf" else 0x200), "ELF float ABI differs from manifest")
        for name in installed:
            if name.startswith("documents/") and name.endswith(".sh"):
                entry = package.getinfo(f"{base}/{name}")
                with package.open(entry) as source:
                    header = source.read(256)
                require(header.startswith(b"#!/bin/sh\n# Name:") and b"\n# Author:" in header, f"invalid scriptlet header: {name}")
        print(f"{archive.name}\t{archive.stat().st_size}\t{actual}")


def main():
    root = Path(sys.argv[1])
    packages = sorted(root.rglob("*.zip"))
    require(packages, f"no packages in {root}")
    for archive in packages:
        try:
            verify(archive)
        except (ValueError, OSError, zipfile.BadZipFile) as error:
            raise SystemExit(f"{archive}: {error}") from None


if __name__ == "__main__":
    main()
