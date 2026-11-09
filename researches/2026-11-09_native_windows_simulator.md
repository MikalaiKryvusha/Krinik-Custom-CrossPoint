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

## Plan

1. Toolchain: `winget install MSYS2.MSYS2`; `pacman -S mingw-w64-ucrt-x86_64-{gcc,SDL2,openssl,cmake,ninja,pkgconf}`;
   PlatformIO in a venv; `C:\msys64\ucrt64\bin` first in PATH for the build.
2. Port in `simulator/` (branch `windows` of the fork), guarded by `_WIN32` so macOS/Linux stay byte-identical.
3. Firmware fork: a `[env:simulator_win]` env (`lib_deps` → our fork, `-lws2_32 -lssl -lcrypto`), extending to X4 Pro.
4. Observation: the simulator starts, renders Home, the screenshot hooks write BMPs, the log has no errors —
   `tools/sim_run.sh` made Windows-aware.
