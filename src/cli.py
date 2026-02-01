
import argparse
from src.capture.screenshot_capture import capture_fullscreen
from src.pipeline import run_pipeline

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--image", type=str, default="")
    p.add_argument("--capture", action="store_true", help="Auto-capture full screen")
    p.add_argument("--ocr", type=str, default="tesseract", choices=["tesseract", "easyocr"])
    p.add_argument("--tess_lang", type=str, default="eng", help="e.g., eng, fra, eng+fra")
    p.add_argument("--easy_langs", type=str, default="en", help="comma separated: en,fr,hi")
    p.add_argument("--no_nlp", action="store_true")
    args = p.parse_args()

    image_path = args.image
    if args.capture:
        image_path = capture_fullscreen()

    if not image_path:
        raise SystemExit("Provide --image path OR use --capture")

    easy_langs = tuple([x.strip() for x in args.easy_langs.split(",") if x.strip()])

    out_txt, out_json, _ = run_pipeline(
        image_path=image_path,
        ocr_engine=args.ocr,
        tesseract_lang=args.tess_lang,
        easyocr_langs=easy_langs,
        run_nlp=not args.no_nlp
    )
    print("Saved:", out_txt)
    print("Saved:", out_json)

if __name__ == "__main__":
    main()
