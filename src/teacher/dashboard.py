import streamlit as st
from src.database.db import (
    get_teacher_subjects,
    get_teacher_attendance
)

def dashboard_page():

    teacher = st.session_state.teacher

    st.header("📊 Teacher Dashboard")

    st.write(f"Welcome **{teacher['full_name']}**")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "My Subjects",
            len(get_teacher_subjects(teacher["teacher_id"]))
        )

    with col2:
        st.metric(
            "Attendance Records",
            len(get_teacher_attendance(teacher["teacher_id"]))
        )