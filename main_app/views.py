import logging
import os

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import FileResponse, Http404, HttpResponse
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
        badge="Featured Project",
        highlights=None,
        short_description="",
        impact="",
        is_initial=True,
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
        self.impact = impact
        self.is_initial = is_initial

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
        badge="Certificate",
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
            badge="Featured Project",
            impact="<!-- TODO: add real result metric (e.g. processed 500+ resumes / reduced screening time by 40%) --> Impact: [TODO: Add key metric, e.g. evaluated 500+ resumes with <2s inference]",
            highlights=[
                "FAISS vector search & ATS resume compatibility scoring",
                "Automated skill gap breakdown with personalized learning paths",
                "LLaMA 3 integration via Groq API for dynamic interview simulations",
                "Live cloud deployment on Hugging Face Spaces with Gradio UI",
            ],
            order=1,
            is_initial=True,
        ),
        StaticProject(
            title="Business Analytics Dashboard",
            short_description="Interactive Streamlit business intelligence dashboard with executive KPI tracking, revenue forecasting, and customer cohort segmentation.",
            description="Interactive business intelligence dashboard with executive KPI tracking, revenue forecasting, dynamic customer segmentation, and multi-dimensional visualizations built for executive decision-making using Streamlit, Python, and Plotly.",
            image_name="bussiness.jpg",
            tech_stack="Python, Streamlit, Pandas, Plotly, Matplotlib, KPI Analytics",
            github_link="http://github.com/ishmal793/business-dshboard-",
            category="analytics",
            badge="Business Analytics",
            impact="<!-- TODO: add real result metric (e.g. automated monthly sales reporting across 10k+ rows) --> Impact: [TODO: Add key metric, e.g. automated monthly sales reporting across 10k+ rows]",
            highlights=[
                "Executive KPI tracking with revenue & trend forecasting",
                "Dynamic interactive charts built with Plotly & Matplotlib",
                "Automated CSV data processing & ETL transformation pipeline",
            ],
            order=2,
            is_initial=True,
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
            impact="<!-- TODO: add real result metric (e.g. consolidated 5 departmental data sources into 1 live dashboard) --> Impact: [TODO: Add key metric, e.g. consolidated 5 departmental data sources into 1 live dashboard]",
            highlights=[
                "Custom DAX calculations for Year-over-Year (YoY) performance metrics",
                "Relational star-schema data modeling integrating multiple sources",
                "Cross-filtering dashboards for drill-through operational reporting",
            ],
            order=3,
            is_initial=True,
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
            impact="<!-- TODO: add real result metric (e.g. modeled multi-year financial forecasting and variance tracking) --> Impact: [TODO: Add key metric, e.g. modeled multi-year financial forecasting and variance tracking]",
            highlights=[
                "Interactive executive dashboards with dynamic slicers & timeline filters",
                "Multi-table pivot data modeling and automated calculation formulas",
                "Actionable variance analysis and statistical data breakdowns",
            ],
            order=4,
            is_initial=False,
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
            impact="<!-- TODO: add real result metric (e.g. deployed 4 modular web apps with authentication and database persistence) --> Impact: [TODO: Add key metric, e.g. deployed 4 modular web apps with authentication and database persistence]",
            highlights=[
                "Modular Django apps implementing robust MTV architectural patterns",
                "Secure user authentication, session state management, and CSRF protection",
                "Clean database models, migrations, and customized admin panel workflows",
            ],
            order=5,
            is_initial=False,
        ),
    ]

    certificates = [
        StaticCertificate(
            title="AI Research Program — Certificate of Completion",
            image_name="ht_tech_ai_research.png",
            issuer="H&T Tech Solutions, Rochester, New York",
            issue_date="2026",
            category="research",
            badge="Research",
            credential_note="Supervised by Ms. Amna Saba (HOD Software Engineering, International Institute of Science, Art and Technology - IISAT Gujranwala). Advanced AI modeling and research methodologies.",
        ),
        StaticCertificate(
            title="Certificate of Appreciation — AI Researcher",
            image_name="google_developers_appreciation.png",
            issuer="Google Developers Initiative",
            issue_date="2026",
            category="research",
            badge="Research",
            credential_note="3-month intensive AI research tenure recognized for technical leadership, research prototypes, and performance.",
        ),
        StaticCertificate(
            title="ISPR Internship Program Certificate",
            image_name="ispr_internship.png",
            issuer="Inter Services Public Relations (ISPR), Pakistan Armed Forces",
            issue_date="Jan 2026 – Feb 2026",
            category="honors",
            badge="Internship",
            credential_note="Completed structured internship at ISPR Headquarters under Lt. Gen. Ahmed Sharif Chaudhry (Serial No. 652).",
        ),
        StaticCertificate(
            title="Generative AI Application Developer Certificate",
            image_name="gen_ai_.jpg",
            issuer="UETIANS Lahore Endowment Foundation (HEC NCEAC)",
            issue_date="March 2026",
            category="certifications",
            badge="Certification",
            credential_note="Authorized by HEC, NCEAC, PakAngels, iCodeGuru, and Aspire Pakistan. Covering LLM pipelines and GenAI application development.",
        ),
        StaticCertificate(
            title="Python for Data Science, AI & Development",
            image_name="corserra_ppython_.jpg",
            issuer="Coursera (Authorized by IBM Skills Network)",
            issue_date="Dec 2025",
            category="certifications",
            badge="Certification",
            credential_note="Mastery in Python programming, data structures, REST APIs, web scraping, and machine learning fundamentals.",
        ),
        StaticCertificate(
            title="Foundations of Agent-Based AI Systems",
            image_name="corsera_agent.jpg",
            issuer="Coursera & LearnQuest",
            issue_date="Dec 2025",
            category="certifications",
            badge="Certification",
            credential_note="Architectures for autonomous AI agents, multi-agent coordination, reasoning models, and agent workflows.",
        ),
        StaticCertificate(
            title="Advance Python Programming & Applications",
            image_name="cerificate_navttac.jpg",
            issuer="National Vocational and Technical Training Commission (NAVTTC), Govt of Pakistan",
            issue_date="Dec 2024",
            category="certifications",
            badge="Certification",
            credential_note="Technical certification in object-oriented Python, backend architecture, and database integrations.",
        ),
    ]

    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Anti-spam Honeypot Check
            if contact_form.cleaned_data.get("website_hp"):
                logger.info("Spam bot submission caught via honeypot.")
                return redirect(reverse("home") + "#contact")

            contact = contact_form.save(commit=False)
            email_sent = _send_contact_email(contact)
            if email_sent:
                messages.success(
                    request,
                    "Thank you! Your message has been sent successfully. I will get back to you shortly.",
                )
            else:
                messages.info(
                    request,
                    "Thank you! Your inquiry was logged and received. I will review it shortly.",
                )
            return redirect(reverse("home") + "#contact")
        messages.error(
            request,
            "Please check the form fields and correct any errors before resubmitting.",
        )

    # 5 Balanced Skill Groups
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
                {"name": "Power BI", "icon": "fas fa-chart-pie", "note": "Interactive Dashboards & Data Modeling"},
                {"name": "Advanced Excel", "icon": "fas fa-file-excel", "note": "Pivot Tables, Slicers & Financial Models"},
                {"name": "Pandas & NumPy", "icon": "fas fa-table", "note": "Data Cleaning, Transformation & ETL"},
                {"name": "Plotly & Matplotlib", "icon": "fas fa-chart-area", "note": "Statistical & Visual Storytelling"},
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

    # Reverse-chronological experience (latest first) with consistent date formatting
    experiences = [
        {
            "role": "Intern — Systems & Media Workflows",
            "company": "Inter Services Public Relations (ISPR), Pakistan Armed Forces",
            "location": "Rawalpindi / Islamabad, Pakistan",
            "date": "Jan 2026 – Feb 2026",
            "badge": "Internship",
            "description": "Selected for the structured internship program at ISPR Headquarters under Lt. Gen. Ahmed Sharif Chaudhry. Gained hands-on experience in structured institutional workflows, technical documentation, large-scale information processing, and communication operations (Serial No. 652).",
            "tags": ["Data Processing", "Technical Reporting", "Organizational Operations", "Communication"],
        },
        {
            "role": "AI Research Program Participant",
            "company": "H&T Tech Solutions",
            "location": "Rochester, NY, USA (Remote)",
            "date": "Jan 2026 – Mar 2026",
            "badge": "Research",
            "description": "Participated in an international AI Research Program under the supervision of Ms. Amna Saba (HOD Software Engineering, IISAT University Gujranwala). Worked on emerging artificial intelligence concepts, research methodologies, analytical modeling, and practical GenAI implementations.",
            "tags": ["AI Modeling", "Research Methodologies", "Analytical Frameworks", "GenAI"],
        },
        {
            "role": "AI Researcher",
            "company": "Google Developers Initiative",
            "location": "Remote",
            "date": "3-Month Tenure (2026)",
            "badge": "Research",
            "description": "Completed an intensive 3-month AI research tenure under Google Developers initiatives. Researched machine learning architectures, evaluated prototype models, and received official Certificate of Appreciation for technical leadership and outstanding performance.",
            "tags": ["AI Research", "Machine Learning", "Python", "Data Science"],
        },
        {
            "role": "Data Analyst",
            "company": "Techohub Data Analytics & AI",
            "location": "Lahore, Pakistan (Remote)",
            "date": "Jul 2024 – Feb 2025",
            "badge": "Industry Role",
            "description": "Data Analyst (July 2024 – Feb 2025), first 3 months as intern. Built interactive executive dashboards using Streamlit and Python, automated repetitive data extraction pipelines, cleaned raw multi-source business datasets, and engineered visual KPI tracking models to inform management strategy.",
            "tags": ["Python", "SQL", "Streamlit", "Power BI", "Pandas", "Plotly"],
        },
    ]

    # Education: CGPA 3.7 and 88.1 score kept here exclusively to remove redundancy
    education = {
        "degree": "Bachelor of Science in Software Engineering (BS SE)",
        "university": "International Institute of Science, Art and Technology (IISAT)",
        "location": "Gujranwala, Pakistan",
        "tenure": "Nov 2022 – 2026 (Graduated)",
        "cgpa": "3.7 / 4.0",
        "highlights": [
            "Graduated with Academic Distinction (CGPA: 3.7 / 4.0)",
            "Specialized in AI Systems, Data Modeling & Backend Engineering",
            "Supervised research by Ms. Amna Saba (HOD Software Engineering)",
            "Core Curriculum: Data Structures, OOP, DBMS, Machine Learning, Web Engineering",
            "National Skills Test Score: 88.1 (Issuing Body: [TODO: Add official issuing body and test name])",
        ],
    }

    context = {
        "projects": projects,
        "certificates": certificates,
        "contact_form": contact_form,
        "skill_categories": skill_categories,
        "experiences": experiences,
        "education": education,
    }
    return render(request, "index.html", context)


def download_cv(request):
    cv_paths = [
        os.path.join(settings.BASE_DIR, "static", "cv", "Ishmal_Shahid_CV.pdf"),
        os.path.join(settings.MEDIA_ROOT, "Ishmal_Shahid_CV_.pdf"),
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


def robots_txt(request):
    site_url = getattr(settings, "SITE_URL", "https://portfolio-website.vercel.app")
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {site_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    site_url = getattr(settings, "SITE_URL", "https://portfolio-website.vercel.app")
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site_url}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{site_url}/download-cv/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""
    return HttpResponse(content.strip(), content_type="application/xml")


def _send_contact_email(contact):
    recipient = getattr(settings, "CONTACT_RECIPIENT_EMAIL", "ishishahid4@gmail.com")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "portfolio@example.com")
    subject = f"Portfolio Message from {contact.name}"
    body = f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}\n"
    try:
        email = EmailMessage(subject=subject, body=body, from_email=from_email, to=[recipient], reply_to=[contact.email])
        email.send(fail_silently=False)
        return True
    except Exception as exc:
        logger.warning("Could not dispatch email notification for contact message from %s: %s", contact.email, exc)
        return False
