import streamlit as st
from src.database.config import supabase
from src.database.db import (
    student_exists,
    create_student,
    student_login
)

from src.dashboard.student_dashboard import student_dashboard


def student_screen():
    if "clear_student_form" not in st.session_state:
       st.session_state.clear_student_form = False

    if st.session_state.clear_student_form:
        st.session_state["student_number"] = ""
        st.session_state["student_fullname"] = ""
        st.session_state["student_email"] = ""
        st.session_state["student_department"] = ""
        st.session_state["student_semester"] = ""
        st.session_state["student_username"] = ""
        st.session_state["student_password"] = ""
        st.session_state["student_confirm"] = ""

        st.session_state.clear_student_form = False
    # ==========================================
    # Session State
    # ==========================================

    if "student_logged_in" not in st.session_state:
        st.session_state.student_logged_in = False

    if "student" not in st.session_state:
        st.session_state.student = None

    # ==========================================
    # If Logged In → Dashboard
    # ==========================================

    if st.session_state.student_logged_in:

        student_dashboard()
        return

    # ==========================================
    # Login / Register
    # ==========================================

    st.title("🎓 Student Portal")

    login_tab, register_tab = st.tabs(
        ["🔑 Login", "📝 Register"]
    )

    # ==========================================
    # LOGIN
    # ==========================================

    with login_tab:

        st.subheader("Student Login")

        username = st.text_input(
            "Username",
            key="student_login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="student_login_password"
        )

        if st.button(
            "Login",
            key="student_login_btn",
            use_container_width=True
        ):

            if username == "" or password == "":

                st.error("Please enter username and password.")

            else:

                student = student_login(username, password)

                if student:

                    st.session_state.student_logged_in = True
                    st.session_state.student = student

                    st.toast("Login Successful 🎉")

                    st.rerun()

                else:

                    st.error("Invalid username or password.")
        else:
            st.info("Please enter your credentials to log in.")

    # ==========================================
    # REGISTER
    # ==========================================

    with register_tab:

        st.subheader("Student Registration")

        student_number = st.text_input(
            "Student ID",
            key="student_number"
        )

        fullname = st.text_input(
            "Full Name",
            key="student_fullname"
        )

        email = st.text_input(
            "Email",
            key="student_email"
        )

        department = st.text_input(
            "Department",
            key="student_department"
        )

        semester = st.text_input(
            "Semester",
            key="student_semester"
        )

        username = st.text_input(
            "Username",
            key="student_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="student_password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="student_confirm"
        )

        if st.button(
            "Create Account",
            key="student_register_btn",
            use_container_width=True
        ):

            if (
                student_number == ""
                or fullname == ""
                or email == ""
                or department == ""
                or semester == ""
                or username == ""
                or password == ""
            ):

                st.error("Please fill all fields.")

            elif password != confirm:

                st.error("Passwords do not match.")

            elif student_exists(username):

                st.error("Username already exists.")

            else:

                create_student(
                    student_number=student_number,
                    full_name=fullname,
                    email=email,
                    username=username,
                    password=password,
                    department=department,
                    semester=semester
                )

                st.toast("Registration Successful 🎉")

                st.toast("Registration Successful 🎉")

                st.session_state.clear_student_form = True

                st.rerun()

               