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
class MockFirestore:
    def collection(self, name):
        return MockCollection()

class MockCollection:
    def document(self, doc_id=None):
        return MockDocument()
    
    def where(self, field, operator, value):
        return MockQuery()

class MockDocument:
    def set(self, data):
        print(f"Mock Firestore: Setting document with data: {data}")
        return True
    
    def get(self):
        return MockDocumentSnapshot()
    
    def update(self, data):
        print(f"Mock Firestore: Updating document with data: {data}")
        return True
    
    def delete(self):
        print("Mock Firestore: Deleting document")
        return True

class MockDocumentSnapshot:
    def exists(self):
        return False
    
    def to_dict(self):
        return {}

class MockQuery:
    def limit(self, count):
        return self
    
    def stream(self):
        return []

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
