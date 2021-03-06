from django import forms
from leads.models import User


class AgentModelForm(forms.models.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )