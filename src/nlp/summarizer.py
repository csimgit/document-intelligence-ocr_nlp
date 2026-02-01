import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def _split_sentences(text: str):
    # simple sentence splitter 
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    # split on . ! ? plus OCR newlines
    sents = re.split(r"(?<=[.!?])\s+|\n+", text)
    sents = [s.strip() for s in sents if len(s.strip()) > 10]
    return sents

def summarize_text(text: str, num_sentences: int = 4) -> str:
    """
    Offline extractive summary:
    - Split into sentences
    - TF-IDF on sentences
    - Score sentences by TF-IDF weight
    - Return top N sentences in original order
    """
    sents = _split_sentences(text)
    if len(sents) <= num_sentences:
        return text.strip()

    vec = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
    X = vec.fit_transform(sents)  # shape: (n_sents, n_terms)

    # sentence score = sum TF-IDF weights
    scores = np.asarray(X.sum(axis=1)).ravel()

    # select top sentences 
    top_idx = np.argsort(scores)[::-1][:num_sentences]
    top_idx_sorted = sorted(top_idx)

    summary = " ".join([sents[i] for i in top_idx_sorted])
    return summary.strip()
