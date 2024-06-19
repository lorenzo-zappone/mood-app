import streamlit as st
from datetime import date
import pandas as pd
import altair as alt
import os
from dotenv import load_dotenv

from streamlit_oauth import OAuth2Component
from db.database import create_table, add_mood_log, get_mood_logs

# Load environment variables from .env file
load_dotenv()

# Set environment variables
AUTHORIZE_URL = st.secrets["oauth"]["AUTHORIZE_URL"]
TOKEN_URL = st.secrets["oauth"]["TOKEN_URL"]
REFRESH_TOKEN_URL = st.secrets["oauth"]["REFRESH_TOKEN_URL"]
REVOKE_TOKEN_URL = st.secrets["oauth"]["REVOKE_TOKEN_URL"]
CLIENT_ID = st.secrets["oauth"]["CLIENT_ID"]
CLIENT_SECRET = st.secrets["oauth"]["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["oauth"]["REDIRECT_URI"]
SCOPE = st.secrets["oauth"]["SCOPE"]

# Ensure SCOPE is not None
if SCOPE is None:
    st.error("SCOPE environment variable is not set. Please check your .env file.")
    st.stop()
else:
    # Create OAuth2Component instance
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

    # Initialize the database
    create_table()

    st.title("Daily Mood Tracker")

    # Check if token exists in session state
    if 'token' not in st.session_state:
        # If not, show authorize button
        result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            # If authorization successful, save token in session state
            st.session_state.token = result.get('token')
            user_info = oauth2.get_user_info(result.get('token'))
            st.session_state.user_info = user_info
            st.rerun()
    else:
        # If token exists in session state, show the token
        token = st.session_state['token']
        user_info = st.session_state.get('user_info', {})
        username = user_info.get("email", "")

        st.sidebar.write(f"Welcome, {username}")

        # List of mood options
        mood_options = ["Happy", "Sad", "Neutral", "Excited", "Angry"]

        # Input for mood and note
        mood = st.selectbox("How are you feeling today?", mood_options)
        note = st.text_area("Add a note (optional)")

        # Button to log the mood
        if st.button("Log Mood"):
            add_mood_log(username, mood, note)
            st.success("Mood logged!")

        # Display the mood log
        st.write("Mood Log:")
        user_logs = get_mood_logs(username)
        if user_logs:
            df = pd.DataFrame(user_logs, columns=["Date", "Mood", "Note"])

            # Convert 'Date' column to datetime
            df['Date'] = pd.to_datetime(df['Date']).dt.date

            st.write(df)

            # Filter by date
            st.subheader("Filter by Date")
            start_date_selected = st.date_input("Start date", min_value=df['Date'].min(), value=df['Date'].min())
            end_date_selected = st.date_input("End date", min_value=df['Date'].min(), value=df['Date'].max())

            filtered_df = df[(df['Date'] >= start_date_selected) & (df['Date'] <= end_date_selected)]
            st.write(filtered_df)

            # Export to CSV
            st.subheader("Export Log")
            if st.button("Export to CSV"):
                filtered_df.to_csv(f'{username}_mood_log.csv', index=False)
                st.success(f"Log exported to {username}_mood_log.csv")

            # Visualize mood distribution
            st.subheader("Mood Distribution")
            mood_counts = filtered_df['Mood'].value_counts().reset_index()
            mood_counts.columns = ['mood', 'count']

            chart = alt.Chart(mood_counts).mark_bar().encode(
                x='mood',
                y='count'
            )
            st.altair_chart(chart, use_container_width=True)

            # Pie chart for mood distribution
            st.subheader("Mood Distribution (Pie Chart)")
            chart = alt.Chart(mood_counts).mark_circle().encode(
                alt.Size('count:Q',
                         legend=None),
                color='mood:N',
                tooltip=['mood', 'count']
            ).properties(
                width=600,
                height=300
            )
            st.altair_chart(chart)
        else:
            st.write("No moods logged yet.")
