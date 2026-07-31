from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# 사용자 정의 UserAdmin 정의
## 관리자 앱에서 User의 어떤 항목(Field)들을 관리할지 정의
## UserAdmin을 상속받아서 구현하며, register()에 UserModel과 함께 전달.

## Class변수로 Field들을 정의
### list_display: list - 사용자 메인화면에서 사용자목록에 보여줄 항목들
### add_fieldsets: tuple - 등록화면에 나올 항목(Field)들을 정의
### fieldsets: tuple - 수정화면에 나올 항목들을 정의 (형식은 add_fieldsets와 동일)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "name", "email"]
    # ("카테고리이름", {"fields": (Field이름, ..)})
    add_fieldsets = (
        ("인증정보", {"fields":("username", "password1", "password2")}),
        ("개인정보", {"fields": ("name", "email", "birthday")}),
        ("권한", {"fields": ("is_staff", "is_active")})
    )
    fieldsets = (
        ("인증정보", {"fields":("username", "password")}),
        ("개인정보", {"fields": ("name", "email", "birthday")}),
        ("권한", {"fields": ("is_staff", "is_active", "is_superuser")})
    )






admin.site.register(CustomUser, CustomUserAdmin)