"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from polls import views
# path(): url과 view를 연결하는 설정
# include(): url과 urls.py(app별로 정의한)를 연결하는 설정.
## config/urls.py
urlpatterns = [
    path("", views.welcome_polls, name="welcome"),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    # polls: url이 polls로 시작하면 나머지는 polls/urls.py를 참조해라.
    path('account/', include('account.urls')),
    
    # 파라미터 1: url, 2: 함수, name="설정이름"
    # path('polls/welcome', views.welcome_polls, name="polls_welcome"),
    # http://127.0.0.1:8000/polls/welcome -> welcome_polls()
]

from django.conf.urls.static import static
from . import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# MEDIA_URL 로 요청이 들어오면 MEDIA_ROOT 경로아래서 찾아라. ==> 장고 개발서버에서 설정
# 운영시 web 서버를 사용할 경우 media 파일들의 경로, static 파일들의 경로를 web 서버에 설정해서
## web 서버가 서비스 하도록 한다. (정적파일들은 web 서버에게 담당시킨다.)

# WebServer + WSGI
## Web Server: 정적파일들 서비스
## WSGI: 장고를 실행(view, template, model, ...)
