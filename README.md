# Daily Mood Tracker

## Overview
The Daily Mood Tracker is a simple web application built using Streamlit that allows users to log their daily moods along with optional notes. This application helps users keep track of their emotional state over time.

## Features
- Select mood from predefined options.
- Add an optional note for each mood entry.
- Log the mood with the current date.
- Display the logged moods.

## Installation

### Prerequisites
- Python 3.12 or later
- pip (Python package installer)

### Steps
1. **Clone the repository** (if applicable) or download the `mood_tracker.py` file to your local machine.
2. **Install Streamlit**:
    ```bash
    pip install streamlit
    ```

## Usage
1. **Navigate to the directory** where `mood_tracker.py` is located.
2. **Run the Streamlit app**:
    ```bash
    streamlit run mood_tracker.py
    ```

## Code Explanation

### Import Libraries
```python
import streamlit as st
from datetime import date
