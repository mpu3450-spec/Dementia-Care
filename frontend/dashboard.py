import streamlit as st

st.set_page_config(
    page_title = "Dementia Care",page_icon = "🧠",
      layout = "wide")
language = st.selectbox("selec language",["English","Hindi","Assamese","Manipuri"])
st.write("selected languages:",language)
st.title("CAREGIVER DASHBOARD")
patient_name = "Ramesh Kumar"
patient_id = "P001"
last_active = "Today, 7:30 PM"

st.write("Patient:", patient_name)
st.write("Patient ID:", patient_id)
st.write("Last Active:", last_active)

with st.sidebar:
    add_radio = st.radio("Go to" ,[ "📊 OVERVIEW","📈 PERFORMANCE","🎮 ACTIVITY" , "🔔 REMINDER"])

if add_radio == "📊 OVERVIEW":
    st.subheader("Patient Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Cognitive Score", "78")
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