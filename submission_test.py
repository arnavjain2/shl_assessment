import pandas as pd
from recommender import SHLRecommender

INPUT_FILE = "data/Gen_AI Dataset test.csv"
OUTPUT_FILE = "data/query_predictions_flat.csv"
QUERY_COL = "Query"
TOP_K = 10

def main():
    df = pd.read_csv(INPUT_FILE)

    if QUERY_COL not in df.columns:
        raise ValueError(f"Input file must contain '{QUERY_COL}' column")

    model = SHLRecommender()

    rows = []

    for idx, row in df.iterrows():
        query = str(row[QUERY_COL]).strip()

        if not query:
            continue

        results = model.recommend(query, top_k=TOP_K)

        for rank, (_, r) in enumerate(results.iterrows(), start=1):
            rows.append({
                "Query": query,
                "Rank": rank,
                "Predicted_URL": r["url"]
            })

        if idx % 5 == 0:
            print(f"Processed {idx + 1}/{len(df)} queries")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved predictions to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
