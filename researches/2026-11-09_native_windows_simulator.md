# Research 01 — native Windows build of the CrossPoint simulator

> **Created:** 2026-11-09 · **Parent:** owner's order in chat, 2026-11-09 14:39–14:43 +03:00 (below) · **Status:**
> recon done 2026-11-09 14:45 +03:00; toolchain install started · **Outbound:** the port may go upstream to
> `crosspoint-reader/crosspoint-simulator` as a PR — owner's decision, later.

## Owner decisions (verbatim, chat 2026-11-09)

- `[OWNER] 14:39` «тестируем на симуляторе на этой машине»
- `[OWNER] 14:41` «WSL - нет, и не будет!»
- `[OWNER] 14:42` «собираем свой симулятор под Windows»
- `[OWNER] 14:43` toolchain: «MSYS2 UCRT64 (Recommended)»; home: «Форк на GitHub (Recommended)»
- `[OWNER] 14:43` «нужно будет - заводим свой форк и проект в GH»

## External truth

- `crosspoint-simulator` README: "Native Windows is not supported; use WSL" · tested on macOS x86_64/ARM64 and Ubuntu
  under WSL · "Other platforms may need additional libraries or platform-specific stubs". Prereqs: SDL2, curl,
  OpenSSL headers (Linux).
- No issue about native Windows in `crosspoint-reader/crosspoint-simulator` or `crosspoint-reader/crosspoint-reader`
  (`gh search issues … windows` → 0, 2026-11-09).
- Firmware fork `platformio.ini` `[env:simulator]` is the macOS sample (`!sdl2-config --cflags --libs`,
  `-D_LIBCPP_DISABLE_AVAILABILITY`); the Linux sample adds `-lssl -lcrypto`.
- FORK: toolchain MSYS2 UCRT64 gcc | MSVC Build Tools + vcpkg · price: rewriting gcc flags and `sdl2-config` for MSVC ·
  consulted: the owner (answer above); the fork's flags are gcc-only.

## POSIX inventory of `crosspoint-simulator` src (110 files, HEAD 04332e7)

| File | POSIX dependency | Windows replacement |
|---|---|---|
| `WebServer.cpp`, `WebSocketsServer.cpp`, `CrossPointWebServer.cpp`, `NetworkClient.cpp`, `lwip/sockets.h` | BSD sockets, `select`, `fcntl(O_NONBLOCK)`, `close` | Winsock2: `WSAStartup` once, `closesocket`, `ioctlsocket(FIONBIO)`, link `-lws2_32` |
| `HalStorage.cpp` | `dirent`, `statvfs`, `mkdir(path, mode)` | MinGW `dirent.h`; `GetDiskFreeSpaceExW`; `mkdir(path)` |
| `nvs.h`, `common/FsApiConstants.h` | `sys/stat`, `fcntl` | MinGW has both; check `mkdir` arity |
| `MD5Builder*.h`, `WolfsslCrypto.h`, `wolfssl/wolfcrypt/hash.h` | `CommonCrypto` (`__APPLE__`) / OpenSSL (`__linux__`) | take the OpenSSL branch for `_WIN32` too (MSYS2 `openssl`) |
| `SimHttpFetch.h` | `popen` + `curl`, `sys/wait` (`WEXITSTATUS`) | `_popen`/`_pclose` + `C:\Windows\System32\curl.exe` |
| `SimulatorLifecycle.cpp` | `execvp` (restart) | `_execvp` (`process.h`) |
| `simulator_main.cpp`, `esp_sntp.h`, `HalClock.cpp` | `unistd`, `sys/time` | MinGW provides; `HalClock.cpp` already has `_WIN32` branches |

The firmware's own simulator paths may hold more POSIX — found only by compiling.

## Installed on this PC (2026-11-09 15:18–15:24 +03:00, under the machine lock `kccp`)

- MSYS2 in **`D:\msys64`** (`winget install MSYS2.MSYS2 --location D:\msys64`), not `C:\msys64` (the partial `C:\msys64`
  from the killed 14:44 install is still there — KAGO: safe to delete). UCRT64: gcc 16.2.0, cmake 4.4.5, ninja, pkgconf,
  SDL2, openssl, python 3.14.10, git, make.
- PlatformIO Core 6.2.0 in the workspace venv `.pio-venv/` (Python 3.11 via `py -3.11`; the `py` launcher lists a 3.12
  whose `python.exe` is gone).
- The env lives in `firmware/platformio.local.ini` (ignored by `*.local*`; `platformio.ini` pulls it via
  `extra_configs`), so `pr/*` branches stay clean: `simulator_win` / `simulator_x4_pro_win`, simulator lib =
  `symlink://` to `simulator/`. `sdl2-config` is a shell script cmd cannot run → the SDL2 flags are spelled out
  (pkg-config's `-mwindows` left out so the log stays on stdout).
- Build: `$env:PATH = "D:\msys64\ucrt64\bin;" + $env:PATH; .pio-venv\Scripts\pio.exe run -d firmware -e simulator_x4_pro_win`.

## Port progress

- Build 1 (2026-11-09 15:24, `pr/screen-redraw-delay` 9448f2a5): failed on `MD5Builder.h` (#error), `SimHttpFetch.h`
  (`sys/wait.h`) and the firmware's `strlcpy` (`WifiSelectionActivity.cpp:228`; MinGW has none).
- `simulator` `d9adeea` (written during the KUMM benchmark pause, NOT compiled): the whole inventory above, behind
  `_WIN32` — OpenSSL MD5; `lwip/sockets.h` = Winsock + `WSAStartup` + send/recv/setsockopt overloads + `fcntl`;
  `SimHttpFetch.h` %TEMP% + cmd quoting; `strlcpy` in `Arduino.h`; `SimPosixCompat.h` (`mkdir` 2-arg, `fsync`,
  `O_BINARY`); `std::filesystem::space` for `statvfs`. The firmware's own `src/network/CrossPointWebServer.cpp`
  includes `<lwip/sockets.h>` and uses `fcntl` / `close` on its UDP discovery socket.
- Risk (b): that `close(fd)` reaches the CRT `_close()` with a Winsock handle — an invalid-parameter abort is
  possible when the web server stops. Not on the path of the PR checks; watch for it when File Transfer is closed.
- Build 2 (2026-11-09 16:43, after the KUMM pause): every object compiled except two — the firmware's
  `src/network/CrossPointWebServer.cpp` (`windows.h` via `lwip/sockets.h` defines `IGNORE`, which kills the enum
  `SHORT_PWRBTN::IGNORE` in `CrossPointSettings.h:167`) and the simulator's `HalClock.cpp` (`setenv`; MinGW has
  `_putenv_s`). Fix: `#undef` the colliding `windows.h` macros right after Winsock; `setenv`/`unsetenv` in
  `SimPosixCompat.h` (also used by `SimulatorLifecycle.cpp`). Note: the UCRT `tzset()` reads only the simple `TZ`
  form, so a POSIX rule with DST may show a shifted clock in the simulator.
- Risk (b), seen in build 2: `windows.h` macros (via `winsock2.h`) inside the firmware's web-server TU — `WIN32_LEAN_AND_MEAN` and
  `NOMINMAX` are set; the compiler will show what is left.

## Upstream PR readiness (2026-11-09 17:23 +03:00, owner asked «в апстрим симулятор Windows можем отправить?»)

- `crosspoint-reader/crosspoint-simulator` takes outside PRs (#46–#61 by osteotek, gkaindl, lpla; no CONTRIBUTING.md);
  we have 0 open there; our branch is level with `upstream/main` (0 commits behind).
- Observed working: build, boot to Home, Home → Library, scripted keys, `WAIT`, screenshots, window placement.
- Not yet observed: File Transfer web server (Winsock path, the `close()`-on-socket risk), HTTP fetch via curl/cmd,
  sleep → wake relaunch (`SimulatorLifecycle` `execvp`), clock in UTC (UCRT `tzset`), the X4 (non-Pro) env, and that
  macOS/Linux still build (no Linux here; WSL is never used — upstream CI #60 may cover it).
- Windows checks 2026-11-10 00:02–00:30 (firmware debug8 `c072214b`, simulator `ba46fb7`):
  - **HTTP via curl — PASS.** Settings → Чтение → Управление шрифтами → Wi-Fi «Simulator WiFi (fake)»: `Downloading:
    https://github.com/…/fonts.json` → `Downloaded 29187 bytes` → `Manifest loaded: 35 families` (`qa_runs/win_font_http`).
    The OTA check does no HTTP in the simulator (`[SIM] OTA check is non-destructive; reporting no update`).
  - **Clock — as documented.** Shots show UTC (21:02 at 00:02 +03:00); README already says the Windows CRT takes only
    the simple `TZ` form.
  - **File Transfer — DEFECT, fixed in `bfe0140` (local, judging).** Hotspot server on :8080 received and served
    `GET /`, `/api/files`, an upload (file written), but curl got `Empty reply from server` (exit 52,
    `qa_runs/win_ft_hotspot`): `WebServer::handleClient()` gave the handler `NetworkClient(::dup(client))`, and `dup()`
    cannot copy a Winsock socket. Now `simDupSocket()` (`WSADuplicateSocketW` + `WSASocketW`).
  - **Sleep/wake — works, but DEFECT in waiting, fixed in `bfe0140`.** Relaunch boots Home and saves the after-wake
    shot, but `_execvp` on Windows spawns a new process and ends the old one: `sim_run.sh` returned before the woken
    instance wrote `wake.bmp` (`qa_runs/win_sleep_wake`), and its exit status is lost. Now `_spawnvp(_P_WAIT)` + exit
    with the child's status.
  - X4 (non-Pro) env — after the judge (builds include the fixes).
- Fixes `dfd450a` on `windows` (local; judged twice: VERIFIED WITH CAVEATS — taken: overlapped duplicate, a log line
  when the duplicate fails, `CreateProcessW` with `GetModuleFileNameW` + the original command line, a kill-on-close
  job; not taken: firmware UDP `close()` → `bugs/05`, WinSock errors logged via `strerror(errno)`). Runs 00:25–00:35:
  - File Transfer (`qa_runs/win_ft_fixed`): `GET /` → 200 1932 B; `/api/files` → 200; upload → 200 «File uploaded
    successfully», the file listed after. Control: `win_ft_hotspot` (before) — empty reply.
  - Sleep/wake (`win_sleep_wake_fixed`): `sim_run.sh` now waits — `wake.webp` present. Control: `win_sleep_wake`
    (before) — the script returned before the woken shot.
  - Exit status (`win_wake_exitcode`): a woken instance whose WAIT times out exits 1, and the run returns `exit 1`.
  - Kill of the top waiter (job object) — NOT run: the permission system refused stopping the process; the run ended
    by its own QUIT, no `program.exe` left after (`win_wake_kill`).
  - X4 (non-Pro) `simulator_win` builds and boots: Home with the button hints, DOWN DOWN ENTER opens File Transfer
    (`win_x4_smoke`).
  Left for the PR: squash the 8 local commits, PR text (owner proofreads), the owner's word to push `windows`; macOS
  and Linux are not buildable here — the upstream CI decides.
- ~~OPEN defect: an in-script `SHOT` stalls after a second `WAIT`~~ — **NOT A DEFECT** (2026-11-09 23:50 +03:00,
  checked). The probe that "showed" it (`shot_probe2`, 20:14) was `…;800:SHOT:…;500:QUIT`: times count from the last
  matched WAIT (README: «Times are measured from process startup, or from the last matched WAIT»), so QUIT fired at
  500 ms, before the SHOT at 800 ms. Variants run today on the current binary: two WAITs + SHOT before QUIT → saved
  (`qa_runs/shot_two_waits`); one WAIT → saved (`shot_one_wait`); the old script verbatim → no shot (`shot_probe3`);
  direct runs: SHOT 800 / QUIT 500 → no BMP, SHOT 800 / QUIT 1300 → BMP; a missing folder → logged
  `[SIM] Cannot save screenshot …: Couldn't open …` (no stall). `c1_display`'s log (17:45), named as "stalled" here,
  in fact has `Saved screenshot` after three WAITs. The claim was mine, from scripts read wrong.
- FIXED defect of the port (2026-11-09 22:10, simulator `ba46fb7`, local): `HalStorage::replaceFile` was a bare
  `::rename`, which on Windows refuses to overwrite an existing file — firmware that rewrites a file in place failed
  (`Writing …books_card_v2.epub failed`, run `qa_runs/cal_lang_en` first try). Now remove-then-rename, as the device.
- ~~Missing: `sample-platformio-windows.ini` + README section~~ — DONE in `d7a0f85` (17:26; corrected 2026-11-09 23:28,
  this line had gone stale). Still missing for a PR: the 7 local commits squashed, PR text for the owner's
  proofreading, the owner's word on pushing branch `windows` (0 commits behind `upstream/main` at 23:28).

## Plan

1. Toolchain: `winget install MSYS2.MSYS2`; `pacman -S mingw-w64-ucrt-x86_64-{gcc,SDL2,openssl,cmake,ninja,pkgconf}`;
   PlatformIO in a venv; `C:\msys64\ucrt64\bin` first in PATH for the build.
2. Port in `simulator/` (branch `windows` of the fork), guarded by `_WIN32` so macOS/Linux stay byte-identical.
3. Firmware fork: a `[env:simulator_win]` env (`lib_deps` → our fork, `-lws2_32 -lssl -lcrypto`), extending to X4 Pro.
4. Observation: the simulator starts, renders Home, the screenshot hooks write BMPs, the log has no errors —
   `tools/sim_run.sh` made Windows-aware.
