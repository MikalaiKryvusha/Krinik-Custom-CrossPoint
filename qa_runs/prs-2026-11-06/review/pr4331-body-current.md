## Summary

* **Goal:** see how full the SD card is without a computer.
* **What changes:** Settings → System → About gets three rows under Flash — **SD Size**, **SD Used**, **SD Free** (GB with one decimal, MB below 1 GB, "No card" when nothing is mounted).
  * The used space comes from the SDK's FAT scan (`SDCardManager::sdUsedBytes`, cached by the SDK), which takes a few seconds on a large card, so a **Loading** popup answers the press before the scan.
  * Labels stay hardcoded English, like the rest of About, for support screenshots.
  * `HalStorage` gets two thin wrappers (`sdTotalBytes`, `sdUsedBytes`) that take the storage lock, like its other calls.

![Settings → System → About, before and after](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/04-about-sd/about-sd-card.png)

*Simulator; it has no SD volume, so the values in the screenshot are the host disk's.*

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool, RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no other popular CrossPoint fork already does.
- [ ] This PR touches `lib/hal/` — two read-only `HalStorage` wrappers over existing SDK calls; happy to adjust to whatever the HAL owner prefers.

## Additional Context

* `pio run -e x4pro` is green (flash +~1 KB).
* The rows and the Loading popup run on my X4 Pro build.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_ — Claude (Anthropic) wrote the change under my direction; I reviewed it.

