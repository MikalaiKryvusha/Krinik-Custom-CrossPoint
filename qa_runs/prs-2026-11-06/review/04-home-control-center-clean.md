# Add Clean Home Screen and Clean After Control Center

## Summary

* **Goal:** let people who see traces of earlier screens clean them at two points where it is cheap to do so.
* **What changes:** two options under **Settings → Display → Screen Cleaning**, both Off by default:
  * **Clean Home Screen** — the first frame of every Home visit is a full refresh.
  * **Clean After Control Center** — closing the control center repaints the screen underneath with the clean (half) waveform. The refresh tile keeps its full refresh, and going to sleep with the control center open is unchanged.

![Screen Cleaning](assets/cleaning-home-control-center-en.webp)

## Scope Check

- [x] I have read SCOPE.md and ROADMAP.md.
- [x] This PR is **not** a new built-in theme.
- [x] This PR is **not** a new external network connector.
- [x] This PR is **not** an interactive app, writing tool, RSS/news/browser, media playback, or PDF feature.
- [x] The stock firmware does not already handle this well, **and** no other popular CrossPoint fork already does.
- [x] This PR does not touch `freeink-sdk/`, `lib/hal/`, the bootloader, OTA, or recovery code.

## Additional Context

* Uses the Screen Cleaning submenu from #<screen-cleaning>; the branch sits on #<redraw-delay>.
* Simulator, refresh mode of every frame logged: with both On, each Home visit starts FULL and a control-center close repaints HALF; the refresh tile still gives FULL; the sleep screen is the same as with both Off. With both Off, Home and the control-center close stay FAST.
* `x4pro` and `default` build; 895 host tests pass. English and Russian strings.
* Not checked over the image viewer, and not yet on hardware in this form. My own X4 Pro build has both options, but its control-center clean is a separate X4 Pro-only scrub; here it is the generic HALF repaint.

---

### AI Usage

Did you use AI tools to help write this code? _**YES**_
