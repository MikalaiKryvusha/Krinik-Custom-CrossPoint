# Add optional one-time image and sleep-screen redraws

## Summary

* **Goal:** a fresh gray picture can keep traces of the menu before it. One quiet repaint a little later removes them.
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

* Depends on #<screen-cleaning> (the Screen Cleaning submenu).
* `default`, `x4pro` and simulator build. Simulator: one redraw in 126 s with a 60 s delay; 40 swipes reopened the viewer 41 times without errors.
* Not yet on hardware in this exact form: the sleep timer and the power button during the redraw. No power-consumption claim.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_
