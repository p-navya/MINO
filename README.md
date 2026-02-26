# Mino - Your Personal AI Assistant

## Overview
Mino is an intelligent chatbot application built with Streamlit and powered by the BlenderBot model. It provides a modern, user-friendly interface for interactive conversations with an AI assistant.

## Features
- 🔐 **Secure Authentication**: User login and signup system with password hashing
- 👤 **Profile Customization**: Upload and display profile pictures
- 💬 **Interactive Chat Interface**: Modern chat UI with message history
- 🎨 **Beautiful Design**: Clean and responsive interface with custom styling
- 🔄 **Session Management**: Persistent chat sessions with timestamp tracking
- 🚪 **Easy Navigation**: Intuitive navigation between home, login, and chat pages

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth + SHA-256 hashing
- **AI Model**: Facebook BlenderBot
- **Image Processing**: PIL (Python Imaging Library)

## Prerequisites
- Python 3.8+
- Firebase project with Firestore enabled
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mino-chatbot.git
cd mino-chatbot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Firebase:
   - Create a Firebase project at https://console.firebase.google.com/
   - Enable Firestore Database
   - Generate a service account key and download the JSON file
   - Replace the `firebase_service_account.json` file with your actual service account key
   - Update the Firebase configuration in `firebase_config.py` with your project details

5. Run the application:
```bash
python -m streamlit run app.py
```

## Project Structure
```
mino-chatbot/
├── app.py              # Main application entry point
├── views/
│   ├── __init__.py    # Views initialization
│   ├── chatbot.py     # Chat interface logic
│   ├── home.py        # Home page view
│   └── login.py       # Authentication views
├── ai.jpg             # AI assistant avatar
├── my.mp4             # Welcome video
├── db_config.py       # Firebase database configuration
├── firebase_config.py # Firebase configuration
├── firebase_service_account.json # Firebase service account key
└── README.md          # Project documentation
```

## Usage
1. Start by creating an account or logging in
2. Optionally upload a profile picture during signup/login
3. Begin chatting with Mino in the interactive chat interface
4. View chat history in the sidebar
5. Clear chat or logout using the provided buttons

## Security Features
- Password hashing using SHA-256
- Secure session management
- Protected routes requiring authentication
- Safe image handling and storage

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 