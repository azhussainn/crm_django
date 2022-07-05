from django import forms
from .models import Lead, User
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

class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    age = forms.IntegerField(min_value=0)


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = { 'username': UsernameField }
