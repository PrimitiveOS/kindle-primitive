# Store signature format

Store and Launcher in PrimitiveOS use SHA-256 by default. They opt in to signed verification when the protected root-owned file
`/var/local/primitive-launcher/catalog-ed25519.pub` contains a trusted 32-byte public key as 64 hexadecimal digits.
Keep the private PKCS#8 key on the signing host and provision the public key through a separate trusted channel.
A signed catalog uses one key for its index and every package it offers.

In signed mode, Store publishes a new offline cache only after authenticating the index and every indexed listing.
It verifies cached listing bytes again when reading them. Store verifies the detached package proof before
downloading. Launcher uses the same key for its Store update check and bootstrap. A missing or invalid proof
fails that signed operation and leaves the last authenticated cache in place.

The `kl-store` library uses `ring` to verify standard Ed25519 signatures. Provisioning rejects small-order and
noncanonical key encodings. Fixed prefixes separate catalog and package messages. Signing the archive fingerprint lets
the Store check large ZIPs with its existing streamed SHA-256 and size checks.
[RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html#section-8),
[ring Ed25519 verifier](https://docs.rs/ring/0.17.14/ring/signature/index.html),
[Curve constants](https://github.com/jedisct1/libsodium/blob/1.0.20-RELEASE/src/libsodium/crypto_core/ed25519/ref10/ed25519_ref10.c#L998-L1031)

## Files and signed messages

The index proof is `index.sig.json` next to `index.json`. The proof holds `schema` (the number `1`), `listings` (a map
of app IDs to 64 hexadecimal SHA-256 digits), and `signature` (128 hexadecimal digits). Listing digests cover the exact
bytes served from `apps/<id>.json`, including its package records and permissions. The signature covers the following
concatenated fields.

| Field | Encoding |
| --- | --- |
| Catalog prefix | `Primitive Kindle Store index signature v1` followed by NUL |
| Index length | Unsigned 64-bit big-endian integer |
| Index hash | 32 raw SHA-256 bytes of `index.json` |
| Listing count | Unsigned 32-bit big-endian integer |
| Listings | For each ASCII-sorted ID, one byte of ID length, the ID bytes, and the 32 raw listing-digest bytes |

Each signed package has a sibling `.zip.sig` file containing the hexadecimal Ed25519 signature. The Store appends
`.sig` to the asset URL's path and keeps any query. The signature covers the following concatenated fields.

| Field | Encoding |
| --- | --- |
| Package prefix | `Primitive Kindle Store package signature v1` followed by NUL |
| Package identity | App ID, version and architecture, each preceded by one byte of field length |
| ZIP length | Unsigned 64-bit big-endian integer |
| ZIP hash | 32 raw SHA-256 bytes of the ZIP |

Publish the index proof, index, and exact listing bytes together once the signed publishing workflow is approved.
Publish each ZIP with its signature so the two stay available at the associated asset URLs.

## Local signing example

Use the [private catalog review](local-catalog-review.md) and a disposable key in a temporary directory. Run these
commands from the umbrella checkout after building the ARMHF simulation.

```sh
signing_demo=$(mktemp -d)
trap 'rm -rf "$signing_demo"' EXIT
cp -R build/simulation/catalog-review/site/v1 "$signing_demo/catalog"
cp build/simulation/packages/primitive-browser/*.zip "$signing_demo/browser.zip"
(
    cd doannt-kindle-tools
    cargo run --offline --locked -q -p kl-store --example sign-store-catalog -- \
        keygen "$signing_demo/key.pkcs8" "$signing_demo/trusted.pub"
    cargo run --offline --locked -q -p kl-store --example sign-store-catalog -- \
        index "$signing_demo/key.pkcs8" "$signing_demo/catalog"
    cargo run --offline --locked -q -p kl-store --example sign-store-catalog -- \
        package "$signing_demo/key.pkcs8" "$signing_demo/browser.zip"
)
```

The example creates the private file with permissions `0600` and refuses to overwrite existing keys or proofs.
The temporary directory holds the key and the proof files. The deployed trust key and publishing process require
owner approval before any real device uses the signed catalog.
