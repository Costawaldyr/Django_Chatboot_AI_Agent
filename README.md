# HELBAgent — Custom AI Agent Platform

HELBAgent is a web application developed as part of the **Web Programming II** course. It allows users to create, manage, and interact with personalized AI agents. Users can choose between internal local models (template-based) or API-based models (OpenAI) to power their agents' personality.

## 🚀 Project Overview

The platform enables a social AI experience where conversations are shared among users in real-time. Key features include:
- **Custom AI Creation**: Configure preprompts, avatars, and model types.
- **Hybrid AI Engine**: Supports internal local logic or OpenAI API models.
- **Shared Live Chat**: Interact with agents alongside other users with real-time updates.
- **Activity Analytics**: Visual representation of user engagement and message statistics using charts.
- **HELBPlays Integration**: A collaborative B2 student chat and live webcam viewer.

## 🛠 Features

### User Management
- **Authentication**: Secure Login and Registration system.
- **User Profiles**: Personalized pages showing user activity and created agents.

### AI Agent System
- **Agent Creation**: Set a title, short description, and a "preprompt" (system instructions) to define the agent's behavior.
- **Model Selection**: 
    - **Local Models**: SmolLM-135M, TinyLlama. These use a **local template engine** that generates responses based on the agent's specific preprompt and the user's input.
    - **API Models**: GPT-4o, GPT-4o mini, o3-mini. Powered by the OpenAI API.
- **Dynamic UI**: The interface adapts based on the model type, hiding API key fields for local agents.
- **Image Processing**: Automatic uniformization of agent avatars with a max resolution of 300x300 pixels.

### Interaction & Real-time Chat
- **Shared Conversations**: Messages from all users and responses from the AI are visible to everyone in the chat room.
- **Spam Protection**: Integrated cooldown system (configurable per agent) to prevent message flooding.
- **Auto-polling**: The chat interface refreshes automatically every 2 seconds via AJAX to display new messages in real-time.
- **Message Alternation (Bonus)**: Logic ensures that a user message is always followed by an agent response, preventing consecutive messages from the same sender type.

### Collaborative Chat (HELBPlays B2)
- **External Resource Sync**: Dynamically fetches `chat.txt` and `frame.jpg` from the HELBPlays server.
- **Real-time Refresh**: The collaborative chat and webcam view refresh every few seconds to show live student activity.
- **Base64 Messaging**: Integrated secure messaging using Base64 encoding for usernames, messages, and personal keys.

### Data Visualization
- **User Analytics**: Charts showing the number of messages sent per agent.
- **Daily Activity**: A private graph (accessible only to the owner) tracking message frequency.

## 📋 Prerequisites

- **Python 3.10+**
- **Django 5.x**
- **pip** (Python package manager)
- **Internet Connection** (For OpenAI API and HELBPlays resources)

## 🚦 How to Run the Project

### On Linux (Ubuntu)
The project is optimized for a Linux environment. A dedicated bash script is provided for one-click execution.

1. Open your terminal in the project root directory.
2. Grant execution permission (if necessary):
   ```bash
   chmod +x run.sh
   ```
3. Launch the application:
   ```bash
   bash run.sh
   ```
This script will automatically upgrade pip, install requirements, apply migrations, and start the development server.

### On Windows
For Windows users, use the provided batch file:
1. Double-click on `run.bat` or run it from CMD:
   ```cmd
   run.bat
   ```

### Manual Execution
If you prefer to run commands manually: