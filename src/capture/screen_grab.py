import mss
import mss.tools
import os
from datetime import datetime

def capture_screen(out_dir="data/input"):
    os.makedirs(out_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(out_dir, f"screen_{ts}.png")

    with mss.mss() as sct:
        monitor = sct.monitors[1] 
        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output=path)

    return path
