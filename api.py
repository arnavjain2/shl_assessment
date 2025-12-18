# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from recommender import SHLRecommender
import uvicorn

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0"
)

# Load model ONCE
model = SHLRecommender()

# ---------------------------
# Schemas
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
    df = model.recommend(req.query, top_k=req.top_k)

    results = []
    for _, row in df.iterrows():
        results.append({
            "name": row["name"],
            "url": row["url"],
            "test_type": row.get("test_type", ""),
            "duration": int(row.get("duration", 0)),
            "score": float(row.get("score", 0.0))
        })

    return {"results": results}

@app.get("/health")
def health():
    return {"status": "ok"}

# Local dev only
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
