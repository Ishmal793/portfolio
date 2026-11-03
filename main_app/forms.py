from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control input-field",
                    "placeholder": "Your full name or organization",
                    "id": "id_name",
                    "required": True,
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control input-field",
                    "placeholder": "name@domain.com",
                    "id": "id_email",
                    "required": True,
                    "autocomplete": "email",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control input-field input-textarea",
                    "placeholder": "Describe your project, position requirements, or inquiry...",
                    "id": "id_message",
                    "rows": 5,
                    "required": True,
                }
            ),
        }
