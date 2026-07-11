from src.attendance.face.face_embedding import (
    compare_embedding
)


# =====================================================
# Find Best Matching Student
# =====================================================

def find_best_match(
    unknown_embedding,
    known_embeddings,
    threshold=0.65
):

    best_student = None

    best_similarity = -1

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

    if best_similarity >= threshold:

        return {

            "student_id":
            best_student["student_id"],

            "confidence":
            round(best_similarity, 4)

        }

    return None