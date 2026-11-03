import logging
import os

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm

logger = logging.getLogger(__name__)


class StaticProject:
    def __init__(
        self,
        title,
        description,
        image_name,
        tech_stack,
        github_link="",
        huggingface_link="",
        live_link="",
        is_featured=True,
        order=0,
        category="ai",
        badge="Flagship",
        highlights=None,
        short_description="",
    ):
        self.title = title
        self.description = description
        self.short_description = short_description or description
        # Simulate Django ImageField's .url property
        self.image = type('Image', (object,), {'url': f'/static/projects/{image_name}'})()
        self.tech_stack = tech_stack
        self.github_link = github_link
        self.huggingface_link = huggingface_link
        self.live_link = live_link
        self.is_featured = is_featured
        self.order = order
        self.category = category
        self.badge = badge
        self.highlights = highlights or []

    def get_tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]

    def get_primary_tech_list(self):
        return self.get_tech_list()[:4]


class StaticCertificate:
    def __init__(
        self,
        title,
        image_name,
        issuer,
        issue_date="",
        order=0,
        category="research",
        badge="Verified",
        credential_note="",
        verify_url="",
    ):
        self.title = title
        # Simulate Django ImageField's .url property
        self.image = type('Image', (object,), {'url': f'/static/certificates/{image_name}'})()
        self.issuer = issuer
        self.issue_date = issue_date
        self.order = order
        self.category = category
        self.badge = badge
        self.credential_note = credential_note
        self.verify_url = verify_url


def home(request):
    projects = [
        StaticProject(
            title="AI Career Readiness System",
            short_description="Autonomous GenAI platform matching resumes against roles via FAISS vector search, computing ATS readiness scores, and orchestrating interactive AI interviews.",
            description="An intelligent career readiness and skill gap analysis platform powered by GenAI. Analyzes resumes against target roles using FAISS vector search, computes ATS compatibility scores, recommends tailored learning paths, and generates interactive interview preparation using NLP and LLaMA 3.",
            image_name="ceerer_ai_.jpg",
            tech_stack="Python, LangChain, LLaMA 3, Groq API, FAISS, Hugging Face, Gradio, PyPDF",
            huggingface_link="https://huggingface.co/spaces/ishi4/Analysis_your_Next_Step",
            github_link="https://github.com/Ishmal793",
            category="ai",
            badge="Flagship AI Agent",
            highlights=[
                "FAISS vector search & ATS resume compatibility scoring",
                "Automated skill gap breakdown with personalized learning paths",
                "LLaMA 3 integration via Groq API for dynamic interview simulations",
                "Live cloud deployment on Hugging Face Spaces with Gradio UI",
            ],
            order=1,
        ),
        StaticProject(
            title="Business Analytics Dashboard",
            short_description="Interactive Streamlit business intelligence dashboard with executive KPI tracking, revenue forecasting, and customer cohort segmentation.",
            description="Interactive business intelligence dashboard with executive KPI tracking, revenue forecasting, dynamic customer segmentation, and multi-dimensional visualizations built for executive decision-making using Streamlit, Python, and Plotly.",
            image_name="bussiness.jpg",
            tech_stack="Python, Streamlit, Pandas, Plotly, Matplotlib, KPI Analytics",
            github_link="http://github.com/ishmal793/business-dshboard-",
            category="analytics",
            badge="Streamlit BI",
            highlights=[
                "Executive KPI tracking with revenue & trend forecasting",
                "Dynamic interactive charts built with Plotly & Matplotlib",
                "Automated CSV data processing & ETL transformation pipeline",
            ],
            order=2,
        ),
        StaticProject(
            title="Excel Data Analysis & Dashboard Project",
            short_description="Executive performance dashboard utilizing multi-table pivot modeling, dynamic slicers, and automated forecasting formulas.",
            description="Comprehensive enterprise business performance analysis utilizing advanced Excel methodologies: dynamic multi-table pivot models, interactive slicers, KPI dashboards, and custom formulas to extract actionable commercial insights.",
            image_name="excel_projects_.jpg",
            tech_stack="Excel, Pivot Tables, Dynamic Slicers, KPI Dashboards, Financial Modeling",
            github_link="https://github.com/Ishmal793/Excel_projects",
            category="analytics",
            badge="Excel Modeling",
            highlights=[
                "Interactive executive dashboards with dynamic slicers & timeline filters",
                "Multi-table pivot data modeling and automated calculation formulas",
                "Actionable variance analysis and statistical data breakdowns",
            ],
            order=3,
        ),
        StaticProject(
            title="Power BI Business Intelligence Dashboard",
            short_description="Multi-page enterprise Power BI dashboard with DAX calculations and relational star-schema modeling for organizational tracking.",
            description="Designed and deployed enterprise-grade Power BI dashboards to track organizational growth metrics and financial performance. Utilized DAX modeling, relational schema design, and interactive visuals for real-time stakeholder insights.",
            image_name="power_bi.jpg",
            tech_stack="Power BI, DAX Modeling, Star Schema, SQL, Relational Analytics",
            github_link="https://github.com/Ishmal793/BI_projects",
            category="analytics",
            badge="Power BI / DAX",
            highlights=[
                "Custom DAX calculations for Year-over-Year (YoY) performance metrics",
                "Relational star-schema data modeling integrating multiple sources",
                "Cross-filtering dashboards for drill-through operational reporting",
            ],
            order=4,
        ),
        StaticProject(
            title="Django Full-Stack Web Applications",
            short_description="Scalable web apps featuring MTV architectural patterns, relational database models, session management, and secure CRUD APIs.",
            description="A suite of scalable Django web applications including Task Manager, Live Weather Portal, Financial Tracker, and Media Player built to master MTV architecture, SQLite persistence, Django Forms, and RESTful CRUD workflows.",
            image_name="django_projects_.jpg",
            tech_stack="Python, Django 5, SQLite, HTML5, CSS3, CRUD APIs",
            github_link="https://github.com/Ishmal793/Django_projects/tree/main",
            category="web",
            badge="Full-Stack Django",
            highlights=[
                "Modular Django apps implementing robust MTV architectural patterns",
                "Secure user authentication, session state management, and CSRF protection",
                "Clean database models, migrations, and customized admin panel workflows",
            ],
            order=5,
        ),
    ]

    certificates = [
        StaticCertificate(
            title="AI Research Program — Certificate of Completion",
            image_name="ht_tech_ai_research.png",
            issuer="H&T Tech Solutions, Rochester, New York",
            issue_date="2026",
            category="research",
            badge="International Research",
            credential_note="Supervised by Ms. Amna Saba (HOD Software Engineering, IISAT University Gujranwala). Advanced AI modeling, analytical frameworks, and research methodologies.",
        ),
        StaticCertificate(
            title="Certificate of Appreciation — AI Researcher",
            image_name="google_developers_appreciation.png",
            issuer="Google Developers Initiative",
            issue_date="2026",
            category="research",
            badge="Google Initiative",
            credential_note="3-month intensive AI research tenure recognized for technical leadership, research prototypes, and outstanding performance.",
        ),
        StaticCertificate(
            title="ISPR Internship Program Certificate",
            image_name="ispr_internship.png",
            issuer="Inter Services Public Relations (ISPR), Pakistan Armed Forces",
            issue_date="12 Jan 2026 – 20 Feb 2026",
            category="honors",
            badge="National Defense Media",
            credential_note="Completed rigorous internship at ISPR Headquarters under Lt. Gen. Ahmed Sharif Chaudhry. Serial No. 652.",
        ),
        StaticCertificate(
            title="Generative AI Application Developer Certificate",
            image_name="gen_ai_.jpg",
            issuer="UETIANS Lahore Endowment Foundation (HEC NCEAC)",
            issue_date="17 March, 2026",
            category="certifications",
            badge="GenAI Certification",
            credential_note="Authorized by HEC, NCEAC, PakAngels, iCodeGuru, and Aspire Pakistan. Covering LLM pipelines, prompt engineering, and GenAI app development.",
        ),
        StaticCertificate(
            title="Python for Data Science, AI & Development",
            image_name="corserra_ppython_.jpg",
            issuer="Coursera (Authorized by IBM Skills Network)",
            issue_date="16 Dec, 2025",
            category="certifications",
            badge="IBM Authorized",
            credential_note="Comprehensive mastery in Python programming, data structures, REST APIs, web scraping, and machine learning fundamentals.",
        ),
        StaticCertificate(
            title="Foundations of Agent-Based AI Systems",
            image_name="corsera_agent.jpg",
            issuer="Coursera & LearnQuest",
            issue_date="16 Dec, 2025",
            category="certifications",
            badge="Agentic AI",
            credential_note="Foundational architectures for autonomous AI agents, multi-agent coordination, reasoning models, and agent workflows.",
        ),
        StaticCertificate(
            title="Advance Python Programming & Applications",
            image_name="cerificate_navttac.jpg",
            issuer="National Vocational and Technical Training Commission (NAVTTC), Govt of Pakistan",
            issue_date="16 Dec, 2024",
            category="certifications",
            badge="Govt of Pakistan",
            credential_note="National-level technical certification in advanced object-oriented Python, backend architecture, and database integrations.",
        ),
    ]

    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            email_sent = _send_contact_email(contact)
            if email_sent:
                messages.success(
                    request,
                    "Thank you! Your message has been sent successfully. I will get back to you shortly.",
                )
            else:
                messages.warning(
                    request,
                    "Thank you! Your message was received, but email notification could not be dispatched right now.",
                )
            return redirect(reverse("home") + "#contact")
        messages.error(
            request,
            "Please check the form fields and correct any errors before resubmitting.",
        )

    # 5 Clearly Categorized Skill Groups as specifically requested:
    # 1. Programming
    # 2. Backend Development
    # 3. Data Analytics
    # 4. AI & Machine Learning
    # 5. Tools & Platforms
    skill_categories = [
        {
            "name": "Programming",
            "icon": "fas fa-code",
            "skills": [
                {"name": "Python 3", "icon": "fab fa-python", "note": "OOP, Scripts & Automation"},
                {"name": "SQL", "icon": "fas fa-database", "note": "Queries, Joins, Aggregations & Schema"},
                {"name": "DAX", "icon": "fas fa-calculator", "note": "Calculated Columns & Time Intelligence"},
            ],
        },
        {
            "name": "Backend Development",
            "icon": "fas fa-server",
            "skills": [
                {"name": "Django 5", "icon": "fas fa-server", "note": "MTV Architecture, ORM, Forms & Auth"},
                {"name": "SQLite & Databases", "icon": "fas fa-table-cells", "note": "Relational Models, Constraints & Migrations"},
                {"name": "RESTful Integration", "icon": "fas fa-network-wired", "note": "API Consumption & JSON Pipelines"},
                {"name": "HTML5 & Semantic CSS", "icon": "fab fa-html5", "note": "Responsive Layouts & Accessible Markup"},
            ],
        },
        {
            "name": "Data Analytics",
            "icon": "fas fa-chart-line",
            "skills": [
                {"name": "Power BI", "icon": "fas fa-chart-pie", "note": "Interactive Executive Dashboards & Star Schema"},
                {"name": "Advanced Excel", "icon": "fas fa-file-excel", "note": "Pivot Tables, Slicers & Financial Models"},
                {"name": "Pandas & NumPy", "icon": "fas fa-table", "note": "Data Cleaning, Transformation & ETL"},
                {"name": "Plotly & Matplotlib", "icon": "fas fa-chart-area", "note": "Dynamic Statistical & Visual Storytelling"},
                {"name": "Streamlit", "icon": "fas fa-stream", "note": "Analytical Web Applications & Reporting"},
            ],
        },
        {
            "name": "AI & Machine Learning",
            "icon": "fas fa-brain",
            "skills": [
                {"name": "LLaMA 3 & Groq API", "icon": "fas fa-brain", "note": "High-Speed LLM Inference & Processing"},
                {"name": "LangChain", "icon": "fas fa-robot", "note": "Agentic Workflows & Multi-step Chains"},
                {"name": "FAISS Vector Search", "icon": "fas fa-project-diagram", "note": "Dense Semantic Retrieval & ATS Matching"},
                {"name": "Hugging Face", "icon": "fas fa-microchip", "note": "Sentence Transformers & Space Deployments"},
                {"name": "Prompt Engineering", "icon": "fas fa-terminal", "note": "Context Framing, System Prompts & Guardrails"},
            ],
        },
        {
            "name": "Tools & Platforms",
            "icon": "fas fa-toolbox",
            "skills": [
                {"name": "Git & GitHub", "icon": "fab fa-github", "note": "Version Control, Branching & Documentation"},
                {"name": "Docker", "icon": "fab fa-docker", "note": "Containerization & Environment Setup"},
                {"name": "PyMuPDF & PyPDF", "icon": "fas fa-file-pdf", "note": "Document Parsing & Text Extraction"},
                {"name": "Web Scraping", "icon": "fas fa-spider", "note": "Automated Web Data Collection"},
            ],
        },
    ]

    # Flat skill list maintained for backwards compatibility
    skills = [
        {"name": "Python", "icon": "fab fa-python"},
        {"name": "Django", "icon": "fas fa-server"},
        {"name": "SQL", "icon": "fas fa-database"},
        {"name": "Power BI", "icon": "fas fa-chart-pie"},
        {"name": "Excel", "icon": "fas fa-file-excel"},
        {"name": "Pandas", "icon": "fas fa-table"},
        {"name": "Plotly", "icon": "fas fa-chart-area"},
        {"name": "Streamlit", "icon": "fas fa-stream"},
        {"name": "LLaMA 3", "icon": "fas fa-brain"},
        {"name": "FAISS", "icon": "fas fa-project-diagram"},
        {"name": "Git", "icon": "fab fa-github"},
    ]

    experiences = [
        {
            "role": "AI Research Program Participant",
            "company": "H&T Tech Solutions",
            "location": "Rochester, NY, USA (Remote)",
            "date": "2026",
            "badge": "International Research",
            "description": "Participated in an international AI Research Program under the supervision of Ms. Amna Saba (HOD Software Engineering, IISAT University Gujranwala). Worked on emerging artificial intelligence concepts, research methodologies, analytical modeling, and practical GenAI implementations.",
            "tags": ["AI Modeling", "Research Methodologies", "Analytical Frameworks", "GenAI"],
        },
        {
            "role": "AI Researcher",
            "company": "Google Developers Initiative",
            "location": "Remote",
            "date": "3-Month Tenure (2026)",
            "badge": "Google Initiative",
            "description": "Completed an intensive 3-month AI research tenure under Google Developers initiatives. Researched machine learning architectures, evaluated prototype models, and received official Certificate of Appreciation for technical leadership and outstanding performance.",
            "tags": ["AI Research", "Machine Learning", "Python", "Data Science"],
        },
        {
            "role": "Intern — ISPR Internship Program",
            "company": "Inter Services Public Relations (ISPR), Pakistan Armed Forces",
            "location": "Rawalpindi / Islamabad, Pakistan",
            "date": "12 Jan 2026 – 20 Feb 2026",
            "badge": "Armed Forces Media Wing",
            "description": "Selected for the prestigious internship program at ISPR Headquarters under Lt. Gen. Ahmed Sharif Chaudhry. Gained hands-on experience in structured institutional workflows, technical documentation, large-scale information processing, and communication operations (Serial No. 652).",
            "tags": ["Data Processing", "Technical Reporting", "Organizational Operations", "Communication"],
        },
        {
            "role": "Data Analyst Intern",
            "company": "Techohub Data Analytics & AI",
            "location": "Lahore, Pakistan (Remote)",
            "date": "Jul 2024 – Feb 2025",
            "badge": "Industry Internship",
            "description": "Built interactive executive dashboards using Streamlit and Python, automated repetitive data extraction pipelines, cleaned raw multi-source business datasets, and engineered visual KPI tracking models to inform management strategy.",
            "tags": ["SQL", "Power BI", "Pandas", "Streamlit", "Plotly", "Excel"],
        },
    ]

    education = {
        "degree": "Bachelor of Science in Software Engineering (BS SE)",
        "university": "IISAT University (Institute of Information Security & Applied Technology)",
        "location": "Gujranwala, Pakistan",
        "tenure": "Nov 2022 – 2026 (Graduated)",
        "cgpa": "3.7 / 4.0",
        "highlights": [
            "Graduated with High Academic Distinction (CGPA: 3.7 / 4.0)",
            "Specialized in AI Systems, Data Modeling & Backend Engineering",
            "Supervised research by Ms. Amna Saba (HOD Software Engineering)",
            "Core Curriculum: Data Structures, OOP, DBMS, Machine Learning, Web Engineering",
        ],
    }

    context = {
        "projects": projects,
        "certificates": certificates,
        "contact_form": contact_form,
        "skill_categories": skill_categories,
        "skills": skills,
        "experiences": experiences,
        "education": education,
    }
    return render(request, "index.html", context)


def download_cv(request):
    cv_paths = [
        os.path.join(settings.MEDIA_ROOT, "Ishmal_Shahid_CV_.pdf"),
        os.path.join(settings.BASE_DIR, "static", "cv", "Ishmal_Shahid_CV.pdf"),
    ]
    for path in cv_paths:
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return FileResponse(
                open(path, "rb"),
                content_type="application/pdf",
                as_attachment=True,
                filename="Ishmal_Shahid_CV.pdf",
            )
    raise Http404("CV file not found.")


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
        logger.error(f"Error sending email: {e}")
        return False
