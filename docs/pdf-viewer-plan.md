# PDF Viewer for PrimitiveOS

Files can open PDFs in an installed KOReader from Primitive Launcher. It passes the selected file as an argument and hands the foreground session to KOReader. Exiting the reader returns to Launcher. KOReader remains a separate installation. [Kindle startup script](https://github.com/koreader/koreader/blob/master/platform/kindle/koreader.sh) · [Document entry point](https://github.com/koreader/koreader/blob/master/reader.lua)

A first-party PDF Viewer is feasible as a standalone, offline Store app. The useful first version would provide fit-page and fit-width views, physical page buttons, horizontal swipes, a page counter, and a go-to-page control. When a page is larger than the viewport, a vertical swipe would move within the page. The viewer would resume reading from a small saved position and open PDFs read-only.

## Engine options

| Engine | Fit for PrimitiveOS |
| --- | --- |
| PDFium | First candidate to prototype. Its C API renders into a caller-owned bitmap and supports reading a file through callbacks. Use an ARMHF build with JavaScript and XFA disabled, then verify sustained memory use and review the compiled dependencies' notices. [C API](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/public/fpdfview.h) · [Build configuration](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/README.md) · [Upstream licence](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/LICENSE) |
| Hayro | Pure Rust with MIT or Apache-2.0 licensing. It is a candidate for a simpler build, but the upstream maintainers identify remaining timeout, memory, and performance gaps. Compare on the Kindle before selecting it. [Hayro development status](https://github.com/LaurenzV/hayro#development-state) |
| MuPDF | Already used by KOReader. Artifex distributes MuPDF under AGPL and offers a commercial licence. Bundling it in a first-party PolyForm Noncommercial app would require a separate licence review. [KOReader base](https://github.com/koreader/koreader-base) · [MuPDF releases](https://mupdf.com/releases) |

## Device prototype

Prototype one grayscale page rendered at the Oasis 3's 1264 × 1680 display size. One framebuffer-sized grayscale image uses about 2 MiB. Keep the current page and a bounded next-page cache. Render only the visible area when zoomed, and measure first-page latency, forward and backward turns, and peak memory on ARMHF before setting a release target. Keep document handles coordinated with USB export and close them before handing storage back to the supervisor. [Oasis 3 profile](https://github.com/DoanNguyenTrong/kindle-primtitive-tools/blob/main/crates/primitive-device/src/profile.rs)

Validate embedded text and fonts, scanned pages, rotated pages, long documents, and clear errors for password-protected or damaged files. Check physical page buttons, both supported device orientations, sleep and wake, USB export, and return to Files or Launcher. Bookmarks, text search, annotations, and PDF editing can follow once the page-rendering path is verified.
