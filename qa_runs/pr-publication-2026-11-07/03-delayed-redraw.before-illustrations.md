## Summary

* **Goal:** a fresh gray picture can keep traces of the menu before it. An optional repaint after a delay is intended to reduce those traces.
* **What changes:** **Refresh Images** and, on X4 Pro, **Refresh Sleep Screen** under Screen Cleaning: Off / after 1 / 2 / 5 min. Both default to Off.
  * The viewer repaints once, without a Loading popup. Each newly opened image starts its own delay.
  * For a custom sleep image, X4 Pro wakes once, redraws the same image with the light off and sleeps again. Low battery, panic recovery and Quick Resume do not arm the wake; the power button wakes as usual.

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool, RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no other popular CrossPoint fork already does.
- [x] This PR does not touch `freeink-sdk/`, `lib/hal/`, the bootloader, OTA, or recovery code.

## Additional Context

* Depends on #4375 (the Screen Cleaning submenu). Merge that PR first. This branch includes its commit; until it is merged, this PR also shows the submenu changes. The delayed-redraw change itself is commit `d7cc4e83`.
* On branch commit `d7cc4e83`, `default`, `x4pro-gh_release` and simulator builds passed. Simulator: one redraw in 126 s with a 60 s delay; 40 swipes reopened the viewer 41 times without errors.
* Not yet on hardware in this exact form: the sleep timer and the power button during the redraw. No power-consumption claim.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_
