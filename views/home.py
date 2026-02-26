import streamlit as st
import base64

def show():
    # Home-specific Styling
    st.markdown("""
        <style>
        /* Fix the hero container to be more responsive */
        .hero-shell {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 85vh;
            width: 90vw;
            margin: 20px auto;
            text-align: center;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 40px;
            padding: 1.5rem;
            color: white;
        }
        
        .hero-title {
            font-size: 3.8rem;
            font-weight: 900;
            margin: 0;
            line-height: 1;
            letter-spacing: -2px;
        }
        
        .hero-subtitle {
            color: rgba(255,255,255,0.6);
            font-size: 1.1rem;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        
        .video-wrapper video {
            width: 400px;
            max-width: 90%;
            max-height: 40vh;
            border-radius: 20px;
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
    st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center;">
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
        # Silently skip if video is missing to keep UI clean in production
        st.write("") 

    # 4. Action Button
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True) # Close hero-shell
    
    