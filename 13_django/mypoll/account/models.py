# account/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# AbstractUser는 기존 UserModel을 사용할 수 있도록 제공하는 클래스.
# 1. AbstractUser 상속
# 2. 기존 Field들에 **추가할 Field들을 정의** (name, birthday)

class CustomUser(AbstractUser):

    name = models.CharField(
        max_length=100,
        verbose_name="이름" # Form 관련 설정(Label). - ModelForm과 연결할 Model의 경우.
    )
    birthday = models.DateField( # DB: date타입, python: datetime.date
        null=True, # Nullable(Null허용) 컬럼 (default: False - Not Null)
        blank=True, # Form 설정: (입력폼에서) required=False
        verbose_name="생일", # Form 설정
    )
    # 프로필사진
    profile_img = models.ImageField(
        verbose_name="프로필 사진",
        null=True, 
        blank=True,
        upload_to="images/profile",
        # MEDIA_ROOT 디렉토리 아래 어디에 저장할 지 경로 지정
    )
    # 일반파일 - 저장디렉토리를 "날짜별로 생성"
    upfile = models.FileField(
        verbose_name="업로드 파일",
        null=True,
        blank=True,
        upload_to="upfile/%Y/%m/%d"
        # media/upfile/2026/07/31/파일
    )
    # 모델 변경 -> DB에 적용
    # python manage.py makemigrations
    # python manage.py migrate

    def __str__(self):
        return f"{self.pk}. {self.username}-{self.name}" # 1. myid-홍길동

