from django.core.files import File
from django.core.management.base import BaseCommand
from pathlib import Path

from main_app.models import Certificate, Project

BASE_DIR = Path(__file__).resolve().parents[3]
STATIC_IMAGES = BASE_DIR / "static" / "images"


class Command(BaseCommand):
    help = "Seed initial projects and sample certificate placeholders"

    def handle(self, *args, **options):
        projects_data = [
            {
                "title": "AI Career Readiness System",
                "description": (
                    "An intelligent career readiness platform powered by GenAI that "
                    "analyzes skills gaps, recommends learning paths, and generates "
                    "personalized interview preparation using NLP and machine learning."
                ),
                "tech_stack": "Python, Django, GenAI, Streamlit, Pandas, SQL",
                "huggingface_link": "",
                "github_link": "https://github.com",
                "live_link": "",
                "image": "project-ai-career.svg",
                "order": 1,
            },
            {
                "title": "Business Analytics Dashboard",
                "description": (
                    "Interactive business intelligence dashboard with KPI tracking, "
                    "revenue forecasting, and dynamic visualizations built for "
                    "executive decision-making using Power BI and Python analytics."
                ),
                "tech_stack": "Python, Power BI, Pandas, Plotly, Excel, SQL",
                "huggingface_link": "",
                "github_link": "https://github.com",
                "live_link": "",
                "image": "project-analytics.svg",
                "order": 2,
            },
        ]

        for data in projects_data:
            image_name = data.pop("image")
            image_path = STATIC_IMAGES / image_name
            if not image_path.exists():
                self.stdout.write(self.style.WARNING(f"Skip missing image: {image_path}"))
                continue
            project, created = Project.objects.get_or_create(
                title=data["title"],
                defaults=data,
            )
            if created or not project.image:
                with open(image_path, "rb") as f:
                    project.image.save(image_name, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"Project: {project.title}"))

        certificates_data = [
            {
                "title": "Certificate of Appreciation (AI Researcher)",
                "issuer": "Google Developers",
                "issue_date": "3-Month Tenure",
                "image_name": "google_developers_appreciation.png",
                "order": 1,
            },
            {
                "title": "Professional Certificate",
                "issuer": "Industry Certification",
                "issue_date": "2025",
                "image_name": "cert-placeholder.svg",
                "order": 2,
            }
        ]

        for cert_data in certificates_data:
            image_name = cert_data.pop("image_name")
            image_path = STATIC_IMAGES / image_name
            if not image_path.exists():
                self.stdout.write(self.style.WARNING(f"Skip missing cert image: {image_path}"))
                continue
            
            cert, created = Certificate.objects.get_or_create(
                title=cert_data["title"],
                defaults=cert_data,
            )
            if created or not cert.image:
                with open(image_path, "rb") as f:
                    cert.image.save(image_name, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"Certificate: {cert.title}"))

        self.stdout.write(self.style.SUCCESS("Seed complete. Add more via Django admin."))
