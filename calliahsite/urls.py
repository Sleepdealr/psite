from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(_("article/<slug:slug>/"), views.article, name="article"),
    path("articles/", views.articles, name="articles"),
    path("contact/", views.contact, name="contact"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("<slug:slug>/", views.dbredirect, name="redirect"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
