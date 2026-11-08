# Calibration curves in the firmware configuration directory

[AI]
Owner: «мне не нравятся, что калибровочные кривые мы сделали так, что нужно
кидать в корень карты. Правильно было бы гидать в скрытую конфигурационную
папку прошивки» (05.11.2026).

Observed: released firmware 8dd71e19 already supports
`/.crosspoint/panel_curve.txt` and `/.crosspoint/panel_curve_book.txt`.
PanelCurve.cpp currently prefers root files; README and KEINKT guide users to
the root. The real card was ejected after flashing; its backed-up v2 curves
are in qa_runs/card-final-2026-11-05/before/. Their verified hashes are in
protected-hashes.json there. Calibration-card generated assets live in a
different directory, `/.crosspoint/calibration/`; keep curves beside settings.

INTENT: hidden configuration paths become authoritative. If a hidden curve is
absent, legacy root curves remain readable without any filesystem writes.
Parsing/dithering/cache hashes stay the same; explicit configuration changes
still use forget() on checkbox toggles. The current card files are moved with
backup and SHA256 verification by the agent on the Mac.

Scope/checklist:
- Use an isolated firmware branch based on released nikolai; keep the installed
  firmware and all pending upstream PR branches intact.
- Prefer hidden paths; keep root paths as a read-only compatibility fallback.
- Compile the real PanelCurve.cpp in host tests; exercise both kinds, precedence,
  valid/invalid legacy data, unavailable reads, disabled calibration, cache reload.
- Update KEINKT Russian/English instructions, firmware README and the Russian
  on-device guide; explain how to reach a hidden directory from Finder.
- Judge with the existing single reviewer, then affected host/firmware checks.
- Move current card files with backup/hash verification once USB is available.
  Released 1.1.0 supports the resulting paths, so this move needs no reflash.

No new release or external publication is requested by this path correction.
[/AI]

[AI]
Review adjustment: initial auto-migration was removed after the single judge
verified that SdFat rename can fail after changing directory entries, so false
does not promise rollback. Eight final tests exercise read-only loading (the
storage stub exposes no write APIs); full host suite 928/928. RU/EN FAQ also
points to /.crosspoint/ and toggling the checkbox; Wi-Fi instructions include
Show Hidden Files because the web file list otherwise hides .crosspoint.

Real card: both original v2 files moved to /.crosspoint/ with matching SHA256;
root copies absent. Guide replaced and its one index record updated to its new
size, six actual book identities checked. Reader state/recent/progress unchanged.
AppleDouble cleaned, .DS_Store absent, .fseventsd removed, card ejected. The
pre-existing .Spotlight-V100 directory is OS protected: normal deletion denied,
mdutil -X requires root and sudo -n requires a password. No admin credentials
requested, no claim that this protected index was removed.
Evidence: qa_runs/curve-config-directory-2026-11-05/card-result.json.
[/AI]
