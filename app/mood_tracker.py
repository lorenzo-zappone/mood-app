import streamlit as st
from datetime import date
import pandas as pd
import altair as alt

# Title
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
    df = pd.DataFrame(st.session_state["moods"])
    st.write(df)

    # Filter by date
    st.subheader("Filter by Date")
    start_date = st.date_input("Start date", min_value=df['date'].min(), value=df['date'].min())
    end_date = st.date_input("End date", min_value=df['date'].min(), value=df['date'].max())
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    st.write(filtered_df)

    # Export to CSV
    st.subheader("Export Log")
    if st.button("Export to CSV"):
        filtered_df.to_csv('mood_log.csv', index=False)
        st.success("Log exported to mood_log.csv")

    # Visualize mood trends
    st.subheader("Mood Trends")
    mood_counts = filtered_df['mood'].value_counts().reset_index()
    mood_counts.columns = ['mood', 'count']
    chart = alt.Chart(mood_counts).mark_bar().encode(
        x='mood',
        y='count'
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.write("No moods logged yet.")
