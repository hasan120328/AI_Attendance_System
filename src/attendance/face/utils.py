import cv2
import numpy as np
import time


# ==========================================================
# Camera
# ==========================================================

def open_camera(camera_id=0):
    """
    Open webcam.

    Returns
    -------
    cv2.VideoCapture
    """

    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        raise RuntimeError(
            "Unable to open webcam."
        )

    return cap


# ==========================================================
# Close Camera
# ==========================================================

def close_camera(cap):
    """
    Release webcam safely.
    """

    if cap is not None:
        cap.release()

    cv2.destroyAllWindows()


# ==========================================================
# Convert BGR -> RGB
# ==========================================================

def to_rgb(frame):

    return cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


# ==========================================================
# Draw Face Box
# ==========================================================

def draw_face_box(
    frame,
    bbox,
    color=(0, 255, 0),
    thickness=2
):
    """
    Draw rectangle around detected face.

    bbox:
    [x1,y1,x2,y2]
    """

    x1, y1, x2, y2 = map(int, bbox)

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        thickness
    )

    return frame


# ==========================================================
# Draw Text
# ==========================================================

def draw_text(
    frame,
    text,
    x=20,
    y=30,
    color=(0, 255, 0)
):

    cv2.putText(

        frame,

        text,

        (x, y),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        color,

        2,

        cv2.LINE_AA

    )

    return frame


# ==========================================================
# FPS Counter
# ==========================================================

class FPS:

    def __init__(self):

        self.start = time.time()
        self.frames = 0

    def update(self):

        self.frames += 1

    def get(self):

        elapsed = time.time() - self.start

        if elapsed == 0:
            return 0

        return self.frames / elapsed


# ==========================================================
# Normalize Embedding
# ==========================================================

def normalize_embedding(embedding):
    """
    Normalize embedding vector.
    """

    emb = np.array(
        embedding,
        dtype=np.float32
    )

    norm = np.linalg.norm(emb)

    if norm == 0:
        return emb.tolist()

    emb = emb / norm

    return emb.tolist()


# ==========================================================
# Cosine Similarity
# ==========================================================

def cosine_similarity(
    embedding1,
    embedding2
):
    """
    Cosine similarity between
    two embeddings.
    """

    emb1 = np.array(
        embedding1,
        dtype=np.float32
    )

    emb2 = np.array(
        embedding2,
        dtype=np.float32
    )

    emb1 = emb1 / np.linalg.norm(emb1)
    emb2 = emb2 / np.linalg.norm(emb2)

    similarity = np.dot(
        emb1,
        emb2
    )

    return float(similarity)


# ==========================================================
# Resize Image
# ==========================================================

def resize_frame(
    frame,
    width=640
):

    h, w = frame.shape[:2]

    ratio = width / w

    new_height = int(h * ratio)

    return cv2.resize(
        frame,
        (width, new_height)
    )


# ==========================================================
# Check Lighting
# ==========================================================

def is_good_lighting(
    frame,
    threshold=60
):
    """
    Check image brightness.
    """

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    brightness = np.mean(gray)

    return brightness >= threshold


# ==========================================================
# Check Blur
# ==========================================================

def is_not_blurry(
    frame,
    threshold=100
):
    """
    Blur detection using
    Laplacian variance.
    """

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    return score >= threshold


# ==========================================================
# Frame Quality
# ==========================================================

def frame_is_valid(frame):
    """
    Verify frame quality before
    extracting embedding.
    """

    if not is_good_lighting(frame):
        return False

    if not is_not_blurry(frame):
        return False

    return True