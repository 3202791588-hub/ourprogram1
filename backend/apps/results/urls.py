from django.urls import path
from .views import FullView,MyResultsView,PreviewView,UnlockView
urlpatterns=[path("results/<int:pk>/preview",PreviewView.as_view()),path("results/<int:pk>/full",FullView.as_view()),path("results/<int:pk>/unlock",UnlockView.as_view()),path("me/results",MyResultsView.as_view())]
