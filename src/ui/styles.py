import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* ==========================
        Main App
    ===========================*/

    .stApp{
        background-color:#F5F7FA;
    }

    .main .block-container{
        padding-top:2rem;
        padding-left:2rem;
        padding-right:2rem;
        padding-bottom:2rem;
    }

    /* ==========================
        Sidebar
    ===========================*/

    section[data-testid="stSidebar"]{
        background:#0F172A;
        color:white;
    }

    section[data-testid="stSidebar"] *{
        color:white;
    }

    /* ==========================
        Headers
    ===========================*/

    h1{
        color:#0F172A;
        font-weight:700;
    }

    h2{
        color:#1E293B;
    }

    h3{
        color:#334155;
    }

    /* ==========================
        Buttons
    ===========================*/

    .stButton>button{

        width:100%;

        background:#2563EB;

        color:white;

        border:none;

        border-radius:12px;

        height:50px;

        font-size:16px;

        font-weight:600;

        transition:0.3s;

    }

    .stButton>button:hover{

        background:#1D4ED8;

        color:white;

    }

    /* ==========================
        Text Input
    ===========================*/

    .stTextInput input{

        border-radius:12px;

        border:1px solid #CBD5E1;

        height:45px;

    }

    /* ==========================
        Selectbox
    ===========================*/

    .stSelectbox div[data-baseweb="select"]{

        border-radius:12px;

    }

    /* ==========================
        Metric Card
    ===========================*/

    div[data-testid="metric-container"]{

        background:white;

        border-radius:15px;

        padding:15px;

        box-shadow:0 3px 8px rgba(0,0,0,.08);

        border:1px solid #E2E8F0;

    }

    /* ==========================
        DataFrame
    ===========================*/

    div[data-testid="stDataFrame"]{

        border-radius:15px;

        border:1px solid #E2E8F0;

    }

    /* ==========================
        Tabs
    ===========================*/

    button[data-baseweb="tab"]{

        font-size:16px;

        font-weight:600;

    }

    /* ==========================
        Success
    ===========================*/

    div[data-testid="stAlert"]{

        border-radius:12px;

    }

    /* ==========================
        Cards
    ===========================*/

    .card{

        background:white;

        padding:25px;

        border-radius:15px;

        box-shadow:0px 3px 10px rgba(0,0,0,.08);

        margin-bottom:20px;

    }

    /* ==========================
        Footer
    ===========================*/

    footer{

        visibility:hidden;

    }

    # header{

    #     visibility:hidden;

    # }

    </style>
    """, unsafe_allow_html=True)