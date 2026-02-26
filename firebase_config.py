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

# Absolute path to your service account JSON (explicit, no defaults)
SERVICE_ACCOUNT_PATH = r"D:\Mino-ChatBot-main\Mino-ChatBot-main\mino-e81f4-firebase-adminsdk-fbsvc-cea5b4030a.json"

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

# Initialize Firebase Admin SDK
def initialize_firebase():
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore, auth
        import streamlit as st
        import json
        
        if not firebase_admin._apps:
            # High-priority check: Search for Firebase Secrets (Streamlit Cloud)
            firebase_secrets = st.secrets.get("firebase")
            if firebase_secrets:
                try:
                    # firebase_secrets can be a dict or a JSON string
                    if isinstance(firebase_secrets, str):
                        key_dict = json.loads(firebase_secrets)
                    else:
                        key_dict = dict(firebase_secrets)
                    cred = credentials.Certificate(key_dict)
                    firebase_admin.initialize_app(cred)
                    return firestore.client()
                except Exception as e:
                    print(f"Error initializing from secrets: {e}")

            # Fallback: Local Service Account JSON
            try:
                if Path(SERVICE_ACCOUNT_PATH).exists():
                    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
                    firebase_admin.initialize_app(cred, {"projectId": PROJECT_ID} if PROJECT_ID else None)
                else:
                    # Final Fallback to default credentials
                    firebase_admin.initialize_app(options={"projectId": PROJECT_ID} if PROJECT_ID else None)
            except Exception as e:
                print(f"Error initializing Firebase with credentials/defaults: {e}")
                return MockFirestore()
        
        return firestore.client()
    except ImportError:
        print("Firebase Admin SDK not available, using mock implementation")
        return MockFirestore()
    except Exception as e:
        print(f"Firebase initialization failed: {e}, using mock implementation")
        return MockFirestore()

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
