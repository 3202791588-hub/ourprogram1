from django.urls import include, path
from .views import HealthView

urlpatterns = [
    path("health", HealthView.as_view()),
    path("", include("apps.users.urls")),
    path("", include("apps.tests.urls")),
    path("", include("apps.results.urls")),
    path("", include("apps.relations.urls")),
    path("", include("apps.ads.urls")),
    path("", include("apps.analytics.urls")),
]
