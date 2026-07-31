from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 챗봇 화면 요청 url
    path('stream/', views.stream_chat, name='stream_chat'), # chat message 전송 처리.
]
