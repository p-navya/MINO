import streamlit as st
import base64

def show():
    # Home-specific Styling
    st.markdown("""
        <style>
        /* Fix the hero container to the viewport */
        .hero-shell {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 90vh;
            width: 85vw;
            text-align: center;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 40px;
            padding: 2rem;
            color: white;
            z-index: 100;
        }
        
        .hero-title {
            font-size: 4.5rem;
            font-weight: 900;
            margin: 0;
            line-height: 1;
            letter-spacing: -2px;
        }
        
        .hero-subtitle {
            color: rgba(255,255,255,0.6);
            font-size: 1.3rem;
            margin-top: 15px;
            margin-bottom: 30px;
        }
        
        .video-wrapper video {
            width: 500px;
            max-width: 80%;
            border-radius: 24px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* Prevent Streamlit from adding extra padding */
        .block-container {
            padding: 0 !important;
        }
        
        /* Premium Blue-Black Buttons */
        div.stButton > button {
            background: #0f172a !important;
            color: #38bdf8 !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            background: #38bdf8 !important;
            color: #0f172a !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
            border-color: #38bdf8 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Main Hero UI
    st.markdown("""
        <div style="text-align: center; margin-top: 5vh;">
            <h1 class="hero-title">
                Meet <span style='background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Mino</span>
            </h1>
            <p class="hero-subtitle">Your intelligent companion for the digital age.</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Video Rendering (Safe Base64 embed)
    try:
        with open("my.mp4", "rb") as video_file:
            video_bytes = video_file.read()
            video_b64 = base64.b64encode(video_bytes).decode()
            
        st.markdown(f"""
            <div class="video-wrapper" style="width: 100%; display: flex; justify-content: center; margin-bottom: 30px;">
                <video autoplay loop muted playsinline>
                    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                </video>
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Preview video (my.mp4) not found.")

    # 4. Action Button
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col1: st.write("") # Spacer
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    with col3: st.write("") # Spacer
    
    