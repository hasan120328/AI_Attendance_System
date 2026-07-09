import streamlit as st
from src.database.config import supabase
from src.dashboard.teacher_dashboard import teacher_dashboard
from src.teacher.create_subject import create_subject_page

from src.database.db import (
    teacher_exists,
    create_teacher,
    teacher_login,
    create_subject,
    get_teacher_subjects,
    create_attendance,
    get_teacher_attendance
)


def teacher_screen():


    # -----------------------------
    # Session State
    # -----------------------------
    if "teacher_logged_in" not in st.session_state:
        st.session_state.teacher_logged_in = False

    if "teacher" not in st.session_state:
        st.session_state.teacher = None
        
    if st.session_state.teacher_logged_in:

        teacher_dashboard()

        return

    # -----------------------------
    # Title
    # -----------------------------
    st.title("👨‍🏫 Teacher Portal")

    # -----------------------------
    # Tabs
    # -----------------------------
    login_tab, register_tab = st.tabs(["Login", "Register"])

    # =====================================================
    # LOGIN
    # =====================================================
    with login_tab:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", key="login_button"):

            if username == "" or password == "":
                st.error("Please enter username and password.")

            else:

                teacher = teacher_login(username, password)

                if teacher:

                    st.session_state.teacher_logged_in = True
                    st.session_state.teacher = teacher

                    st.session_state.teacher_logged_in = True
                    st.session_state.teacher = teacher

                    st.rerun()

                else:

                    st.error("Invalid username or password.")

    # =====================================================
    # REGISTER
    # =====================================================
    with register_tab:
        
        if "register_success" not in st.session_state:
            st.session_state.register_success = False

        if st.session_state.register_success:
            st.success("✅ Account created successfully!")
            st.toast("Teacher registered successfully 🎉")
            st.balloons()

            st.session_state.register_success = False

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        phone = st.text_input(
            "Phone",
            key="register_phone"
        )

        username = st.text_input(
            "Username",
            key="register_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )

        if st.button("Create Account", key="register_button"):

            if (
                name == ""
                or email == ""
                or username == ""
                or password == ""
            ):
                st.error("All fields are required.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            elif teacher_exists(username):
                st.error("Username already exists.")

            else:

                create_teacher(
                    full_name=name,
                    email=email,
                    username=username,
                    password=password,
                    phone=phone
                )

                st.success("Account created successfully!")

                st.toast("Teacher registered successfully 🎉")