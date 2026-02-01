
import os
import json
from datetime import datetime

from src.ocr.preprocess import preprocess_for_ocr
from src.ocr.tesseract_ocr import ocr_tesseract
from src.ocr.easyocr_ocr import ocr_easyocr

from src.nlp.text_cleaning import clean_text
from src.nlp.language_detect import detect_language
from src.nlp.summarizer import summarize_text
from src.nlp.ner import extract_entities
from src.nlp.keywords import extract_keywords

from src.config import OUTPUT_DIR

def run_pipeline(
    image_path: str,
    ocr_engine: str = "tesseract",
    tesseract_lang: str = "eng",
    easyocr_langs=("en",),
    run_nlp: bool = True
):

    if not image_path:
        raise ValueError(
            "image_path is None or empty. "
            "Upload an image or click 'Capture full screen now' first."
        )
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(image_path))[0]
    out_txt = os.path.join(OUTPUT_DIR, f"{base}_{ts}.txt")
    out_json = os.path.join(OUTPUT_DIR, f"{base}_{ts}.json")

    # OCR
    if ocr_engine.lower() == "tesseract":
        processed = preprocess_for_ocr(image_path)
        text = ocr_tesseract(processed, lang=tesseract_lang)
    elif ocr_engine.lower() == "easyocr":
        text = ocr_easyocr(image_path, langs=easyocr_langs)
    else:
        raise ValueError("ocr_engine must be 'tesseract' or 'easyocr'")

    text = clean_text(text)

    result = {
        "image_path": image_path,
        "ocr_engine": ocr_engine,
        "text": text
    }

    if run_nlp:
        lang = detect_language(text)
        summary = summarize_text(text)
        entities = extract_entities(text)
        keywords = extract_keywords(text)

        result.update({
            "language": lang,
            "summary": summary,
            "entities": entities,
            "keywords": keywords
        })

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(text)

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return out_txt, out_json, result
