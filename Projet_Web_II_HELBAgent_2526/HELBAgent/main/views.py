# main/views.py
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile
from .forms import AgentForm
from .models import Agent
from .constants import *
import requests
import json



def get_agent_statistics(user) -> dict:
    """
    Centralized function to generate agent statistics for a user.
    Args:
        user: Django User object
    Returns:
        dict: Dictionary containing labels, message counts, and agents queryset
    """
    labels, message_counts, agents = Agent.get_user_stats(user)

    return {
        'labels_agents': json.dumps(labels),
        'messages_per_agent': json.dumps(message_counts),
        'agents': agents
    }


def calculate_messages_by_day(agents) -> tuple:
    """
    Calculate message count aggregated by day for given agents.
    Args:
        agents: QuerySet of Agent objects
    Returns:
        tuple: (labels_days, data_days) as JSON-serializable lists
    """
    all_messages = []
    for agent in agents:
        for message in (agent.conversation or []):
            if isinstance(message, dict) and message.get("timestamp"):
                all_messages.append(message["timestamp"])

    messages_by_day = {}
    for timestamp in all_messages:
        try:
            date = parse_datetime(timestamp).date()
            date_str = str(date)
            messages_by_day[date_str] = messages_by_day.get(date_str, 0) + 1
        except:
            pass  # Skip invalid timestamps

    labels_days = sorted(messages_by_day.keys())
    data_days = [messages_by_day[label] for label in labels_days]

    return json.dumps(labels_days), json.dumps(data_days)


def check_cooldown_violation(agent, user, cooldown_seconds) -> tuple:
    """
    Check if user is violating the cooldown period.
    Args:
        agent: Agent object
        user: User object
        cooldown_seconds: Cooldown duration in seconds
    Returns:
        tuple: (is_violated: bool, remaining_seconds: int)
    """
    user_messages = [
        msg for msg in (agent.conversation or [])
        if isinstance(msg, dict) and msg.get("sender") == user.username
    ]

    if not user_messages:
        return False, 0

    last_message = user_messages[-1]
    try:
        last_timestamp = parse_datetime(last_message["timestamp"])
        if last_timestamp:
            time_difference = (timezone.now() - last_timestamp).total_seconds()
            if time_difference < cooldown_seconds:
                remaining = cooldown_seconds - int(time_difference)
                return True, remaining
    except:
        pass  # If parsing fails, ignore cooldown check

    return False, 0


# ==================== Class-Based Views ====================

class AgentListView(ListView):
    """
    Display a list of all agents, sorted by activity score.
    """
    model = Agent
    template_name = 'main/home.html'
    context_object_name = 'agents'
    paginate_by = DEFAULT_PAGINATION_COUNT

    def get_queryset(self) -> list:
        """
        Return agents sorted by activity score (descending).
        """
        agents = list(Agent.objects.all())
        agents.sort(key=lambda x: x.get_activity_score(), reverse=True)
        return agents


class AgentCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new agent.
    """
    model = Agent
    form_class = AgentForm

    def form_valid(self, form) -> HttpResponse:
        """
        Set the current user as the agent's author before saving.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class AgentDetailView(DetailView):
    """
    Display detailed information about a specific agent.
    """
    model = Agent
    template_name = 'main/agent_detail.html'


class UserProfileView(DetailView):
    """
    Display a user's profile with agent statistics.
    """
    model = Profile
    context_object_name = "profile"

    def get_object(self) -> object:
        """
        Retrieve the profile based on username from URL.
        """
        username = self.kwargs.get("username")
        return Profile.objects.get(user__username=username)

    def get_context_data(self, **kwargs) -> dict:
        """
        Add agent statistics to context.
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object().user

        # Add agent statistics
        stats = get_agent_statistics(user)
        context.update(stats)

        return context


class UserAgentListView(ListView):
    """
    Display a paginated list of agents created by a specific user.
    """
    model = Agent
    template_name = 'main/agents_user.html'
    context_object_name = 'agents'
    paginate_by = DEFAULT_PAGINATION_COUNT

    def get_queryset(self) -> object:
        """
        Return agents created by the user specified in the URL.
        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Agent.objects.filter(author=user).order_by('-date_created')


class AgentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing agent.
    Only the agent's author can update it.
    """
    model = Agent
    form_class = AgentForm

    def form_valid(self, form) -> HttpResponse:
        """
        Ensure the author remains the current user.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> bool:
        """
        Check if the current user is the agent's author.
        """
        agent = self.get_object()
        return self.request.user == agent.author


class AgentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting an agent.
    Only the agent's author can delete it.
    """
    model = Agent
    success_url = '/'

    def test_func(self) -> bool:
        """
        Check if the current user is the agent's author.
        """
        agent = self.get_object()
        return self.request.user == agent.author


# ==================== Function-Based Views ====================

@login_required
def chat_view(request, pk) -> HttpResponse:
    """
    Display the chat interface for interacting with an agent.
    Args:
        request: HttpRequest object
        pk: Agent primary key (UUID)
    Returns:
        Rendered chat template
    """
    agent = get_object_or_404(Agent, pk=pk)
    return render(request, 'main/agent_chat.html', {'agent': agent})


@login_required
def chat_b2(request) -> HttpResponse:
    """
    Display the collaborative B2 chat interface.
    Args:
        request: HttpRequest object
    Returns:
        Rendered chat_b2 template with user context
    """
    context = {
        'username': request.user.username,
        'personal_key': '4Bzdacosta4u5Vy',
    }
    return render(request, 'main/chat_b2.html', context)


@login_required
def proxy_chat_txt(request) -> HttpResponse:
    """
    Proxy endpoint for fetching chat.txt from external source.
    Args:
        request: HttpRequest object
    Returns:
        HttpResponse with plain text content
    """
    response = requests.get(HELBPLAYS_CHAT_URL, timeout=API_REQUEST_TIMEOUT_SECONDS)
    return HttpResponse(response.content, content_type='text/plain')


@login_required
def send_message(request, pk) -> JsonResponse:
    """
    Handle sending a message to an agent and generating a response.
    Args:
        request: HttpRequest object
        pk: Agent primary key (UUID)
    Returns:
        JsonResponse with success status or error message
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    agent = get_object_or_404(Agent, pk=pk)

    # Parse request body
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format."},
            status=HTTP_BAD_REQUEST
        )

    if not user_message:
        return JsonResponse(
            {"error": "Message cannot be empty."},
            status=HTTP_BAD_REQUEST
        )

    # Check cooldown
    is_violated, remaining = check_cooldown_violation(
        agent,
        request.user,
        agent.cooldown
    )

    if is_violated:
        return JsonResponse(
            {"error": f"Cooldown: wait {remaining} second(s) before sending again."},
            status=HTTP_TOO_MANY_REQUESTS
        )
    # Add user message
    agent.add_message(
        sender=request.user,
        text=user_message,
        is_agent=False,
        save=True
    )

    # Generate and add agent response
    try:
        response_text = agent.run(user_message)
        agent.add_message(
            sender=request.user,
            text=response_text,
            is_agent=True,
            save=False
        )
        agent.save()
        return JsonResponse({
            "success": True,
            "messages": agent.conversation
        })
    except Exception as error:
        # Rollback user message on error
        if agent.conversation and isinstance(agent.conversation, list):
            agent.conversation = agent.conversation[:-1]
            agent.save()
        return JsonResponse(
            {"error": f"Agent error: {str(error)}"},
            status=HTTP_INTERNAL_SERVER_ERROR
        )


@login_required
def get_messages(request, pk) -> JsonResponse:
    """
    Retrieve all messages for a specific agent.
    Args:
        request: HttpRequest object
        pk: Agent primary key (UUID)
    Returns:
        JsonResponse containing message list
    """
    agent = get_object_or_404(Agent, pk=pk)
    messages = agent.conversation or []
    return JsonResponse({"messages": messages})


def about_view(request) -> HttpResponse:
    """
    Display the about page.
    Args:
        request: HttpRequest object
    Returns:
        Rendered about template
    """
    return render(request, 'main/about.html')