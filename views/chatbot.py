import streamlit as st
from transformers import pipeline
from datetime import datetime
import os
import base64
import pyttsx3
import threading
import pygame
import time
import hashlib
from db_config import save_chat, get_user_chats, delete_chat, rename_chat
from textwrap import dedent
from html import escape

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize pygame mixer
try:
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.set_num_channels(1)
except Exception as e:
    st.error(f"Error initializing audio system: {str(e)}")

def get_image_base64():
    with open("ai.jpg", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def speak_text(text):
    def speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            del engine
        except Exception as e:
            st.error(f"Error in text-to-speech: {str(e)}")
    
    thread = threading.Thread(target=speak)
    thread.daemon = True
    thread.start()

def show():
    if not st.session_state.get("logged_in", False):
        st.session_state.page = "login"
        st.rerun()

    if "chats" not in st.session_state:
        user_id = st.session_state.get("user_id")
        if user_id:
            st.session_state.chats = get_user_chats(user_id)
            if not st.session_state.chats:
                st.session_state.chats = {"Chat 1": []}
        else:
            st.session_state.chats = {"Chat 1": []}
    
    # Ensure current_chat is valid
    if "current_chat" not in st.session_state or st.session_state.current_chat not in st.session_state.chats:
        if st.session_state.chats:
            st.session_state.current_chat = list(st.session_state.chats.keys())[0]
        else:
            st.session_state.chats = {"Chat 1": []}
            st.session_state.current_chat = "Chat 1"
    
    st.session_state.messages = st.session_state.chats[st.session_state.current_chat]

    @st.cache_resource
    def load_model():
        return pipeline("text2text-generation", model="facebook/blenderbot-400M-distill", framework="pt")

    ai_image = get_image_base64()
    user_image = st.session_state.get("user_profile_image", None)

    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1) !important;
        width: 300px !important;
    }
    .logo-text {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: white;
    }
    .chat-message {
        margin: 2rem 0;
        display: flex;
        gap: 20px;
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
        animation: slideUp 0.4s ease-out;
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message { flex-direction: row-reverse; }
    .message-content {
        color: #e0e0e0;
        font-size: 1.05rem;
        line-height: 1.6;
        padding: 5px 0;
    }
    .user-message .message-content {
        background: #1e1e1e;
        padding: 15px 20px;
        border-radius: 15px;
        border-bottom-right-radius: 4px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .avatar-img {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        object-fit: cover;
    }
    .assistant-avatar {
        background: linear-gradient(135deg, #FF0080 0%, #7928CA 100%);
        padding: 2px;
    }
    .profile-card {
        background: #1a1a1a;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        position: fixed;
        top: 70px;
        right: 40px;
        z-index: 1000;
        width: 280px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }
    /* Fixed height for chat area to allow internal scrolling */
    .stChatFloatingInputContainer {
        border-top: none !important;
        background: transparent !important;
    }
    
    /* Premium Blue-Black Buttons */
    div.stButton > button {
        background: #0f172a !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #38bdf8 !important;
        color: #0f172a !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
        border-color: #38bdf8 !important;
    }
    
    /* Specific styling for the primary "New Chat" and "Active" buttons */
    button[data-testid="baseButton-primary"] {
        background: #38bdf8 !important;
        color: #0f172a !important;
        border: none !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        background: #7dd3fc !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

    if "show_profile" not in st.session_state:
        st.session_state.show_profile = False

    # 1. Top Right Buttons (Profile & Logout)
    _, top_right_col = st.columns([4, 1])
    with top_right_col:
        btn_c1, btn_c2 = st.columns([1, 1])
        with btn_c1:
            if st.button("Profile", key="nav_profile"):
                st.session_state.show_profile = not st.session_state.show_profile
        with btn_c2:
            if st.button("Logout", key="nav_logout"):
                st.session_state.logged_in = False
                st.session_state.page = "home"
                st.query_params.clear()
                st.rerun()

    # 2. Greeting Header (Below buttons, aligned left)
    st.markdown("""
        <div style="margin-top: -10px; margin-bottom: 25px;">
            <h1 style="margin: 0; color: white; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.5px;">Hi, I'm Mino</h1>
            <p style="margin: 0; color: rgba(255,255,255,0.4); font-size: 0.85rem;">Start a masterpiece with your AI assistant.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.show_profile:
        st.markdown(f"""
        <div class="profile-card">
            <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                {f'<img src="data:image/jpeg;base64,{user_image}" style="width:50px; height:50px; border-radius:10px;">' if user_image else '<div style="width:50px; height:50px; background:#333; border-radius:10px; display:flex; align-items:center; justify-content:center;">👤</div>'}
                <div>
                    <h3 style="margin:0; font-size:1.1rem; color:white;">{st.session_state.username}</h3>
                    <p style="margin:0; font-size:0.8rem; color:#a1a1a1;">Personal Member</p>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:10px; font-size:0.85rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <span style="color:#666;">Status</span>
                    <span style="color:#00ff88;">● Online</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#666;">ID</span>
                    <span style="color:#aaa;">{st.session_state.user_id[:8]}...</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.sidebar:
        # 1. Sidebar Header
        st.markdown('<h2 style="color: white; margin-top: -30px; margin-bottom: 20px;">Chats</h2>', unsafe_allow_html=True)
        
        # 2. Prominent New Chat Button
        if st.button("New chat", key="new_chat_btn", use_container_width=True, type="primary"):
            new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
            st.session_state.chats[new_chat_name] = []
            st.session_state.current_chat = new_chat_name
            
            # Save to DB
            user_id = st.session_state.get("user_id")
            if user_id: save_chat(user_id, new_chat_name, [])
            st.rerun()

        # 3. Chat History Subheading
        st.markdown('<p style="color:#666; font-size:0.75rem; font-weight:700; text-transform:uppercase; margin: 2.5rem 0 1rem 0.2rem;">Chat History</p>', unsafe_allow_html=True)
        
        # Redesigned Chat List with modern horizontal action row
        for chat_name in reversed(list(st.session_state.chats.keys())):
            c_col1, c_col2 = st.columns([5, 1])
            with c_col1:
                # Toggle between Chat Button and Rename Input
                if st.session_state.get("editing_chat") == chat_name:
                    new_name = st.text_input("New name:", value=chat_name, key=f"input_rename_{chat_name}", label_visibility="collapsed")
                    # Simplified layout to avoid nested columns in sidebar
                    if st.button("Save", key=f"save_{chat_name}", use_container_width=True, type="primary"):
                        if new_name and new_name != chat_name:
                            user_id = st.session_state.get("user_id")
                            if user_id:
                                rename_chat(user_id, chat_name, new_name)
                                st.session_state.chats[new_name] = st.session_state.chats.pop(chat_name)
                                if st.session_state.current_chat == chat_name:
                                    st.session_state.current_chat = new_name
                        st.session_state.editing_chat = None
                        st.rerun()
                    if st.button("Cancel", key=f"cancel_{chat_name}", use_container_width=True):
                        st.session_state.editing_chat = None
                        st.rerun()
                else:
                    # Normal Chat selection button
                    button_type = "primary" if chat_name == st.session_state.current_chat else "secondary"
                    if st.button(f"{chat_name}", key=f"chat_btn_{chat_name}", use_container_width=True, type=button_type):
                        st.session_state.current_chat = chat_name
                        st.rerun()
            
            with c_col2:
                # Simple toggle for options
                if st.button("⋮", key=f"toggle_{chat_name}", help="Options"):
                    st.session_state[f"show_opts_{chat_name}"] = not st.session_state.get(f"show_opts_{chat_name}", False)
            
            # Action Card - appears vertically below the chat button when toggled
            if st.session_state.get(f"show_opts_{chat_name}"):
                with st.container():
                    st.markdown('<div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 10px; margin-bottom: 10px;">', unsafe_allow_html=True)
                    
                    if st.button("Rename", key=f"rename_{chat_name}", use_container_width=True):
                        st.session_state.editing_chat = chat_name
                        st.session_state[f"show_opts_{chat_name}"] = False
                        st.rerun()
                        
                    if st.button("Delete", key=f"delete_{chat_name}", use_container_width=True):
                        user_id = st.session_state.get("user_id")
                        if user_id:
                            delete_chat(user_id, chat_name)
                            if chat_name in st.session_state.chats:
                                del st.session_state.chats[chat_name]
                            if st.session_state.current_chat == chat_name:
                                keys = list(st.session_state.chats.keys())
                                st.session_state.current_chat = keys[0] if keys else "Chat 1"
                                if "Chat 1" not in st.session_state.chats:
                                    st.session_state.chats["Chat 1"] = []
                            st.rerun()
                            
                    if st.button("Share", key=f"share_{chat_name}", use_container_width=True):
                        st.session_state.share_link = f"https://mino-ai.chat/share/{hashlib.md5(chat_name.encode()).hexdigest()[:8]}"
                        st.rerun()
                        
                    st.markdown('</div>', unsafe_allow_html=True)
            
        # Shared link notification
        if st.session_state.get("share_link"):
            st.info(f"Chat link created! (Mock): {st.session_state.share_link}")
            if st.button("OK"):
                st.session_state.share_link = None
                st.rerun()

    chat_container = st.container()
    with chat_container:
        current_messages = st.session_state.chats[st.session_state.current_chat]
        if not current_messages:
            st.markdown(f"""
                <div style="height: 60vh; display: flex; align-items: center; justify-content: center; opacity: 0.1;">
                    <h1 style="font-size: 8rem; font-weight: 900; letter-spacing: -5px;">MINO</h1>
                </div>
            """, unsafe_allow_html=True)
        
        for message in current_messages:
            is_assistant = message["role"] == "assistant"
            st.markdown(f"""
                <div class="chat-message {'assistant-message' if is_assistant else 'user-message'}">
                    <div style="flex-shrink: 0;">
                        {f'<img src="data:image/jpeg;base64,{ai_image}" class="avatar-img assistant-avatar">' if is_assistant else 
                         (f'<img src="data:image/jpeg;base64,{user_image}" class="avatar-img">' if user_image else '<div class="avatar-img" style="background:#333; display:flex; align-items:center; justify-content:center;">👤</div>')}
                    </div>
                    <div class="message-content">
                        {escape(str(message.get("content",""))).replace('\n','<br>')}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    if prompt := st.chat_input("Ask Mino anything..."):
        user_msg = {"role": "user", "content": prompt, "time": datetime.now().strftime("%I:%M %p")}
        st.session_state.chats[st.session_state.current_chat].append(user_msg)
        save_chat(st.session_state.user_id, st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_prompt = st.session_state.messages[-1]["content"]
        with st.spinner("Thinking..."):
            try:
                chatbot = load_model()
                response = chatbot(last_prompt, max_length=100)[0]['generated_text']
            except Exception:
                response = "I'm having trouble responding right now."
            
            assistant_msg = {"role": "assistant", "content": response, "time": datetime.now().strftime("%I:%M %p")}
            st.session_state.chats[st.session_state.current_chat].append(assistant_msg)
            save_chat(st.session_state.user_id, st.session_state.current_chat, st.session_state.chats[st.session_state.current_chat])
            speak_text(response)
            st.rerun()