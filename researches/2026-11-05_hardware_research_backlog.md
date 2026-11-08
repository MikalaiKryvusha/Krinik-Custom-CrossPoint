# X4 Pro: PWM, battery indication, charging and frontlight wear

[AI]
Status: research requested by Nikolai, not started. Separate from the four
upstream PRs. No firmware change or hardware measurement is claimed here.

Goal: establish the actual hardware/driver limits before proposing settings.
Evidence must distinguish source-code configuration, component documentation,
and physical measurements. An inferred current is not a measured current.

Owner requests, verbatim:
> и по ШИМ будет задачка на изучение - можно ли будет сделать больше, чем 1024 шага, или это невозможно, или это слишком сложно.

> и ещё задачки на изучение:
> 1) изучить, каким напряжениям на АКБ равны уровни в индикаторе заряда 0% и 100%
> 2) изучить возможность добавления опции защиты АКБ от износа (зарядка до 80% и отключение контроллера заряда на этом уровне)
> 3) изучить ток через светодиоды подсветки на 100% яркости, и нужна ли им опция Защиты от износа подсетки - что снижает максимальную яркость на 100%, до реальных 80% под капотом в драйвере

Research queue and acceptance:
- [ ] PWM: pin the real timer frequency/resolution and brightness mapping in
      the released SDK; inspect permitted hardware combinations above 1024
      levels. Determine complexity and whether more levels address the visible
      low-brightness cutoff. Separate LED turn-on threshold from quantization.
- [ ] Battery indicator: trace voltage acquisition, ADC calibration/divider,
      filtering and percentage mapping, including USB/charging differences.
      Give source-backed voltage values/curves for 0% and 100%, with limitations.
- [ ] Charge cap: identify the charger IC, wiring, and any accessible enable or
      programmable threshold. Determine whether firmware can actually stop
      charging at 80%, how the threshold is known, and restart/hysteresis behavior.
      Hiding 100% on the indicator is not evidence of charge control.
- [ ] Frontlight current: identify LED strings, driver IC and current-setting
      components; establish nominal/maximum current at full output. Compare
      with component working ratings and available thermal data. Determine
      whether an optional internal 80% cap is useful and what it would change
      in PWM/current, measured light output and lifetime evidence.

Deliverable for each question: factual answer, source links and code paths,
known/unknown measurements, feasibility and implementation complexity. Any
proposal to modify the firmware follows the research; do not treat the owner's
80% examples as already implemented or validated protection thresholds.
[/AI]
