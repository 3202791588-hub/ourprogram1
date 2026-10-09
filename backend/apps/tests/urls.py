from django.urls import path
from .views import AnswerView,SessionListView,SessionView,SubmitView,TestDetailView,TestListView
urlpatterns=[path("tests",TestListView.as_view()),path("tests/<slug:slug>",TestDetailView.as_view()),path("test-sessions",SessionListView.as_view()),path("test-sessions/<int:pk>",SessionView.as_view()),path("test-sessions/<int:pk>/answers",AnswerView.as_view()),path("test-sessions/<int:pk>/submit",SubmitView.as_view())]
