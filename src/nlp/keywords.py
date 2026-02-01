
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text: str, top_k: int = 15):
    if not text or len(text.split()) < 20:
        return []

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1,2))
    X = vectorizer.fit_transform([text])
    scores = X.toarray()[0]
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return [t for t, s in ranked[:top_k] if s > 0]
