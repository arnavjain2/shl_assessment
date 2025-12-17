import pandas as pd
import numpy as np
from recommender import SHLRecommender
from urllib.parse import urlparse


DATASET_PATH = "data/Gen_AI Dataset(Train-Set).csv"
QUERY_COL = "Query"
GT_COL = "Assessment_url"
K_VALUES = [10]

def normalize_shl_url(url: str) -> str:
    if not isinstance(url, str):
        return ""

    url = url.strip().lower()
    parsed = urlparse(url)
    path = parsed.path.replace("/solutions", "").rstrip("/")
    return path

def load_eval_data():
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna(subset=[QUERY_COL, GT_COL])

    grouped = (
        df.groupby(QUERY_COL)[GT_COL]
        .apply(lambda x: [normalize_shl_url(u) for u in x])
        .to_dict()
    )

    print(f"Loaded {len(grouped)} unique evaluation queries")
    return grouped

def recall_at_k(retrieved, relevant, k):
    if not relevant:
        return 0.0
    retrieved_k = retrieved[:k]
    return len(set(retrieved_k) & set(relevant)) / len(relevant)


def mean_recall_at_k(model, grouped_gt, k):
    scores = []

    for query, relevant_urls in grouped_gt.items():
        results = model.recommend(query, top_k=k)

        retrieved = [
            normalize_shl_url(url)
            for url in results["url"].tolist()
        ]

        score = recall_at_k(retrieved, relevant_urls, k)
        scores.append(score)
        print(f"Recall@10 for query: {score:.2f}")
    return float(np.mean(scores))


def run_evaluation():
    model = SHLRecommender()
    grouped_gt = load_eval_data()

    print("\n📊 Mean Recall@K Results")
    print("-" * 30)

    for k in K_VALUES:
        score = mean_recall_at_k(model, grouped_gt, k)
        print(f"Mean Recall@{k}: {score:.4f}")

if __name__ == "__main__":
    run_evaluation()
