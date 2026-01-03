# main/models.py
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
from .constants import *
from PIL import Image
import requests
import random
import uuid



class Agent(models.Model):
    """
    Agent model representing an AI assistant with configurable behavior.
    An Agent can use either local models or API-based models (like GPT-4).
    It maintains a conversation history and tracks user engagement metrics.
    """

    MODEL_TYPE_LOCAL = 'local'
    MODEL_TYPE_API = 'api'
    MODEL_NAME_GPT4_MINI = 'gpt-4o-mini'
    MODEL_NAME_SMOL_LM = 'SmolLm-135M'

    MODEL_TYPES = [
        (MODEL_TYPE_LOCAL, 'Local'),
        (MODEL_TYPE_API, 'API')
    ]
    MODEL_NAMES = [
        (MODEL_NAME_GPT4_MINI, 'GPT-4o Mini'),
        (MODEL_NAME_SMOL_LM, 'Smol LM 135M'),
    ]

    # Sender identifiers for conversation messages
    SENDER_AGENT = "agent"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    date_created = models.DateTimeField(default=timezone.now)
    conversation = models.JSONField(default=list, blank=True)
    users = models.ManyToManyField(User, blank=True, related_name='used_agents')
    user_count = models.PositiveIntegerField(default=0)
    message_count = models.PositiveIntegerField(default=0)
    model_type = models.CharField(max_length=10,choices=MODEL_TYPES,default=MODEL_TYPE_API)
    model_name = models.CharField(max_length=120,choices=MODEL_NAMES,default=MODEL_NAME_GPT4_MINI)
    preprompt = models.TextField(blank=True)
    description = models.CharField(max_length=250)
    avatar = models.ImageField(default='default.jpg',upload_to='agent_pics/',null=True,blank=True)
    is_public = models.BooleanField(default=True, editable=False)
    cooldown = models.PositiveIntegerField(default=5)
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('agent-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Override save to update computed fields and resize avatar.
        """
        self.user_count = self.get_unique_user_count()
        self.message_count = self.get_message_count()
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > MAX_AVATAR_SIZE or img.width > MAX_AVATAR_SIZE:
                output_size = (MAX_AVATAR_SIZE, MAX_AVATAR_SIZE)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    def get_message_count(self) -> int:
        """
        Calculate the total number of messages in the conversation.
        """
        return len(self.conversation or [])

    def get_unique_user_count(self) -> int:
        """
        Get the number of unique users who have interacted with this agent.
        """
        return self.users.count()

    def get_activity_score(self) -> int:
        """
        Calculate activity score based on messages and unique users.
        Higher score indicates more popular/active agents.
        """
        return self.get_message_count() + (self.user_count * ACTIVITY_USER_WEIGHT)

    @staticmethod
    def get_user_stats(user) -> tuple:
        """
        Get statistics for all agents created by a specific user.
        Returns:
            tuple: (labels, message_counts, agents_queryset)
        """
        agents = Agent.objects.filter(author=user).order_by('-user_count')
        labels = []
        message_counts = []

        for agent in agents:
            truncated_title = (
                agent.title[:TITLE_TRUNCATE_LENGTH] + "..."
                if len(agent.title) > TITLE_TRUNCATE_LENGTH
                else agent.title
            )
            labels.append(truncated_title)
            message_counts.append(agent.get_message_count())
        return labels, message_counts, agents

    def ensure_message_alternation(self) -> None:
        """
        Ensure proper alternation between user and agent messages.
        Merges consecutive messages from the same sender.
        """
        if not self.conversation or len(self.conversation) < 2:
            return

        cleaned_conversation = []
        previous_message = None

        for message in self.conversation:
            is_agent_message = (message.get("sender") == self.SENDER_AGENT)

            if previous_message is None:
                cleaned_conversation.append(message)
                previous_message = message
            else:
                previous_is_agent = (previous_message.get("sender") == self.SENDER_AGENT)

                if is_agent_message == previous_is_agent:
                    # Same sender type - merge messages
                    previous_message["text"] += "\n\n" + message.get("text", "")
                    previous_message["timestamp"] = message.get("timestamp")
                else:
                    # Different sender - add normally
                    cleaned_conversation.append(message)
                    previous_message = message

        self.conversation = cleaned_conversation

    def add_message(self, sender, text, is_agent=False, save=True) -> None:
        """
        Add a formatted message to the conversation with proper alternation.
        Args:
            sender: User object or string identifier
            text: Message content
            is_agent: Boolean indicating if message is from the agent
            save: Boolean indicating whether to save immediately
        """
        timestamp = timezone.now()
        timestamp_str = timestamp.isoformat()

        if is_agent:
            message_data = {
                "sender": self.SENDER_AGENT,
                "display_name": self.title,
                "profile_url": None,
                "text": text,
                "timestamp": timestamp_str,
                "avatar": self.avatar.url if self.avatar else "/static/img/default.jpg",
            }
        else:
            avatar_url = (
                sender.profile.image.url
                if hasattr(sender, "profile")
                else "/static/img/default.jpg"
            )
            message_data = {
                "sender": sender.username,
                "display_name": sender.username,
                "profile_url": f"/user/{sender.username}/profile/",
                "text": text,
                "timestamp": timestamp_str,
                "avatar": avatar_url,
            }
        self.conversation.append(message_data)

        if not is_agent:
            if sender not in self.users.all():
                self.users.add(sender)
            self.user_count = self.get_unique_user_count()

        self.ensure_message_alternation()

        if save:
            self.save()

    def run_local_model(self, prompt: str) -> str:
        """
        Generate a response using a local model (template-based).
        Args:
            prompt: User's input message
        Returns:
            Generated response string
        """
        template = random.choice(LOCAL_MODEL_TEMPLATES)
        return template.format(
            preprompt=self.preprompt[:100],
            prompt=prompt[:50]
        )

    def run_api_model(self, prompt: str) -> str:
        """
        Generate a response using an external API (e.g., OpenAI).
        Args:
            prompt: User's input message
        Returns:
            API response string or error message
        """
        if not self.api_key:
            return "No API key configured."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if self.preprompt:
            messages.append({
                "role": "system",
                "content": self.preprompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": DEFAULT_TEMPERATURE,
            "max_tokens": MAX_TOKENS_PER_REQUEST
        }

        try:
            response = requests.post(
                OPENAI_API_URL,
                headers=headers,
                json=payload,
                timeout=API_REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as http_error:
            error_detail = self._extract_api_error_message(response)
            return f"API error {response.status_code}: {error_detail or str(http_error)}"

        except Exception as general_error:
            return f"API error: {general_error}"

    def _extract_api_error_message(self, response) -> str:
        """
        Extract error message from API response if available.
        Args:
            response: requests.Response object
        Returns:
            Error message string or empty string
        """
        try:
            return response.json().get("error", {}).get("message", "")
        except:
            return ""

    def run(self, prompt: str) -> str:
        """
        Generate a response using the appropriate model type.
        Args:
            prompt: User's input message
        Returns:
            Generated response string
        """
        if self.model_type == self.MODEL_TYPE_LOCAL:
            return self.run_local_model(prompt)
        else:
            return self.run_api_model(prompt)