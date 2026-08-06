# HELBAgent — Custom AI Agent Platform

HELBAgent is a web application developed as part of the **Web Programming II** course at HELB. It allows users to create, manage, and interact with personalized AI agents. Users can choose between internal local models (template-based) or API-based models (OpenAI) to power their agents' personality.

## 🚀 Project Overview

The platform enables a social AI experience where conversations are shared among users in real-time. Key features include:

- **Custom AI Creation** — Configure preprompts, avatars, and model types.
- **Hybrid AI Engine** — Supports internal local logic or OpenAI API models.
- **Shared Live Chat** — Interact with agents alongside other users with real-time updates.
- **Activity Analytics** — Visual representation of user engagement and message statistics using charts.
- **HELBPlays Integration** — A collaborative B2 student chat and live webcam viewer.

## 🛠 Features

### User Management
- **Authentication** — Secure login and registration system.
- **User Profiles** — Personalized pages showing user activity and created agents.

### AI Agent System
- **Agent Creation** — Set a title, short description, and a "preprompt" (system instructions) to define the agent's behavior.
- **Model Selection**
  - *Local models*: SmolLM-135M, TinyLlama — use a local template engine that generates responses based on the agent's specific preprompt and the user's input.
  - *API models*: GPT-4o, GPT-4o mini, o3-mini — powered by the OpenAI API.
- **Dynamic UI** — The interface adapts based on the model type, hiding API key fields for local agents.
- **Image Processing** — Automatic uniformization of agent avatars with a max resolution of 300x300 pixels.

### Interaction & Real-time Chat
- **Shared Conversations** — Messages from all users and responses from the AI are visible to everyone in the chat room.
- **Spam Protection** — Integrated cooldown system (configurable per agent) to prevent message flooding.
- **Auto-polling** — The chat interface refreshes automatically every 2 seconds via AJAX to display new messages in real-time.
- **Message Alternation (Bonus)** — Logic ensures that a user message is always followed by an agent response, preventing consecutive messages from the same sender type.

### Collaborative Chat (HELBPlays B2)
- **External Resource Sync** — Dynamically fetches `chat.txt` and `frame.jpg` from the HELBPlays server.
- **Real-time Refresh** — The collaborative chat and webcam view refresh every few seconds to show live student activity.
- **Base64 Messaging** — Integrated secure messaging using Base64 encoding for usernames, messages, and personal keys.

### Data Visualization
- **User Analytics** — Charts showing the number of messages sent per agent.
- **Daily Activity** — A private graph (accessible only to the owner) tracking message frequency.

## 🧰 Tech Stack

| Technology | Role in the project |
|---|---|
| **Python 3.10+** | Core programming language for the whole backend. |
| **Django 5.x** | Main web framework — handles routing (URLs), the ORM/database layer, the built-in authentication system, and the admin panel. Follows Django's MVT (Model-View-Template) architecture. |
| **SQLite** | Default relational database used in development — file-based, zero configuration, stores users, agents, messages and analytics data. |
| **django-crispy-forms** + **crispy-bootstrap4** | Renders Django forms (login, registration, agent creation) with clean, consistent Bootstrap 4 styling instead of Django's default raw HTML. |
| **Pillow (PIL)** | Image processing library — used to automatically resize/crop uploaded agent avatars to a uniform 300x300 resolution. |
| **channels** | Django Channels — extends Django to support asynchronous features (WebSockets, background tasks), used as the foundation for the app's real-time capabilities. |
| **requests** | HTTP client used server-side to fetch external resources from the HELBPlays server (`chat.txt`, `frame.jpg`) for the collaborative chat integration. |
| **openai** | Official OpenAI Python SDK — sends prompts to and receives responses from the OpenAI API for API-based agents (GPT-4o, GPT-4o mini, o3-mini). |
| **python-dotenv** | Loads environment variables (like `OPENAI_API_KEY`) from a local `.env` file into the app at runtime, keeping secrets out of the source code. |
| **AJAX (JavaScript)** | Powers the front-end auto-polling (every 2 seconds) that refreshes the shared chat and the HELBPlays webcam view without reloading the page. |
| **Local template engine (custom)** | A lightweight rule/template-based response generator used for local models (SmolLM-135M, TinyLlama) — builds replies from the agent's preprompt and the user's input without calling an external API. |
| **Charting library (e.g. Chart.js)** | Renders the analytics dashboard — messages per agent and daily activity graphs. |

## 📁 Project Structure

```
helbagent/
├── users/          # Authentication, user profiles
├── main/           # Agents, chat, analytics, HELBPlays integration
└── helbagent/      # Project configuration (settings, urls, wsgi/asgi)
```

## 📋 Prerequisites

- Python 3.10+
- pip (Python package manager)
- Internet connection (for the OpenAI API and HELBPlays resources)
- (optional) git

## 🔑 Environment Variables

This project requires an OpenAI API key to use the API-based models. **Never commit real keys to the repository.**

1. Create a `.env` file at the project root:

```
OPENAI_API_KEY=your-openai-api-key-here
```

2. Make sure `.env` is listed in `.gitignore` (see below).

## 🚦 How to Run the Project

### On Linux (Ubuntu)

The project is optimized for a Linux environment. A dedicated bash script is provided for one-click execution.

```bash
chmod +x run.sh   # grant execution permission (if necessary)
bash run.sh
```

This script automatically upgrades pip, installs requirements, applies migrations, and starts the development server.

### On Windows

```
run.bat
```

Double-click `run.bat`, or run it from CMD.

### Manual Setup

1. **Create and activate a virtual environment** (recommended name: `.venv`):

```bash
python -m venv .venv

# Windows (cmd)
.\.venv\Scripts\Activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

To deactivate: `deactivate`

2. **Install dependencies**:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. **Apply database migrations**:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create an admin account**:

```bash
python manage.py createsuperuser
```

5. **Run the development server**:

```bash
python manage.py runserver
```

## 🌐 Local Addresses

- Application: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin

## 🧪 Testing

```bash
python manage.py test
```

## 🔒 Security Notes

- Never commit `.venv/`, `.env`, or any file containing API keys, passwords, or secrets.
- `.gitignore` should include at minimum:

```
.venv/
__pycache__/
.env
*.pyc
db.sqlite3
```

- Rotate any credentials immediately if they are ever accidentally exposed (commit history, chat, screenshots, etc.).
- For production deployment: run `collectstatic`, configure WSGI/ASGI properly, use a reverse proxy, and store all secrets as environment variables (never hardcoded).

## 👤 Author

**Waldyr Costa** — Application Development student at HELB
[GitHub](https://github.com/Costawaldyr) · [LinkedIn](https://www.linkedin.com/in/waldyr-c-b38304257/)
