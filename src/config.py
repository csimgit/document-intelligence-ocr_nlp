
import os


TESSERACT_CMD = os.environ.get(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "data/output")
