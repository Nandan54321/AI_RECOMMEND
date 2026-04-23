import streamlit as st
import requests

st.title("AI Resume Recommender")

query = st.text_input("Enter Job Description")

if st.button("Search"):
    res = requests.post(
        "http://127.0.0.1:8000/api/v1/search/",
        json={"query": query}
    )

    data = res.json()
    results = data.get("results", [])

    if not results:
        st.warning("No candidates found")
    else:
        for c in results:
            st.subheader(c.get("name"))
            st.write("Title:", c.get("title"))
            st.write("Final Score:", c.get("final_score"))
            st.write("Vector Score:", c.get("vector_score"))
            st.write("LLM Score:", c.get("llm_score"))
            st.write("Rule Score:", c.get("rule_score"))
            st.write("Matched Skills:", c.get("matched_skills"))
            st.write("Missing Skills:", c.get("missing_skills"))
            st.write("Reason:", c.get("reasoning"))
            st.divider()