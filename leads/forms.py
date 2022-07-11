from django import forms
from .models import Lead, User, Agent
from django.contrib.auth.forms import UserCreationForm, UsernameField


class LeadModelForm(forms.models.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent'
        )


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = { 'username': UsernameField }


class AssignAgentForm(forms.Form):
    agents = forms.ModelChoiceField(queryset = Agent.objects.none() )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organization__user=request.user)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agents"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )