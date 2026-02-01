
import easyocr


_READER_CACHE = {}

def ocr_easyocr(image_path: str, langs=("en",)) -> str:
    key = tuple(langs)
    if key not in _READER_CACHE:
        _READER_CACHE[key] = easyocr.Reader(list(langs), gpu=False) 
    reader = _READER_CACHE[key]

    results = reader.readtext(image_path, detail=0, paragraph=True)
    if isinstance(results, list):
        return "\n".join([r.strip() for r in results if r and r.strip()])
    return str(results)
