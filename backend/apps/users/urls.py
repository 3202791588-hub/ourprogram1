from django.urls import path
from .views import DeleteMyDataView, MeView, WechatLoginView
urlpatterns=[path("auth/wechat",WechatLoginView.as_view()),path("me",MeView.as_view()),path("me/data",DeleteMyDataView.as_view())]
