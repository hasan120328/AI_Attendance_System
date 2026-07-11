import cv2
import streamlit as st

from insightface.app import FaceAnalysis

# =====================================================
# Load InsightFace
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
# Estimate Head Direction
# =====================================================

def get_head_direction(face, frame_width):

    center_x = (face.bbox[0] + face.bbox[2]) / 2

    if center_x < frame_width * 0.35:
        return "LEFT"

    elif center_x > frame_width * 0.65:
        return "RIGHT"

    else:
        return "CENTER"


# =====================================================
# Liveness Detection
# =====================================================

def perform_liveness_check():

    st.subheader("🛡 Face Liveness Detection")

    st.info(
        """
        Please follow the instructions:

        1. Turn your head LEFT

        2. Turn your head RIGHT

        3. Look back to CENTER
        """
    )


    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        st.error("Cannot open camera.")

        return False

    frame_placeholder = st.empty()

    status = st.empty()

    left_done = False
    right_done = False
    center_done = False

    while True:

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

            direction = get_head_direction(
                face,
                frame.shape[1]
            )

            if not left_done:

                status.warning("Turn LEFT")

                if direction == "LEFT":
                    left_done = True

            elif not right_done:

                status.warning("Turn RIGHT")

                if direction == "RIGHT":
                    right_done = True

            elif not center_done:

                status.warning("Look CENTER")

                if direction == "CENTER":
                    center_done = True

            if left_done and right_done and center_done:

                cap.release()

                cv2.destroyAllWindows()

                status.success("✅ Liveness Check Passed")

                return True

        elif len(faces) > 1:

            status.warning("Multiple faces detected.")

        else:

            status.warning("No face detected.")

        frame_placeholder.image(
            cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            ),
            channels="RGB"
        )

    cap.release()

    cv2.destroyAllWindows()

    return False