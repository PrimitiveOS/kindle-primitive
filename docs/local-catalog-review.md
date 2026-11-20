# Private Store catalog review

Run the ARMHF simulation from the PrimitiveOS checkout with Pillow and `jsonschema` installed. It builds the review,
refreshes and installs from it in both verification modes, and renders the desktop Store captures.
[Local verification guide](local-verification.md)

```sh
sh scripts/simulate.sh build/simulation --packages
```

The generator uses the catalog's listing, image, index and archive checks. It reads each package's manifest,
measures the ZIP size, and verifies the SHA-256 against its sidecar. `build/simulation/catalog-review/receipts.json` records the
results by app ID. Keep one ARMHF release candidate per app in the simulation package directory. Use
`--date YYYY-MM-DD` to reproduce the catalog dates for a specific review.

The baseline review covers the package set in [`scripts/simulate.sh`](../scripts/simulate.sh) and the KOReader link.
Candidate listings use `.invalid` asset URLs and leave `tested_on` empty. The generator looks for artwork in
`build/simulation/proposals/` and uses letter tiles when no proposed image is available.

For the 20 November 2026 **Study and work** releases, the published packages were checked with a separate fixture
containing those eleven app IDs. See [the release checks](local-verification.md#study-and-work-release-verification).
The public index and collections serve the approved listings and artwork. [Live Store catalog](https://primitiveos.github.io/kindle-primitive-catalog/v1/index.json)

To rebuild the review and repeat the signed verification from existing simulation output, run these commands.

```sh
python3 scripts/build-local-catalog.py build/simulation
python3 scripts/verify-signed-local-catalog.py build/simulation
```

The signed check creates and removes its own temporary key and proofs. The unsigned API, receipts, screenshots, and
the signed and unsigned test logs remain in the simulation output. [Store signature format](store-signatures.md)
