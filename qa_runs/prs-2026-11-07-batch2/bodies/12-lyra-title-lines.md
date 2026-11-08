## Summary

* **Goal:** a long book title on the Lyra Home screen is readable.
* **What changes:** the recent-book tile in **Lyra** shows up to five title lines instead of three. The cover tile is tall enough, and the text block stays centered next to the cover. Short titles look the same.

| Before (3 lines) | After (up to 5 lines) |
| --- | --- |
| ![before](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/12-lyra-title-lines/lyra-before.webp) | ![after](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/12-lyra-title-lines/lyra-after.webp) |

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool, RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no other popular CrossPoint fork already does.
- [x] This PR does not touch `freeink-sdk/`, `lib/hal/`, the bootloader, OTA, or recovery code.

## Additional Context

* One number in `LyraTheme::drawRecentBookCover` (`wrappedText(..., 5, ...)`). Lyra Extended and the other themes are not touched.
* `x4pro`, `default` (C3) and the simulator build; 898 host tests pass.
* Running in my own X4 Pro build.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_
