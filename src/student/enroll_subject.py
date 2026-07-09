import streamlit as st

from src.database.db import (
    get_all_subjects,
    get_student_subjects,
    enroll_student
)


def enroll_subject_page():

    student = st.session_state.student

    st.header("📚 Enroll Subject")

    st.write("Select a subject created by your teacher.")

    st.divider()

    all_subjects = get_all_subjects()

    enrolled_subjects = get_student_subjects(
        student["student_id"]
    )

    enrolled_ids = []

    for item in enrolled_subjects:
        enrolled_ids.append(
            item["subject_id"]
        )

    available_subjects = []

    for subject in all_subjects:

        if subject["subject_id"] not in enrolled_ids:
            available_subjects.append(subject)

    if len(available_subjects) == 0:

        st.success("You have already enrolled in all available subjects.")

        return

    for subject in available_subjects:

        with st.container(border=True):

            col1, col2 = st.columns([4,1])

            with col1:

                st.subheader(subject["subject_name"])

                st.write(
                    f"**Code:** {subject['subject_code']}"
                )

                st.write(
                    f"**Section:** {subject['section']}"
                )

                st.write(
                    f"**Semester:** {subject['semester']}"
                )

            with col2:

                if st.button(
                    "Enroll",
                    key=f"enroll_{subject['subject_id']}"
                ):

                    enroll_student(
                        student["student_id"],
                        subject["subject_id"]
                    )

                    st.toast(
                        "Successfully enrolled 🎉"
                    )

                    st.rerun()