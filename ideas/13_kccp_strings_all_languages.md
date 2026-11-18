Ключи KCCP есть только на английском и русском

ПЕЕРЕВЕСТИ KCCP на все поддерживаемые языки CrossPoint. Не сейчас, но в планах это ДЕЛАТЬ!

---

# Idea 13 — the KCCP strings in every language CrossPoint supports

> **Created:** 2026-11-18 (the owner's words above, chat 10:14, tossed mid-task while idea 11 was in work) · **Parent:** — ·
> **Status:** 📋 planned by the owner («Не сейчас, но в планах это ДЕЛАТЬ!»), not started · **Outbound:** —

Facts (2026-11-18): `firmware/lib/I18n/translations/` holds 35 language files; the KCCP keys (`STR_SHADE_TILES…`,
`STR_FLASHLIGHT`, the Home-buttons screen, the sleep settings, …) exist only in `english.yaml` and `russian.yaml`, and
`scripts/gen_i18n.py` falls back to English for a missing key. Done when: every KCCP key exists in every file — a
script lists the keys of `russian.yaml` absent from each other file and prints 0 for all 35; the translations are
read back (no machine leftovers, the CrossPoint glossary of each language kept).
