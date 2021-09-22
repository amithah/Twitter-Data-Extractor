from django import forms
from .models import Contact
from django.core.validators import validate_email


class ContactForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True,validators=[validate_email])
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea,required=True)

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
