from django import forms
from leads.models import Agent
# from django.contrib.auth.forms import UserCreationForm, UsernameField


class AgentModelForm(forms.models.ModelForm):
    class Meta:
        model = Agent
        fields = (
            'user',
        )