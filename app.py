import streamlit as st
from views import home, login, chatbot

# Page config
st.set_page_config(
    page_title="Mino",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# Persistent Global Theme and No-Scroll logic
st.markdown("""
    <style>
    header { visibility: hidden; }
    footer { visibility: hidden; }
    div[data-testid="stSidebarNav"] { display: none !important; }
    
    /* Global theme background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460) !important;
    }
    
    /* Allow scrolling but hide scrollbar for clean UI */
    [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stSidebar"] {
        overflow-y: auto !important;
        scrollbar-width: none; /* Firefox */
        -ms-overflow-style: none; /* IE/Edge */
    }
    
    [data-testid="stAppViewContainer"]::-webkit-scrollbar, 
    [data-testid="stMain"]::-webkit-scrollbar,
    [data-testid="stSidebar"]::-webkit-scrollbar {
        display: none; /* Chrome, Safari, Opera */
    }
    
    .block-container {
        padding: 0 !important;
    }
    
    /* Ensure images dont flicker to full size before CSS loads */
    img {
        max-width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    # Basic persistence check using query params
    query_user = st.query_params.get("user")
    if query_user:
        st.session_state.page = "chatbot"
        st.session_state.logged_in = True
        st.session_state.username = query_user
        st.session_state.user_id = query_user
        # Note: In a real app, you'd verify a secure token here
    else:
        st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Page routing
if st.session_state.page == "home":
    home.show()
elif st.session_state.page == "login":
    login.show()
elif st.session_state.page == "chatbot":
    chatbot.show() 