# Private Store catalog review

Start with a Mac simulation directory containing the ARMHF packages and desktop captures. Run these commands from
the umbrella checkout with Pillow and `jsonschema` installed in the Python environment. [Local verification guide](local-verification.md)

```sh
sh scripts/simulate.sh build/simulation --packages
python3 scripts/build-local-catalog.py build/simulation
```

The generator uses the catalog's listing, image, index and archive checks. It reads each package's manifest,
measures the ZIP size, and verifies the SHA-256 against its sidecar. `build/simulation/catalog-review/receipts.json` records the
results by app ID. Keep one ARMHF release candidate per app in the simulation package directory. Use
`--date YYYY-MM-DD` to reproduce the catalog dates for a specific review.

The review includes Launcher, Browser, Store, Hello, the thirteen native apps, the existing KOReader link, and
Terminal for private review. Candidate listings use `.invalid` asset URLs and leave `tested_on` empty. The Store
and native icons use the artwork proposals in `build/simulation/proposals/` when available. A simulation without
proposals uses letter tiles. Public listing text, artwork, compatibility claims, and Terminal's inclusion require
owner approval.

Run a Store cache refresh from the generated API and install each real archive using its cached listing.

```sh
simulation=$(cd build/simulation && pwd)
(
    cd doannt-kindle-tools
    KL_TEST_PACKAGE_SET="$simulation/packages" \
    KL_TEST_CATALOG_SITE="$simulation/catalog-review/site/v1" \
        cargo test --offline --locked -p kl-store --test local_package_set -- --nocapture
)
```

To see the listings in the desktop Store, render the review catalog in a separate capture folder.

```sh
(
    cd doannt-kindle-launcher
    cargo run --offline --locked -q -p kl-desktop -- \
        --documents "$simulation/documents" \
        --catalog "$simulation/catalog-review" \
        --out "$simulation/previews/catalog-review"
)
```
