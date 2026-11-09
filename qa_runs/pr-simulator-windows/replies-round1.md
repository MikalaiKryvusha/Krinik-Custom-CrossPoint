# PR #62 — replies to CodeRabbit round 1 (to post after the fix is pushed and run)

Owner's mandate 2026-11-10 01:36 +03:00: «работай автономно … поправить - если он даст замечания … довести работу до
состояния, что у кодрабита замечаний нет». Facts only; `<sha>` = the pushed fix commit.

## 4518663995 — src/SimHttpFetch.h:49 (cmd.exe)
Fixed in <sha>. On Windows curl now starts through `CreateProcessW` with each argument quoted for the C runtime's own
command-line rules, so no shell is involved: `%NAME%`, `&` and `"` mean nothing. The body goes through
`--data-binary @<temp file>` and the URL through `--url`. The POSIX path and `shellQuote()` are back to `main`.
Checked with a POST whose header held `a" & echo PWNED > <file> & "b %TEMP% c` and whose JSON body held quotes,
`%TEMP%` and a newline: the server received both verbatim and no file appeared; the previous build created the file.

## 4518663990 — src/HalStorage.cpp:400 (replaceFile)
Fixed in <sha>: POSIX is plain `rename()` again, as in `main`; Windows uses `MoveFileEx(..., MOVEFILE_REPLACE_EXISTING)`,
which replaces in one step and leaves the destination as it was when the move fails. Checked: with a missing source
the destination stays; with a present source it is replaced.

## outside diff — src/HalStorage.cpp:33-41 (backslash segments)
Fixed in <sha>: on Windows `\` is turned into `/` before the `..` check. Checked: `..\outside.txt` is rejected.

## 4518664001 — src/WebServer.cpp:621 (failed duplicate)
Fixed in <sha>: the server answers 500 on the original socket and skips the handler. This path also applies on POSIX
when `dup()` fails (for example EMFILE), where the handler used to run with fd -1.

## 4518663982 — README.md:34 (clock)
Fixed in <sha>. Measured with a small UCRT program: fixed offsets (`MSK-3`, `UTC-3:00`) are exact; zones with daylight
saving switch on the US dates whatever rule follows (`CET-1CEST,M3.5.0,M10.5.0/3`); names that are not three letters
(`AKST9AKDT,…`, `AEST-10AEDT,…`, `<+03>-3`) give a wrong local time. The README now says that.
