## Summary

* **Goal:** the same gray looks different on an e-ink panel than intended, and differently in pictures and in book images. Let a reader correct both for their own panel.
* **What changes:** **Display → Screen Calibration** with a pictures target and a books target, and two checkboxes that apply optional tone curves from the SD card: `/.crosspoint/panel_curve.txt` and `/.crosspoint/panel_curve_book.txt`. [KEINKT Calibrator](https://mikalaikryvusha.github.io/KEINKT/calibrator/) builds the curves from phone photos of the targets.
  * Both checkboxes default to Off; a checkbox reloads its curve at once. A missing or invalid file leaves tones unchanged. No curve measured on someone else's panel is built in.
  * Back from a target returns to the calibration menu; the targets do not replace the resumed book or enter Recent books.

| Screen Calibration | Pictures target | Books target |
| --- | --- | --- |
| ![Calibration menu](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/calibration-calibration-en.webp) | ![Pictures](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/calibration-pictures-card-en.webp) | ![Books](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/calibration-books-card-en.webp) |

![Photo measurements on my X4 Pro](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/calibration-accuracy-x4pro-en.png)

| Pictures: before | Pictures: with curve |
| --- | --- |
| ![before](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/pictures-before-framed.jpg) | ![after](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/pictures-after-framed.jpg) |

| Books: before | Books: with curve |
| --- | --- |
| ![before](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/books-before-framed.jpg) | ![after](https://raw.githubusercontent.com/MikalaiKryvusha/crosspoint-reader/pr-assets/08-calibration/books-after-framed.jpg) |

*Real photos of one X4 Pro, cropped to keep the screen and device bezel, without tone edits. Light and exposure vary between photos; the graph uses the measured, normalized response.*

### From a phone photo to a tone curve

```mermaid
flowchart LR
    A["Open a calibration target on the reader"] --> B["Photograph the real screen"]
    B --> C["Measure the target with KEINKT Calibrator"]
    C --> D["Save the corresponding curve to the SD card"]
    D --> E["Enable calibration for pictures or book images"]
```

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool, RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no other popular CrossPoint fork already does.
- [x] This PR does not touch `freeink-sdk/`, `lib/hal/`, the bootloader, OTA, or recovery code.

## Additional Context

* This branch is independent of #4375 and #4376 on the current `develop`. They touch some of the same settings and viewer files, so integration will need reconciliation if those merge first.

* On branch commit `e72706b7`, 912 host tests passed and `default` and `x4pro-gh_release` builds passed. Simulator: Back from both targets in all four orientations; a small BMP keeps its size with calibration Off and On.
* The same feature runs on my X4 Pro build; this upstream port itself has not been flashed yet.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_

