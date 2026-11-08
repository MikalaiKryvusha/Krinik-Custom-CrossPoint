# Reader card cleanup and final krinik 1.1.0 image

[AI]
Owner authorization: «давай прошьем, сейчас дам читалку на провод»;
«и наведи порядок с дубликатами книг, опять там призраки».

Observed source: /Volumes/X4-KRINIK, 2026-11-05. Six real EPUBs.
Recent store has seven entries: both /Калибровка.epub and /КАЛИБРОВКА.epub.
The former does not resolve through the macOS FAT driver. The six-record CLX1
index still names /Калибровка.epub (248394 bytes versus actual 251017), and
РУКОВОДСТВО.epub has stale size 38849 versus actual 40330. File-size and
byte-exact path hash are index identities (LibraryIndexFile::recentRowsFor).
State now points to the existing Schopenhauer book; the old handover observation
about state.json no longer applies. No need to change the current reading state.

Sources read: firmware/src/RecentBooksStore.cpp; CrossPointState.cpp;
firmware/lib/LibraryIndex/{LibraryFormat.h,LibraryIndexFile.cpp,LibraryText.cpp};
tools/card_clean.sh; qa_runs/calibration-2026-11-05/release-krinik-1.1.0.md.

Plan/checklist:
- Back up every file before replacement and record initial hashes.
- Merge the calibration recent entries under the actual uppercase spelling;
  discard references to missing thumbnail directories for the two utility books.
- Patch only the two utility-book index records and their existing name blobs.
  Preserve header, section sizes, permutations, firstSeen and all other records.
  Both spellings have the same UTF-8 byte length and the same folded sort key.
  Use zero modificationTime to avoid pretending cached metadata is current.
- Copy the released guide and firmware, checking their published SHA256 values.
- Verify all index identities against actual files, recent uniqueness, untouched
  reading state/book content/calibration curves, and unchanged index permutations.
- Run card_clean.sh; only after every check succeeds, sync and eject.

Do not force a library rescan: that previously froze the home screen (03.11).
Physical update and visual confirmation remain with Nikolai on the reader.

Observed result: `qa_runs/card-final-2026-11-05/result.json`.
Recent entries reduced 7 → 6; six indexed paths/hashes/sizes agree with the
actual files. The two utility-book records were repaired in place; the other
four records, section layout and sort permutations were preserved. Released
firmware and guide SHA256 matched the published sums. Fourteen protected files
(books, progress, bookmarks, current state and calibration curves) matched their
initial hashes. Backups: `qa_runs/card-final-2026-11-05/before/`.
No firmware source edits, new build, push or release occurred in this task.
[/AI]
