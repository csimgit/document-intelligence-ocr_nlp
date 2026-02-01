
from transformers import pipeline

_ner = None

def extract_entities(text: str):
    global _ner
    if _ner is None:
        _ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

    if not text.strip():
        return []

    # NER 
    entities = []
    for ch in text.split("\n"):
        ch = ch.strip()
        if len(ch) < 15:
            continue
        try:
            entities.extend(_ner(ch))
        except Exception:
            pass
    # simplify output
    clean = []
    for e in entities:
        clean.append({
            "entity": e.get("entity_group"),
            "text": e.get("word"),
            "score": float(e.get("score", 0.0))
        })
    return clean
