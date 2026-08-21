import os

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm


class StaticProject:
    def __init__(self, title, description, image_name, tech_stack, github_link="", huggingface_link="", live_link="", is_featured=True, order=0):
        self.title = title
        self.description = description
        # Simulate Django ImageField's .url property
        self.image = type('Image', (object,), {'url': f'/static/projects/{image_name}'})()
        self.tech_stack = tech_stack
        self.github_link = github_link
        self.huggingface_link = huggingface_link
        self.live_link = live_link
        self.is_featured = is_featured
        self.order = order

    def get_tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]


class StaticCertificate:
    def __init__(self, title, image_name, issuer, issue_date="", order=0):
        self.title = title
        # Simulate Django ImageField's .url property
        self.image = type('Image', (object,), {'url': f'/static/certificates/{image_name}'})()
        self.issuer = issuer
        self.issue_date = issue_date
        self.order = order


def home(request):
    projects = [
        StaticProject(
            title="AI Career Readiness System",
            description="An intelligent career readiness platform powered by GenAI that analyzes skills gaps, recommends learning paths, and generates personalized interview preparation using NLP and machine learning.",
            image_name="ceerer_ai_.jpg",
            tech_stack="Python, Gradio, LangChain, Groq API, LLaMA 3 (LLM Models), PyPDF, Pandas, NLP, Prompt Engineering, Agentic AI Workflows",
            huggingface_link="https://huggingface.co/spaces/ishi4/Analysis_your_Next_Step",
        ),
        StaticProject(
            title="Business Analytics Dashboard",
            description="Interactive business intelligence dashboard with KPI tracking, revenue forecasting, and dynamic visualizations built for executive decision-making using Power BI and Python analytics.",
            image_name="bussiness.jpg",
            tech_stack="Python, Streamlit, Pandas, Plotly, Data Visualization, Data Analysis, CSV Data Processing",
            github_link="http://github.com/ishmal793/business-dshboard-",
        ),
        StaticProject(
            title="Excel Data Analysis & Dashboard Project",
            description="Analyzed and visualized data using Excel by creating interactive dashboards, charts, and pivot tables to extract actionable insights.",
            image_name="excel_projects_.jpg",
            tech_stack="Excel, Data Analysis, Data Visualization, Pivot Tables, Charts, Dashboard Design",
            github_link="https://github.com/Ishmal793/Excel_projects",
        ),
        StaticProject(
            title="Power BI Business Intelligence Dashboard",
            description="Designed and developed a Power BI dashboard to visualize business performance and key KPIs.\nUtilized data modeling and interactive charts to deliver actionable insights for strategic decision-making.",
            image_name="power_bi.jpg",
            tech_stack="Power BI, Data Visualization, Business Intelligence, DAX, Data Modeling, Excel, SQL, Analytics",
            github_link="https://github.com/Ishmal793/BI_projects",
        ),
        StaticProject(
            title="Django Web Development Projects",
            description="Multiple Django web apps including To-Do, Weather, Finance, and Music Player built for learning backend development and CRUD operations.",
            image_name="django_projects_.jpg",
            tech_stack="Python, Django, SQLite, HTML, CSS",
            github_link="https://github.com/Ishmal793/Django_projects/tree/main",
        )
    ]

    certificates = [
        StaticCertificate(
            title="Advance Python Programming & Applications",
            image_name="cerificate_navttac.jpg",
            issuer="National Vocational and Technical Training Commission, Government of Pakistan",
            issue_date="16 Dec 2024",
        ),
        StaticCertificate(
            title="Foundations of Agent-Based AI Systems",
            image_name="corsera_agent.jpg",
            issuer="Coursera (online learning platform) in collaboration with LearnQuest (professional IT training provider)",
            issue_date="16 Dec, 2025",
        ),
        StaticCertificate(
            title="Python for Data Science, AI & Development",
            image_name="corserra_ppython_.jpg",
            issuer="Coursera (Authorized by IBM) – IBM Skills Network course completion certificate",
            issue_date="16 Dec, 2025",
        ),
        StaticCertificate(
            title="Generative AI Application Developer Certificate",
            image_name="gen_ai_.jpg",
            issuer="UETIANS Lahore Endowment Foundation (NCEAC, HEC, PAkAngels, iCodeGuru, Aspire Pakistan)",
            issue_date="17 March, 2026",
        )
    ]

    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Save the form in-memory (commit=False) without writing to any database
            contact = contact_form.save(commit=False)
            email_sent = _send_contact_email(contact)
            if email_sent:
                messages.success(
                    request,
                    "Thank you! Your message has been sent successfully.",
                )
            else:
                messages.warning(
                    request,
                    "Thank you! Your message was received, but we couldn't send an email notification at this time.",
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
