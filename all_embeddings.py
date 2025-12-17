import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
CSV_PATH = "data/shl_assessments.csv"
EMB_PATH = "data/embeddings_alls.npy"
MODEL_NAME = "all-mpnet-base-v2"

# -------------------------------------------------
# TEST TYPE FULL FORM MAPPING
# -------------------------------------------------
TEST_TYPE_MAP = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

def expand_test_types(test_type_str: str) -> str:
    """
    Convert test type codes (e.g. K,P) to full semantic forms.
    """
    if not isinstance(test_type_str, str):
        return ""

    expanded = []
    for code in test_type_str.split(","):
        code = code.strip().upper()
        if code in TEST_TYPE_MAP:
            expanded.append(TEST_TYPE_MAP[code])

    return ", ".join(expanded)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
def load_data():
    df = pd.read_csv(CSV_PATH)

    # Duration → int, N/A → 0
    df["duration"] = (
        pd.to_numeric(df["duration"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    # Fill remaining NaNs
    df = df.fillna("")
    return df

# -------------------------------------------------
# BUILD EMBEDDING TEXT
# -------------------------------------------------
def build_embedding_text(row):
    expanded_test_types = expand_test_types(row["test_type"])
    a = ""
    if row['remote_support']:
        a += " Supports remote online unproctored testing \n"
    if row['adaptive_support']:
        a += " Adaptive IRT assessment that adjusts difficulty \n"
    if "K" in row["test_type"]:
        a += " Cognitive ability assessment for knowledge and reasoning \n"
    if "P" in row["test_type"]:
        a += " Personality behavioral assessment for workplace behavior \n"
    return f"""
    Assessment Name: {row['name']}
    Description: {row['description']}
    Test Type: {row['test_type']}
    {a}
    """.strip().lower()

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    df = load_data()

    texts = df.apply(build_embedding_text, axis=1).tolist()

    model = SentenceTransformer(
        MODEL_NAME
    )

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    ).astype("float32")

    np.save(EMB_PATH, embeddings)

    print(f"Saved embeddings with shape: {embeddings.shape}")

# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    main()
