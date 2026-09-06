import streamlit as st
st.title("DEMENTIA CARE")
st.subheader("CAREGIVER LOGIN")
st.text_input('Email Address')
st.text_input("password",type = "password")
if st.button("login"):
    st.switch_page("pages/dashboard.py")
