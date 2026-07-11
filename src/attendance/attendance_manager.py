from datetime import datetime

from src.database.db import (
    get_active_session,
    attendance_exists,
    save_attendance
)


# ==========================================================
# Mark Student Attendance
# ==========================================================

def mark_face_attendance(
    student_id,
    confidence
):
    """
    Mark attendance after successful face verification.

    Returns
    -------
    dict

    Example
    -------
    {
        "success": True,
        "message": "...",
        "session": {...}
    }
    """

    # ------------------------------------------------------
    # Find Active Session
    # ------------------------------------------------------

    session = get_active_session()

    if session is None:

        return {

            "success": False,

            "message":
            "No active attendance session."

        }

    # ------------------------------------------------------
    # Check Duplicate Attendance
    # ------------------------------------------------------

    exists = attendance_exists(

        student_id=student_id,

        session_id=session["session_id"]

    )

    if exists:

        return {

            "success": False,

            "message":
            "Attendance already submitted."

        }

    # ------------------------------------------------------
    # Save Attendance
    # ------------------------------------------------------

    save_attendance(

        student_id=student_id,

        subject_id=session["subject_id"],

        session_id=session["session_id"],

        attendance_date=datetime.now().date(),

        method="Face",

        confidence=confidence

    )

    return {

        "success": True,

        "message":
        "Attendance marked successfully.",

        "session": session

    }