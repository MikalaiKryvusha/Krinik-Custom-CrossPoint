# feat(sd): report SD usage scan failures

## What

`SDCardManager::sdUsedBytes()` returns 0 for an empty card, for an unmounted card and for a failed FAT free-cluster scan, so a caller cannot tell a failure from a real zero.

This adds `bool sdUsedBytes(uint64_t& usedBytes)`: false when no card is mounted or the scan failed. The result, success or failure, is cached for the existing 20 s TTL. The old `uint64_t sdUsedBytes()` stays and calls the new one.

## Why

CrossPoint's Settings → About shows SD size, used and free space (crosspoint-reader/crosspoint-reader#4331). With the old call it would show "0 MB used" on a card whose scan failed.

## Checks

- `libs/hardware/SDCardManager/test/host/run.sh` passes. New cases: unmounted card and failed scan return false, a real empty card returns true with 0, and a failure stays cached for the TTL.
- The same change runs on my X4 Pro build of CrossPoint.

## AI usage

YES.
