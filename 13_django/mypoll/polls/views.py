from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# 모델 클래스  import
from .models import Question, Choice



# View 함수 정의 - URL Conf에 등록(url mapping)
## URL Conf: 요청URL과 View함수를 mapping 하는 파일.
## config/settings.py -> ROOT_URLCONF 에 설정된 파일.

# 설문 웰컴 페이지응답하는 View함수
def welcome_polls_backup(request):
    now = datetime.now() # 실행시점 일시
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # 응답페이지를 생성
    res_html = f"""<!doctype html>
<html>
    <head>
        <title>Polls - Welcome</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>저희 설문 페이지에 방문해 주셔서 감사합니다.</p>
        현재 시간: {now_str}
    </body>
</html>
"""
    print("polls/welcome 실행")
    return HttpResponse(res_html)


def welcome_polls(request):
    now = datetime.now() # 실행시점 일시
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # 응답 -> polls/welcome.html 템플릿 호출 -> html string
    ## template을 호출하는 함수 -> render()
    res_html = render(
        request, # request
        "polls/welcome.html", # 템플릿 파일 경로(app/templates 빼고 나머지 경로)
        {"now":now_str}# context-value를 dictionary 설정. -> View가 Template에게 전달하는 값(객체)
    )
    print(res_html) # HttpResponse
    return res_html

##########################################
# 설문 목록 조회
## 전체 question들을 조회해서 목록으로 출력
## 요청 url:  polls/list
## View 함수: vote_list
## template: polls/vote_list.html
##########################################
# View함수 파라미터: 1 - request: HttpRequest 객체(HTTP 요청정보)를 받는 변수(필수)
#                   2 부터 - path 파라미터를 받기 위한 변수들.(옵션)
def vote_list(request):
    # DB에서 Question들을 조회
    question_list = Question.objects.all().order_by("-pub_date")
    # QuerySet [M, M, M]
    # 응답화면 - Conext Value로 question_list를 전달.
    return render(
        request, "polls/vote_list.html", {"question_list":question_list}
    )

###############################################
# 설문폼 페이지를 응답하는 View
## 요청 URL: /polls/vote_form/question_id
## view함수: vote_form
## template: polls/vote_form.html
#
# question_id로 질문과 그 질문의 보기를 조회
## question_id를 Path Parameter 로 받는다.
## Path Parameter: url 경로를 이용해서 클라이언트가 서버에 값을 전달하는 방식
# View의 두번째 파라미터 부터 path paramter를 받을 변수들.
## url conf에서 path parameter와 변수를 연결.
###############################################

def vote_form(request, question_id):
    # question_id의 질문, 그 질문의 choice들을 조회
    try:
        question = Question.objects.get(pk=question_id)
        choice_list = question.choice_set.all()
        return render(
            request, 
            "polls/vote_form.html",
            {"question":question, "choice_list":choice_list}
        )
    except:
        return render(
            request, 
            "polls/error.html", 
            {"error_message": f"{question_id}번 질문은 없는 질문 입니다."}
        )

##############################################
# 설문 처리
## vote_form에서 선택한 보기의 vote값을 1 증가
## 투표 결과를 보여주는 화면을 응답.
#
## 요청 URL: /polls/vote
## view함수: vote
## 응답    : 정상 - polls/vote_result.html
##           오류 - polls/vote_form.html (보기를 선택하지 않고 투표한 경우)
##############################################
# 요청파라미터를 조회
## GET : request.GET: Dictionary로 요청파라미터를 반환.
## POST: request.POST:Dictionary로 요청파라미터를 반환.

def vote(request):
    # choice 를 조회
    choice_id = request.POST.get("choice")
    question_id = request.POST.get("question_id")

    if choice_id != None: # 선택된 보기가 넘어온 경우.
        # choice.vote += 1
        choice = Choice.objects.get(pk=choice_id)
        choice.vote += 1
        choice.save() # update 쿼리 실행.

        # vote_result.html 로 이동
        ## Question과 choice들을 조회
        question = Question.objects.get(pk=question_id)
        choice_list = question.choice_set.all()
        return render(
            request, 
            "polls/vote_result.html", 
            {"question":question, "choice_list":choice_list}
        )



    else: # 보기를 선택하지 않고 투표한 경우.
        pass