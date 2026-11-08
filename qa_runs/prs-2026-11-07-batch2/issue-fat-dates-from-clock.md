<!-- DRAFT, not published. Needs Nikolai's text review. Personal ~/Xteink project. -->

**Title:** Files the reader writes get no real FAT date, so a same-size replacement can reuse a stale cache

## What I see

Two places treat a file's modification time as "this file changed":

* the sleep image cache key — `path|size|modificationTime` (`src/activities/boot_sleep/SleepActivity.cpp:771`);
* the library index — `entry.modificationTime()` (`lib/LibraryIndex/LibraryBuilder.cpp:483`).

The firmware registers no `FsDateTime::setCallback`, so every file the reader itself creates or rewrites (web upload, WebDAV, "Set as sleep cover") gets the same default FAT date. If such a file is replaced by another one of the same size, path, size and date all match and the old cache entry is reused.

## Proposal

Register a FAT date/time callback that takes the time from the reader's clock (`HalClock`), and leave the default date when the clock is not set. That is a few lines in `lib/hal/HalStorage.cpp` at mount time.

This touches `lib/hal/`, so I am asking first rather than opening a PR. My own X4 Pro build has this, and I can open the PR if the approach is welcome.

## Not claimed

This came out of a code review of my own build. I have not reproduced either case on the device.
