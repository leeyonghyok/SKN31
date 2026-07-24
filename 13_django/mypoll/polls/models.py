from django.db import models

# 모델 클래스들을 정의 - Question(설문과 질문), Choice(설문 보기)
## -Miodel을 상속
## - class이름: 단수형
## - class변수로 Field들을 정의.(Field - Table의 컬럼)
### - field: 필드이름(컬럼이름, instance변수 이름) = field객체(컬럼 설정)
## - primary key field 가 없으면 자동으로 생성
### - Field명: id, type: 양의 정수, 1씩 자동 증가
### - 특정 field를 pk로 설정하려면 `xxxField(primary_key=True)`로 설정`

# Question Model class 정의
class Question(models.Model): # create table question(
                              
    # 질문 문장                          
    question_text = models.CharField(max_length=200) # question_text, varchar(2000)
    # 질문 등록 일시
    pub_date = models.DateTimeField(auto_now_add=True) # pub_date datetime
    # auto_now_add = True: insert 시점의 일시를 자동으로 입력

    def __str__(self):
        return f"{self.pk}. {self.question_text}"
        # self.pk: Primary Key Field의 값을 조회.

# Choice 모델 클래스
class Choice(models.Model):
                              
                  
    choice_text = models.CharField(max_length=200) 
    
    vote = models.PositiveBigIntegerField(default=0) 
    question = models.ForeignKey(
        Question, # 참조 mODEL 클래스
        on_delete=models.CASCADE # 부모 데이터서 삭제되면 같이 삭제.
    )
    def __str__(self):
            return f"{self.pk}. {self.choice_text}"
            

# 모델 클래스를 최초 생성, 수정한 경우 Database 적용
# 1. python manage.py makemigrations [app 이름] # app 이름을 주면 그 app에만 적용
#    - DB에 적용할 것들을 코드로 작성
# 2. python manage.py migrate # DB에 적용
# 데이터 이름: app이름_class이름(polls_question)
