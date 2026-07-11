import time
import streamlit as st

from src.attendance.face.liveness_detection import (
    perform_liveness_check
)

from src.attendance.face.face_embedding import (
    capture_face_embedding
)

from src.attendance.face.face_recognition import (
    find_best_match
)

from src.database.db import (
    get_face_embeddings,
    get_student
)


# =====================================================
# Verify Student Face
# =====================================================

def verify_student_face():
    """
    Verify a student's identity using ArcFace.

    Returns
    -------
    dict | None

    Example
    -------
    {
        "verified": True,
        "student_id": 5,
        "confidence": 0.93
    }
    """

    st.subheader("📷 Face Verification")

    st.info(
        """
        ### Instructions

        • Look directly at the camera.

        • Only one face should be visible.

        • Remove sunglasses or masks.

        • Keep your face centered.
        """
    )

    if not st.button(
        "Start Verification",
        type="primary",
        use_container_width=True
    ):
        return None

    start_time = time.time()

    # =====================================================
    # Liveness Detection
    # =====================================================

    with st.spinner("Performing liveness detection..."):

        if not perform_liveness_check():

            st.error(
                "❌ Liveness detection failed."
            )

            return None

    # =====================================================
    # Capture Face
    # =====================================================

    try:

        with st.spinner("Capturing face..."):

            unknown_embedding = capture_face_embedding(
                samples=10
            )

    except Exception as e:

        st.error(
            f"Camera Error:\n{e}"
        )

        return None

    if unknown_embedding is None:

        st.error(
            "❌ No valid face detected."
        )

        return None

    # =====================================================
    # Load Database
    # =====================================================

    with st.spinner("Loading registered faces..."):

        database_embeddings = get_face_embeddings()

    if not database_embeddings:

        st.warning(
            "No registered faces found."
        )

        return None

    # =====================================================
    # Face Matching
    # =====================================================

    with st.spinner("Matching face..."):

        result = find_best_match(

            unknown_embedding,

            database_embeddings,

            threshold=0.70

        )

    if result is None:

        st.error(
            "❌ Face verification failed."
        )

        return None

    # =====================================================
    # Load Student Information
    # =====================================================

    student = get_student(
        result["student_id"]
    )

    elapsed = time.time() - start_time

    st.success(
        f"""
        ✅ Face Verified Successfully

        Student :
        {student['full_name']}

        Student ID :
        {student['student_number']}

        Confidence :
        {result['confidence']:.3f}
        """
    )

    st.caption(
        f"Verification Time : {elapsed:.2f} seconds"
    )

    return {

        "verified": True,

        "student_id": result["student_id"],

        "student_name": student["full_name"],

        "confidence": result["confidence"]

    }