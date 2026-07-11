from src.database.config import supabase
import bcrypt

# =====================================================
# PASSWORD
# =====================================================

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

# =====================================================
# TEACHER
# =====================================================

def teacher_exists(username):

    response = (
        supabase
        .table("teachers")
        .select("teacher_id")
        .eq("username", username)
        .execute()
    )

    return len(response.data) > 0


def create_teacher(full_name, email, username, password, phone=None):

    data = {

        "full_name": full_name,
        "email": email,
        "username": username,
        "password": hash_password(password),
        "phone": phone

    }

    response = (
        supabase
        .table("teachers")
        .insert(data)
        .execute()
    )

    return response.data


def teacher_login(username, password):

    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if response.data:

        teacher = response.data[0]

        if verify_password(password, teacher["password"]):
            return teacher

    return None

# =====================================================
# STUDENT
# =====================================================

def student_exists(username):

    response = (
        supabase
        .table("students")
        .select("student_id")
        .eq("username", username)
        .execute()
    )

    return len(response.data) > 0


def create_student(

    student_number,
    full_name,
    email,
    username,
    password,
    department,
    semester

):

    data = {

        "student_number": student_number,
        "full_name": full_name,
        "email": email,
        "username": username,
        "password": hash_password(password),
        "department": department,
        "semester": semester

    }

    response = (
        supabase
        .table("students")
        .insert(data)
        .execute()
    )

    return response.data


def student_login(username, password):

    response = (
        supabase
        .table("students")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if response.data:

        student = response.data[0]

        if verify_password(password, student["password"]):
            return student

    return None

## it will check before enroll_subject , if student is already enrolled or not
def is_student_enrolled(student_id, subject_id):

    response = (
        supabase
        .table("subject_students")
        .select("id")
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )

    return len(response.data) > 0




# =====================================================
# SUBJECT
# =====================================================

def create_subject(

    subject_code,
    subject_name,
    section,
    semester,
    teacher_id

):

    data = {

        "subject_code": subject_code,
        "subject_name": subject_name,
        "section": section,
        "semester": semester,
        "teacher_id": teacher_id

    }

    response = (
        supabase
        .table("subjects")
        .insert(data)
        .execute()
    )

    return response.data




def get_teacher_subjects(teacher_id):

    response = (
        supabase
        .table("subjects")
        .select("*")
        .eq("teacher_id", teacher_id)
        .execute()
    )

    return response.data


def get_all_subjects():

    response = (
        supabase
        .table("subjects")
        .select("*")
        .execute()
    )

    return response.data

# =====================================================
# ENROLLMENT
# =====================================================

def enroll_student(student_id, subject_id):

    data = {

        "student_id": student_id,
        "subject_id": subject_id

    }

    response = (
        supabase
        .table("subject_students")
        .insert(data)
        .execute()
    )

    return response.data
# =====================================================
## to get student id 
# =====================================================
def get_student(student_id):

    response = (
        supabase
        .table("students")
        .select("*")
        .eq("student_id", student_id)
        .single()
        .execute()
    )

    return response.data
# =====================================================
# REGISTERED STUDENTS FOR TEACHER
# =====================================================

def get_registered_students(teacher_id):

    response = (
        supabase
        .table("subject_students")
        .select("""
            student_id,
            students(
                student_number,
                full_name,
                email,
                department,
                semester
            ),
            subjects!inner(
                subject_id,
                subject_code,
                subject_name,
                section,
                teacher_id
            )
        """)
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )

    return response.data

def unenroll_student(student_id, subject_id):

    response = (
        supabase
        .table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data


def get_student_subjects(student_id):

    response = (
        supabase
        .table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )

    return response.data


# =====================================================
# FACE EMBEDDING EXISTS
# =====================================================

def face_exists(student_id):

    response = (
        supabase
        .table("face_embeddings")
        .select("student_id")
        .eq("student_id", student_id)
        .execute()
    )

    return len(response.data) > 0
# =====================================================
# FACE EMBEDDINGS
# =====================================================
def save_face_embedding(

    student_id,
    embedding,
    image_path

):

    data = {

        "student_id": student_id,
        "embedding": embedding,
        "image_path": image_path

    }

    # ---------------------------------------
    # Student already registered
    # ---------------------------------------

    if face_exists(student_id):

        response = (
            supabase
            .table("face_embeddings")
            .update(data)
            .eq("student_id", student_id)
            .execute()
        )

    # ---------------------------------------
    # First registration
    # ---------------------------------------

    else:

        response = (
            supabase
            .table("face_embeddings")
            .insert(data)
            .execute()
        )

    return response.data


def get_face_embeddings():

    response = (
        supabase
        .table("face_embeddings")
        .select("*")
        .execute()
    )

    return response.data

## if face exists 
def face_exists(student_id):

    response = (
        supabase
        .table("face_embeddings")
        .select("student_id")
        .eq("student_id", student_id)
        .execute()
    )

    return len(response.data) > 0
# =====================================================
## for active session 
# =====================================================
def get_active_session():

    response = (

        supabase

        .table("attendance_sessions")

        .select("*")

        .eq("is_active", True)

        .limit(1)

        .execute()

    )

    if len(response.data) == 0:
        return None

    return response.data[0]

# =====================================================
## attendance_exists
# =====================================================
def attendance_exists(
    student_id,
    session_id
):

    response = (

        supabase

        .table("attendance")

        .select("attendance_id")

        .eq("student_id", student_id)

        .eq("session_id", session_id)

        .execute()

    )

    return len(response.data) > 0

# =====================================================
## save_attendance
# =====================================================
def save_attendance(
    student_id,
    subject_id,
    session_id,
    attendance_date,
    method,
    confidence
):

    data = {

        "student_id": student_id,

        "subject_id": subject_id,

        "session_id": session_id,

        "attendance_date": str(attendance_date),

        "method": method,

        "confidence": confidence

    }

    return (

        supabase

        .table("attendance")

        .insert(data)

        .execute()

    )


# =====================================================
# VOICE EMBEDDINGS
# =====================================================

def save_voice_embedding(

    student_id,
    embedding,
    audio_path

):

    data = {

        "student_id": student_id,
        "embedding": embedding,
        "audio_path": audio_path

    }

    response = (
        supabase
        .table("voice_embeddings")
        .insert(data)
        .execute()
    )

    return response.data


def get_voice_embeddings():

    response = (
        supabase
        .table("voice_embeddings")
        .select("*")
        .execute()
    )

    return response.data

# =====================================================
# ATTENDANCE
# =====================================================

def create_attendance(

    session_id,
    student_id,
    subject_id,
    method,
    confidence

):

    data = {

        "session_id": session_id,
        "student_id": student_id,
        "subject_id": subject_id,
        "attendance_date": None,
        "method": method,
        "confidence": confidence

    }

    response = (
        supabase
        .table("attendance_logs")
        .insert(data)
        .execute()
    )

    return response.data


def get_student_attendance(student_id):

    response = (
        supabase
        .table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )

    return response.data


def get_teacher_attendance(teacher_id):

    response = (
        supabase
        .table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )

    return response.data

# =====================================================
# DASHBOARD
# =====================================================

def total_students():

    return len(
        supabase
        .table("students")
        .select("student_id")
        .execute()
        .data
    )


def total_teachers():

    return len(
        supabase
        .table("teachers")
        .select("teacher_id")
        .execute()
        .data
    )


def total_subjects():

    return len(
        supabase
        .table("subjects")
        .select("subject_id")
        .execute()
        .data
    )
    
    
def update_subject(
    subject_id,
    subject_code,
    subject_name,
    section,
    semester
):

    response = (
        supabase
        .table("subjects")
        .update(
            {
                "subject_code": subject_code,
                "subject_name": subject_name,
                "section": section,
                "semester": semester
            }
        )
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data

def delete_subject(subject_id):

    response = (
        supabase
        .table("subjects")
        .delete()
        .eq("subject_id", subject_id)
        .execute()
    )

    return response.data

def count_students(subject_id):

    response = (
        supabase
        .table("subject_students")
        .select("student_id")
        .eq("subject_id", subject_id)
        .execute()
    )

    return len(response.data)