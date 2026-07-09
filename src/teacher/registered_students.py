import streamlit as st
import pandas as pd

from src.database.db import get_registered_students


def registered_students_page():

    teacher = st.session_state.teacher

    st.header("👨‍🎓 Registered Students")

    students = get_registered_students(
        teacher["teacher_id"]
    )

    if not students:

        st.info("No students have enrolled in your subjects yet.")
        return

    rows = []

    for item in students:

        student = item["students"]
        subject = item["subjects"]

        rows.append(
            {
                "Student ID": student["student_number"],
                "Student Name": student["full_name"],
                "Email": student["email"],
                "Department": student["department"],
                "Semester": student["semester"],
                "Subject Code": subject["subject_code"],
                "Subject": subject["subject_name"],
                "Section": subject["section"],
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.metric(
        "Total Enrollments",
        len(df)
    )

    st.metric(
        "Unique Students",
        df["Student ID"].nunique()
    )