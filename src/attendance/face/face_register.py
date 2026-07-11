import os
import json
import streamlit as st

from src.attendance.face.face_embedding import (
    capture_face_embedding
)

from src.database.db import (
    save_face_embedding
)


# ==========================================================
# Face Registration Page
# ==========================================================

def face_register_page():

    st.header("📷 Face Registration")

    student = st.session_state.get("student")

    if student is None:
        st.error("Student session not found.")
        return

    st.info(
        """
### Registration Instructions

✔ Look directly at the camera.

✔ Keep only ONE face visible.

✔ Remove sunglasses or masks.

✔ Slowly turn your head:
- Left
- Right
- Up
- Down

✔ Around 20 face samples will be collected automatically.
"""
    )

    st.warning(
        "Please ensure the room has good lighting before starting."
    )

    if st.button(
        "Start Face Registration",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Capturing face samples..."):

            embedding = capture_face_embedding(
                samples=20
            )

        if embedding is None:

            st.error(
                """
Face registration failed.

Possible reasons:

• No face detected

• Multiple faces detected

• Camera unavailable

Please try again.
"""
            )
            return

        # ---------------------------------------
        # Create Folder
        # ---------------------------------------

        folder = "data/face"

        os.makedirs(
            folder,
            exist_ok=True
        )

        file_path = os.path.join(
            folder,
            f"{student['student_id']}.json"
        )

        # ---------------------------------------
        # Save locally
        # ---------------------------------------

        with open(
            file_path,
            "w"
        ) as file:

            json.dump(
                embedding,
                file,
                indent=4
            )

        # ---------------------------------------
        # Save into Supabase
        # ---------------------------------------

        save_face_embedding(

            student_id=student["student_id"],

            embedding=embedding,

            image_path=file_path

        )

        st.success("✅ Face registered successfully!")

        st.balloons()

        st.info(
            """
Your facial biometric template has been stored.

You can now use Face Attendance for future classes.
"""
        )