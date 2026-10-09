from django.urls import path
from .views import InviteAcceptView,InviteCreateView,InviteView,MyRelationshipsView,RelationshipView
urlpatterns=[path("relation-invites",InviteCreateView.as_view()),path("relation-invites/<str:code>",InviteView.as_view()),path("relation-invites/<str:code>/accept",InviteAcceptView.as_view()),path("relationships/<int:pk>",RelationshipView.as_view()),path("me/relationships",MyRelationshipsView.as_view())]
