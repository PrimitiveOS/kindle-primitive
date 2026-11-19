#!/usr/bin/env python3
"""Sign a private simulation catalog with a disposable key and run the Store package test."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "doannt-kindle-tools"


def build_signer():
    command = [
        "cargo", "build", "--offline", "--locked", "-p", "kl-store",
        "--example", "sign-store-catalog", "--message-format=json",
    ]
    build = subprocess.run(command, cwd=TOOLS, text=True, stdout=subprocess.PIPE, check=True)
    for line in build.stdout.splitlines():
        artifact = json.loads(line)
        if (artifact.get("reason") == "compiler-artifact"
                and artifact["target"]["name"] == "sign-store-catalog"
                and artifact.get("executable")):
            return artifact["executable"]
    raise RuntimeError("Cargo did not report the signer executable")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("simulation", type=Path)
    simulation = parser.parse_args().simulation.resolve(strict=True)
    review = simulation / "catalog-review"
    receipts = json.loads((review / "receipts.json").read_text(encoding="utf-8"))
    if not receipts:
        raise ValueError("The private review has no candidate archives")
    packages = simulation / "packages"
    signer = build_signer()

    with tempfile.TemporaryDirectory(prefix="primitive-signed-catalog-") as directory:
        work = Path(directory)
        site = work / "site"
        shutil.copytree(review / "site/v1", site,
                        ignore=shutil.ignore_patterns("index.sig.json", "packages"))
        private_key, public_key = work / "key.pkcs8", work / "trusted.pub"
        subprocess.run([signer, "keygen", private_key, public_key], check=True)
        subprocess.run([signer, "index", private_key, site], check=True)
        for receipt in receipts.values():
            archive = (simulation / receipt["archive"]).resolve(strict=True)
            target = site / "packages" / archive.relative_to(packages)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(archive)
            subprocess.run([signer, "package", private_key, target], check=True)
        print(f"Signed the private catalog and {len(receipts)} ARMHF archives", flush=True)

        env = {
            **os.environ,
            "KL_TEST_PACKAGE_SET": str(packages),
            "KL_TEST_CATALOG_SITE": str(site),
            "KL_TEST_CATALOG_PUBLIC_KEY": str(public_key),
        }
        subprocess.run([
            "cargo", "test", "--offline", "--locked", "-p", "kl-store",
            "--test", "local_package_set", "--", "--nocapture",
        ], cwd=TOOLS, env=env, check=True)
        env.update({
            "KL_STORE_BOOTSTRAP_PACKAGE": str(simulation / receipts["primitive-store"]["archive"]),
            "KL_STORE_BOOTSTRAP_CATALOG": str(site),
        })
        subprocess.run([
            "cargo", "test", "--offline", "--locked", "-p", "kl-launcher",
            "bootstrap_installs_the_staged_store_archive", "--", "--nocapture",
        ], cwd=ROOT / "doannt-kindle-launcher", env=env, check=True)


if __name__ == "__main__":
    main()
