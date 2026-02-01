
import pytesseract
from src.config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def ocr_tesseract(processed_image, lang: str = "eng") -> str:
    # oem 3 = default engine, psm 6 = block of text
    config = r"--oem 3 --psm 6"
    return pytesseract.image_to_string(processed_image, lang=lang, config=config)
