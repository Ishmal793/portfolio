from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Anti-spam Honeypot field (hidden from legitimate users, filled by bots)
    website_hp = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "d-none",
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
            }
        ),
    )

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
                    "aria-label": "Full Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control input-field",
                    "placeholder": "name@domain.com",
                    "id": "id_email",
                    "required": True,
                    "autocomplete": "email",
                    "aria-label": "Email Address",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control input-field input-textarea",
                    "placeholder": "Describe your project, position requirements, or inquiry...",
                    "id": "id_message",
                    "rows": 5,
                    "required": True,
                    "aria-label": "Message Content",
                }
            ),
        }
