Thanks, @Uri-Tauber — both points are right.

- **SDK:** the `sdUsedBytes()` change is now its own PR: Free-Ink/freeink-sdk#<N>. This PR will point the submodule at it once it is merged.
- **No card:** instead of dropping the row, the device now boots without a card. Settings keep their defaults and are not saved, the library is empty, and About shows "No card". Before this change it stopped on "SD card error". Recovery mode (Down + Power) still needs a card; without one the device boots normally.

Checked in the simulator with storage made to fail (a local patch to the simulator): boot, Settings → System → About, a setting toggle, Back to Home, Browse Files ("No files found"), sleep and wake. With a card nothing changes. `x4pro` and `default` build, 893 host tests pass.
