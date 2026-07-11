import cv2
import numpy as np
import streamlit as st

from insightface.app import FaceAnalysis
from src.attendance.face.utils import normalize_embedding


# =====================================================
# Load ArcFace Model
# =====================================================

@st.cache_resource
def load_face_model():

    app = FaceAnalysis(
        name="buffalo_l"
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    return app


face_model = load_face_model()


# =====================================================
# Generate Face Embedding
# =====================================================

def get_face_embedding(image):
    """
    Generate a normalized ArcFace embedding.

    Parameters
    ----------
    image : numpy.ndarray (BGR)

    Returns
    -------
    list | None
    """

    faces = face_model.get(image)

    if len(faces) != 1:
        return None

    embedding = normalize_embedding(
        faces[0].embedding
    )

    return embedding.tolist()


# =====================================================
# Capture Face Embedding
# =====================================================

def capture_face_embedding(samples=20):
    """
    Capture multiple face embeddings and
    return the averaged embedding.

    Parameters
    ----------
    samples : int

    Returns
    -------
    list | None
    """

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        st.error("Unable to access webcam.")

        return None

    embeddings = []

    captured = 0

    frame_placeholder = st.empty()

    status = st.empty()

    try:

        while captured < samples:

            success, frame = cap.read()

            if not success:
                continue

            faces = face_model.get(frame)

            if len(faces) == 1:

                face = faces[0]

                box = face.bbox.astype(int)

                cv2.rectangle(

                    frame,

                    (box[0], box[1]),

                    (box[2], box[3]),

                    (0, 255, 0),

                    2

                )

                embedding = normalize_embedding(
                    face.embedding
                )

                embeddings.append(
                    embedding
                )

                captured += 1

                status.success(
                    f"Captured {captured}/{samples}"
                )

                cv2.putText(

                    frame,

                    f"{captured}/{samples}",

                    (20, 40),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    1,

                    (0, 255, 0),

                    2

                )

            elif len(faces) > 1:

                status.warning(
                    "Multiple faces detected."
                )

            else:

                status.warning(
                    "No face detected."
                )

            frame_placeholder.image(

                cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                ),

                channels="RGB"

            )

    finally:

        cap.release()

        cv2.destroyAllWindows()

    if len(embeddings) == 0:

        return None

    embedding = np.mean(
        embeddings,
        axis=0
    )

    embedding = normalize_embedding(
        embedding
    )

    return embedding


# =====================================================
# Compare Embeddings
# =====================================================

def compare_embedding(
    embedding1,
    embedding2
):
    """
    Compute cosine similarity.
    """

    emb1 = np.asarray(
        embedding1,
        dtype=np.float32
    )

    emb2 = np.asarray(
        embedding2,
        dtype=np.float32
    )

    norm1 = np.linalg.norm(emb1)

    norm2 = np.linalg.norm(emb2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    emb1 /= norm1

    emb2 /= norm2

    similarity = np.dot(
        emb1,
        emb2
    )

    return float(similarity)


# =====================================================
# Find Best Match
# =====================================================

def find_best_match(
    unknown_embedding,
    known_embeddings,
    threshold=0.70
):
    """
    Find the most similar student.

    Parameters
    ----------
    unknown_embedding : list

    known_embeddings : list

    threshold : float

    Returns
    -------
    dict | None
    """

    best_similarity = -1.0

    best_student = None

    for item in known_embeddings:

        similarity = compare_embedding(

            unknown_embedding,

            item["embedding"]

        )

        if similarity > best_similarity:

            best_similarity = similarity

            best_student = item

    if best_student is None:
        return None

    if best_similarity < threshold:
        return None

    return {

        "student_id": best_student["student_id"],

        "confidence": round(
            best_similarity,
            4
        )

    }