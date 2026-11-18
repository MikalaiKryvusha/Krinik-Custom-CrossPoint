# Research — FB2 → EPUB 3 converters and an on-device converter on the X4 Pro

> **Created:** 2026-11-18 · **Parent:** ideas/04 · **Status:** recon done · **Outbound:** a summary to the owner (chat)

The owner's question (chat, 2026-11-18): «поищи в интернете опенсоурс открытые реализации легких и мощных конвентеров
FB2->EPUB3. Можно ли его запихнуть в код прошивки, чтобы на ESP32 такое конвертирвоание выполнять, или это слишком
трудная задача для такого слабого SoC».

What `ideas/04` already settled is not repeated here: upstream CrossPoint refused FB2 three times (issue #592, PR #755,
PR #2484); papyrix reads FB2 directly; the firmware already has expat, miniz and the on-device TXT → HTML converter.

**How facts are marked.** A plain statement was read this session from the named source (the repo page or its file via
`gh api`, the firmware tree, a measurement). *(i)* marks an inference that was not read in the source.

## The test book, measured (2026-11-18 ≈ 09:05 +03:00, in memory, nothing written)

`D:\Hofshtadter_…198312.fb2.zip` — 4,144,669 B zip, one entry (deflate) → 7,908,212 B FB2, `encoding="UTF-8"`, FictionBook
2.0 namespace. Text part (everything before the first `<binary>`) 3,508,282 B; 3 `<body>` (one `name="notes"`), 144
`<section>`, 7,339 paragraphs, 91 `type="note"` links, 0 tables. 180 binaries = **103 JPEG + 77 PNG** (the brief's «180
JPEG» is wrong; `ideas/04` itself says «180 `<binary>`»): base64 4,399,377 B, decoded 3,202,737 B, largest binary
130,498 B base64; every JPEG baseline (0 progressive); JPEG ≤ 639×514; PNG up to 1296×1048; 12 JPEG and 42 PNG wider than
480 px.

## Converters

| # | Project · repo | Lang | Licence | Last push | Core size | Dependencies | Output |
|---|---|---|---|---|---|---|---|
| 1 | **fb2cng** (`fbc`) · `rupor-github/fb2cng` | Go | GPL-3.0 | 2026-11-15 | own Go ≈ 2.4 MB for all formats (`fb2/` 164 KB, `content/` 173 KB, `convert/epub/` 31 KB) + vendored | beevik/etree, disintegration/imaging, golang.org/x/image, hidez8891/zip, tdewolff/parse … | EPUB2, **EPUB3**, KEPUB, KFX, AZW3, PDF, TXT, MD; README: «intended to pass the latest epubcheck without errors or warnings» |
| 2 | **fb2converter** (`fb2c`) · `rupor-github/fb2converter` | Go | GPL-3.0 | 2026-02-13, archived | repo 49 MB | etree *(i)*, kindlegen for MOBI | EPUB2, KEPUB, MOBI, AZW3 — «[DEPRECATED]», superseded by #1 |
| 3 | **calibre FB2 input** · `kovidgoyal/calibre` | Python | GPL-3.0 | 2026-11-18 | `fb2_input.py` 7.9 KB + `resources/templates/fb2.xsl` 18.3 KB + the calibre pipeline | lxml (XSLT), css_parser | through calibre's EPUB output: EPUB 2 by default, EPUB 3 by option *(i)* |
| 4 | **pandoc FB2 reader** · `jgm/pandoc` `src/Text/Pandoc/Readers/FB2.hs` | Haskell | GPL-2.0-or-later («GNU GPL, version 2 or above») | 2026-11-15 | `FB2.hs` 16.8 KB | pandoc, xml-light | `-f fb2 -t epub` = «EPUB v3 book» (`MANUAL.txt:328`); `epub2` too |
| 5 | **fb2toepub** (Alexey Bobkov, Google Code export) · `ava1ar/fb2-to-epub-converter` | C++ | GPL-3.0 | 2015-06-13 | ≈ 320 KB own source (`scanner.cpp` 75 KB flex-generated, `convpass2.cpp` 72 KB, `convpass1.cpp` 28 KB) + bundled minizip, tiniconv | flex, zlib (`DEPENDENCIES`) | **EPUB 2.0** (`convpass2.cpp:792` OPF `version="2.0"`, `:871` `toc.ncx`) |
| 6 | **EbookConverter** · `gregko/EbookConverter` | C/C++ | none in GitHub metadata; README «under LGPL»; it embeds #5 (GPL-3.0), so GPL-3.0 governs *(i)* | 2025-06-29 | Android NDK `.so` (libmobi + #5) | libmobi, #5 | EPUB 2 (#5's) *(i)*; used in the «@Voice Aloud Reader» app |
| 7 | **inkMOD `lib/Fb2`** · `alpzoloto-sudo/inkmod` (a CrossPoint/FreeInk-derived Xteink firmware) | C++ | MIT (`LICENSE`: «Copyright (c) 2025 Dave Allie») | repo 2026-11-13; `lib/Fb2` 2026-09-15 «Release inkMOD 1.1.8 - X4 Pro support» | ≈ 260 KB source (`Fb2.cpp` 137 KB, `native/Fb2Parser.cpp` 37 KB, `Fb2XmlReader.h` 17 KB, own `Inflate`/`ZipReader` 12 KB each) | own XML reader and inflate *(i)* | an «FB2 -> EPUB-shaped package» in the book cache, **not a standalone .epub** (`Fb2.h:22–36`) |
| 8 | **papyrix `lib/Fb2`** · `bigbag/papyrix-reader` | C | MIT | 2026-11-15 | `Fb2.cpp` 36.8 KB, `Fb2Parser.cpp` 19.7 KB, `Base64Decoder.h` 3 KB | expat | none — reads FB2 directly (`ideas/04`) |
| 9 | **fb2epub** (Rust) · `KiberBomzh/fb2epub` | Rust | MIT | 2026-11-03 | ≈ 80 KB `.rs` incl. CLI | quick-xml, epub-builder 0.8, zip (deflate), base64 | **EPUB 3.3** (`epub_creator.rs:72` `EpubVersion::V33`) |
| 10 | **fb2epub** (Go) · `reinventer/fb2epub` | Go | MIT | 2024-07-23 | ≈ 16 KB Go | encoding/xml, google/uuid | EPUB 2 (`toc.ncx`); README limits: no zipped FB2, UTF-8 only, TOC incomplete |
| 11 | **FB2ePub** (Lord KiRon) · `LordKiRon/fb2converters` | C# .NET | MIT | 2015-07-20 | ≈ 1.5 MB C# | .NET | EPUB 2 and 3 (`EPubFileV2.cs`, `EPubFileV3.cs`); Windows GUI |
| 12 | **fb2mobi** · `rupor-github/fb2mobi` | Python 3 | MIT | 2020-03-15, deprecated | `modules/fb2html.py` 67 KB … | lxml *(i)* | EPUB, MOBI |
| 13 | **foliate-js `fb2.js`** · `johnfactotum/foliate-js` | JavaScript | MIT | 2026-05-01 | 12.3 KB | browser `DOMParser` | no EPUB file — an in-memory book of XHTML sections for the reader |
| 14 | **CrossPoint PR #2484** (lxyd) — in-browser converter in the reader's own `FilesPage.html` | JavaScript | CrossPoint MIT had it merged *(i)* | closed 2026-07-12 | +1109 lines in one file | JSZip (the page already loads `/js/jszip.min.js`) | EPUB, chapter-split by FB2 sections; closed as «out of scope … belongs in it's own web tool» |

| # | Images (base64 binaries) | Notes | TOC | «Рис. N» caption / `<figure>` | Typography extras | Memory model |
|---|---|---|---|---|---|---|
| 1 | keep format; optional resize, `fit_to_screen`, `screen` size, `baseline_jpeg`, `grayscale`, JPEG quality 95 (`docs/images.md`) | bodies `notes`/`comments`/`примечания`/`комментарии`; modes `default` · `float` · `floatRenumbered`; EPUB3 float = semantic popup markup; generated backlinks (`docs/footnotes.md`) | NCX / EPUB nav, optional visible TOC page; nested sections split by CSS page-break (`docs/stylesheets.md`) | block image in a `.image` div; `figcaption` occurs only in `convert/azw3/anchors.go` (code search) — no pairing with the next paragraph | `insert_soft_hyphen` (off by default), drop caps, vignettes, dash/dialogue transformations (`docs/config.md`) | DOM (beevik/etree) — the whole book in memory *(i)* |
| 2 | resize, kindlegen path | footnotes, backlinks *(i)* | NCX | none *(i)* | hyphenation dictionaries (README «slightly different hyphenation algorithm»), drop caps | DOM *(i)* |
| 3 | `extract_embedded_content` writes binaries to files; FB2 cover → `opf.guide.set_cover` | `<a type="note">` → plain links + ids (`fb2_input.py:114–129`) | XPath `//h:h1..h3` + inline FB2 TOC (`no_inline_fb2_toc`) | none *(i)* | calibre heuristics *(i)* | whole-document DOM + XSLT (`safe_xml_fromstring`, `etree.XSLT`) |
| 4 | `insertMedia` into the media bag | notes body parsed FIRST, `type="note"` → real pandoc notes (`FB2.hs:120–151`) | from headers *(i)* | none *(i)* | none; tables are a TODO (`FB2.hs` header) | whole-document DOM (`parseXMLElement`) |
| 5 | base64 → `OPS/bin/<id>` files, cover index | `noteRefIds` → `BuildAnchors` (anchors for back references *(i)*) | NCX `navMap` | none *(i)* | style + font directory (embedded fonts), transliterated names | two-pass streaming over a flex scanner; each binary's base64 held whole in a `std::string` (`convpass2.cpp:1319–1324`); text files split at 0x30000 B (`config.h:73`); errors are C++ exceptions (`error.cpp:63–95`) |
| 6 | as #5 | as #5 | as #5 | none *(i)* | — | as #5 |
| 7 | decoded on first view, only the last few raw images kept (`Fb2.h:76–85`) | field bugs: inkMOD issues #31 #38 #40 #52 #54 #56 — FB2 note, link and bookmark navigation (all closed) | NCX + a section index written by `load()` | none in `lib/Fb2` (code search) | README: annotations, epigraphs, subtitles, poems, stanzas; issue #33 nbsp in dialogues | one scan pass, then lazy per-chapter XHTML through the reader's own `ChapterHtmlSlimParser` (`Fb2.h:22–36`); README lists X3/X4 (ESP32-C3) and X4 Pro (ESP32-S3) |
| 8 | `Base64Decoder.h` | links *(i)* | own TOC | — | — | streaming (expat) |
| 9 | `Paragraph::Image` | `epub:type="noteref"` links, notes as `<aside epub:type="footnote">` (`html_builder.rs:137–344`) | epub-builder nav *(i)* | none (code search) | none | pull parser into an in-memory model; epub-builder holds the book *(i)* |
| 10 | `epub/binary.go` | none *(i)* | partial (README TODO) | none | header transliteration | token streaming (`xml.Decoder.Token`) |
| 11 | yes *(i)* | yes *(i)* | yes *(i)* | none *(i)* | fonts, templates *(i)* | DOM (`XDocument.Load` in `FB2FileLoader.cs`) |
| 12 | `image_utils.py` | yes *(i)* | yes | none *(i)* | `myhyphen.py` hyphenation, smart drop caps, XSLT pre-transform | DOM *(i)* |
| 13 | `data:` URIs | `type="note"` → `epub:type="noteref"` (`fb2.js:102–103`) | from sections | image `title` → `title` attribute (`fb2.js:95`) | — | browser DOM |
| 14 | the page's optimizer resizes to «Max 480×800px» (KCCP `FilesPage.html:957`) | *(i)* | by FB2 sections | *(i)* none | user-editable CSS | browser memory |

Notes on the inventory:

- **No converter turns a picture + the «Рис. N …» paragraph after it into `<figure>`/`<figcaption>`.** FB2 has its own
  caption slot — `imageType` carries an optional `title` attribute (`gribuser/fb2` `FictionBook.xsd:283–292`) — but the
  test book writes captions as the next paragraph (`ideas/04`). The KCCP rule (now `epub-linter/krinik_figures.py`,
  run by the linter's `fix` since 2026-11-18; `tools/figure_retypeset.py` removed) has to be added to whichever converter
  is used.
- **Only #7 is a converter that runs on an Xteink reader today**, and it is the closest relative of KCCP's code (CrossPoint
  lineage, MIT). It does not write a portable `.epub`; it builds an EPUB-shaped package in the cache and renders chapters
  lazily through hooks in `Epub::readItemContentsToStream()` and `ImageBlock::render()` (`Fb2.h:30–36`, `:69–79`).
- **#5 is the only one written for embedded use** — README: «intended to be used in embedded systems and other
  resource-critical facilities» — but it is GPL-3.0, EPUB 2, needs zlib deflate and flex, and reports errors by C++
  exceptions while the firmware builds with `-fno-exceptions` (`firmware/platformio.ini:123`, `-fexceptions` unflagged at
  `:127`).
- **#1 is the strongest PC tool**: active (pushed three days ago), EPUB3, epubcheck-clean by design, configurable image
  shaping for a screen, popup notes. A Windows binary is on its releases page (README).
- The schema orders the root as `description`, `body`, `body` (notes), `binary*` (`FictionBook.xsd:207–224`): notes and
  pictures come AFTER the text, so a streaming writer learns note targets and image types only at the end — two passes
  (as #5) or a pass-1 index (as #7).

## The reader's hardware (firmware tree, branch `wip/kccp-1.1.4` `c1c38089`)

| Fact | Value | Evidence |
|---|---|---|
| SoC | **ESP32-S3** (not the X4's ESP32-C3 of `[base]`) | `[env:x4pro-krinik]` `extends = env:x4pro-gh_release` (`platformio.ini:772–773`) → `board = esp32-s3-devkitc1-n16r8` (`:540`); `[base]` `board = esp32-c3-devkitm-1` (`:16`) is overridden |
| CPU clock | 240 MHz; power saving drops it to 80 MHz (`IDLE_POWER_SAVING_MS = 3000` — «after 3 s idle unless a lock is held» *(i)* from the names) | `sdkconfig.h:896` `CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ 240` (`~/.platformio/packages/framework-arduinoespressif32-libs/esp32s3/dio_opi/include/sdkconfig.h`); `lib/hal/HalPowerManager.h:29,33` |
| Internal SRAM | linker budget 327,680 B for static data; 1.1.x builds use 112,380 B (34.3 %) | board JSON (`~/.platformio/platforms/espressif32/boards/esp32-s3-devkitc1-n16r8.json`) `maximum_ram_size: 327680`; `qa_runs/debug4-2026-11-06/build.log` «RAM: 34.3% (used 112380 bytes from 327680 bytes)» |
| PSRAM | **8 MB octal**, heap-mapped: any `malloc` above 4,096 B goes to PSRAM | board JSON name «16 MB Flash Quad, 8 MB PSRAM Octal»; `-DBOARD_HAS_PSRAM` (`platformio.ini:778`), `memory_type = dio_opi` (`:542`); `sdkconfig.h:881,891,892` `CONFIG_SPIRAM_MODE_OCT`, `CONFIG_SPIRAM_USE_MALLOC 1`, `CONFIG_SPIRAM_MALLOC_ALWAYSINTERNAL 4096`; `HalMemory::allocatePsram` (`lib/hal/HalMemory.cpp`) |
| Runtime free heap on the device | **not observed** — the reader has no serial port (`HOUSE_RULES.md` dossier); the simulator's `[MEM]` lines are stubs (1,048,576 / 8,388,608 B constant) | `src/main.cpp:1183–1191` logs both heaps every 10 s when a console exists |
| Flash | 16 MB; app slot `app0` 0x640000 = 6,553,600 B (two OTA slots) | `platformio.ini:39`, `:132`; `partitions.csv:4–5` |
| Flash used / headroom | release 1.1.3 image 5,447,040 B = 83.1 % of the slot (PlatformIO: 83.0 %) → **≈ 1.1 MB free** (1,106,560 B by file size) | `firmware-builds/cp-2.0.0-krinik-1.1.3.bin`; `STATUS.md:29` |
| SD card | native SDMMC, **1-bit, 40 MHz** → ≤ 5 MB/s bus ceiling | `freeink-sdk/libs/hardware/BoardConfig/include/BoardConfig.h:1961`; `SDCardManager/src/SdmmcBlockDevice.cpp:52` |
| XML | expat 2.7.3, `XML_GE=0`, 2 KB input buffer (`XML_CONTEXT_BYTES=0`); no `XML_SetUnknownEncodingHandler` anywhere | `lib/expat/library.json`; `platformio.ini:51,53`; `git grep` over `src lib` |
| ZIP read | `ZipFile` reads STORED (0) and DEFLATED (8) entries | `lib/ZipFile/ZipFile.cpp:415,426,485,515` |
| ZIP write / deflate | **compiled out**: `MINIZ_NO_ARCHIVE_APIS`, `MINIZ_NO_ARCHIVE_WRITING_APIS`, `MINIZ_NO_DEFLATE_APIS`; `mz_crc32` kept (renamed) | `lib/miniz/src/MinizConfig.h:10–12,27`; `third_party/miniz.c:96` |
| Inflate state | 32 KB ring + tinfl tables (`m_look_up` 3×1024×2 B) ≈ 43 KB | `lib/InflateReader/InflateReader.h:53`; `miniz.h:1042` |
| JPEG | progressive JPEG decodes DC-only (⅛ resolution) | `lib/Epub/Epub/converters/JpegToFramebufferConverter.cpp:443–445` |
| EPUB parser | reads EPUB 3 nav (`properties="nav"`) and EPUB 2 NCX | `lib/Epub/Epub/parsers/ContentOpfParser.cpp:366–369`; `lib/Epub/Epub.cpp:185` |
| Licences | CrossPoint source MIT (`firmware/LICENSE`); this repo MIT (`LICENSE`); the combined image GPLv3 «because it includes wolfSSL» | `firmware/licenses/README.md` |

## Feasibility

**Verdict: feasible on the X4 Pro — the SoC is not the obstacle.** Upstream's «impacts memory» is about the X4
(ESP32-C3, no PSRAM); the X4 Pro has 8 MB PSRAM, a 240 MHz dual-core S3 and 1.1 MB of free app flash, and the firmware
already carries the read side of the job (ZipFile + InflateReader for `.fb2.zip`, expat, CRC32). What is missing is the
write side: a ZIP writer and, optionally, deflate.

**Which code can run there.** None of the PC tools (#1–4, #9–12: Go, Python, Haskell, Rust, C#) can be linked into an
Arduino C++ image. Of the C/C++ ones: #5 is a poor port (exceptions vs `-fno-exceptions`, flex, zlib, GPL-3.0, EPUB 2);
#8 reads but writes no EPUB; #7 works on Xteink hardware but builds a cache package coupled to its own `lib/Epub`, not a
file the owner can copy, lint or reopen elsewhere, and its fork point against KCCP 1.1.3 is unknown *(i)*.

**The approach that fits: a KCCP streaming converter of its own, on what the firmware has**, borrowing MIT mappings from
#7, #8 and #13:

1. Pass 1 — stream `.fb2.zip` → inflate → expat: metadata, cover id, section tree with byte sizes, every `id` → the
   chapter file it lands in, binary ids and content types. Nothing but this index is kept.
2. Pass 2 — stream again; write `mimetype` (first, stored, no extra field — EPUB 3.3 §4.3.3), `META-INF/container.xml`,
   one XHTML per top-level section split by size (#5 splits at 0x30000 B), each `<binary>` base64-decoded chunk by chunk
   straight into its image entry; then the OPF (EPUB 3 with `dcterms:modified`, §5.5.5) and a nav document plus an NCX;
   last, the ZIP central directory. KCCP rules built in: picture + «Рис. N» paragraph → `<figure>`/`<figcaption>`; note
   links in the linter's `[N]` form with backlinks.
3. ZIP writing: stored entries only — the reader already opens them (`ZipFile.cpp:415`), CRC32 is there, about 200–300
   lines *(i)*. Deflate is optional: miniz's `tdefl_compressor` is 319,149 B of state with defaults, 167,597 B with
   `TDEFL_LESS_MEMORY=1` (summed from `miniz.h:794–868`), plus its code.

**Peak RAM for the test book (streaming, stored ZIP)** — *(i)* except the sourced lines:

| Part | Bytes |
|---|---|
| inflate of the `.fb2.zip` entry (ring + tables) | ≈ 43 KB (sourced above) |
| expat parser + 2 KB input buffer + name pool | ≈ 10–20 KB |
| base64 → image entry (4-byte carry + write buffer) | ≤ 4 KB; never the whole binary (largest is 130,498 B anyway) |
| id → file map + section index (144 sections, 91 notes, 180 images) | ≈ 20–40 KB |
| ZIP central directory (≈ 330 entries × ~80 B) | ≈ 26 KB |
| XHTML / file write buffers | ≈ 8 KB |
| **total** | **≈ 110–140 KB in PSRAM; + 168–319 KB if deflate is enabled** — 2–6 % of 8 MB |

**Flash cost:** ≈ 40–80 KB of code *(i)* (+ ≈ 10–15 KB if `tdefl` is compiled in *(i)*) against ≈ 1.1 MB free.

**Output size (test book):** stored ≈ 3.2 MB images (measured) + ≈ 3.5–4 MB XHTML (the FB2 text part is 3,508,282 B) ≈
7 MB; with deflate the text would shrink to about 1 MB *(i)*.

**Time class: tens of seconds to a few minutes, unmeasured.** The bus alone gives a floor of ≈ 3 s ((2 × 4.1 MB read +
≈ 7 MB written) / 5 MB/s); two expat passes over 7.9 MB and the inflate on a 240 MHz Xtensa dominate, and no ESP32
throughput figure for expat or tinfl was found. The job must hold the power lock against power saving (80 MHz). After
conversion the reader still indexes the book on first open, as for any EPUB. A first plan phase measures this on the
reader (timestamps to an SD log, since there is no serial port).

**Licences.** MIT sources (#7, #8, #9–13, CrossPoint's own) can be ported with their notice. GPL-3.0 sources (#1–3, #5,
#6) and GPL-2.0-or-later pandoc are legal inside the GPLv3 image, but they turn the KCCP firmware source (MIT) into a
mixed-licence tree and could never go upstream — moot for FB2 (upstream refused it), still a cost. Calling a GPL program
on the PC from the MIT linter as a separate tool mixes no code *(i — the usual aggregation reading, not legal advice)*.

## Risks

**(a) The three hardest — build defences:**

1. **Real-world FB2 against a strict streaming XML parser.** Old library files are often `windows-1251`; expat knows only
   UTF-8, UTF-16, ISO-8859-1 and US-ASCII natively *(i — expat docs)*, and the firmware sets no unknown-encoding handler
   (a 256-entry cp1251 map is the fix). Expat stops at the first well-formedness error, so one broken tag fails the whole
   book, where PC tools recover *(i)*. Huge single sections must be split by size.
2. **Links and notes.** Targets and images are known only after the text (schema order), so the converter needs two
   passes and an id → file map; inkMOD's tracker shows six closed FB2 note/link/bookmark navigation bugs on these very
   readers. And the KCCP quality rules (figure pairs, `[N]` notes, backlinks) would live twice — in the linter and in the
   firmware — a pair to keep in sync (DRY).
3. **A minutes-long SD write job on a battery e-reader.** Auto-sleep and power saving mid-job, power loss or a pulled card
   → a half-written EPUB (write to a temporary name, rename at the end); ≈ 7 MB free space plus the temporary; a progress
   screen on e-ink; and no serial log to see failures — only an SD log.

**(b) Plausible — contingency named:** progressive JPEGs decode at ⅛ resolution and an on-device converter cannot
re-encode them (the test book has none; fb2cng has `baseline_jpeg`); big PNGs (up to 1296×1048 here) pass through
unshrunk (the reader decodes ≤ 2048 px wide — `PNG_MAX_BUFFERED_PIXELS`); the 1.1 MB flash headroom shrinks for every
later feature.

**(c) Small — listed:** `dcterms:modified` needs a time (the FB2 `document-info` date will do); stored EPUBs are about 1.7×
the size of the `.fb2.zip`; inline images inside paragraphs; FB2 tables (0 in the test book).

## Recommendation

`FORK: options <PC tool only | on-device converter | both, PC first> · price of error <weeks of firmware work and a second
copy of the quality rules vs one PC step per book> · consulted <this recon doc · the owner>` — the choice is the owner's.
The recon's recommendation: **both, PC first.** On the PC the owner already runs Krinik EPUB Linter on every book; putting
FB2 → EPUB 3 there (fb2cng #1 as an external step, or a `fb2` command of the linter's own on Python's stdlib, MIT, with
the figure and `[N]` rules native) gives a correct EPUB 3 today, keeps one copy of the quality rules, and can shape
pictures for the 480×800 screen and re-encode progressive JPEGs, which the reader cannot. The on-device converter is
feasible — the X4 Pro is an ESP32-S3 with 8 MB PSRAM, not a weak SoC for this job — and its value is convenience (drop a
`.fb2.zip` onto the card, no PC). It is a heavy KCCP epic (`/plan-epic`): an own streaming converter on expat + InflateReader
+ a stored-ZIP writer, the inkMOD and papyrix MIT code as references, emitting the same EPUB 3 the linter would. A third,
cheaper route exists for the upload path: convert in the browser on the reader's own File Transfer page (upstream PR
#2484; the page already carries JSZip and an EPUB optimizer).

## Sources

- fb2cng — https://github.com/rupor-github/fb2cng (README, `docs/footnotes.md`, `docs/images.md`, `docs/config.md`,
  `docs/stylesheets.md`, `docs/guide.md`, `go.mod`)
- fb2converter — https://github.com/rupor-github/fb2converter
- calibre FB2 input — https://github.com/kovidgoyal/calibre/blob/master/src/calibre/ebooks/conversion/plugins/fb2_input.py ·
  https://github.com/kovidgoyal/calibre/blob/master/resources/templates/fb2.xsl
- pandoc FB2 reader — https://github.com/jgm/pandoc/blob/main/src/Text/Pandoc/Readers/FB2.hs ·
  https://github.com/jgm/pandoc/blob/main/MANUAL.txt
- fb2toepub — https://github.com/ava1ar/fb2-to-epub-converter (README, DEPENDENCIES, `fb2toepub/convpass2.cpp`,
  `config.h`, `error.cpp`)
- EbookConverter — https://github.com/gregko/EbookConverter
- inkMOD — https://github.com/alpzoloto-sudo/inkmod (README, `lib/Fb2/Fb2.h`, `THIRD_PARTY.md`, `LICENSE`, issues #31 #33
  #38 #40 #52 #54 #56)
- papyrix — https://github.com/bigbag/papyrix-reader/tree/main/lib/Fb2
- fb2epub (Rust) — https://github.com/KiberBomzh/fb2epub (`Cargo.toml`, `src/lib/epub_creator.rs`,
  `src/lib/epub_creator/html_builder.rs`)
- fb2epub (Go) — https://github.com/reinventer/fb2epub
- FB2ePub — https://github.com/LordKiRon/fb2converters
- fb2mobi — https://github.com/rupor-github/fb2mobi
- foliate-js — https://github.com/johnfactotum/foliate-js/blob/main/fb2.js
- CrossPoint PR #2484 — https://github.com/crosspoint-reader/crosspoint-reader/pull/2484 · PR #755 —
  https://github.com/crosspoint-reader/crosspoint-reader/pull/755
- FictionBook 2 schema — https://github.com/gribuser/fb2 (`FictionBook.xsd`, BSD-2-Clause)
- EPUB 3.3 — https://www.w3.org/TR/epub-33/ (§4.3.2 ZIP methods 0/8, §4.3.3 mimetype, §5.5.5 `dcterms:modified`,
  §5.6.2.1 one nav item)
- Krinik EPUB Linter — `epub-linter/README.md`
