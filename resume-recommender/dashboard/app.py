import streamlit as st
import requests

st.title("AI Resume Recommender")

query = st.text_input("Enter Job Description")

if st.button("Search"):
    res = requests.post(
        "http://127.0.0.1:8000/api/v1/search/",
        params={"query": query}
    )

    data = res.json()

    for c in data:
        st.subheader(c["name"])
        st.write("Final Score:", c["final_score"])
        st.write("Matched Skills:", c.get("matched_skills"))
        st.write("Missing Skills:", c.get("missing_skills"))
        st.write("Reason:", c.get("reasoning"))
        st.divider()