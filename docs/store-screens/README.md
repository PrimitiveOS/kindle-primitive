# Store screens (for review)

Desktop renders of Primitive Store, at the Kindle Oasis 3's size (1264 × 1680). Demo data: the catalog's KOReader and
the draft listings of Primitive Launcher and Browser; Updates shows an installed app as a preview, not a real install.

| File | Screen |
|---|---|
| `store-today.png` | Today: the featured app and the next apps |
| `store-apps.png` | Apps: every app, with the action on the right |
| `store-updates.png` | Updates: installed apps, and an update ready |
| `store-app.png` | A product page with screenshots (Primitive Browser) |
| `store-app-scrolled.png` | The same page, scrolled to About and Information |
| `store-link.png` | A link listing without screenshots (KOReader) |

To rebuild: `cargo run -p kl-desktop -- --documents <folder> --out <folder>` in the launcher, with the catalog next to it.
