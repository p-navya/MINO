import streamlit as st
from db_config import create_user, authenticate_user
import base64
from PIL import Image
import io

def get_image_base64():
    try:
        with open("ai.jpg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except: return ""

def convert_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def show():
    st.markdown("""
        <style>
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        div.stButton > button {
            background: #0f172a !important;
            color: #38bdf8 !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    ai_image = get_image_base64()
    
    st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <img src="data:image/jpeg;base64,{ai_image}" style="width: 70px; border-radius: 50%;">
            <h2>Access Mino</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            l_user = st.text_input("Username", key="login_u")
            l_pass = st.text_input("Password", type="password", key="login_p")
            if st.button("SIGN IN", type="primary", use_container_width=True, key="do_login"):
                if l_user and l_pass:
                    success, res_data, res_id = authenticate_user(l_user, l_pass)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = l_user
                        st.session_state.user_id = res_id
                        st.session_state.page = "chatbot"
                        st.success("Success! Redirecting...")
                        st.rerun()
                    else:
                        st.error(f"Error: {res_data}")
                else:
                    st.warning("Fill all fields")

        with tab2:
            s_user = st.text_input("New Username", key="signup_u")
            s_pass = st.text_input("New Password", type="password", key="signup_p")
            if st.button("CREATE ACCOUNT", type="primary", use_container_width=True, key="do_signup"):
                if s_user and s_pass:
                    success, res = create_user(s_user, s_pass)
                    if success:
                        st.success("Account created! Now login.")
                    else:
                        st.error(res)
                else:
                    st.warning("Fill all fields")
        
        if st.button("← Back", key="btn_goback"):
            st.session_state.page = "home"
            st.rerun()

    # Debug Section
    with st.expander("🛠 System Connection Diagnostics"):
        st.write(f"Page State: `{st.session_state.get('page')}`")
        from firebase_config import get_connection_status
        mode, error = get_connection_status()
        st.write(f"Connection Mode: **{mode}**")
        if error:
            st.error(f"Last Connection Error: {error}")
        else:
            st.success("✅ Firebase connection status: Connected")