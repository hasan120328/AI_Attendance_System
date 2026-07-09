import streamlit as st

from src.database.db import (
    get_teacher_subjects,
    update_subject,
    delete_subject,
    count_students
)


def manage_subject_page():

    teacher = st.session_state.teacher

    st.header("📚 Manage Subjects")

    subjects = get_teacher_subjects(
        teacher["teacher_id"]
    )

    if not subjects:
        st.info("No subjects created yet.")
        return

    for subject in subjects:

        student_count = count_students(
            subject["subject_id"]
        )

        with st.expander(
            f"{subject['subject_code']} - {subject['subject_name']}",
            expanded=False
        ):

            st.write(f"**Section:** {subject['section']}")
            st.write(f"**Semester:** {subject['semester']}")
            st.write(f"👨 Registered Students: **{student_count}**")

            st.divider()

            st.subheader("✏ Edit Subject")

            new_code = st.text_input(
                "Subject Code",
                value=subject["subject_code"],
                key=f"code_{subject['subject_id']}"
            )

            new_name = st.text_input(
                "Subject Name",
                value=subject["subject_name"],
                key=f"name_{subject['subject_id']}"
            )

            new_section = st.text_input(
                "Section",
                value=subject["section"],
                key=f"section_{subject['subject_id']}"
            )

            new_semester = st.text_input(
                "Semester",
                value=subject["semester"],
                key=f"semester_{subject['subject_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Save Changes",
                    key=f"save_{subject['subject_id']}",
                    use_container_width=True
                ):

                    update_subject(
                        subject["subject_id"],
                        new_code,
                        new_name,
                        new_section,
                        new_semester
                    )

                    st.success("Subject updated successfully.")
                    st.rerun()

            with col2:

                delete_key = f"confirm_delete_{subject['subject_id']}"

                if delete_key not in st.session_state:
                    st.session_state[delete_key] = False

                if not st.session_state[delete_key]:

                    if st.button(
                        "🗑 Delete Subject",
                        key=f"delete_{subject['subject_id']}",
                        use_container_width=True
                    ):

                        st.session_state[delete_key] = True
                        st.rerun()

                else:

                    st.warning(
                        "Are you sure you want to delete this subject?"
                    )

                    yes_col, no_col = st.columns(2)

                    with yes_col:

                        if st.button(
                            "✅ Yes",
                            key=f"yes_{subject['subject_id']}",
                            use_container_width=True
                        ):

                            delete_subject(
                                subject["subject_id"]
                            )

                            st.success(
                                "Subject deleted successfully."
                            )

                            st.rerun()

                    with no_col:

                        if st.button(
                            "❌ No",
                            key=f"no_{subject['subject_id']}",
                            use_container_width=True
                        ):

                            st.session_state[delete_key] = False
                            st.rerun()