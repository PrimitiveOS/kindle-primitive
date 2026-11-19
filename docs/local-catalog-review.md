# Private Store catalog review

Run the ARMHF simulation from the umbrella checkout with Pillow and `jsonschema` installed. It builds the review,
refreshes and installs from it in both verification modes, and renders the desktop Store captures.
[Local verification guide](local-verification.md)

```sh
sh scripts/simulate.sh build/simulation --packages
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

To rebuild the review and repeat the signed verification from existing simulation output, run these commands.

```sh
python3 scripts/build-local-catalog.py build/simulation
python3 scripts/verify-signed-local-catalog.py build/simulation
```

The signed check creates and removes its own temporary key and proofs. The unsigned API, receipts, screenshots, and
the signed and unsigned test logs remain in the simulation output. [Store signature format](store-signatures.md)
