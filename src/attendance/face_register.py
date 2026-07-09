import os
import cv2
import json
import numpy as np
import streamlit as st

from insightface.app import FaceAnalysis

from src.database.db import save_face_embedding


# =====================================================
# Load Face Model
# =====================================================

@st.cache_resource
def load_model():

    app = FaceAnalysis(
        name="buffalo_l"
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    return app


face_app = load_model()


# =====================================================
# Capture Face Embedding
# =====================================================

def capture_face_embedding():

    cap = cv2.VideoCapture(0)

    embeddings = []

    captured = 0

    frame_placeholder = st.empty()

    status = st.empty()

    while captured < 20:

        ret, frame = cap.read()

        if not ret:
            continue

        faces = face_app.get(frame)

        if len(faces) == 1:

            face = faces[0]

            embeddings.append(face.embedding)

            captured += 1

            status.info(
                f"Captured {captured}/20"
            )

            box = face.bbox.astype(int)

            cv2.rectangle(
                frame,
                (box[0], box[1]),
                (box[2], box[3]),
                (0,255,0),
                2
            )

        frame_placeholder.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            channels="RGB"
        )

    cap.release()

    cv2.destroyAllWindows()

    embedding = np.mean(
        embeddings,
        axis=0
    )

    return embedding.tolist()


# =====================================================
# Face Registration Page
# =====================================================

def face_register_page():

    st.header("📷 Register Face")

    student = st.session_state.student

    st.info(
        "Look directly at the camera.\n\n"
        "20 face samples will be collected."
    )

    if st.button(
        "Start Face Registration",
        use_container_width=True
    ):

        with st.spinner("Capturing face..."):

            embedding = capture_face_embedding()

            folder = "data/faces"

            os.makedirs(
                folder,
                exist_ok=True
            )

            image_path = os.path.join(
                folder,
                f"{student['student_id']}.json"
            )

            with open(
                image_path,
                "w"
            ) as f:

                json.dump(
                    embedding,
                    f
                )

            save_face_embedding(

                student_id=student["student_id"],

                embedding=embedding,

                image_path=image_path

            )

        st.success("✅ Face Registered Successfully!")