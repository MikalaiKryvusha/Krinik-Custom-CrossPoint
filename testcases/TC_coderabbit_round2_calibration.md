# Test cases — #4377 `pr/screen-calibration`: fixes for the CodeRabbit round

**Created:** 2026-11-09 · **Under test:** fork branch `pr/screen-calibration` at `d8573ad5` (fixes `b6477e41`, `75b92fc0`,
`7addf5be`, `b661b6be`) · **Version/build:** `simulator_x4_pro_win` (native Windows simulator, `simulator` `98a4777`)
**Test basis:** the CodeRabbit comments quoted in `researches/2026-11-09_coderabbit_pr_review.md`; the owner's choice in
`interviews/interview_003_coderabbit_round2.md` Q2 = B; the commit messages of the fixes.

## 1. Goal vector

Maintain: screen calibration keeps working, and the review findings no longer hold — a curve file with a 257th value
is reported, the books card carries a valid UUID and replaces its old file, a new book curve removes the image
caches of the previous one.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion |
|---|---|---|
| R1 | IF the picture curve file holds a 257th value with no line end, THEN the reader shall log an error and use the identity curve. | log line `[ERR] [CRV] More than 256 values` · count 1 |
| R2 | WHEN the books calibration card is opened, the reader shall write `books_card_v2.epub` with a valid UUID and remove `books_card_v1.epub`. | card folder listing · `uuid.UUID()` round-trip |
| R3 | WHEN a book is decoded after its curve changed, the reader shall remove the book's `img_*.pxc` caches of other curves. | cache folder listing before/after · log `Removed N image caches` |
| R4 | IF the settings section of a pending sub-section cannot open, THEN the pending sub-section shall be dropped. | OOM path — not reproduced on the simulator |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| curve file | 257 values unterminated (R1), valid 256 values | 257 values with a trailing newline — the older branch of the same check, risk low |
| cache names | other curve `_k<hash>`, stock (no suffix), non-`img_` decoy, the source image | a book with several chapters of images — same loop |
| R4 | — | needs an allocation failure in `SettingsListActivity::openSection`; no fault injection used |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 | card: `panelCalPictures` on, `.crosspoint/panel_curve.txt` = 0…255 + `255` without a line end; open a BMP → one `More than 256 values` | boundary (count = 257) | pass 2026-11-09 18:36 · `qa_runs/cal_curve257/log.txt:33` |
| C2 | same card with the template's valid 256-value curve → `Curve loaded`, no error | partition (valid) | pass 18:37 · `qa_runs/cal_curve256`: `Curve loaded … be170a3a` |
| C3 smoke | card with a placeholder `books_card_v1.epub`; Settings → Экран → Калибровка экрана → «Калибровочный экран книг» → `books_card_v2.epub` written, v1 gone, UUID valid, the book opens | use-case walk | pass 18:42 · `qa_runs/cal_books_card`: folder = `books_card_v2.epub` only; OPF uuid `4b1f6c2e-9d0a-4f3e-8c51-6b65696e6b74` valid; `Loading ePub …v2`, 0 errors |
| C4 | books curve A, open the books card → `img_0_0_kcb71c9af.pxc`; then curve B + decoys `img_0_0.pxc`, `notimg_k00000000.pxc`; open again → `Removed 2`, left: `img_0_0.png`, `notimg_…`, `img_0_0_kf66dd6d9.pxc` | partitions (other curve · stock · non-img · current) | pass 18:45 · `qa_runs/cal_cacheA`, `qa_runs/cal_cacheB` |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | C1 on `f90b29b4` (before `b6477e41`) → no `CRV` line | red as expected 18:38 · `qa_runs/cal_curve257_pre`: 0 `CRV` lines |
| K2 | C3 on `f90b29b4` → the old code opens `books_card_v1.epub` | observed by accident 18:41 (stale binary): `Loading ePub …v1`, zip errors on the placeholder |
| K3 | C4 on `7addf5be` (before `b661b6be`) → every cache stays | red as expected 18:47 · `qa_runs/cal_cacheB_pre`: stock, A and B caches all present |

## 6. Verdict

R1–R3 pass with controls; R4 not observed (named hole). Feature marker not set: the reader itself is the owner's.
