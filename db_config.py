from firebase_config import get_firestore_client, get_firebase_auth
import hashlib
from datetime import datetime

def get_db_connection():
    """Get Firestore client - equivalent to MySQL connection"""
    try:
        return get_firestore_client()
    except Exception as e:
        print(f"Error connecting to Firestore: {e}")
        return None

def create_database():
    """Initialize Firestore collections - equivalent to creating MySQL database"""
    try:
        db = get_firestore_client()
        
        # Create a test document to ensure the collection exists
        test_doc = db.collection('users').document('test')
        test_doc.set({
            'username': 'test',
            'created_at': datetime.now(),
            'test': True
        })
        
        # Delete the test document
        test_doc.delete()
        
        print("Firestore collections initialized successfully")
        return True
        
    except Exception as e:
        print(f"Error initializing Firestore: {e}")
        return False

def create_user(username, password, profile_image=None):
    """Create a new user in Firestore using username as document ID."""
    try:
        db = get_firestore_client()
        firebase_auth = get_firebase_auth()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # If a user doc with this username already exists, return conflict
        user_doc_ref = db.collection('users').document(username)
        existing_doc = user_doc_ref.get()
        # Normalize Firestore vs mock: property .exists or method .exists()
        doc_exists_attr = getattr(existing_doc, 'exists', None)
        if callable(doc_exists_attr):
            doc_exists = doc_exists_attr()
        else:
            doc_exists = bool(doc_exists_attr)
        if doc_exists:
            return False, "Username already exists"

        # If Firebase Auth is available, create an Auth user with deterministic UID
        if firebase_auth is not None:
            try:
                # Use username as UID so it aligns with our Firestore doc ID
                firebase_auth.create_user(uid=username, password=password)
            except Exception as auth_err:
                # If UID already exists in Auth, continue and reconcile Firestore.
                # Only fail for other auth errors.
                auth_err_msg = str(auth_err)
                if 'already exists' in auth_err_msg.lower() or 'uid' in auth_err_msg.lower():
                    pass
                else:
                    return False, f"Auth error: {auth_err_msg}"

        # Create user document
        user_data = {
            'username': username,
            'password': hashed_password,
            'profile_image': profile_image,
            'created_at': datetime.now(),
            'chats': {}
        }

        # Add user to Firestore with deterministic ID (username)
        user_doc_ref.set(user_data)

        # Return the user ID (username)
        return True, username

    except Exception as e:
        print(f"Error creating user: {e}")
        return False, f"Error: {str(e)}"

def authenticate_user(username, password):
    """Authenticate user against Firestore by reading the username doc and verifying hash."""
    try:
        db = get_firestore_client()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Fetch deterministic doc by username
        user_doc_ref = db.collection('users').document(username)
        user_doc = user_doc_ref.get()
        doc_exists_attr = getattr(user_doc, 'exists', None)
        if callable(doc_exists_attr):
            doc_exists = doc_exists_attr()
        else:
            doc_exists = bool(doc_exists_attr)
        if doc_exists:
            user_data = user_doc.to_dict()
            if user_data and user_data.get('password') == hashed_password:
                return True, user_data, username
        return False, None, None

    except Exception as e:
        print(f"Error authenticating user: {e}")
        return False, None, None

def save_chat(user_id, chat_name, messages):
    """Save chat messages to Firestore"""
    try:
        db = get_firestore_client()
        
        # Update user's chats
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            if 'chats' not in user_data:
                user_data['chats'] = {}
            
            user_data['chats'][chat_name] = messages
            user_ref.update({'chats': user_data['chats']})
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error saving chat: {e}")
        return False

def get_user_chats(user_id):
    """Get all chats for a user"""
    try:
        db = get_firestore_client()
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return user_data.get('chats', {})
        return {}
    except Exception as e:
        print(f"Error getting user chats: {e}")
        return {}

def delete_chat(user_id, chat_name):
    """Delete a chat from Firestore"""
    try:
        db = get_firestore_client()
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            chats = user_data.get('chats', {})
            if chat_name in chats:
                del chats[chat_name]
                user_ref.update({'chats': chats})
                return True
        return False
    except Exception as e:
        print(f"Error deleting chat: {e}")
        return False

def rename_chat(user_id, old_name, new_name):
    """Rename a chat in Firestore"""
    try:
        db = get_firestore_client()
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            chats = user_data.get('chats', {})
            if old_name in chats:
                chats[new_name] = chats.pop(old_name)
                user_ref.update({'chats': chats})
                return True
        return False
    except Exception as e:
        print(f"Error renaming chat: {e}")
        return False 