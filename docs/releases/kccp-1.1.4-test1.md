**Тестовый релиз для проверки обновления по воздуху из канала KCCP.** Читать на нём не нужно: внутри отладочная
сборка 1.1.4. После проверки его заменит релиз KCCP 1.1.4.

Как проверить:
1. Поставьте на читалку с SD-карты сборку `cp-2.0.0-kccp-1.1.4-debug2.bin` (в 1.1.3 канала KCCP ещё нет).
2. Откройте «Настройки → Система» и убедитесь, что «Канал обновлений» — KCCP.
3. Нажмите «Проверить обновление». Читалка находит `kccp-1.1.4-test1`, ставит его и перезагружается.
4. В «Об устройстве» стоит версия `cp-2.0.0-kccp-1.1.4-test1`; повторная проверка обновления больше не предлагает.

---

**A test release for the over-the-air update from the KCCP channel.** Not for reading: it holds a 1.1.4 debug build.
The KCCP 1.1.4 release replaces it after the check.

To check:
1. Install `cp-2.0.0-kccp-1.1.4-debug2.bin` on the reader from the SD card (1.1.3 has no KCCP channel yet).
2. Open «Settings → System» and make sure «Update channel» is KCCP.
3. Tap «Check for Updates». The reader finds `kccp-1.1.4-test1`, installs it and restarts.
4. «About» shows `cp-2.0.0-kccp-1.1.4-test1`; a second check offers no update.
