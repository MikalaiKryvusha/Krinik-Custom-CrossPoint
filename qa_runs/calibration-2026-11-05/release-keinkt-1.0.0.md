**KEINKT Calibrator 1.0.0** — the first release. Measures how your e-ink screen really shows grays from phone photos and gives the reader a correction curve (`panel_curve.txt` for pictures and sleep images, `panel_curve_book.txt` for images inside books).

**Open in the browser:** https://mikalaikryvusha.github.io/KEINKT/calibrator/ — or download `KEINKT-Calibrator-1.0.0.html` below and open it offline with a double click. Nothing you load leaves your computer.

![Xteink X4 Pro: screen response without the curve, with the first and with the refined curve](https://raw.githubusercontent.com/MikalaiKryvusha/KEINKT/main/design/accuracy-x4pro-en.png)

### What it does
- Finds the four corner marks, straightens perspective and rotation, evens the light against the paper and the marks, measures 33 gray steps.
- **Several photos of one screen** are measured together — the shot-to-shot spread (2–3 gray points) averages out.
- **Second iteration:** a photo of the screen *with* the correction shows how evenly the tones fall and refines the curve from it. On a fresh page drop the curve file from the card together with the photo.
- Light smoothing keeps the panel's own steep steps (e-ink panels are not ideal); its strength was chosen on held-out real photos.
- Tells night mode, glare, tilt, overexposure and a hidden mark apart and explains each; manual marks when the search fails.
- English and Russian.

### Measured on a real Xteink X4 Pro (05.11.2026)
Mean distance of the screen from the straight line, gray points:

| | no curve | first curve | refined curve |
|---|---|---|---|
| Pictures | 17.6 | 3.2 | 2.2 / 2.5 (two lights) |
| Books | 9.1 | 3.8 | 1.1 / 2.7 (two lights) |

### Needs
CrossPoint firmware with screen calibration — [krinik 1.1.0](https://github.com/MikalaiKryvusha/crosspoint-reader/releases/tag/krinik-1.1.0) (Xteink X4 Pro). The curve is a plain text file of 256 numbers, so other firmwares can adopt it.

---

**KEINKT Calibrator 1.0.0** — первый выпуск. Измеряет по фото с телефона, как e-ink экран на самом деле показывает серое, и даёт читалке кривую поправки. **Открыть:** https://mikalaikryvusha.github.io/KEINKT/calibrator/ — или скачать `KEINKT-Calibrator-1.0.0.html` ниже. Несколько фото одного экрана считаются вместе; фото экрана с поправкой уточняет кривую (вторая итерация). На X4 Pro после двух итераций отклонение — 2,2–2,5 пункта серого на картинках (было 17,6) и 1,1–2,7 на книгах (было 9,1).
