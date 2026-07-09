import streamlit as st

from src.database.db import (
    create_subject,
    get_teacher_subjects
)


def create_subject_page():

    teacher = st.session_state.teacher

    st.header("📚 Create Subject")

    st.write("Create a new course for students to enroll.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        subject_code = st.text_input(
            "Subject Code",
            placeholder="CSE401"
        )

        subject_name = st.text_input(
            "Subject Name",
            placeholder="Machine Learning"
        )

    with col2:

        section = st.text_input(
            "Section",
            placeholder="A"
        )

        semester = st.selectbox(
            "Semester",
            [
                "Spring",
                "Summer",
                "Fall"
            ]
        )

    st.divider()

    if st.button(
        "➕ Create Subject",
        use_container_width=True
    ):

        if (
            subject_code.strip() == ""
            or subject_name.strip() == ""
            or section.strip() == ""
        ):

            st.error("Please fill all fields.")

        else:

            try:

                create_subject(
                    subject_code=subject_code.upper(),
                    subject_name=subject_name,
                    section=section.upper(),
                    semester=semester,
                    teacher_id=teacher["teacher_id"]
                )

                st.toast("Subject created successfully 🎉")

                st.rerun()

            except Exception as e:

                st.error(f"Error : {e}")

    st.divider()

    st.subheader("📖 My Subjects")

    subjects = get_teacher_subjects(
        teacher["teacher_id"]
    )

    if len(subjects) == 0:

        st.info("No subjects created yet.")

    else:

        for subject in subjects:

            with st.container(border=True):

                c1, c2 = st.columns([4, 1])

                with c1:

                    st.markdown(
                        f"""
### {subject['subject_code']}

**{subject['subject_name']}**

**Section:** {subject['section']}

**Semester:** {subject['semester']}
"""
                    )

                with c2:

                    st.success("Active")