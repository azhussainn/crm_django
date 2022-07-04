from django import forms
from .models import Lead


class LeadModelForm(forms.models.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent'
        )