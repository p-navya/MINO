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

        .welcome-badge {
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            padding: 6px 16px;
            border-radius: 100px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 20px;
            border: 1px solid rgba(56, 189, 248, 0.2);
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
    # Start the Hero Shell
    st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
    
    # Welcome & Title
    st.markdown("""
        <div class="welcome-badge">Welcome to the future</div>
        <h1 class="hero-title">
            Meet <span style='background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Mino</span>
        </h1>
        <p class="hero-subtitle">Your intelligent companion for the digital age.</p>
    """, unsafe_allow_html=True)

    # 3. Video Rendering - Separate from main text to avoid f-string parsing issues
    try:
        with open("my.mp4", "rb") as video_file:
            video_bytes = video_file.read()
            video_b64 = base64.b64encode(video_bytes).decode()
            
        st.markdown(f"""
            <div class="video-wrapper" style="display:flex; justify-content:center; width:100%; margin: 10px 0;">
                <video autoplay loop muted playsinline style="width:100%; max-width:420px; border-radius:18px; box-shadow:0 15px 30px rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1);">
                    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                </video>
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.write("")

    # 4. Action Button
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    # Close the Hero Shell
    st.markdown('</div>', unsafe_allow_html=True)