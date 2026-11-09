# Bug 05 — native Windows simulator: the File Transfer UDP discovery socket leaks (closed with `close()`)

**Status:** 🔍 found by reading (independent judge, 2026-11-10 00:10 +03:00), NOT reproduced yet · **Severity:** S3
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

## Next

Reproduce first (the hunt rule, ≥ 3 variants). A fix is either in the firmware (close sockets through a helper the
simulator can map) or in the simulator's lwip shim — an upstream design choice; not part of the simulator PR.
