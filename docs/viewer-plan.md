# Viewer for PrimitiveOS

**Viewer** opens PDFs and images offline in one standalone app. The reading view keeps the document close to the
edges, with compact controls above and below it.

## Planned first release

| Format | What the reader can do |
|---|---|
| PDF | Swipe vertically to scroll through adjacent pages. The Kindle page buttons scroll by most of the visible area. Tap the page indicator to jump to a page. Recent resumes the reading position. |
| JPEG | View photos with their embedded orientation. The decoder enforces limits on file size and dimensions. |
| PNG | View screenshots and illustrations, with transparency composited over white. |

The bottom bar shows a page indicator for PDFs and **−** and **+** zoom controls. The **View** menu contains
**Fit screen**, **Fit width**, and **Rotate**. Swipe horizontally to pan content wider than the view. Images can
pan vertically after zooming. The e-ink screen redraws once after a swipe. Viewer opens files read-only and saves
reading position in its own local data. WebP and plain-text previews are candidates for the same interface.

## Opening a file

- **From Launcher.** Open Viewer and choose **Open** to pick a supported file from Kindle user storage. **Recent**
  reopens a document and restores its saved position. The Kindle page buttons move through both lists one screen
  of files at a time.
- **From Files.** Offer **Open in Viewer** when Viewer is installed and accepts the selected format, and
  **Open in KOReader** for supported documents when KOReader is installed.

Files passes a validated document path directly to the installed Viewer entry point. The handoff keeps the same
foreground process ID, so the Launcher supervisor continues to manage USB storage. Closing Viewer after opening
it from Files returns to Launcher. [Files repository](https://github.com/PrimitiveOS/kindle-primitive-files)

## Rendering on the Kindle

Viewer draws one grayscale viewport for PDFs and images. It rasterizes the visible parts of adjacent PDF pages
and uses the same fit, zoom, and rotation model for JPEGs and PNGs. It detects the format by the file header and
bounds decoded image and output dimensions. It reports password-protected, damaged, and oversized files.

| PDF engine | Prototype considerations |
|---|---|
| PDFium | First candidate. Render to a caller-owned bitmap and read the document through file callbacks. Prototype an ARMHF build with JavaScript and XFA disabled. Measure memory and review the compiled dependencies’ notices before selecting it. [C API](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdfview.h) · [Build configuration](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/README.md) · [Licence](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/LICENSE) |
| Hayro | The selected renderer builds for ARMHF and clips to a caller-sized raster. The package includes the upstream notices for Hayro, standard fonts, and Adobe CMaps. [Hayro](https://github.com/LaurenzV/hayro) |
| MuPDF | Used by KOReader. Artifex distributes MuPDF under AGPL and offers a commercial licence. Review redistribution terms before choosing it for a PolyForm Noncommercial build. [KOReader base](https://github.com/koreader/koreader-base) · [MuPDF releases](https://mupdf.com/releases) |

The Oasis 3 display is 1264 × 1680. One full-screen grayscale buffer occupies about 2 MiB. Render the visible
area when zoomed and start with one current frame. Bound any adjacent-page cache using device measurements.
Close decoder handles before USB export. After eject, revalidate the document before restoring its view.
[Oasis 3 profile](https://github.com/PrimitiveOS/kindle-primtitive-tools/blob/main/crates/primitive-device/src/profile.rs)

## Implementation and verification

1. Build the shared viewport and exercise fit, zoom, pan, and rotation with photos, large images, transparent PNGs,
   and corrupt fixtures in the desktop simulator.
2. Prototype PDF rendering in that viewport. Test text and fonts, scans, rotated pages, long documents, and
   password-protected or damaged files. Measure first-render time, page-turn time, and peak memory on the ARMHF Oasis 3.
3. Check entry from Launcher and Files, saved position, reader exit, page buttons, both portrait orientations,
   sleep and wake, and USB eject. Package the verified build, publish the GitHub release, and link it in Store.
