import streamlit as st
from datetime import date

st.title("Daily Mood Tracker")

mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Neutral", "Excited", "Angry"])
note = st.text_area("Add a note (optional)")

if st.button("Log Mood"):
    if "moods" not in st.session_state:
        st.session_state["moods"] = []
    st.session_state["moods"].append({"date": date.today(), "mood": mood, "note": note})

st.write("Mood Log:")
if "moods" in st.session_state:
    for entry in st.session_state["moods"]:
        st.write(f"{entry['date']}: {entry['mood']} - {entry['note']}")
