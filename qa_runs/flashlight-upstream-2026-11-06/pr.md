## Summary

Add **Flashlight** to Home on devices with a frontlight: a white screen at full output, with a localized exit header. Leaving it restores the previous brightness and on/off state. Warmth and saved settings stay unchanged.

The entry follows the runtime frontlight capability and appears in the list, Lyra, and cover-grid menus. It does not add another control-center item. Two label keys are included in all 35 locale files.

## Validation

- I use the corresponding feature on my X4 Pro fork while reading at night.
- Host tests compile the actual activity and HAL: temporary output, state restoration, dark/light screen polarity, oriented header width and exit inputs.
- The actual Home index helpers are checked with and without the optional library service and flashlight.
- Full host suite: 897/897 passed.

This upstream port still needs its final firmware builds and interface checks before submission. Screenshots and the proposal issue link will be added after those checks.

## Scope

No new network service, task, setting, or persistent data. The screen uses the existing framebuffer. The patch does not include the separate frontlight-animation work or battery logging.

### AI Usage

Yes, AI tools helped prepare the implementation and tests under my direction.
