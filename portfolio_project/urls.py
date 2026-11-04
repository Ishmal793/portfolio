from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from main_app import views as main_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", main_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", main_views.sitemap_xml, name="sitemap_xml"),
    path("", include("main_app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
