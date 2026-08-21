import os

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm
from .models import Certificate, Project


def home(request):
    projects = Project.objects.filter(is_featured=True)
    certificates = Certificate.objects.all()
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save()
            email_sent = _send_contact_email(contact)
            if email_sent:
                messages.success(
                    request,
                    "Thank you! Your message has been sent successfully.",
                )
            else:
                messages.warning(
                    request,
                    "Thank you! Your message has been saved, but we couldn't send an email notification at this time.",
                )
            return redirect(reverse("home") + "#contact")
        messages.error(
            request,
            "Please correct the errors below and try again.",
        )

    skills = [
        {"name": "Python", "icon": "fab fa-python"},
        {"name": "Django", "icon": "fas fa-server"},
        {"name": "SQL", "icon": "fas fa-database"},
        {"name": "GenAI", "icon": "fas fa-robot"},
        {"name": "HTML", "icon": "fab fa-html5"},
        {"name": "CSS", "icon": "fab fa-css3-alt"},
        {"name": "Power BI", "icon": "fas fa-chart-pie"},
        {"name": "Excel", "icon": "fas fa-file-excel"},
        {"name": "Pandas", "icon": "fas fa-table"},
        {"name": "Plotly", "icon": "fas fa-chart-area"},
        {"name": "Streamlit", "icon": "fas fa-stream"},
    ]

    context = {
        "projects": projects,
        "certificates": certificates,
        "contact_form": contact_form,
        "skills": skills,
    }
    return render(request, "index.html", context)


def download_cv(request):
    cv_path = os.path.join(settings.MEDIA_ROOT, "Ishmal_Shahid_CV_.pdf")
    if not os.path.exists(cv_path):
        raise Http404("CV file not found.")
    response = FileResponse(
        open(cv_path, "rb"),
        content_type="application/pdf",
        as_attachment=True,
        filename="Ishmal_Shahid_CV.pdf",
    )
    return response


def _send_contact_email(contact):
    recipient = getattr(
        settings,
        "CONTACT_RECIPIENT_EMAIL",
        "ishishahid4@gmail.com",
    )
    subject = f"Portfolio Contact: {contact.name}"
    body = (
        f"Name: {contact.name}\n"
        f"Email: {contact.email}\n\n"
        f"Message:\n{contact.message}"
    )
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[contact.email],
    )
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error sending email: {e}")
        return False
