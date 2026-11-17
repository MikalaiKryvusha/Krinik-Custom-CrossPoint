# Checks the on-device guide's settings chapters against the screens the simulator shows: every <b>name</b> of a
# «Настройки: <chapter>» section must appear on a captured screen of that chapter (plan 15, criterion 2). The captures are
# sim_run.sh runs with CROSSPOINT_SIM_SCREEN_TEXT=1 (their log.txt carries «[SIM] SCREEN: …» lines).
# Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/guide_screens_check.py <guide.xhtml> [qa_runs dir]   → exit 1 on a miss
#        .pio-venv/Scripts/python.exe -I -X utf8 tools/guide_screens_check.py --selftest
# [TESTED: 2026-11-17 · red on the 2026-11-08 section (16 names), selftest green and red on a no-gap mutant · plan 15 G3]
import re
import sys
from pathlib import Path

# The capture runs of each chapter (plan 15, recon) — the chapter's own screen and its sub-screens.
CHAPTER_RUNS = {
    "Система": ["guide_system", "guide_clock"],
    "Экран": ["guide_display", "guide_sleep", "guide_clean", "guide_calib"],
    "Чтение": ["guide_reading", "guide_text", "guide_statusbar"],
    "Кнопки": ["guide_keys", "guide_homekey"],
    "Библиотека": ["guide_library"],
    "Подключения": ["guide_network", "guide_sync"],
}
# Guide names a capture on the standard card cannot show, each with its reason (plan 15, G2 and G4):
DEVICE_ONLY = {
    "Точная температура": "a device-build row (FREEINK_FRONTLIGHT_DITHER && X4 Pro)",
    "Bluetooth-пульт": "the simulator is built without Bluetooth",
    "Словарь": "the row exists only with a dictionary in /dictionaries (the guide says so)",
    "Быстрый возврат из ссылок": "the row exists only with «Питание коротко» = «Ссылки и примечания» (the guide says so)",
    "Зоны тапа": "a note under the two page-turn rows, not a row",
    "Действия Home": "the list of actions the three Home key rows take, not a row",
    "URL сервера синхронизации": "the row draws only its value («По умолчанию: sync.crosspointreader.com»)",
}
SPACE = re.compile(r"\s+")


def norm(text):
    return SPACE.sub(" ", text.replace(" ", " ")).strip().casefold()


def guide_names(text):
    """{chapter: [names]} from <h2>Настройки: X</h2> and the <b>…</b> names under it ('› ' and the colon dropped)."""
    out, chapter = {}, None
    for line in text.splitlines():
        h = re.search(r"<h2>\s*Настройки:\s*(.*?)\s*</h2>", line)
        if h:
            chapter = h.group(1)
            out[chapter] = []
            continue
        b = re.search(r"<b>(.*?)</b>", line)
        if chapter and b:
            name = re.sub(r"<[^>]+>", "", b.group(1)).strip().lstrip("›").strip().rstrip(":").strip()
            out[chapter].append(name)
    return out


def screen_text(log_text):
    """All «[SIM] SCREEN:» lines of a run, joined: a row label the screen wraps («Ориентация | заставки сна») is one
    phrase again."""
    parts = [line.split("[SIM] SCREEN:", 1)[1] for line in log_text.splitlines() if "[SIM] SCREEN:" in line]
    return norm(" ".join(p.replace(" | ", " ") for p in parts))


def shown(name, text):
    """The name's words in order, up to 3 other words between them: a wrapped label has its value drawn in the middle
    («Ориентация | По картинке | заставки сна»)."""
    words = norm(name).split()
    if not words:
        return True
    gap = r"(?:\s+\S+){0,3}\s+"
    return re.search(r"(?<!\S)" + gap.join(map(re.escape, words)) + r"(?!\S)", text) is not None


def check(guide_text, screens):
    """screens: {chapter: joined text}. → [(chapter, name)] of guide names no captured screen shows."""
    misses = []
    for chapter, names in guide_names(guide_text).items():
        if chapter not in screens:
            misses.append((chapter, "(no capture for this chapter)"))
            continue
        for name in names:
            if name in DEVICE_ONLY:
                continue
            # «Имя пользователя, Пароль» names two rows: each part must be shown
            if not all(shown(part, screens[chapter]) for part in name.split(",")):
                misses.append((chapter, name))
    return misses


def selftest():
    guide = ("<h2>Настройки: Экран</h2>\n<p><b>Очищать каждые:</b> …</p>\n<p><b>› Ориентация заставки сна:</b> …</p>\n"
             "<p><b>Точная температура:</b> …</p>\n<h2>Настройки: Система</h2>\n<p><b>Имя пользователя, Пароль:</b> …</p>\n")
    screens = {"Экран": screen_text("[SIM] SCREEN: 12:00 | Очищать каждые | 30 стр. | Ориентация | По картинке | "
                                    "заставки сна"),
               "Система": screen_text("[SIM] SCREEN: 12:00 | Имя пользователя | Пароль")}
    fails = []
    if check(guide, screens):
        fails.append(f"all shown, but misses {check(guide, screens)}")
    renamed = guide.replace("Очищать каждые", "Частота обновления")
    if check(renamed, screens) != [("Экран", "Частота обновления")]:
        fails.append(f"a renamed row not caught: {check(renamed, screens)}")
    if check(guide + "<h2>Настройки: Кнопки</h2>\n", screens) != [("Кнопки", "(no capture for this chapter)")]:
        fails.append("a chapter with no capture not named")
    if shown("Очищать после", screens["Экран"]) or shown("каждые Очищать", screens["Экран"]):
        fails.append("words out of order or absent counted as shown")
    for f in fails:
        print("FAIL " + f)
    print(f"selftest: {'FAIL' if fails else 'OK'} ({len(fails)} failure(s))")
    return 1 if fails else 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if len(sys.argv) not in (2, 3):
        print("usage: guide_screens_check.py <guide.xhtml> [qa_runs dir] | --selftest")
        return 2
    runs = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("qa_runs")
    screens = {}
    for chapter, names in CHAPTER_RUNS.items():
        texts = [screen_text((runs / n / "log.txt").read_text(encoding="utf-8", errors="replace"))
                 for n in names if (runs / n / "log.txt").exists()]
        if texts:
            screens[chapter] = " ".join(texts)
    misses = check(Path(sys.argv[1]).read_text(encoding="utf-8"), screens)
    for chapter, name in misses:
        print(f"  {chapter}: «{name}» — not on any captured screen")
    print(f"{sys.argv[1]}: {len(misses)} guide name(s) not on the reader's screens")
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
