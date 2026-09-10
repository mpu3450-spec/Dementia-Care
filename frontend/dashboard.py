import streamlit as st
import requests
import pandas as pd

#page config
st.set_page_config(
    page_title = "Dementia Care",page_icon = "🧠",
      layout = "wide")

# M5 BACKEND
API_URL = "http://127.0.0.1:8000"
patient_id = "P001"

# HELPER FUNCTION

def get_api_data(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None

#language
language_data = get_api_data("/languages")
if language_data:
    languages = language_data.get(
        "languages",
        ["English"]
    )
else:
    languages = ["English"]
language = st.selectbox("selec language",["English","Hindi","Assamese","Manipuri"])
st.write("selected languages:",language)

# PATIENT INFORMATION

patient = get_api_data(
    f"/patient/{patient_id}"
)
if patient:
    patient_name = patient.get(
        "name",
        "Unknown"
    )
    last_active = patient.get(
        "last_active",
        "Unknown"
    )
else:
    patient_name = "Patient not found"
    last_active = "Unknown"

#header
st.title("CAREGIVER DASHBOARD")
st.write("**Patient:**", patient_name)
st.write("**Patient ID:**", patient_id)
st.write("**Last Active:**", last_active)

#get data
progress = get_api_data(
    f"/progress/{patient_id}"
)

games = get_api_data(
    f"/games/{patient_id}"
)

reminders = get_api_data(
    f"/reminders/{patient_id}"
)

ai_data = get_api_data(
    f"/ai-performance/{patient_id}"
)

#sidebars
with st.sidebar:
    add_radio = st.radio("Go to" ,[ "📊 OVERVIEW","📈 PERFORMANCE","🎮 ACTIVITY" , "🔔 REMINDER"])

if add_radio == "📊 OVERVIEW":
    st.subheader("Patient Overview")
    if progress:
     col1, col2, col3 = st.columns(3)
     with col1:
        st.metric("🧠 Average Score",progress.get("average_score",0))
     with col2:
        st.metric("🎯 Accuracy", "85%")
     with col3:
        st.metric("🎮 Games Completed", "12")
  

if add_radio == "🎮 ACTIVITY":
    st.subheader("Games Activity")
    col1,col2 = st.columns(2)
    with col1:
        st.metric("Memory Game - Score","80")
    with col2:
        st.metric("Pattern Game - Score:" ,"75")

if add_radio == "🔔 REMINDER":
    st.subheader("Patient Reminder")
    col1,col2 = st.columns(2)
    with col1:
        st.metric("Medicine Reminder:","80")
    with col2:
        st.metric("Appointmen:" ,"75")

if add_radio == "📈 PERFORMANCE":
    st.subheader("Performance Trend")
    df = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Score": [65, 70, 68, 75, 78]
    }
    st.line_chart(df,x = "Day",y = "Score")

with st.container(border = True):
 st.subheader("🎯 AI Recommendation")
 col1, col2 = st.columns(2)
 with col1:
    st.info("🎮 Next Game\n\n**Memory Game**")
 with col2:
    st.success("⚡ Difficulty\n\n**Medium**")

if st.button("⚠️ ALERTS", key="alerts_button"):
    st.switch_page("pages/alerts.py")