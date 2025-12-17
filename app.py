import streamlit as st
import pandas as pd
from recommendor2 import SHLRecommender

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="SHL Assessment Recommender",
    layout="centered"
)

st.title("🔍 SHL Assessment Recommendation Engine")

st.write(
    "Enter a job description or hiring requirement to get the most relevant SHL assessments."
)

# ---------------------------------
# LOAD MODEL (CACHE)
# ---------------------------------
@st.cache_resource
def load_model():
    return SHLRecommender()

model = load_model()

# ---------------------------------
# INPUTS
# ---------------------------------
query = st.text_area(
    "Job Requirement / Query",
    placeholder="e.g. Hiring a Senior Data Analyst with SQL, Python and Excel skills"
)

top_k = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=15,
    value=10
)

# ---------------------------------
# RUN RECOMMENDER
# ---------------------------------
if st.button("Recommend Assessments"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Finding best assessments..."):
            results = model.recommend(query, top_k=top_k)

        if results.empty:
            st.error("No assessments found.")
        else:
            st.success(f"Top {len(results)} recommendations")

            for idx, row in results.iterrows():
                st.markdown("### " + row["name"])
                st.markdown(f"🔗 **URL:** {row['url']}")
                st.markdown(f"⏱️ **Duration:** {row['duration']} minutes")
                st.markdown(f"🧠 **Test Type:** {row['test_type']}")
                st.markdown("---")
