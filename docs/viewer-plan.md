# Viewer for PrimitiveOS

**Viewer** is a proposed standalone Store app for opening PDFs and images offline. It brings the same open, fit,
zoom, and rotate controls to each format. Apple's Preview is the reference for opening different file types in
one place and adding page navigation when a document has multiple pages. [Apple Preview guide](https://support.apple.com/en-mide/guide/preview/prvw11470/mac)

## Planned first release

| Format | What the reader can do |
|---|---|
| PDF | Read a page at a time, use the Kindle page buttons or swipe horizontally, and tap the page number to jump to a page. Resume at the last page. |
| JPEG | View photos with their embedded orientation and open larger photos at a reduced resolution when the decoder supports it. |
| PNG | View screenshots and illustrations, with transparency composited over white. |

The same toolbar offers **Fit screen**, **Fit width**, **Zoom in**, **Zoom out**, and **Rotate** for all three formats.
Swipe vertically to pan content taller than the viewport. Horizontal swipes pan wide content or turn PDF pages
when the width fits. The physical page buttons always turn PDF pages. Apply swipes after the finger lifts so the
e-ink panel redraws once per gesture. The first release opens files read-only and saves reading position in Viewer’s
own local data. WebP and plain-text previews are candidates for the same interface.

## Opening a file

- **From Launcher.** Open Viewer and choose **Open** to pick a supported file from Kindle user storage. **Recent**
  reopens a document and restores its saved position.
- **From Files.** Offer **Open in Viewer** when Viewer is installed and accepts the selected format, and
  **Open in KOReader** for supported documents when KOReader is installed.

Files 0.1.0 already opens PDFs in KOReader. Its handoff replaces the foreground Files process, and the Launcher
supervisor regains control when the reader exits. Prototype Viewer with a validated document path passed as data
to a verified installed entry point. Test the return to Launcher first. Returning to the same Files folder and
scroll position needs a saved Files session and a separate return check. [Files release](https://github.com/PrimitiveOS/kindle-primitive-files/releases/tag/v0.1.0)

## Rendering on the Kindle

Keep one grayscale viewport for PDFs and images. Each decoder reports the content size and supplies pixels for
that viewport. Reuse PrimitiveOS’s PNG-to-grayscale and fit routines where their limits fit the input. Prototype
JPEG with a decoder that supports reduced-size output and explicit limits. Detect the file type from its header
and check dimensions, decoded bytes, and output limits before allocating image buffers. Use specific messages for
unsupported, damaged, password-protected, or oversized files. [Shared PNG renderer](https://github.com/PrimitiveOS/kindle-primtitive-tools/blob/main/crates/kl-render/src/image.rs) · [JPEG decoder API](https://docs.rs/jpeg-decoder/latest/jpeg_decoder/struct.Decoder.html)

| PDF engine | Prototype considerations |
|---|---|
| PDFium | First candidate. Render to a caller-owned bitmap and read the document through file callbacks. Prototype an ARMHF build with JavaScript and XFA disabled. Measure memory and review the compiled dependencies’ notices before selecting it. [C API](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdfview.h) · [Build configuration](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/README.md) · [Licence](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/LICENSE) |
| Hayro | Pure Rust with MIT or Apache-2.0 licensing. Compare performance and memory on the same fixtures. Its maintainers identify remaining gaps around rendering time and memory use. [Upstream development status](https://github.com/LaurenzV/hayro#development-state) |
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
