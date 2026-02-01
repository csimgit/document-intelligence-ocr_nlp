
from __future__ import annotations
import os
from datetime import datetime
import mss
import mss.tools

def capture_fullscreen(out_dir: str = "data/input") -> str:
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(out_dir, f"screenshot_{ts}.png")

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output=out_path)

    return out_path
