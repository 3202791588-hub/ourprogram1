from django.urls import path
from .views import AdEventView
urlpatterns=[path("ad-events",AdEventView.as_view())]
