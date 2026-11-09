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
- Risk (b): `windows.h` macros (via `winsock2.h`) inside the firmware's web-server TU — `WIN32_LEAN_AND_MEAN` and
  `NOMINMAX` are set; the compiler will show what is left.

## Plan

1. Toolchain: `winget install MSYS2.MSYS2`; `pacman -S mingw-w64-ucrt-x86_64-{gcc,SDL2,openssl,cmake,ninja,pkgconf}`;
   PlatformIO in a venv; `C:\msys64\ucrt64\bin` first in PATH for the build.
2. Port in `simulator/` (branch `windows` of the fork), guarded by `_WIN32` so macOS/Linux stay byte-identical.
3. Firmware fork: a `[env:simulator_win]` env (`lib_deps` → our fork, `-lws2_32 -lssl -lcrypto`), extending to X4 Pro.
4. Observation: the simulator starts, renders Home, the screenshot hooks write BMPs, the log has no errors —
   `tools/sim_run.sh` made Windows-aware.
