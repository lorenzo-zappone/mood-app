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

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

# Initialize the database
create_table()

st.title("Daily Mood Tracker")

def authorize_user():
    """Authorize the user and handle token retrieval and refresh."""
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
        # If token exists in session state, check if it's expired
        token = st.session_state['token']
        if oauth2.is_token_expired(token):
            # Attempt to refresh the token
            new_token = oauth2.refresh_token(token)
            if new_token:
                st.session_state.token = new_token
                user_info = oauth2.get_user_info(new_token)
                st.session_state.user_info = user_info
            else:
                # If refresh failed, clear session and reauthorize
                st.session_state.clear()
                st.error("Session expired. Please reauthorize.")
                st.experimental_rerun()

authorize_user()

if 'user_info' in st.session_state:
    user_info = st.session_state['user_info']
    username = user_info.get("email", "")

    st.sidebar.write(f"Welcome, {username}")

    # List of mood options
    mood_options = ["Happy", "Sad", "Neutral", "Excited", "Angry"]

    # Input for mood and note
    mood = st.selectbox("How are you feeling today?", mood_options)
    note = st.text_area("Add a note (optional)")

    # Button to log the mood
    if st.button("Log Mood"):
        add_mood_log(username, mood, note)  # Pass username to log mood
        st.success("Mood logged!")

    # Display the mood log
    st.write("Mood Log:")
    user_logs = get_mood_logs(username)  # Retrieve logs for the specific user
    if user_logs:
        df = pd.DataFrame(user_logs, columns=["Date", "Mood", "Note"])

        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date']).dt.date

        st.write(df)

        # Filter by date
        st.subheader("Mood Trends by Date")
        start_date_selected = st.date_input("Start date", min_value=df['Date'].min(), value=df['Date'].min())
        end_date_selected = st.date_input("End date", min_value=df['Date'].min(), value=df['Date'].max())

        filtered_df = df[(df['Date'] >= start_date_selected) & (df['Date'] <= end_date_selected)]
        st.write(filtered_df)

        # Visualize mood trends
        st.subheader("Mood Trends by Date")
        mood_counts_by_date = filtered_df.groupby(['Date', 'Mood']).size().reset_index(name='count')

        trend_chart = alt.Chart(mood_counts_by_date).mark_bar().encode(
            x=alt.X('Date:T', axis=alt.Axis(title='Date')),
            y=alt.Y('count:Q', axis=alt.Axis(title='Count')),
            color=alt.Color('Mood:N', legend=alt.Legend(title="Mood")),
            tooltip=['Date:T', 'Mood:N', 'count:Q']
        ).properties(
            width=800,
            height=400
        )

        st.altair_chart(trend_chart, use_container_width=True)
    else:
        st.write("No moods logged yet.")
else:
    st.write("Please authorize to use the app.")
