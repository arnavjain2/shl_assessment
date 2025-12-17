import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("🧠 SHL Assessment Recommendation System")

query = st.text_area(
    "Enter Job Requirement / Query",
    placeholder="e.g. Senior Data Analyst with SQL, Python and Excel skills",
    height=120
)

top_k = st.slider("Number of recommendations", 5, 15, 10)

if st.button("🔍 Recommend Assessments"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Finding best assessments..."):
            response = requests.post(
                API_URL,
                json={"query": query, "top_k": top_k},
                timeout=30
            )

        if response.status_code != 200:
            st.error("API Error")
        else:
            data = response.json()["results"]

            if not data:
                st.info("No recommendations found.")
            else:
                st.subheader("📋 Recommended Assessments")

                for i, r in enumerate(data, 1):
                    with st.container():
                        st.markdown(f"### {i}. {r['name']}")
                        st.markdown(f"🔗 **URL:** {r['url']}")
                        st.markdown(f"🧪 **Test Type:** {r['test_type']}")
                        st.markdown(f"⏱ **Duration:** {r['duration']} minutes")
                        st.markdown(f"⭐ **Score:** {r['score']:.3f}")
                        st.markdown("---")
