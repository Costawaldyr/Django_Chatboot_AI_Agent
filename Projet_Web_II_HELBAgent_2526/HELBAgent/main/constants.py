# main/constants.py
"""
Central configuration file for application constants.
This file contains all magic numbers and configuration values used throughout the application.
"""

# ==================== IMAGE PROCESSING ====================
MAX_AVATAR_SIZE = 300  # Maximum dimension for avatar images in pixels
TITLE_TRUNCATE_LENGTH = 20  # Maximum length before truncating agent titles

# ==================== PAGINATION ====================
DEFAULT_PAGINATION_COUNT = 5  # Default number of items per page

# ==================== ACTIVITY SCORING ====================
ACTIVITY_USER_WEIGHT = 2  # Multiplier for user count in activity score calculation

# ==================== API CONFIGURATION ====================
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"  # OpenAI API endpoint
DEFAULT_TEMPERATURE = 0.7  # Default temperature for LLM responses
MAX_TOKENS_PER_REQUEST = 1000  # Maximum tokens in API responses
API_REQUEST_TIMEOUT_SECONDS = 30  # Timeout for external API calls

# ==================== EXTERNAL SERVICES ====================
HELBPLAYS_CHAT_URL = 'https://helbplays2526.alwaysdata.net/chat.txt'  
HELBPLAYS_IMAGE_URL = 'https://helbplays2526.alwaysdata.net/frame.jpg'  
HELBPLAYS_SEND_URL = 'https://helbplays2526.alwaysdata.net/chat.php' 

# ==================== HTTP STATUS CODES ====================
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_SERVER_ERROR = 500

# ==================== COOLDOWN SETTINGS ====================
DEFAULT_COOLDOWN_SECONDS = 5 

# ==================== MODEL CONFIGURATIONS ====================
LOCAL_MODEL_TEMPLATES = [
    "Thank you for your question. {preprompt} Regarding '{prompt}', here is my response...",
    "Interesting! '{prompt}' is a good question. {preprompt}",
    "I understand your request about '{prompt}'. Let me answer according to my instructions: {preprompt}",
    "Alright! You're asking me '{prompt}'. As an agent configured as follows: {preprompt}, I respond..."
]

# ==================== CHAT CONFIGURATION ====================
CHAT_REFRESH_INTERVAL_MS = 2000  # Chat refresh interval in milliseconds
IMAGE_REFRESH_INTERVAL_MS = 5000  # Image refresh interval in milliseconds
ENTER_KEY_CODE = 13  # Keyboard code for Enter key

# ==================== SUCCESS MESSAGES ====================
ACCOUNT_CREATED_MESSAGE = 'Your account has been created! You are now able to log in'
ACCOUNT_UPDATED_MESSAGE = 'Your account has been updated!'

# ==================== ERROR MESSAGES ====================
INVALID_REQUEST_METHOD_ERROR = "Invalid request method."
INVALID_JSON_ERROR = "Invalid JSON format."
EMPTY_MESSAGE_ERROR = "Message cannot be empty."
NO_API_KEY_ERROR = "No API key configured."
COOLDOWN_ERROR_TEMPLATE = "Cooldown: wait {remaining} second(s) before sending again."
AGENT_ERROR_TEMPLATE = "Agent error: {error}"