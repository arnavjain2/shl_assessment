from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from recommender import SHLRecommender   # <-- your file

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0"
)

# Load model once
model = SHLRecommender()

# ---------------------------
# Request / Response Schemas
# ---------------------------
class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

class Assessment(BaseModel):
    name: str
    url: str
    test_type: str
    duration: int
    score: float

class RecommendResponse(BaseModel):
    results: List[Assessment]

# ---------------------------
# API Endpoint
# ---------------------------
@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    results_df = model.recommend(req.query, top_k=req.top_k)

    results = []
    for _, row in results_df.iterrows():
        results.append({
            "name": row["name"],
            "url": row["url"],
            "test_type": row.get("test_type", ""),
            "duration": int(row.get("duration", 0)),
            "score": float(row.get("score", 0.0))
        })

    return {"results": results}

# ---------------------------
# Health check
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
