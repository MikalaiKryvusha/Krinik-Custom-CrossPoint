# Four focused upstream candidates after krinik 1.1.1

[AI]
Goal: prepare calibration and three screen-cleaning PRs without the personal
fork's unrelated features.
No untrue claims. Publication of each PR waits for Nikolai's review
of its description, as already agreed in HANDOVER.md.

Sources observed: upstream/develop bb93a462 (fetched 05.11; one button-remap
commit after the parked base 5936f485); released nikolai a06a20d6 and SDK
50196ef; upstream SDK 5e94fe7. Existing evidence: calibration card/curve tests,
935 host tests, eight simulator navigation cases, final X4Pro build. Nikolai
confirmed installed 1.1.1 and both calibration Back paths, then both immediate
checkbox effects. Those results cover the personal fork, not unbuilt PR ports.

INTENT: preserve the released user-visible features while adapting them to the
upstream board, input, rendering, persistence and cache contracts. Never copy
the complete personal viewer, main.cpp, SDK or settings files into upstream.

Candidates and acceptance:
- [ ] Calibration: two generated cards; separate optional curves under
      /.crosspoint/; checkbox reload; image-cache identity; no Recent/boot book
      pollution; direct Back and complete parent chain; KEINKT instructions.
      No default curve measured on Nikolai's individual panel for other users.
- [ ] A: Display → Screen Cleaning with explanation and existing
      refreshFrequency/fadingFix; preserve JSON keys, defaults and board filters.
- [ ] B: optional one-time picture/sleep redraw after Off/1/2/5 minutes;
      no repeated wake loop; preserve power wake, low-battery/panic guards.
- [ ] C: optional Home and control-sheet cleanup; preserve input/render owners.
- [ ] Every candidate: bounded source diff, relevant host tests and simulator
      observation, one independent reviewer reused, final C3/X4Pro builds as
      applicable; English factual PR draft for Nikolai, no unobserved claims.
- [ ] Publish the already-reviewed KEINKT instructions to main/Pages, verify
      deployed /.crosspoint/ guidance. Do not replace the immutable 1.0.0 asset.

A is independent of calibration. B and C build on A's submenu; keep their
incremental diffs separate rather than duplicating A in two independent PRs.
The final PR bases and descriptions must make those dependencies explicit.

Resource constraints: C3 remains the baseline. Calibration's two cached tables
are 512 bytes plus metadata; card writers stream bounded rows. No new task or
network dependency. Runtime heap/power claims require device measurements and
will not be inferred from passing host/native builds.
[/AI]
