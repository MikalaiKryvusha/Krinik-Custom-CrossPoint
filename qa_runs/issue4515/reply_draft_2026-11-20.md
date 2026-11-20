Thanks for looking into this!

One pointer so the work doesn't overlap: on current `develop`, `HomeCoverCache::prepare()` already drops the cached covers when the polarity changes (`src/components/HomeCoverCache.cpp`, lines 35–41, added in #4494). If your checkout is older than Nov 16, the Cover Grid cache part should be gone after a rebase.

This issue is about the moment while the shade is still open. The Night tile flips `SETTINGS.screenInverted` and redraws only the sheet, so the part of Home still visible below the sheet keeps the old polarity until the shade closes (step 3: the second cover is a negative). Once the shade closes, Home repaints and the cover is normal. So the fix likely belongs on the shade side — converting or repainting what is visible below the sheet — rather than in the cover cache.
