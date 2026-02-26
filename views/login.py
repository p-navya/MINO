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
    # 1. Page Styling
    st.markdown("""
        <style>
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        div.stButton > button {
            background: #0f172a !important;
            color: #38bdf8 !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            background: #38bdf8 !important;
            color: #0f172a !important;
        }
        </style>
    """, unsafe_allow_html=True)

    ai_image = get_image_base64()
    
    # 2. Header
    st.markdown(f"""
        <div style="text-align: center; margin: 30px 0;">
            <img src="data:image/jpeg;base64,{ai_image}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #7928CA; padding: 5px;">
            <h2 style="margin-top: 15px;">Access Mino</h2>
            <p style="color: rgba(255,255,255,0.5);">Your gateway to intelligence.</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Form Content
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        # LOGIN TAB
        with tab1:
            l_user = st.text_input("Username", key="login_u_final", placeholder="e.g. user123")
            l_pass = st.text_input("Password", type="password", key="login_p_final", placeholder="••••••••")
            if st.button("SIGN IN", type="primary", use_container_width=True, key="do_login_final"):
                if l_user and l_pass:
                    with st.spinner("Checking credentials..."):
                        success, res_data, res_id = authenticate_user(l_user, l_pass)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = l_user
                            st.session_state.user_id = res_id
                            st.session_state.page = "chatbot"
                            st.success(f"Welcome back, {l_user}!")
                            st.rerun()
                        else:
                            st.error(f"Failed: {res_data}")
                else:
                    st.warning("Please enter your username and password.")

        # SIGNUP TAB
        with tab2:
            s_user = st.text_input("New Username", key="signup_u_final", placeholder="e.g. tech_ninja")
            s_pass = st.text_input("New Password", type="password", key="signup_p_final", placeholder="••••••••")
            if st.button("CREATE ACCOUNT", type="primary", use_container_width=True, key="do_signup_final"):
                if s_user and s_pass:
                    with st.spinner("Creating your persona..."):
                        success, res = create_user(s_user, s_pass)
                        if success:
                            st.success("Account created successfully! Please switch to the Login tab.")
                        else:
                            st.error(res)
                else:
                    st.warning("Please provide a username and password.")
        
        # Navigation
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="btn_goback_final", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    # 4. Deep Connection Diagnostics
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("🛠 SYSTEM CONNECTION DIAGNOSTICS"):
        from firebase_config import get_connection_status, SERVICE_ACCOUNT_PATH
        mode, error = get_connection_status()
        
        st.write(f"**Connection Mode:** `{mode}`")
        st.write(f"**Config Path:** `{SERVICE_ACCOUNT_PATH}`")
        
        if error:
            st.error(f"❌ Connection Error: {error}")
            st.markdown("""
                ### How to Fix your Connection:
                1. **If you are on Streamlit Cloud:**
                   - Go to **Settings** -> **Secrets**.
                   - Paste your Firebase Service Account JSON content Into a field named `firebase`.
                2. **If you are Running Locally:**
                   - Ensure the file `mino-e81f4-firebase-adminsdk-fbsvc-cea5b4030a.json` is sitting in your root directory.
            """)
        else:
            st.success("✅ Database Status: Online and Connected")
            st.info("You can now safely login or sign up.")