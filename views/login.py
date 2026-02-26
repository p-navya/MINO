import streamlit as st
from db_config import create_user, authenticate_user
import base64
from PIL import Image
import io

def get_image_base64():
    with open("ai.jpg", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def convert_image_to_base64(image):
    # Convert PIL Image to base64 string
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def show():
    # Login-specific styling
    st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem !important;
        }
        
        /* Premium Blue-Black Buttons */
        div.stButton > button {
            background: #0f172a !important;
            color: #38bdf8 !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            background: #38bdf8 !important;
            color: #0f172a !important;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important;
        }
        
        /* Style forms and tabs to match */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Get AI image
    ai_image = get_image_base64()
    
    # Hero Header
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem; margin-top: 1rem;">
            <img src="data:image/jpeg;base64,{ai_image}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #7928CA; padding: 5px; margin-bottom: 0.5rem; box-shadow: 0 0 15px rgba(121, 40, 202, 0.4);">
            <h1 style="color: white; font-weight: 800; font-size: 2.2rem; margin-bottom: 0;">Access <span style="background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Mino</span></h1>
            <p style="margin: 0; color: rgba(255,255,255,0.5); font-size: 0.9rem;">Join our community of future-thinkers.</p>
        </div>
    """, unsafe_allow_html=True)

    # Centered container for the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Create tabs for login and signup with custom style via container
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        # Login tab
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                login_username = st.text_input("Username", placeholder="Enter your username")
                login_password = st.text_input("Password", type="password", placeholder="••••••••")
                
                # Profile picture upload
                uploaded_file = st.file_uploader("Set Profile Picture (optional)", type=['jpg', 'jpeg', 'png'], key="login_uploader")
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    image.thumbnail((150, 150))
                    st.image(image, width=80)
                    st.session_state.temp_profile_image = convert_image_to_base64(image)
                
                login_submit = st.form_submit_button("Sign In")
                
                if login_submit:
                    if not login_username or not login_password:
                        st.error("Missing credentials")
                    else:
                        success, user_data, user_id = authenticate_user(login_username, login_password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.session_state.user_id = user_id
                            st.query_params["user"] = login_username
                            if 'temp_profile_image' in st.session_state:
                                st.session_state.user_profile_image = st.session_state.temp_profile_image
                            elif user_data and 'profile_image' in user_data:
                                st.session_state.user_profile_image = user_data['profile_image']
                            st.success("Welcome back!")
                            st.session_state.page = "chatbot"
                            st.rerun()
                        else:
                            st.error("Invalid credentials")

        # Signup tab
        with tab2:
            with st.form("signup_form", clear_on_submit=False):
                signup_username = st.text_input("Choose Username", placeholder="e.g. tech_ninja")
                signup_password = st.text_input("Choose Password", type="password", placeholder="••••••••")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                
                uploaded_file = st.file_uploader("Profile Picture", type=['jpg', 'jpeg', 'png'], key="signup_uploader")
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    image.thumbnail((150, 150))
                    st.image(image, width=80)
                    st.session_state.temp_profile_image = convert_image_to_base64(image)
                
                signup_submit = st.form_submit_button("Create Account")
                
                if signup_submit:
                    if not signup_username or not signup_password or not confirm_password:
                        st.error("Please fill all fields")
                    elif signup_password != confirm_password:
                        st.error("Passwords mismatch")
                    else:
                        profile_image = st.session_state.get('temp_profile_image')
                        success, result = create_user(signup_username, signup_password, profile_image)
                        if success:
                            st.success("Ready! You can now login.")
                        else:
                            st.error(result)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Center the back button
        st.markdown('<div style="margin-top: 1rem; text-align: center;">', unsafe_allow_html=True)
        if st.button("Cancel & Return"):
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True) 