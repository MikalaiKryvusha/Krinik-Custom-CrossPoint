# Krinik Custom CrossPoint — Project History (the chronicle)

> The APPEND-ONLY chronicle of how this project lived and grew: closed sessions, shipped phases,
> releases, big decisions in the order they happened. This is where `STATUS.md` sheds its past —
> STATUS stays a short live summary of NOW; everything finished moves HERE (the "bonsai trim" step
> of `/end-chat-soft`).
>
> **Not required reading.** This file is NOT part of `/resume`'s canon set and not in the
> before-every-task minimum — open it only when you actually need the archaeology: how a decision
> came to be, what an old phase contained, when something shipped.
>
> **Chronicle rules (ADR discipline):**
> - **Append-only, newest on top.** A recorded entry is never edited to say something else —
>   history that can be rewritten is not history. Corrections come as NEW entries that reference
>   and supersede the old one.
> - An entry moves here VERBATIM from `STATUS.md` when its work closes — move, don't rewrite;
>   the entry already carries its dates, counters and file pointers.
> - Entries mention versions and dates freely — a chronicle legitimately speaks of old versions,
>   and the update machinery's stale-claims scan knows to leave this file alone.
> - When the file grows unwieldy, split by era: keep the newest era here, move older ones to
>   `PROJECT_HISTORY_<era>.md` files, and leave a one-line index at the top of this file
>   (the pattern large changelogs use).
>
> Living document — never DONE-tagged.

---

## Entries (newest first)

### 2026-11-13 — STATUS trim 4 (2026-11-13 19:45 +03:00): the summary of the closed chat 13:51 → 16:21 (moved verbatim)

- **Chat 2026-11-13 13:51 → 16:21 closed** (the owner's word 16:21 «закрывай чат, и продолжим в новом»). Done — detail in
  `PROJECT_HISTORY.md` (entry «STATUS trim 3»):
  - **debug10** = `wip/krinik-debug10` in `firmware/` (local, NOT pushed, NO image yet — the owner 16:02 «пока нет»):
    `9f02db5f` idea 07 long-tap rotation · `435d2493` epic 01 Ф1 (shade tile model + storage) · `551173b8` comment fix ·
    `52212d81` idea 08 «Настройки сна» · `8538f3dd` viewer: every TOUCH follows the picture as it stands, the KEYS keep
    the reading orientation, the book holds touch after a turned picture · `085c70d9` keys: short press pages, LONG press
    turns (`[AI]` forward clockwise, back counterclockwise) · `ed5e2f0d` a comment fix. All judged; simulator reports in `testcases/reports/2026-11-13_*`.
    The device env `x4pro-krinik-debug` builds on `085c70d9`: SUCCESS 2026-11-13 16:33, RAM 34.3 %, Flash 82.7 % — no image
    copied to `firmware-builds/` (the image comes with the shade, Ф4).
  - **msys64 moved to `F:\ai_sandbox\msys64`** (the owner 14:06); the old copy `D:\msys64.moved-2026-11-13` waits for his
    double-click on `Udalit staryj msys64 (KCCP).cmd` (desktop) — the agent's delete is refused by the permission rules.
  - Ideas recorded: 07 (rotation: built, simulator-tested), 08 (sleep settings: built, simulator S3 — the value-change part, S4 and S6 open), 09 (the viewer opens a picture in the orientation that
    fits its shape — verbatim only), epic 01 planned (`plans/01_EPIC_shade_tiles.md`, Russian).

- **The shade's elements are «кнопки» — the owner 2026-11-13 17:06 +03:00:** «Плитки шторки - переименовать в "Кнопки в
  шторке"» · «это не плитки, это Кнопки». Applied 17:07: the screen and the on-device strings, the meta-plan, MASTER_PLAN,
  plan 03, the cases, the map, code comments. Russian texts say «кнопка»; code identifiers (`ShadeTiles`, `Tile`) and
  English agent docs keep "tile"; the owner's own past quotes are left verbatim.
- KNOWLEDGE: the image viewer keeps the renderer in the picture's orientation and the keys in the reading orientation
  (internal map, `ideas/07`); one physical gesture has several input names and consumers — gate the touch frame
  (EXP-0016); simulator scripts need `<ms>:` on every item and rising times inside a WAIT segment — now a guard in
  `tools/sim_run.sh` (EXP-0015); the clock placeholder is filled only by Write/Edit, not by scripts (EXP-0012); the full
  host-test suite on this PC is 773/781 with 8 native-Windows failures (research 01); MSYS2 lives in `F:\ai_sandbox\msys64`
  (AGENT_GUIDE Build); Settings sub-screens past `SettingsSection::End` (internal map); `python -I` ignores `PYTHONUTF8`
  — use `-X utf8`; Settings screens are portrait while the reader and its shade follow the reading orientation.

### 2026-11-13 — STATUS trim 3: chat 13:51 → 16:21 closed, its «Where to continue» body (moved verbatim)

- **msys64 moved (owner 14:06 «D:\msys64\ давай переместим в F:\ai_sandbox\»)** — now `F:\ai_sandbox\msys64`
  (robocopy 14:09, 60 379 files / 2 293 125 441 bytes both sides); paths fixed: `firmware/platformio.local.ini`,
  `tools/sim_run.sh`, AGENT_GUIDE Build, research 01, Start-menu shortcuts, HKCU uninstall entry. The old folder is
  RENAMED `D:\msys64.moved-2026-11-13`; checked on F: alone — clean simulator build 271 files (0 from cache) SUCCESS,
  host tests 761/769 (the 8 are native-Windows portability, research 01), simulator runs with SDL2.dll from F:. The
  agent's delete of the old copy was refused by the permission rules → **`Udalit staryj msys64 (KCCP).cmd` on the
  owner's desktop** (checks F: first, removes the old copy, deletes itself) — waits for his double-click. Not ours to
  fix: Vibepollo/KAST build caches name `D:/msys64` (KAST's own MSYS2 was removed 2026-10-15; its plan 01 reinstalls to `D:\msys64`).
- **Idea 07 built and simulator-tested** on `wip/krinik-debug10` `9f02db5f` (from debug9, local): right-half long tap
  clockwise, left-half counterclockwise; judge no blockers; cases D0, C1–C5 pass
  (`testcases/reports/2026-11-13_idea07_simulator.md`). **Open with the owner:** after he turns the reader in his hands,
  whose halves — the owner chose B 14:54 «половины давай считать по картинке, убедил», then 15:05 every viewer gesture by the picture «как смотришь на картинку, так и управляешь, да, логично» (code change in flight). The
  device image comes with idea 05 (his «делаем» = one debug10).
- **debug10 now (firmware, local, not pushed):** `435d2493` epic 01 Ф1 · `52212d81` idea 08 «Настройки сна» (simulator
  S3 pass) · `8538f3dd` viewer: every TOUCH follows the picture as it stands (halves, swipes, Back), the KEYS keep the
  reading orientation (`MappedInputManager::setKeysFollowReadingOrientation`; the owner 15:20–15:21 «НЕТ! ФИзические
  кнопки крутят в одном направлении» · «одна кнопка в одном, вторая - в противоположном»), and after a turned book
  picture closes the book skips screen touches until its page repaints (≤ 3 s; device time is logged). Simulator C6–C9
  pass (`testcases/reports/2026-11-13_idea07_08_simulator.md`); five judge passes, two shapes refused (EXP-0016).
  The keys PAGE the pictures as before — the owner 16:01 «А — листают картинки, как и было» (no code change).
- **Idea 07 keys done 16:14** (firmware `085c70d9`): a short press of a page key pages the pictures on the release, a
  LONG press turns the picture (`[AI]` forward clockwise, back counterclockwise); judge no blockers; simulator C10–C12
  pass (`testcases/reports/2026-11-13_idea07_keys_simulator.md`). No interim image (the owner 16:02 «пока нет. работаем
  дальше»). **Next: epic 01 Ф2 P2.3** (`plans/03_epic01_p2_tiles_screen.md`). Context window 80 % at 16:03 — close the
  chat soon (`/end-chat-soft`).
- **Idea 05 = epic 01** (heaviness 2 of 5): research `researches/2026-11-13_idea05_shade_tiles_epic.md` (AOSP tile
  list, WCAG 2.5.7 up/down, CSS space-evenly, long tap → tile settings); meta-plan `plans/01_EPIC_shade_tiles.md`
  (Russian; phases Ф1 model+storage → Ф2 the «Плитки шторки» screen → Ф3 the shade row, new tiles, icons, long tap →
  Ф4 acceptance + image). **Ф1 closed 15:02** (firmware `435d2493`: `src/util/ShadeTiles.h` + host test 12/12 +
  storage; report `testcases/reports/2026-11-13_epic01_p1.md`). **Next: idea 08 «Настройки сна»** (plan inside the idea),
  then the Ф2 plan — written: `plans/03_epic01_p2_tiles_screen.md`, P2.1 recon done (a UiAppHost screen, not a
  UiListActivity: the list hides row rects); P2.2 icons — `tools/make_icon.py` draws ▲ ▼ and the half-filled circle
  (1-bit `freeink::Icon`); **next: paste them into `customListIcons.h`, then P2.3 `ShadeTilesActivity`.** Waiting on the owner: whether ALL viewer gestures (swipes, side taps, Back, the shade) follow the
  picture like the long-tap halves (asked 14:56, recommended yes — one rule; it also suits idea 09).
- **Chat 2026-11-13 10:34 → 13:35 closed — features for KCCP 1.1.3** (the owner's task under `resume`). Results:
  - **Idea 02 (tap a book picture → full screen, swipe Back → the same page): built.** `wip/krinik-debug9`
    (`526c7452` + `35dc070c`, local in `firmware/`, not pushed) = debug8 + the picture tap + battery log OFF; judged
    three times; host test `test/page_image_target/` 4/4 (red on a `<=` mutation); simulator C1–C5, C7, K1–K3 pass
    (`testcases/reports/2026-11-13_idea02_simulator.md`; C6 — the second fast Back swipe — only on the reader). Image
    `firmware-builds/cp-2.0.0-krinik-1.1.1-debug9.bin` (SHA256 `6b5f4f36…`) is on the reader's card since 11:47
    (card = debug9 + debug8 + 1.1.2). **On the reader 2026-11-13 13:51 +03:00 the owner: «открытие картинок на
    фулскрин работает»** (homework 04 steps 1, 3); steps 2, 4–7 (Back to the same page, the second fast Back, text taps,
    page brightness, long-tap rotation) not reported yet; no serial log taken.
  - **Bug 06** — the simulator kept its absolute gray mode after the image viewer (pages dark); fixed in the simulator
    clone on the LOCAL branch `fix/gray-absolute-reset` (`49ded1a`); PR #62 (`windows`, `087cb54`) untouched.
  - **Idea 03 (caption stays with its picture):** recon + research (`researches/2026-11-13_figure_caption_keep_together.md`,
    СТП 01-2017 БГУИР 2.5 read verbatim); direction by the owner: re-typeset the books to `<figure>`/`<figcaption>` +
    the firmware keeps a figure on one page (picture shrinks if needed); no first-line indent (owner 11:13);
    `[AI]` caption centred under the picture — the reading of СТП 2.5.5, not his word.
  - **Idea 04 (FB2 → EPUB on the reader):** first recon (upstream declined FB2 three times; papyrix-reader `lib/Fb2`,
    MIT); heavy → `/plan-epic`; test FB2 `D:\Hofshtadter_Gyodel-Esher-Bah-Eta-beskonechnaya-girlyanda.9y7ehg.198312.fb2.zip`.
  - **Idea 05 (shade tiles): AGREED, go-ahead 13:28** — a long tap on any tile opens Settings straight on «Плитки
    шторки» (list: icon · name · ▲▼ · firmware square checkbox; portrait; cursor on the tapped tile); seven tiles
    (night mode — new iOS-style half-filled circle icon, cleanup, orientation, touch, Bluetooth, Sleep — crescent,
    Flashlight); EQUAL gaps between tiles and at the edges for any count (today the edge gap is half). Final view
    `homeworks/05_shade_mockups/final.html`. `[AI]` defaults: Back returns to the book; also in «Настройки → Экран».
  - **Idea 06 (Home buttons settings)** — the same screen kind for the Home menu items (owner 13:29); verbatim only.
- **Chat 2026-11-13 13:51 → (open).** The owner on debug9: picture opening works; «подписи … всё ещё открываются от
  картинок» — `[AI]` read as «отрываются», expected (idea 03 has no code; recorded there). New **idea 07** (owner 13:51):
  in the viewer a long tap on the right half turns the picture clockwise, on the left half counterclockwise — code recon
  in the idea (`BmpViewerActivity::loop()` already gets the long-tap point in reading-orientation coordinates and ignores
  it; `rotate()` turns one way); answered «можно», offered for debug10 together with idea 05 — **go-ahead 14:03 «делаем»**: debug10 = debug9 +
  idea 07 + idea 05.
- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` (shared PC: KUMM, KAGO).
  2. **The rest of the owner's debug9 check (homework 04, steps 2, 4–7).** When he says the reader is on the cable (book screen, NOT USB drive):
     `.pio-venv/Scripts/python.exe -I -X utf8 tools/serial_log.py <scratch>/serial_debug9.log` in the background; watch
     `Image tap`, `Back swipe`, `[ERR]`, `OOM` (the debug image logs at LOG_LEVEL=1 — INF and up). His verdict → homework
     04 «Итог», `ideas/02` closure, `testcases/TC_idea02…` C6.
  3. **Epic 01 (idea 05) by `plans/01_EPIC_shade_tiles.md`** — the phase in flight and its plan are named at the top
     of this list; the «Плитки шторки» screen of Ф2 is reused later by idea 06 «Кнопки главного экрана».
- **Open work, in order:**
  1. Idea 05 + 06 (one list component); 2. Idea 03 (re-typeset tool + firmware `<figure>`); 3. KCCP 1.1.3 assembly:
     merge release 1.1.2 (`198d385e`) into the debug line (conflicts `lib/hal/HalFrontlight.{cpp,h}`,
     `test/frontlight_dither/`); the owner's open choice: light-linger hold (400 ms) vs timer-redraw hold; 4. Idea 04
     (epic). 5. Bug 01 PR `pr/library-tab-fit` (`d2b45c0e`, `d0c99508`) — a free upstream slot (5/5) + proofreading.
     6. `bugs/05`, `bugs/06` (a simulator PR for 06 needs the owner's proofreading). 7. The test hook does not see
     `tools/sim_run.sh` runs: a `testHook` block in `.kaif/kaif.json` — to be asked (the auto-mode
     classifier refused the agent's edit). 8. Proofread `GOAL.md`. 9. Delete the partial `C:\msys64` (check the machine lock).
  - Reviews to read: simulator PR #62 and firmware PRs #4328 #4332 #4375 #4376 #4377
    (`gh api repos/<owner>/<repo>/pulls/<n>/comments --jq '.[]|select(.created_at>"<last read>")'`).
- KNOWLEDGE: `python -I` ignores `PYTHONUTF8` — use `-X utf8` (AGENT_GUIDE Code style, updated);
  the simulator's reader takes the OVERLAY gray path, only the viewer uses absolute (`bugs/06`); Settings screens are
  portrait while the reader and its shade follow the reading orientation; the firmware checkbox is a square with a
  filled inner square (FreeInkUI `list.h`); a launched Edge window is not a shown window (EXP-0014); a page server under
  `timeout` dies (EXP-0013); `pdftotext` is at `/mingw64/bin` (Git for Windows); the debug image number lives in
  `platformio.ini` (AGENT_GUIDE Build, updated). Reader clock may run ≈ 40 min fast (unverified, PROJECT_HISTORY).

### 2026-11-13 — STATUS trim 2: closed hardware research, the tiles idea, old debug-line notes (moved verbatim)

### Hardware research

- Closed 2026-11-08: no charging cut-off (needs a board modification); the charger analysis and the battery/light
  measurements moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-09, STATUS trim).
- **Closed [2026-11-13 10:36 +03:00]: battery-discharge measurements stop; no more search for ways to cut the current
  through the frontlight** — `[OWNER] 2026-11-13 10:36 +03:00 · chat: «там ты замерял разряд батареи, я думаю, что можно
  прекратить эти замеры. Подсветка не много кушает заряда батареи, и можно перестать искать способы снижения тока через
  подсветку»`. Open: whether the debug-only 20-minute battery log leaves the debug builds (asked in chat, same turn).
- LED driver/current/ratings stay unknown — no longer researched (decision above).

### Future (owner, 2026-11-06: "on the future")

- Configurable Control Center tiles in a separate menu (add Sleep/Flashlight, hide Bluetooth/Clean). Recon:
  `src/activities/util/FrontlightPanelActivity.*`, `kTileCount`, `runTile(idx)`, `buildPanelScreen`.

From «Device»:

- Battery log every 20 min is a **DEBUG ONLY** aid — keep it out of release builds.
- Debug line: debug3 (precise temperature), debug4 (battery log tick every 20 min), debug5 (= debug4 + "Sleep" item in the Home
  menu under "Flashlight"). Images and SHA256 in `firmware-builds/`; evidence in
  `qa_runs/precise-temperature-2026-11-06/`, `qa_runs/debug4-2026-11-06/`, `qa_runs/debug5-sleep-menu-2026-11-06/`.
- The debug2–5 code was uncommitted on the laptop; it is now `wip/krinik-debug5` in both forks (see the code map). The debug2 image
  itself is in `firmware-builds/` (`cp-2.0.0-krinik-1.1.1-debug2.bin`).

### 2026-11-13 — STATUS trim: the 2026-11-10 chat's handover lines (moved verbatim from STATUS "Where to continue")

- **Chat 2026-11-09 20:30 → 2026-11-10 (CodeRabbit round 3, debug7/8, simulator PR #62) closed** — its full log moved
  verbatim to `PROJECT_HISTORY.md` (entry 2026-11-10). Result: #4377 books-card title fix pushed (`c9d69cbd`); #4376
  redraw-timer fix pushed (`94e1c3a2`) after the owner's reader check; debug7 (bugs 03/04) and debug8 (idea 01) PASS on
  the reader; native Windows simulator PR **#62** opened and its CodeRabbit round 1 fixed (`087cb54`).
- **Rules born this chat** (all in `AGENT_GUIDE.md`): reviewer bots can be wrong — trace a finding in code before
  acting; after a code change an independent judge first, build after; a PR description carries no AI-participation
  line and nothing sent out carries AI authorship (no `Co-Authored-By` trailer on pushed commits).
- KNOWLEDGE: Windows UCRT `TZ` — three-letter names only, DST on US dates (simulator README, research 01); Winsock
  sockets cannot be `dup()`-ed and `_execvp` does not replace the process (research 01); `MoveFileEx` for an
  overwrite-safe replace; lessons EXP-0008…0010 (`EXPERIENCE.md`): Git Bash grep crashes on long pipes, a "defect" that
  was my script quitting first, parallel shell calls must not rely on `cd`.

### 2026-11-13 — battery research closed; the debug battery log's final numbers ✅

The owner closed it (`[OWNER] 2026-11-13 10:36 +03:00 · chat: «…можно прекратить эти замеры. Подсветка не много кушает
заряда батареи…»`, 11:04 «логи можно отключать в следующей дебаг сборке. чтобы они не кушали батарею и флешку не
изнашивали»): `KRINIK_BATTERY_LOG` is off from `1.1.1-debug9`. The final log — 7.0 days, 2026-11-06 11:05 →
2026-11-13 11:18 by the reader's clock, 732 rows (`qa_runs/battery_log-2026-11-13-final.csv`; summary
`python -I -X utf8 tools/battery_summary.py <csv>`):

| Mode (not charging) | Hours | Drain | One charge lasts |
|---|---|---|---|
| reading, light off | 3.7 | 3.56 %/h | ~28 h |
| light on 11–50 % (UI) | 2.5 | 4.01 %/h | ~25 h |
| light on > 50 % (UI) | 11.3 | 8.46 %/h | ~12 h |
| sleep (40 periods) | 111.5 | 0.43 %/day | months |

Sleep periods ≥ 6 h: 8, 86.8 h, 0 % lost. Caveats: the gauge counts in 1 % steps; few light-off hours; page turns
are mixed into the awake rows. Side finding, not checked: the log's last row is a boot at 11:18 by the reader's
clock, while the reader was on the wire at ≈ 10:37 PC time — the reader's clock may run ≈ 40 min fast.

### 2026-11-10 — CodeRabbit round 3, debug7/8, simulator PR #62 (moved verbatim from STATUS "Where to continue")

- **Chat 2026-11-09 (resume → CodeRabbit round 2) closed 20:20 +03:00** — its full log moved verbatim to
  `PROJECT_HISTORY.md` (entry 2026-11-09, "CodeRabbit round 2"). Result: all 14 CodeRabbit comments answered or fixed,
  `pr/screen-redraw-delay` and `pr/screen-calibration` pushed to the fork, 12 replies posted (research 02 → "Reply
  drafts"); the owner checked the power-hold fix on his reader (debug6). Interviews #001 and #003 closed.
- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` — the PC is shared with KUMM (Conan
     benchmarks) and KAGO; during another agent's quiet window: no builds, no simulator, no GUI windows.
  2. Read CodeRabbit / maintainer answers on #4328 #4332 #4375 #4376 #4377:
     `gh api repos/crosspoint-reader/crosspoint-reader/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id!=null)'`.
     READ [2026-11-09 20:30 +03:00]: all 12 replied threads resolved by CodeRabbit, no maintainer comments, CI green on #4376/#4377.
     OPEN: #4377 new round on `d8573ad5`, two Minor — `CalibrationCardStorage.cpp:17` (books card keeps the old-language
     title, written once) and `:104` (v1 EPUB's `/.crosspoint/epub_<hash>/` cache not removed); #4376 asks for an X4 Pro
     hold/short-press check (owner did it on debug6 — reply); #4328 asks whether to open a follow-up issue (post-table OOM).
     Traced by me (not taken on CodeRabbit's word): `:17` holds — the title is baked into the EPUB (`CalibrationCard.cpp`
     dc:title/nav/page) and shown via `epub->getTitle()`; a fix must also drop the card's `epub_<hash>` cache (title is
     cached in `book.bin`). `:104` is true but low value — v1 existed only inside this unmerged PR.
     Owner 20:33 «да, это наш промах. Доработать нужно»; on `:104` «можно сделать строку для перестраховки, но написать,
     что это несущественно». DONE: fix `c9d69cbd` pushed to the fork 22:17 (#4377 head) — `booksCard()` reuses the
     card only while `Epub::loadMetadata()` title == current language, else `clearBookCache` + rewrite via
     `Storage.replaceFile`; v1 cache cleared. Simulator: RU→EN title, reuse, control on `d8573ad5` red (testcases
     `TC_coderabbit_round2_calibration.md` §7). Found on the way: simulator `replaceFile` could not overwrite on Windows
     — fixed `ba46fb7` on simulator `windows` (LOCAL, its push is the owner's open question). 4 replies POSTED
     22:17–22:22 (owner «отправляй», #4328 «A»). WAITING FOR THE OWNER (research 02 → "Round 3 — posted"): #4376 —
     owner 22:26 «Питание коротко: сон стоит»; his repeat with «Игнорировать» 22:31–22:39 (homework 01): hold during the
     redraw wakes ✅, click during the redraw sleeps ✅, and TWO defects → `bugs/03` (redraw timed from the last
     non-waking press on debug6; LOST entirely on PR #4376) and `bugs/04` (click in the light linger cancels the
     sleep; owner A1: click only with «Сон», else a hold). Fixes judged twice by an independent agent (round 1 REFUTED
     the PR fix — the path was cleared before the re-arm), both now VERIFIED WITH CAVEATS: debug7 `2b150595`
     (`wip/krinik-debug7`, local) built → `firmware-builds/cp-2.0.0-krinik-1.1.1-debug7.bin` (SHA256 `8662b4db…368f`),
     smoke `qa_runs/smoke_2b150595`; PR `94e1c3a2` local, NOT pushed (x4pro compile check running). x4pro compile of
     `94e1c3a2` SUCCESS. 23:14 debug7 on the card (SHA256 checked there), card cleaned to debug7 + debug6 + 1.1.2,
     reader ejected. 23:22 owner: homework 02 «все кейсы PASS, всё ок» → bugs 03/04 DONE. NEXT: push `94e1c3a2` + reply CodeRabbit #4376 (owner's word); idea 01 (Home «Сон» highlight on tap, owner 23:22).
     Owner's open choice: the linger hold (400 ms) vs the redraw hold (≈ reset-to-sample) rules differ.
     #4377 `:115` truncated-card finding — decline draft to proofread. CI on `c9d69cbd`.
  3. Card cleanup DONE 2026-11-09 23:14 (`[OWNER] 20:09 «и образы старые поудаляй»`; rule: current debug + previous
     debug + latest release): `/.firmware/` = debug7 + debug6 + 1.1.2; reader ejected.
- **Open work, in order:**
  0. **debug8 DONE** 2026-11-09 23:46 (idea 01, Home «Сон» highlight on tap): `c072214b` on `wip/krinik-debug8`
     (local), judged, simulator + control, on the owner's reader «да, работает» (homework 03). Card = debug8 + debug7 +
     1.1.2. #4376 fix `94e1c3a2` PUSHED 23:26 + CodeRabbit reply 4517595666 (owner «1 да»).
  1. **Simulator upstream PR** (owner «делай» 20:13; order agreed 23:29): the «SHOT stalls after a second WAIT»
     defect is NOT A DEFECT (23:50, research 01 — my probe had QUIT at 500 ms before SHOT at 800 ms). Windows checks
     2026-11-10 00:02–00:35 (research 01): HTTP ✅, clock = UTC as documented, X4 env ✅; File Transfer (empty reply,
     `dup()` of a Winsock socket) and sleep/wake (caller not waiting, exit status lost) fixed in `dfd450a` (local,
     judged twice, runs pass with controls, kill-the-waiter PASS after the owner's «РАЗРЕШАЮ» 00:46). `bugs/05` (firmware
     UDP `close()` on Windows) — found by reading, not reproduced. SQUASHED 00:51 → `ad131dc` (backup branch `windows-unsquashed`). On firmware `develop` `f8db833f`: builds, web_manager_smoke 8/8 (pre-fix ❌), the sample ini as written builds (+ the #60-style substitutions), system curl.exe HTTPS ✅. PR draft `qa_runs/pr-simulator-windows/body.md`, images pr-assets `15-windows-simulator/` (HTTP 200). Owner proofread «no remarks» 01:07, «отправляем» 01:08 → `windows` pushed, **PR #62 OPENED** 01:09 https://github.com/crosspoint-reader/crosspoint-simulator/pull/62 (mergeable, CodeRabbit running; AI footer removed per owner 01:09). `firmware/` back on `wip/krinik-debug8`. CodeRabbit round 1 on #62 (5 findings, all traced valid) → fix `2c34be9`+ judged (VERIFIED WITH CAVEATS; ANSI TEMP path regression found and fixed). AUTH: `[OWNER] 2026-11-10 01:38 +03:00 · chat: «на все отпраки ДАЮ РАЗРЕШЕНИЕ» · «на все твои сообщения ДАЮ РАЗРЕШЕНИЯ»` (pushes, PR replies, the closing push of this repo). OWNER 01:36 «работай автономно»: push the fixes, read CodeRabbit ~20 min later, fix until no remarks and the PR waits for a maintainer, then close the chat. 01:40–01:47 round-1 fixes run (injection probe: verbatim, no marker; control on ad131dc ran the command; replaceFile probe; web_manager_smoke 8/8; HTTPS via the new launcher; WebDAV backslash escape rejected), commits reworded without AI trailers (owner «только без авторства ИИ» 01:39), force-pushed `087cb54`, 5 replies posted, PR body updated. NEXT: ~02:08 read CodeRabbit round 2 on #62; was: squash 8 local commits, PR text for the
     owner's proofreading, his word to push `windows`.
  2. **Bug 01 PR** `pr/library-tab-fit` (`d2b45c0e`, `d0c99508`) — five themes checked; waits for a free upstream
     slot (5/5 open) and the owner's proofreading of the PR text.
  3. **Debug line**: `wip/krinik-debug6` (`e7a29dd4`, local in `firmware/`, not pushed) = debug5 + the hold fix, on
     the owner's reader now. BACKLOG: merge release 1.1.2 (`198d385e`) into the debug line (conflicts in
     `lib/hal/HalFrontlight.{cpp,h}`, `test/frontlight_dither/`), then `1.1.2-debugN`.
  4. Owner's open questions: proofread `GOAL.md`; the push of this repo is done each closing.
  5. Delete the partial `C:\msys64` left by the killed 14:44 install (KAGO said it is safe) — check the machine lock first.
- **Rules born this chat** (all in `AGENT_GUIDE.md`): screenshots WebP q90, viewed as WebP; simulator window 480×800
  1:1, borderless, top-left; images to the reader only after a simulator smoke of the same commit, only KCCP
  debug/release builds, eject the reader after copying; build from PowerShell with `PYTHONUTF8=1`; the `firmware/`
  clone keeps `core.autocrlf=false`.
- KNOWLEDGE: native Windows simulator works (research 01, `AGENT_GUIDE.md` → Build/Test harness); debug line is on
  1.1.1 without 1.1.2 (this file); seven lessons EXP-0001…0007 (`EXPERIENCE.md`); bug 01 (`bugs/01_…`), bug 02 not a
  defect (`bugs/02_DONE_…`).

### 2026-11-09 — CodeRabbit round 2, native Windows simulator (moved verbatim from STATUS "Where to continue")

- **Active task (owner, chat 2026-11-09 14:39):** «чиним замечания, которые нам сделаны в наших ПР» — the 14 CodeRabbit
  inline comments on PRs #4328 (3), #4332 (1), #4375 (1), #4376 (4), #4377 (5); «тестируем на симуляторе на этой машине».
  Comments dumped by `gh api repos/crosspoint-reader/crosspoint-reader/pulls/<n>/comments` (filter `coderabbit`).
  Fixes go to the fork's `pr/*` branches in `firmware/`; no push and no reply text without the owner's word.
  Progress 2026-11-09 14:56: all 14 triaged in `researches/2026-11-09_coderabbit_pr_review.md` — 2 addressed earlier
  (#4328), 1 already fixed on the branch (#4332, ca5d9fa0), **5 local fixes committed, NOT built, NOT pushed**:
  `pr/screen-redraw-delay` d101e463 · 2d5bb845; `pr/screen-calibration` b6477e41 · 75b92fc0 · 7addf5be. Open: #4328-3
  (defensive fix proposed), #4375 string (owner's wording), #4376 main.cpp:541 and :722, #4377 ImageBlock and
  orientations (replies proposed). Correction: commit 338f0b7 says "6 local fixes" — the count is 5.
  Progress 2026-11-09 15:25: re-dump — still 14 CodeRabbit comments, no human review comments. #4376 main.cpp:541
  fixed locally `9448f2a5` (6 local fixes now); #4328-3 → reply, no code (path unreachable; research 02). Interview
  #001 closed (both answers were already in code). Still open: #4375 string, #4376 main.cpp:722, #4377 ImageBlock —
  owner answered interview #003 at 15:43: Q1 D (no change, reply), Q2 B → `b661b6be` on `pr/screen-calibration`,
  Q3 B → `4818dba0` on `pr/screen-redraw-delay` (device check is the owner's). 8 local fixes, none pushed.
  2026-11-09 18:35–18:47: KAIF marks stripped (`2dbfff7d`, `d8573ad5`; grep → 0 on every `pr/*`); simulator runs
  done for both branches with controls — `testcases/TC_coderabbit_round2_redraw_delay.md`,
  `testcases/TC_coderabbit_round2_calibration.md`; status per comment in research 02. Not observable here:
  `9448f2a5`, `4818dba0` (`!SIMULATOR`), `75b92fc0` (OOM). Owner's word on sending, 2026-11-09 18:50 +03:00, after
  seeing all 12 reply texts in the question preview: `[OWNER] «давай протестируем кнопку, и всё тправим»` (typed
  first in the wrong layout: «jnghfdkztv jndtns» = «отправляем ответы»). Order: device image of
  `pr/screen-redraw-delay` → the owner checks the power hold during the timer redraw on his reader → push both
  branches → post the 12 replies of research 02 → "Reply drafts".
  19:05–19:12: the owner ran step 4 on the bare-upstream PR image — the hold woke the reader (bug 02 closed, not a
  defect) — and then ruled: test images are KCCP debug/release builds only (`AGENT_GUIDE.md` → The device). New:
  `wip/krinik-debug6` = debug5 + the #4376 hold fix ported by hand (`e7a29dd4`, firmware fork, local; the other three
  #4376 fixes do not apply to the KCCP code). Next, after KUMM's «замеры закончены»: build `x4pro-krinik-debug` →
  simulator smoke of `e7a29dd4` → image to the card → homework 01 steps 4–5 on debug6 → push + replies.
  20:10: debug6 built, smoke pass, on the card (SHA256 bf9f0a9f…), reader ejected. PENDING on the next connect: delete
  from the card's `/.firmware/` debug3, debug4, `crosspoint-2.0.0-x4pro.bin`, `cp-2.0.0-pr4376-2dbfff7d.bin` (owner:
  keep debug6 + debug5 + 1.1.2), then eject.
  Owner asked 20:10 why the debug builds say 1.1.1 («давно вышел релиз 1.1.2»): the debug line forked from 1.1.1
  (`a06a20d6`); the 1.1.2 release is one commit `198d385e` NOT in it; a merge conflicts in `lib/hal/HalFrontlight.{cpp,h}`
  and `test/frontlight_dither/FrontlightDitherTest.cpp` (both sides reworked the frontlight). Owner: test debug6 as it
  is now. BACKLOG: merge 1.1.2 into the debug line → `1.1.2-debugN` (frontlight conflicts, the owner's reader check).
- **DONE 2026-11-09 20:15 +03:00:** the owner confirmed the power button on debug6 («если нажать во время
  перерисовки - перерисовка выполняется и устройство просыпается»); pushed `pr/screen-redraw-delay` d7cc4e83..2dbfff7d
  and `pr/screen-calibration` f90b29b4..d8573ad5 to the fork; posted the 12 CodeRabbit replies (texts of research 02,
  first reply https://github.com/crosspoint-reader/crosspoint-reader/pull/4328#discussion_r4515664220). Next: watch for
  CodeRabbit/maintainer answers.
- **Owner's bug 01 (2026-11-09 16:55):** Library tab «Недав...» → `bugs/01_library_tab_label_truncated.md`; fix
  `d2b45c0e` on the new branch `pr/library-tab-fit` (cut from `upstream/develop` f8db833f), red/green WebP shots in
  `qa_runs/tab_fit_before|after/`; the owner wants it as an upstream PR — it waits for a free slot (5/5 open).
- Runs 2026-11-09 17:27–17:48 (after the KUMM windows): bug 01 English control pixel-identical; #4376 C1 pass (X4
  Pro shows «Обновлять заставку» in «Настройки очисток экрана»), C2 pass + K1 red (X4 keeps `sleepRedrawDelay`; the
  pre-fix `d7cc4e83` drops it). Bug 01 later widened per the owner (`d0c99508`, content-width pills, five themes).
  KUMM may ask for more quiet windows: then no builds and no GUI windows until its «замеры закончены».
- **Simulator upstream PR** — owner «окей» 2026-11-09 17:25 +03:00 to the plan: after the KUMM window run the
  unobserved parts (File Transfer, curl, sleep/wake relaunch, clock, X4 env), add `sample-platformio-windows.ini` +
  README, squash, bring the PR text for proofreading; sending only on his word (research 01 → "Upstream PR readiness").
- **Simulator:** WORKS natively on Windows since 2026-11-09 16:52 (`simulator` `0431782` + window placement). Build
  from PowerShell with `$env:PYTHONUTF8="1"`; run `SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh …` from Git Bash.
  Native Windows build of our fork `MikalaiKryvusha/crosspoint-simulator`, branch `windows`, clone in
  `simulator/` — route and POSIX inventory in `researches/2026-11-09_native_windows_simulator.md`. WSL is never used.
- Toolchain installed 2026-11-09 15:18–15:24 (lock `kccp` taken until 16:03): MSYS2 UCRT64 in `D:\msys64`,
  PlatformIO 6.2.0 in `.pio-venv/`, envs `simulator_win` / `simulator_x4_pro_win` in the ignored
  `firmware/platformio.local.ini` (research 01 → "Installed on this PC"). Partial `C:\msys64` still to delete.
- **Next:** finish the runs of `pr/screen-redraw-delay` and `pr/screen-calibration` → strip the marks → device image
  for the owner's Q3 check → ask the owner before any push or reply. Owner's open questions: proofread GOAL.md; push
  of this repo (`git log --oneline origin/main..HEAD`); the CodeRabbit reply texts (after the runs).
- KNOWLEDGE: the simulator needs a native-Windows port, WSL is never used · `AGENT_GUIDE.md` → Build, research 01;
  the PC is shared with the KAGO agent (machine lock) · `AGENT_GUIDE.md` → Build, `EXPERIENCE.md` EXP-0002.

### 2026-11-08 — Left on the laptop (moved verbatim from STATUS on 2026-11-09)


The repo is public, so this stayed in `~/Xteink` on the laptop (≈ 3.2 GB, 3 162 files; per-file list with sizes in
`legacy/left-on-laptop.tsv`):

| Size | Files | What | Why not here |
|---|---|---|---|
| 1 650 MB | 1 162 | test books (EPUB) | third-party texts |
| 1 466 MB | 1 462 | BMP sleep screens and panel test images | third-party art, size |
| 86 MB | 195 | SD-card and simulator binaries in `qa_runs/` | rebuildable |
| 19 MB | 125 | stock-firmware research: vendor firmware, disassembly, certification and teardown photos, datasheet | vendor/third-party material |
| 8 MB | 212 | reader cache copied from the card (book chapters, images) | third-party texts |
| — | 3 | `.crosspoint/wifi.json` copies | Wi-Fi credentials |

Also stayed: the local clones `firmware/`, `fw-pr/`, `pr-fixes/*` (all branches are on the fork — checked 2026-11-08), `pr-assets/`,
`KEINKT/`, `keinkt-fixes/` (on GitHub), the PlatformIO venv, `.kaif/` scratch of the old setup. The Home Wi-Fi network name was
replaced with a placeholder in `restore.mjs` and the legacy README.


### 2026-11-09 — STATUS trim: closed hardware research (charging, measurements) ✅
- Charging cannot be stopped in software at 4.1 V or N %: no charger on I²C, no CE/EN line to the ESP32. Only a board modification
  could do it. **Not doing it** (owner, 2026-11-08: «это не будет делаться»). Available now: a "unplug the charger" reminder at N % in firmware. Analysis:
  `researches/2026-11-06_stock_batinfo_charger_analysis.md` (its raw inputs — vendor firmware, disassembly, third-party photos —
  stayed on the laptop, see below).
- Measurements, do not repeat without a goal: charge 50→100 % in 1:07:06, gauge max 4.381 V
  (`qa_runs/debug2-charge-2026-11-06-180555/`); awake hour: light off ≈ 4–5 pp, light 100 % ≈ 8–9 pp
  (`qa_runs/debug2-light-hours-2026-11-06-201434/`).

### 2026-11-09 — KAIF deployed on the owner's PC (Task 0 step 3) ✅
- **Task 0 step 3 done 2026-11-09:** KAIF 2.9 (+2.10 WIP) deployed from KAIF commit d2f21274d396, commits 8a78058,
  2924afa; field report KAIF issue #195. Steps 1 (firmware clone — done 2026-11-09), 2, 4–6 open.

Earlier history (laptop era, Russian): `legacy/PROJECT_HISTORY.ru.md`.
