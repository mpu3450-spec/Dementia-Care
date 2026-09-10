import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🧠 Dementia Care Dashboard")

st.write("Connected to M5 Backend")


# Patient ID
patient_id = st.text_input("Enter Patient ID", "P001")


# Patient Information
if st.button("Get Patient"):

    response = requests.get(
        f"{API_URL}/patient/{patient_id}"
    )

    data = response.json()

    if response.status_code == 200:
        st.subheader("Patient Information")
        st.json(data)


# Game History
if st.button("Get Game History"):

    response = requests.get(
        f"{API_URL}/games/{patient_id}"
    )

    data = response.json()

    st.subheader("Game History")
    st.json(data)


# Progress
if st.button("Get Progress"):

    response = requests.get(
        f"{API_URL}/progress/{patient_id}"
    )

    data = response.json()

    st.subheader("Cognitive Progress")
    st.json(data)


# Languages
if st.button("Get Languages"):

    response = requests.get(
        f"{API_URL}/languages"
    )

    data = response.json()

    st.subheader("Available Languages")
    st.write(data["languages"])