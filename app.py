import streamlit as st
import requests

# ---------------------------------
# CONFIG
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
# API URL (CHANGE AFTER DEPLOY)
# ---------------------------------
API_URL = "https://shl-api-zt7k.onrender.com/recommend"
# during local testing:
# API_URL = "http://localhost:10000/recommend"

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
# CALL API
# ---------------------------------
if st.button("Recommend Assessments"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Finding best assessments..."):
            response = requests.post(
                API_URL,
                json={"query": query, "top_k": top_k},
                timeout=60
            )

        if response.status_code != 200:
            st.error("API error. Please try again.")
        else:
            data = response.json()["results"]

            if not data:
                st.warning("No assessments found.")
            else:
                st.success(f"Top {len(data)} recommendations")

                for item in data:
                    st.markdown(f"### {item['name']}")
                    st.markdown(f"🔗 **URL:** {item['url']}")
                    st.markdown(f"⏱️ **Duration:** {item['duration']} minutes")
                    st.markdown(f"🧠 **Test Type:** {item['test_type']}")
                    st.markdown("---")
