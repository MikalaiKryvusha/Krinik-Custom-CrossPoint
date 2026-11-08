# Add optional one-time image and sleep-screen redraws

A fresh gray picture can retain traces of the preceding menu. Add **Refresh Images** and, on X4 Pro, **Refresh Sleep Screen** under Screen Cleaning: **Off / after 1 / 2 / 5 min**. Both default to Off.

The viewer repaints once without a Loading popup. For a custom sleep image, X4 Pro can wake once, redraw the same image with the light off, and sleep again. Low battery, panic recovery and Quick Resume do not arm the wake. Normal power-button wake remains available.

```mermaid
flowchart LR
    A[Show image] --> B[Wait 1, 2 or 5 min]
    B --> C[Redraw once]
    C --> D[No further timer until another image]
```

Depends on the Screen Cleaning submenu PR. C3/X4 Pro/native builds passed. The native viewer produced one redraw during 126 seconds with a 60-second delay; 40 swipes reopened the viewer 41 times without errors. Hardware validation of the sleep timer and button during redraw is still pending. No power-consumption claim is made from native results.
