# Bug 05 — native Windows simulator: the File Transfer UDP discovery socket leaks (closed with `close()`)

**Status:** 🔴 REPRODUCED 2026-11-17 16:09 +03:00 (run log mtime; found by reading 2026-11-10 00:10 +03:00) · the fix
waits for a design choice (firmware helper or simulator shim, below) · **Fixing:** after that choice — not this day loop · **Severity:** S3
(simulator only; the device is not affected) · **Version/build:** firmware `wip/krinik-debug8` (same code upstream
`develop`), simulator `windows` `fcd0112` · **Where:** firmware `src/network/CrossPointWebServer.cpp:625` `close(fd);` and
`:633` `close(discoverySocket);`.

## Claim (judge, verified by reading; my check pending)

The UDP discovery socket comes from `socket(AF_INET, SOCK_DGRAM, …)`. On Windows that is a Winsock SOCKET, which the C
runtime's `close()` cannot close (EBADF), so the socket stays bound to 8134. Leaving File Transfer and entering it again
in the same process then fails `bind(8134)` (WSAEADDRINUSE) and discovery stays off for the session; the handle is also
inherited by a woken instance after sleep/wake.

## Acceptance

On the Windows simulator: File Transfer → Hotspot, back, File Transfer → Hotspot again → the log shows discovery enabled
on 8134 both times, no bind error.

## Repro (deterministic, 2026-11-17, firmware `de8feb20`, `simulator_x4_pro_win`, card `qa_runs/sd_template`)

`SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh bug05_repro '0:WAIT:Entering activity: Home;1500:TAP:0.5,0.60;1500:WAIT:Entering activity: NetworkModeSelection;1500:TAP:0.5,0.43;5000:BACK;5000:WAIT:Entering activity: Home;1500:TAP:0.5,0.60;1500:WAIT:Entering activity: NetworkModeSelection;1500:TAP:0.5,0.43;5000:SHOT:hot2;6000:BACK;8000:QUIT' ''`
(Home «Передача файлов» → «Создать точку доступа», Back — it returns to Home —, the same again). `qa_runs/bug05_repro/log.txt`:

```
[3625] [DBG] [WEB] Discovery UDP enabled on port 8134
[10434] [DBG] [WEB] Discovery UDP failed on port 8134
```

The second entry in the same process cannot bind 8134 — the first socket was not closed. One variant reproduced it on the
first attempt, so the hunt for more variants is not needed.

## Next

The claim above is confirmed by the run. A fix is either in the firmware (close sockets through a helper the
simulator can map) or in the simulator's lwip shim — an upstream design choice; not part of the simulator PR.
