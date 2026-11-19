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
HELPER_EXECUTABLES = {
    "primitive-launcher": "launcher/ssh/bin/dropbear",
    "primitive-browser": "browser/bin/fbink",
}
LAUNCHER_ZLIB = "launcher/ssh/lib/libz.so.1"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_elf(archive, entry, arch, must_be_static, required):
    with archive.open(entry) as source:
        header = source.read(52)
        if not header.startswith(b"\x7fELF") and not required:
            return
        require(len(header) == 52 and header.startswith(b"\x7fELF\x01\x01")
                and struct.unpack_from("<H", header, 18)[0] == 40,
                f"not little-endian 32-bit ARM ELF: {entry.filename}")
        flags = struct.unpack_from("<I", header, 36)[0]
        require(flags & 0x600 == (0x400 if arch == "armhf" else 0x200),
                f"ELF float ABI differs from manifest: {entry.filename}")
        if must_be_static:
            offset = struct.unpack_from("<I", header, 28)[0]
            size, count = struct.unpack_from("<HH", header, 42)
            require(size == 32 and count > 0 and offset + size * count <= entry.file_size,
                    f"invalid ELF program headers: {entry.filename}")
            source.seek(offset)
            for _ in range(count):
                program_header = source.read(size)
                segment_type = struct.unpack_from("<I", program_header)[0]
                require(segment_type not in (2, 3), f"ELF needs a dynamic loader: {entry.filename}")


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
        required_executables = {binaries[0]}
        if app_id in HELPER_EXECUTABLES:
            required_executables.add(HELPER_EXECUTABLES[app_id])
        required_elf = set(required_executables)
        if app_id == "primitive-launcher" and arch == "armhf":
            required_elf.add(LAUNCHER_ZLIB)
        if app_id == "primitive-launcher" and arch == "armel":
            require(LAUNCHER_ZLIB not in installed, "ARMEL Launcher should use its statically linked zlib")
        require(required_elf <= installed, f"missing ARM file(s): {', '.join(sorted(required_elf - installed))}")
        for name in sorted(installed):
            entry = package.getinfo(f"{base}/{name}")
            if name in required_executables:
                require(entry.external_attr >> 16 & stat.S_IXUSR, f"executable bit is missing: {name}")
            verify_elf(package, entry, arch, arch == "armel" and name in required_executables, name in required_elf)
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
