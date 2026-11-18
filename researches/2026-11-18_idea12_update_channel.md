# Research — idea 12: the update channel KCCP / CrossPoint (how OTA works today, the KCCP channel's design)

> **Created:** 2026-11-18 · **Parent:** `ideas/12_update_channel_kccp_or_crosspoint.md` (the owner, 2026-11-17 21:49) ·
> **Status:** recon done 2026-11-18 10:25 +03:00; implementation next in 1.1.4 · **Outbound:** one question to the owner (below)

The owner's words (verbatim, `ideas/12`): «В сборке KCCP должена быть настройка выбора канала обновления: обновиться на
офисицальный CrossPoint, или получать обновления от канала KCCP с проверкой обновлений. По умолчанию - KCCP канал
включен».

## How OTA works today (firmware `wip/kccp-1.1.4`, read 2026-11-18)

1. `OtaUpdater::checkForUpdate` (`src/network/OtaUpdater.cpp:25`) streams
   `https://api.github.com/repos/crosspoint-reader/crosspoint-reader/releases/latest` (`:22`) into `ReleaseJsonParser`;
   on the tag it sets the wanted asset name `crosspoint-<tag><suffix>.bin`, suffix `-x3-x4` for the C3 combined image or
   `-<board tag>` (`board_tag::boardName()`, X4 Pro: `x4pro`) — an exact name match.
2. `isUpdateNewer` (`:94`) compares three numeric segments of the tag with `CROSSPOINT_VERSION` after an optional `cp-`
   prefix (`:102–103`): a KCCP image `cp-2.0.0-kccp-1.1.4` compares as CrossPoint 2.0.0 against upstream tags. An `-rc`
   current build counts an equal tag as newer (`:131`).
3. `installUpdate` (`:143`) streams the asset into the inactive OTA slot through `HttpDownloader`, checking the chip id
   and the image's board tag (`FirmwareBoardTag.h`; a wrong board aborts) before the boot switch.

## The KCCP channel — design

- **Setting:** `updateChannel` in `settings.json` — 0 KCCP (default), 1 CrossPoint; a row «Канал обновлений: KCCP /
  CrossPoint» in Settings → System beside «Проверить обновления». Old files without the key read as KCCP.
- **Source:** KCCP → `https://api.github.com/repos/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/latest`, tag
  `kccp-<KCCP version>`; CrossPoint → today's URL and asset rule, unchanged.
- **Asset (HOUSE_RULES П5):** the owner's build takes the asset whose name ends `-kccp-<tag version>.bin`, the mother's
  build (`KRINIK_MAMA`) `-kccpm-<tag version>.bin`; the CrossPoint part of the name (`cp-2.0.0-`) is not predictable on
  the device, so `ReleaseJsonParser` gets a suffix match beside its exact match.
- **Compare:** KCCP channel — the tag's version after `kccp-` against the image's KCCP version (the build flag
  `-DKCCP_VERSION=\"${krinik.version}\"`, three numeric segments); a `-debugN` build counts an equal release as newer
  (the `-rc` rule). CrossPoint channel — today's compare.
- **Release ritual:** every KCCP release carries both images under the П5 names (the `/release` checklist gains the line).
- **Tests:** host tests of the parser's suffix match and of the KCCP compare (equal, newer, older, debug, malformed
  tags); simulator: the setting row and its saved value. The download itself cannot run on the simulator (no network
  stack there) — not verified on the reader until the owner's reader is on Wi-Fi.

## Open fork — for the owner

`FORK: options <A the CrossPoint channel installs upstream's image as today, no extra warning | B before installing from
the CrossPoint channel a dialog says that KCCP's features (Home «Сон» / «Фонарик», the shade buttons, the Russian guide…)
go away, [Установить] [Отмена]> · price of error <A: one tap replaces KCCP on the owner's or his mother's reader without
a word; B: one more dialog> · consulted <the owner's words above (the choice exists, KCCP by default); the existing OTA
screen shows only the version number>` → asked in chat; the agent recommends B. Work on everything else proceeds.

## Decisions made without the owner

- `[AI]` The setting lives in Settings → System beside the update check; the key name `updateChannel`.
- `[AI]` Assets matched by the `-kccp-` / `-kccpm-` suffix (the П5 names), not by a second stable copy in each release.
- `[AI]` A debug build is offered the release of the same version.
