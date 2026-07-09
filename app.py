import streamlit as st

from src.screens.home import home_screen
from src.screens.teacher import teacher_screen
from src.screens.student import student_screen
from src.ui.styles import load_css

load_css()

st.set_page_config(
    page_title="AI Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Teacher",
        "Student"
    ]
)

if page == "Home":
    home_screen()

elif page == "Teacher":
    teacher_screen()

elif page == "Student":
    student_screen()