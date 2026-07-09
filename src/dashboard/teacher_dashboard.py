import streamlit as st

from src.teacher.dashboard import dashboard_page
from src.teacher.create_subject import create_subject_page
from src.teacher.manage_subject import manage_subject_page
from src.teacher.registered_students import registered_students_page
from src.teacher.face_attendance import face_attendance_page


# Uncomment these when you create them
# from src.teacher.voice_attendance import voice_attendance_page
# from src.teacher.attendance_history import attendance_history_page
# from src.teacher.analytics import analytics_page
# from src.teacher.settings import settings_page


def teacher_dashboard():

    # -----------------------------
    # Check Login
    # -----------------------------
    if "teacher" not in st.session_state or st.session_state.teacher is None:
        st.error("Please login first.")
        return

    teacher = st.session_state.teacher

    st.title("👨‍🏫 Teacher Dashboard")
    st.write(f"Welcome **{teacher['full_name']}**")
    st.divider()

    # -----------------------------
    # Sidebar Menu
    # -----------------------------
    menu = st.sidebar.radio(
        "Teacher Menu",
        [
            "Dashboard",
            "Create Subject",
            "Manage Subjects",
            "Registered Students",
            "Face Attendance",
            "Voice Attendance",
            "Attendance History",
            "Analytics",
            "Settings"
        ]
    )

    # -----------------------------
    # Dashboard
    # -----------------------------
    if menu == "Dashboard":

        dashboard_page()

    # -----------------------------
    # Create Subject
    # -----------------------------
    elif menu == "Create Subject":

        create_subject_page()

    # -----------------------------
    # Manage Subjects
    # -----------------------------
    elif menu == "Manage Subjects":

        manage_subject_page()

    # -----------------------------
    # Registered Students
    # -----------------------------
    elif menu == "Registered Students":

        registered_students_page()

    # -----------------------------
    # Face Attendance
    # -----------------------------
    elif menu == "Face Attendance":

        face_attendance_page()

    # -----------------------------
    # Voice Attendance
    # -----------------------------
    elif menu == "Voice Attendance":

        st.info("Voice Attendance Module Coming Soon.")

    # -----------------------------
    # Attendance History
    # -----------------------------
    elif menu == "Attendance History":

        st.info("Attendance History Module Coming Soon.")

    # -----------------------------
    # Analytics
    # -----------------------------
    elif menu == "Analytics":

        st.info("Analytics Module Coming Soon.")

    # -----------------------------
    # Settings
    # -----------------------------
    elif menu == "Settings":

        st.info("Settings Module Coming Soon.")