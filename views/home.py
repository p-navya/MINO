import streamlit as st
import base64

def show():
    # Home-specific Styling
    st.markdown("""
        <style>
        .hero-shell {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 32px;
            padding: 40px;
            max-width: 800px;
            margin: 5vh auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 40px 100px rgba(0,0,0,0.4);
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 900;
            margin: 0;
            line-height: 1.1;
            letter-spacing: -2px;
            text-align: center;
        }
        
        .hero-subtitle {
            color: rgba(255,255,255,0.6);
            font-size: 1.1rem;
            margin-top: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .video-wrapper video {
            width: 100%;
            max-width: 450px;
            border-radius: 20px;
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
            margin-top: 30px;
        }
        div.stButton > button:hover {
            background: #38bdf8 !important;
            color: #0f172a !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Main Hero UI
    video_html = ""
    try:
        with open("my.mp4", "rb") as video_file:
            video_bytes = video_file.read()
            video_b64 = base64.b64encode(video_bytes).decode()
        # Use a simpler data-uri injection to prevent raw text glitch
        video_html = f'''
            <div class="video-container" style="display: flex; justify-content: center; width: 100%; margin: 15px 0;">
                <video autoplay loop muted playsinline style="width: 100%; max-width: 440px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);">
                    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                </video>
            </div>
        '''
    except FileNotFoundError:
        video_html = '<div style="height: 10px;"></div>'

    # Single-block rendering to ensure everything stays INSIDE the shell
    st.markdown(f'''
        <div class="hero-shell">
            <div style="text-align: center; margin-bottom: 30px;">
                <p style="color: #38bdf8; font-weight: 700; font-size: 0.85rem; letter-spacing: 2px; margin-bottom: 10px; opacity: 0.8;">WELCOME TO THE FUTURE</p>
                <h1 class="hero-title">
                    Meet <span style="background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Mino</span>
                </h1>
                <p class="hero-subtitle">Your intelligent companion for the digital age.</p>
                {video_html}
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 3. Action Button - Positioned to look like it's part of the shell footer
    st.markdown('<div style="margin-top: -60px;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)