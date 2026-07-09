import streamlit as st


def home_screen():

    st.title("🎓 AI Smart Attendance System")

    st.write("---")

    col1, col2 = st.columns([2,1])

    with col1:

        st.header("Welcome")

        st.write("""
        AI Attendance System using

        ✔ Face Recognition

        ✔ Voice Recognition

        ✔ QR Attendance

        ✔ Supabase Database

        ✔ Streamlit
        """)

        st.success("Secure • Fast • Intelligent")

    with col2:

        st.image(
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
            use_container_width=True
        )