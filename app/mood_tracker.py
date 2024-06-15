import streamlit as st
from datetime import date

st.title("Daily Mood Tracker")

# List of mood options
mood_options = ["Happy", "Sad", "Neutral", "Excited", "Angry"]

# Input for mood and note
mood = st.selectbox("How are you feeling today?", mood_options)
note = st.text_area("Add a note (optional)")

# Button to log the mood
if st.button("Log Mood"):
    if "moods" not in st.session_state:
        st.session_state["moods"] = []
    st.session_state["moods"].append({"date": date.today(), "mood": mood, "note": note})
    st.success("Mood logged!")

# Display the mood log
st.write("Mood Log:")
if "moods" in st.session_state:
    for entry in st.session_state["moods"]:
        st.write(f"{entry['date']}: {entry['mood']} - {entry['note']}")
