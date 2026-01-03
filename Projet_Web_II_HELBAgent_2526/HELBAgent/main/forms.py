from django import forms
from django.core.exceptions import ValidationError

from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'title',
            'description',
            'model_type',
            'model_name',
            'avatar',
            'preprompt',
            'cooldown',
            'api_key',
        ]

class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'title',
            'description',
            'model_type',
            'model_name',
            'avatar',
            'preprompt',
            'cooldown',
            'api_key',
        ]