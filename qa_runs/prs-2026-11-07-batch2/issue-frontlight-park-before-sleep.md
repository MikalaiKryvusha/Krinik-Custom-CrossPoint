<!-- DRAFT, not published. Needs Nikolai's text review. Personal ~/Xteink project. -->

**Title:** X4 Pro: frontlight is not parked before deep sleep (SDK contract `FrontlightManager::prepareForDeepSleep()` is never called)

## What I see

The SDK asks every board to park the frontlight on the way into deep sleep:

> `prepareForDeepSleep()` every board. Parks the pad at the LED's INACTIVE level …
> Not the same as off(): off() writes a zero duty, but the pad is still owned by LEDC and sleep entry hands it to `esp_sleep_config_gpio_isolate()`, which floats it -- what the light does then is down to an external pull, a board-layout detail.
> — `freeink-sdk/libs/hardware/FrontlightManager/include/FrontlightManager.h`

In the firmware nothing calls it. `HalPowerManager::startDeepSleep()` (`lib/hal/HalPowerManager.cpp`) turns the light off only on EEGO A4 and Picco (`Frontlight.setOn(false)`, shared I²C with touch); on the X4 Pro the PWM pads go into sleep isolation as they are.

## Proposal

On the X4 Pro, call the SDK's `prepareForDeepSleep()` from `HalPowerManager::startDeepSleep()` (a one-line `HalFrontlight` wrapper plus the call). `begin()` already releases the hold on the next boot, per the SDK comment. The saved brightness/warmth are untouched.

This touches `lib/hal/`, so I am asking first rather than opening a PR. My own X4 Pro build has this, and I can open the PR if the approach is welcome.

## Not claimed

I have not measured sleep current with and without the park. The point is the SDK contract, not a measured drain.
