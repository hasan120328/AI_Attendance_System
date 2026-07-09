import streamlit as st
import pandas as pd


from src.student.enroll_subject import enroll_subject_page
# from src.attendance.face_register import face_register_page

from src.database.db import (
    get_student_subjects,
    get_student_attendance,
    get_all_subjects,
    enroll_student,
    unenroll_student
)


def student_dashboard():

    student = st.session_state.get("student")

    if student is None:
        st.error("Student session expired.")
        st.session_state.student_logged_in = False
        st.rerun()

    st.title("🎓 Student Dashboard")
    st.write(f"Welcome, **{student['full_name']}**")

    st.divider()

    dashboard_tab, subjects_tab, enroll_tab, attendance_tab, profile_tab = st.tabs(
    [
        "🏠 Dashboard",
        "📚 My Subjects",
        "➕ Enroll Subject",
        "📋 Attendance",
        "📸 Face Registration",
        "👤 Profile"
    ]
)

    # ==================================================
    # DASHBOARD
    # ==================================================

    with dashboard_tab:

        my_subjects = get_student_subjects(student["student_id"])
        attendance = get_student_attendance(student["student_id"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Registered Subjects",
                len(my_subjects)
            )

        with col2:
            st.metric(
                "Attendance Records",
                len(attendance)
            )

    # ==================================================
    # MY SUBJECTS
    # ==================================================

    with subjects_tab:

        st.subheader("My Registered Subjects")

        my_subjects = get_student_subjects(student["student_id"])

        if my_subjects:

            for item in my_subjects:

                info = item.get("subjects")

                if info is None:
                    continue

                with st.container(border=True):

                    st.write(f"### {info['subject_code']}")
                    st.write(info["subject_name"])
                    st.caption(f"Section: {info['section']}")
                    st.caption(f"Semester: {info['semester']}")

                    if st.button(
                        "Unenroll",
                        key=f"unenroll_{info['subject_id']}"
                    ):

                        unenroll_student(
                            student["student_id"],
                            info["subject_id"]
                        )

                        st.success("Subject removed successfully.")
                        st.rerun()

        else:
            st.info("You are not enrolled in any subject.")

    # ==================================================
    # ENROLL SUBJECT
    # ==================================================

    with enroll_tab:

        enroll_subject_page()

    # ==================================================
    # ATTENDANCE
    # ==================================================
    
    

    with attendance_tab:

        st.subheader("Attendance History")

        attendance = get_student_attendance(
            student["student_id"]
        )

        if attendance:

            rows = []

            for item in attendance:

                subject = item.get("subjects")

                rows.append(
                    {
                        "Date": item.get("attendance_date"),
                        "Subject": subject["subject_name"] if subject else "-",
                        "Method": item.get("method"),
                        "Confidence": item.get("confidence")
                    }
                )

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True
            )

        else:
            st.info("No attendance records found.")

    # # ==================================================
    # # FACE REGISTRATION
    # # ==================================================

    # with face_tab:

    #     st.subheader("Face Registration")

    #     face_register_page()
    #     st.info("Face registration module coming soon.")

    # ==================================================
    # PROFILE
    # ==================================================

    with profile_tab:

        st.subheader("Student Profile")

        st.write(f"**Student ID:** {student['student_number']}")
        st.write(f"**Full Name:** {student['full_name']}")
        st.write(f"**Email:** {student['email']}")
        st.write(f"**Department:** {student['department']}")
        st.write(f"**Semester:** {student['semester']}")

        st.divider()

        if st.button(
            "Logout",
            key="student_logout"
        ):

            st.session_state.student_logged_in = False
            st.session_state.student = None
            st.rerun()