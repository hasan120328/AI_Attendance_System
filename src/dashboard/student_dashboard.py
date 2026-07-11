import streamlit as st
import pandas as pd

from src.student.enroll_subject import enroll_subject_page
from src.attendance.face.face_register import face_register_page
from src.attendance.face.face_verify import verify_student_face
from src.attendance.attendance_manager import (
    mark_face_attendance
)


from src.database.db import (
    get_student_subjects,
    get_student_attendance
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

    (
        dashboard_tab,
        subjects_tab,
        enroll_tab,
        attendance_tab,
        face_register_tab,
        face_attendance_tab,
        profile_tab
    ) = st.tabs(
        [
            "🏠 Dashboard",
            "📚 My Subjects",
            "➕ Enroll Subject",
            "📋 Attendance",
            "📸 Face Registration",
            "📷 Face Attendance",
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

        else:
            st.info("You are not enrolled in any subject.")

    # ==================================================
    # ENROLL SUBJECT
    # ==================================================

    with enroll_tab:

        enroll_subject_page()

    # ==================================================
    # ATTENDANCE HISTORY
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

    # ==================================================
    # FACE REGISTRATION
    # ==================================================

    with face_register_tab:

        face_register_page()

    # ==================================================
    # FACE ATTENDANCE
    # ==================================================

    with face_attendance_tab:

        st.subheader("📷 Face Attendance")

        st.write(
            "Verify your identity to mark attendance."
        )

        result = verify_student_face()

    if result:

        attendance = mark_face_attendance(

            student_id=result["student_id"],

            confidence=result["confidence"]

        )

        if attendance["success"]:

            st.success(attendance["message"])

        else:

            st.warning(attendance["message"])

        if result:

            st.success(
                f"""
                ✅ Attendance Verified

                Student ID: {result['student_id']}

                Confidence: {result['confidence']:.3f}
                """
            )

            # Next step:
            # save_attendance(...)
            # mark_attendance(...)
            # create_attendance_record(...)

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