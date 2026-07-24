from django.contrib import admin

from . import models
# polls/admin.py
# 관리자 앱에서 관리할 모델들을 등록

admin.site.register(models.Question)
admin.site.register(models.Choice)
