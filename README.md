# SHL Assessment Recommendation Engine
This project implements an AI-powered recommendation system that suggests the most relevant SHL assessments based on a natural-language job description or hiring requirement.
The solution combines Sentence-BERT embeddings, FAISS vector search, and light domain-specific reranking to deliver accurate and explainable assessment recommendations.

# Features

Semantic search using SBERT (all-mpnet-base-v2)
Fast retrieval using FAISS
Domain-aware reranking (skills, URL keywords, test type signals)
REST API built with FastAPI
Interactive UI built with Streamlit
Evaluation using Mean Recall@K

# Structure
shl_assessment/
├── api.py
├── app.py
├── recommender.py
├── all_embeddings.py
├── build_faiss_index.py
├── crawler.py
├── train_eval.py
├── submission_test.py
├── requirements.txt
├── shl_assessments.csv
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
└── data/
├── embeddings_alls.npy
├── faiss_index.index
├── Arnav_Jain.csv
└── shl_assessments.csv



# Setup Instructions
### Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate
venv\Scripts\activate   

### Install dependencies
pip install -r requirements.txt

Install dependencies
pip install -r requirements.txt

### Running the Application
uvicorn api:app --reload
Open API docs in browser:
http://127.0.0.1:8000/docs
Example API request
POST /recommend
{
  "query": "Hiring a Senior Data Analyst with SQL and Python skills"
}

## Run the Streamlit UI
Start the UI:
streamlit run app.py
Open in browser:
http://localhost:8501

# Deployed on streamlit cloud
https://shlassessment-recommender.streamlit.app/

