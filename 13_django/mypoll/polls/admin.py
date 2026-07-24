from django.contrib import admin

# Register your models here.
# 관리자앱에서 관ㄹ이할 모델들을 둥록

from . import models
admin.site.register(models.Question)
admin.site.register(models.Choice)