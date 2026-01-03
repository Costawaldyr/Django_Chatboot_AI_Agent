# users/views.py
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import Agent
from django.utils.dateparse import parse_datetime
from main.constants import (ACCOUNT_CREATED_MESSAGE,ACCOUNT_UPDATED_MESSAGE)
import json



def register(request):
    """
    Handle user registration.
    Args:
        request: HttpRequest object
    Returns:
        Rendered registration form or redirect to login on success
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, ACCOUNT_CREATED_MESSAGE)
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """
    Display and handle updates to the user's profile.
    Args:
        request: HttpRequest object
    Returns:
        Rendered profile page with forms and statistics
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, ACCOUNT_UPDATED_MESSAGE)
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Get statistics for charts
    stats = get_agent_statistics_for_profile(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': request.user.profile,
    }
    context.update(stats)
    return render(request, 'users/profile.html', context)


def get_agent_statistics_for_profile(user):
    """
    Generate agent statistics for a user's profile page.
    Args:
        user: Django User object
    Returns:
        dict: Dictionary containing statistics data for template context
    """
    agents = Agent.objects.filter(author=user).order_by('-user_count')

    # Graph 1: Messages per agent
    labels_agents = []
    messages_per_agent = []

    for agent in agents:
        truncated_title = (
            agent.title[:20] + "..."
            if len(agent.title) > 20
            else agent.title
        )
        labels_agents.append(truncated_title)
        messages_per_agent.append(agent.get_message_count())

    # Graph 2: Messages per day
    labels_days, data_days = calculate_daily_message_distribution(agents)

    return {
        'agents': agents,
        'labels_agents': json.dumps(labels_agents),
        'messages_per_agent': json.dumps(messages_per_agent),
        'labels_days': json.dumps(labels_days),
        'data_days': json.dumps(data_days),
    }


def calculate_daily_message_distribution(agents):
    """
    Calculate the distribution of messages across days for given agents.
    Args:
        agents: QuerySet of Agent objects
    Returns:
        tuple: (labels_days, data_days) as sorted lists
    """
    all_messages = []
    for agent in agents:
        for message in (agent.conversation or []):
            if isinstance(message, dict) and message.get("timestamp"):
                all_messages.append(message["timestamp"])

    messages_by_day = {}
    for timestamp_str in all_messages:
        try:
            date = parse_datetime(timestamp_str).date()
            date_str = str(date)
            messages_by_day[date_str] = messages_by_day.get(date_str, 0) + 1
        except:
            pass  # Skip invalid timestamps

    labels_days = sorted(messages_by_day.keys())
    data_days = [messages_by_day[label] for label in labels_days]

    return labels_days, data_days

