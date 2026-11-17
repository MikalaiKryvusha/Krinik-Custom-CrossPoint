**What happens**
When Night mode is toggled from the shade while it is open over a screen with pictures, the part of that screen still visible below the sheet keeps the old polarity. Pictures there (Home covers, book images) show as a negative until the shade is closed. Text and UI under the sheet look fine; only pictures are affected.

**Steps**
1. Home with two recent books that have covers, Cover Grid theme (the second cover sits below the sheet), Night mode on.
2. Swipe down from the top edge to open the shade.
3. Tap the Night mode tile.

**Expected:** the cover below the sheet looks normal in the new mode.
**Actual:** the cover below the sheet is a negative. After the shade closes, Home repaints and the cover is normal.

**Why, as far as I can tell**
Night mode keeps images pre-inverted in the framebuffer. The Night tile (`FrontlightPanelActivity.cpp`, `case 0`) flips `SETTINGS.screenInverted` and redraws only the sheet, so the pixels of the screen underneath stay in the old byte form until that screen repaints.
