## Summary

* **Goal:** a damaged file in the sleep folder does not spoil the sleep screen.
* **Problem:** a BMP that was copied only partly (an interrupted copy to the card, a power loss) keeps valid headers, so it passes the sleep-image check. The reader then draws it until the data runs out: the rest of the screen stays empty and the log shows `Failed to read row …`.
* **What changes:** when the reader picks an image from the sleep folders, the check also compares the file size with what the headers promise (pixel data offset plus every row). A shorter file is skipped like any other invalid image, so the reader picks another image or falls back to the default screen. No pixel reads, one size comparison per file.

Simulator, `/sleep` holding only `cut.bmp`, the first third of a valid 480×800 1-bit BMP, **Sleep Screen: Custom**:

![sleep before and after](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/14-sleep-skip-truncated-bmp/sleep-before-after.webp)

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool, RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no other popular CrossPoint fork already does.
- [x] This PR does not touch `freeink-sdk/`, `lib/hal/`, the bootloader, OTA, or recovery code.

## Additional Context

* `Bitmap::expectedFileSize()` and one condition in `findNextValidSleepImage()`.
* Out of scope: `/sleep.bmp` and a root `/sleep-overlay.bmp` are not picked through `findNextValidSleepImage()` and keep the old check. Cover-mode BMPs are written by the firmware itself.
* `rowBytes` already includes row padding, and the renderer reads full rows, so a rejected file would fail on its last rows anyway. A writer that drops the padding of the last row only (none of GIMP, ImageMagick, Pillow, Photoshop does) is now skipped instead of drawn without its top row. Log before: `Loading: /sleep/cut.bmp` … `Failed to read row 265 from 1-bit bitmap`; after: `Skipping invalid sleep image: cut.bmp`.
* `x4pro`, `default` (C3) and the simulator build; 906 host tests pass, including a new `BmpToBmpTest.ExpectedFileSizeCoversEveryPaddedRow` (1 and 24 bpp, bottom-up and top-down, padded rows).
* Running in my own X4 Pro build.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_
