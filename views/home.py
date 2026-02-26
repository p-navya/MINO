import streamlit as st
import base64
import os

def show():
    # 1. Home-specific Styling (Premium Dark Theme)
    st.markdown("""
        <style>
        .hero-shell {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 32px;
            padding: 40px;
            max-width: 700px;
            margin: 5vh auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 40px 100px rgba(0,0,0,0.4);
            text-align: center;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 900;
            margin: 0;
            line-height: 1.1;
            letter-spacing: -2px;
        }
        
        .hero-subtitle {
            color: rgba(255,255,255,0.6);
            font-size: 1.1rem;
            margin-top: 15px;
            margin-bottom: 30px;
        }

        /* Essential: Hide Streamlit's default video controls for a clean background-video look */
        [data-testid="stVideo"] {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Premium Blue-Black Buttons */
        div.stButton > button {
            background: #0f172a !important;
            color: #38bdf8 !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 12px !important;
            padding: 12px 32px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            margin-top: 20px;
        }
        div.stButton > button:hover {
            background: #38bdf8 !important;
            color: #0f172a !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Main Hero Container
    with st.container():
        # Open the shell div
        st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
        
        # Header text
        st.markdown("""
            <h1 class="hero-title">
                Meet <span style='background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Mino</span>
            </h1>
            <p class="hero-subtitle">Your intelligent companion for the digital age.</p>
        """, unsafe_allow_html=True)

        # 3. Stable Video Rendering (Using st.video to prevent "raw code" leak)
        video_path = "my.mp4"
        if os.path.exists(video_path):
            # st.video is much more stable than embedding base64 in markdown
            # This prevents the raw string from leaking onto your screen
            st.video(video_path, autoplay=True, loop=True, muted=True)
        
        # 4. Action Button
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            if st.button("Get Started", type="primary", use_container_width=True, key="home_start_final"):
                st.session_state.page = "login"
                st.rerun()

        # Close the shell div
        st.markdown('</div>', unsafe_allow_html=True)