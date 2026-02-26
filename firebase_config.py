import os
from pathlib import Path

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyD-WkOuSCmhr_stngWndP1R65zjTN_U0hs",
    "authDomain": "mino-e81f4.firebaseapp.com",
    "projectId": "mino-e81f4",
    "storageBucket": "mino-e81f4.firebasestorage.app",
    "messagingSenderId": "75490538160",
    "appId": "1:75490538160:web:0cae9bbc9c4947ee4b8175",
    "measurementId": "G-CP90EPSF3M"
}

# Handle relative path for service account (works locally and deployed)
BASE_DIR = Path(__file__).parent
SERVICE_ACCOUNT_NAME = "mino-e81f4-firebase-adminsdk-fbsvc-cea5b4030a.json"
SERVICE_ACCOUNT_PATH = BASE_DIR / SERVICE_ACCOUNT_NAME

PROJECT_ID = firebase_config.get("projectId") or os.environ.get("GOOGLE_CLOUD_PROJECT")

# Mock Firebase classes for development
# Global mock storage to make Demo Mode functional
MOCK_DATA = {"users": {}, "chats": {}}

class MockFirestore:
    def collection(self, name):
        return MockCollection(name)

class MockCollection:
    def __init__(self, name):
        self.name = name
    def document(self, doc_id):
        return MockDocument(self.name, doc_id)

class MockDocument:
    def __init__(self, coll_name, doc_id):
        self.coll_name = coll_name
        self.doc_id = doc_id
    
    def set(self, data):
        if self.coll_name not in MOCK_DATA: MOCK_DATA[self.coll_name] = {}
        MOCK_DATA[self.coll_name][self.id] = data
        return True
    
    @property
    def id(self): return self.doc_id

    def get(self):
        data = MOCK_DATA.get(self.coll_name, {}).get(self.doc_id)
        return MockDocumentSnapshot(data)
    
    def update(self, data):
        if self.coll_name in MOCK_DATA and self.doc_id in MOCK_DATA[self.coll_name]:
            MOCK_DATA[self.coll_name][self.doc_id].update(data)
        return True
    
    def delete(self):
        if self.coll_name in MOCK_DATA and self.doc_id in MOCK_DATA[self.coll_name]:
            del MOCK_DATA[self.coll_name][self.doc_id]
        return True

class MockDocumentSnapshot:
    def __init__(self, data):
        self._data = data
    def exists(self):
        return self._data is not None
    def to_dict(self):
        return self._data or {}

# Global connection status tracker
LAST_ERROR = "Not initialized"
CONNECTION_MODE = "None"

# Initialize Firebase Admin SDK
def initialize_firebase():
    global LAST_ERROR, CONNECTION_MODE
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore, auth
        import streamlit as st
        import json
        
        if not firebase_admin._apps:
            # 1. Streamlit Cloud Secrets
            if hasattr(st, "secrets") and "firebase" in st.secrets:
                try:
                    secret_raw = st.secrets["firebase"]
                    key_dict = json.loads(secret_raw) if isinstance(secret_raw, str) else dict(secret_raw)
                    cred = credentials.Certificate(key_dict)
                    firebase_admin.initialize_app(cred)
                    CONNECTION_MODE = "Streamlit Secrets"
                    LAST_ERROR = None
                    return firestore.client()
                except Exception as e:
                    LAST_ERROR = f"Secrets Error: {e}"

            # 2. Local Service Account JSON
            if Path(SERVICE_ACCOUNT_PATH).exists():
                try:
                    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
                    firebase_admin.initialize_app(cred, {"projectId": PROJECT_ID} if PROJECT_ID else None)
                    CONNECTION_MODE = "Local JSON File"
                    LAST_ERROR = None
                    return firestore.client()
                except Exception as e:
                    LAST_ERROR = f"Local JSON Error: {e}"
            else:
                LAST_ERROR = f"File not found at {SERVICE_ACCOUNT_PATH}"

            # 3. Final Fallback
            try:
                firebase_admin.initialize_app(options={"projectId": PROJECT_ID} if PROJECT_ID else None)
                CONNECTION_MODE = "ADC / Default"
                LAST_ERROR = None
                return firestore.client()
            except Exception as e:
                LAST_ERROR = f"Default Init Failed: {e}"
                CONNECTION_MODE = "MOCK (Offline)"
                return MockFirestore()
        
        return firestore.client()
    except Exception as e:
        LAST_ERROR = str(e)
        CONNECTION_MODE = "MOCK (Error)"
        return MockFirestore()

def get_connection_status():
    return CONNECTION_MODE, LAST_ERROR

# Get Firestore client
def get_firestore_client():
    return initialize_firebase()

# Get Firebase Auth
def get_firebase_auth():
    try:
        from firebase_admin import auth
        return auth
    except ImportError:
        print("Firebase Auth not available, using mock implementation")
        return None
