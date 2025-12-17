import re
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-mpnet-base-v2"

STOPWORDS = {
    "the", "and", "for", "with", "role", "looking",
    "hiring", "who", "that", "this", "can", "able",
    "require", "requiring"
}

def extract_keywords(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {
        t for t in tokens
        if len(t) > 2 and t not in STOPWORDS
    }

def needs_personality(query):
    q = query.lower()
    return any(x in q for x in [
        "collaborate", "team", "culture",
        "communication", "interpersonal", "personality"
    ])

class SHLRecommender:
    def __init__(self):
        self.df = pd.read_csv("data/shl_assessments.csv")
        self.df["duration"] = (
            pd.to_numeric(self.df["duration"], errors="coerce")
            .fillna(0)
            .astype(int)
        )
        self.df = self.df.fillna("")

        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index("data/faiss_index.index")

    def recommend(self, query, top_k=10):
        q_emb = self.model.encode([query], normalize_embeddings=True)
        scores, indices = self.index.search(
            q_emb.astype("float32"),
            top_k * 4
        )

        results = self.df.iloc[indices[0]].copy()
        results["score"] = scores[0]

        keywords = extract_keywords(query)

        def keyword_boost(row):
            url = row["url"].lower()
            hits = sum(1 for k in keywords if k in url)
            return min(hits * 0.03, 0.09)

        results["score"] += results.apply(keyword_boost, axis=1)

        want_p = needs_personality(query)

        def kp_boost(row):
            tt = str(row.get("test_type", "")).upper()
            if want_p and "P" in tt:
                return 0.04
            if not want_p and "K" in tt:
                return 0.02
            return 0.0

        results["score"] += results.apply(kp_boost, axis=1)

        results = results.sort_values("score", ascending=False)

        return results.head(top_k)
