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
            border-radius: 24px;
            padding: 20px 35px;
            max-width: 600px;
            margin: 3vh auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 30px 60px rgba(0,0,0,0.3);
        }
        
        .hero-title {
            font-size: 2.8rem;
            font-weight: 900;
            margin: 0;
            line-height: 1.1;
            letter-spacing: -1.5px;
            text-align: center;
        }
        
        .hero-subtitle {
            color: rgba(255,255,255,0.6);
            font-size: 1rem;
            margin-top: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .video-wrapper {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-bottom: 15px;
        }
        
        .video-wrapper video {
            width: 100%;
            max-width: 380px;
            border-radius: 16px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* Premium Blue-Black Buttons */
        div.stButton > button {
            background: #0f172a !important;
            color: #38bdf8 !important;
            border: 1px solid #38bdf8 !important;
            border-radius: 10px !important;
            padding: 10px 28px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            margin-top: 15px;
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
        video_html = f"""
            <div class="video-wrapper">
                <video autoplay loop muted playsinline>
                    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                </video>
            </div>
        """
    except FileNotFoundError:
        video_html = ""

    # Single-block rendering to ensure everything stays INSIDE the shell
    st.markdown(f'''
        <div class="hero-shell">
            <div style="text-align: center;">
                <h1 class="hero-title">
                    Meet <span style="background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Mino</span>
                </h1>
                <p class="hero-subtitle">Your intelligent companion for the digital age.</p>
                {video_html}
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 3. Action Button - Use standard Streamlit columns for maximum clickability
    # Use a container to manage vertical spacing properly
    with st.container():
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            if st.button("Get Started", type="primary", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()