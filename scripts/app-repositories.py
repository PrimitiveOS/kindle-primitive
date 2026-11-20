"""Resolve a stable PrimitiveOS package ID to its GitHub repo and local checkout."""

import json
import re

REPOSITORY_BASE = "https://github.com/DoanNguyenTrong/kindle-primitive-"
REPOSITORY_SLUGS = {
    "primitive-crateshift": "crate-shift",
    "primitive-hello": "app-template",
    "primitive-memorypairs": "memory-match",
    "primitive-picturelogic": "nonogram",
    "primitive-tidefork": "2048",
}


def repository_slug(workspace, app_id):
    if app_id in REPOSITORY_SLUGS:
        return REPOSITORY_SLUGS[app_id]
    # The catalog is optional for local archive verification.
    listing_path = workspace / "doannt-kindle-catalog" / "apps" / app_id / "app.json"
    try:
        listing = json.loads(listing_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        listing = {}
    if isinstance(listing, dict) and listing.get("id") == app_id and listing.get("source") == "hosted":
        repo = listing.get("repo")
        if isinstance(repo, str) and repo.startswith(REPOSITORY_BASE):
            slug = repo.removeprefix(REPOSITORY_BASE)
            if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                return slug
    return app_id.removeprefix("primitive-")


def repository_url(workspace, app_id):
    return REPOSITORY_BASE + repository_slug(workspace, app_id)


def local_checkout(workspace, app_id):
    canonical = workspace / f"doannt-kindle-{repository_slug(workspace, app_id)}"
    legacy = workspace / f"doannt-kindle-{app_id.removeprefix('primitive-')}"
    # An older workspace can still check its existing packages before moving its checkout.
    if canonical.is_dir() or not legacy.is_dir():
        return canonical
    return legacy
