# polls/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import transaction
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
# 로그인 해야지만 처리할 수 있는 view함수에 붙이는 decorator. 로그인이 안된 상태로 요청이 
# 들어오면 로그인 화면으로 이동(이동할 URL은 settings.py에 LOGIN_URL 변수에 설정)시킨다. 

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
def vote_list_backup(request):  #######Paging 처리 전#######
    # DB에서 Question들을 조회
    question_list = Question.objects.all().order_by("-pub_date")
    # QuerySet [M, M, M]
    # 응답화면 - Conext Value로 question_list를 전달.
    return render(
        request, "polls/vote_list.html", {"question_list":question_list}
    )

################################################################################################
# vote_list: Paging 처리 
#
# context value:
## 현재 페이지의 데이터: Page객체 : question_list
## 현재 페이지가 속한 페이지그룹의 시작/종료 page 번호: page_range
## 페이지 그룹의 시작페이지가 이전페이지가 있는지 여부와 이전페이지 번호:
#                                                    has_previous, previous_page_number
## 페이지 그룹의 마지막페이지가 다음페이지가 있는지 여부와 다음페이지 번호:
#                                                    has_next, next_page_number
#
# 요청 url: polls/list?page=페이지번호  (page가 생략되면 첫번째 페이지를 출력)
################################################################################################
def vote_list(request):
    pagenate_by = 10      # 한 페이지에 보여줄 데이터의 개수
    page_group_count = 10 # 한 페이지그룹에 속한 페이지 개수

    current_page = int(request.GET.get("page", 1))# 현재 응답할 페이지

    # DB 조회 -> Paginator생성
    q_list = Question.objects.all().order_by("-pk") # 최신 등록 질문순으로 조회
    pn = Paginator(q_list, pagenate_by)

    # 현재 페이지가 속한 페이지그룹의 시작/종료 페이지 번호를 조회
    start_index = int((current_page-1)/page_group_count) * page_group_count
    end_index = start_index + page_group_count
    page_range = pn.page_range[start_index : end_index]

    # 현재페이지의 데이터들
    question_list = pn.page(current_page)

    context_value = {
        "page_range": page_range,
        "question_list": question_list,
    }

    # 페이지그룹의 시작페이지가 **이전페이지**가 있는지 여부, 있다면 이전페이지 번호
    # 페이지그룹의 마지막페이지가 다음페이지가 있는지 여부, 있다면 다음페이지 번호
    start_page = pn.page(page_range[0]) # 시작페이지의 Page객체
    end_page = pn.page(page_range[-1])  # 끝 페이지의 Page객체
    
    if start_page.has_previous():
        context_value['has_previous'] = True
        context_value['previous_page_number'] = start_page.previous_page_number()

    if end_page.has_next():
        context_value['has_next'] = True
        context_value['next_page_number'] = end_page.next_page_number()

    return render(
        request, "polls/vote_list.html", context_value
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

##################################################################################
# 설문 처리
## vote_form에서 선택한 보기의 vote값을 1 증가
## 투표 결과를 보여주는 화면을 응답.
#
## 요청 URL: /polls/vote
## view함수: vote
## 응답    : 정상 - polls/vote_result.html -> vote_result View로 redirect방식으로 이동
##           오류 - polls/vote_form.html (보기를 선택하지 않고 투표한 경우)
##################################################################################
# 요청파라미터를 조회
## GET : request.GET: Dictionary로 요청파라미터를 반환.
## POST: request.POST:Dictionary로 요청파라미터를 반환.

def vote(request):
    # choice 를 조회
    choice_id = request.POST.get("choice")
    question_id = request.POST.get("question_id")

    ##############################################################
    # 사용자가 이미 투표한 적이 있으면 투표를 못하게 하기 - 쿠키이용
    #
    #  - 예제용. 실제는 DB에 저장. (사용자가 어떤 문제들을 투표했는지 DB에 저장 후 검색)
    # -----------------------------
    # 쿠키에 투표한 질문들 id들을 저장한다.
    #  현재 투표하려는 질문의 id가 cookie에 있으면 투표하지 못하게 한다.
    ##############################################################
    # 쿠키에 현재 질문 ID가 있는지 확인.
    voted_question_ids = request.COOKIES.get("voted_question_ids") #value: "1,6,7,10"
    print(voted_question_ids)
    if voted_question_ids:
        if question_id in voted_question_ids.split(","): # 이미 투표한 질문
            # vote_form.html로 이동
            question = Question.objects.get(pk=question_id)
            choice_list = question.choice_set.all()
            return render(
                request, 
                "polls/vote_form.html", 
                {"question":question, "choice_list":choice_list, 
                                      "error_message":"이미 투표한 질문입니다."}
            )


    if choice_id != None: # 선택된 보기가 넘어온 경우.
        # choice.vote += 1
        choice = Choice.objects.get(pk=choice_id)
        choice.vote += 1
        choice.save() # update 쿼리 실행.

        ######################################################
        # (투표처리 종료) -> 현재 사용자가 투표한 질문 -> cookie에 등록
        ######################################################
        # cookie에 저장할 value 생성
        voted_question_ids = str(question_id) if not voted_question_ids else f"{voted_question_ids},{question_id}"


        # Redirect 방식으로 vote_result View로 이동
        ## Web Browser에게 결과를 보여주는 View로 이동하도록 요청. 그래서 새로고침을 하더라도
        ##   투표가 다시 되는 것을 막도록 한다.

        # url = "/polls/vote_result/"+str(question_id) # redirect할 URL
        # urls.py 의 설정된 URL을 조회 -> reverse(url mapping 설정이름)
        # url mapping 설정이름: app_name:설정name
        url = reverse("polls:vote_result", args=[question_id]) # path paramter: args에 순서대로 입력
        print(">>>>>>> reverse url:", url)
        res =  redirect(url) # 응답상태코드가 302인 HttpResponse를 반환.

        #################################
        #  HttpResponse에 cookie setting
        #################################
        res.set_cookie("voted_question_ids", voted_question_ids,
                        max_age=60*60*24*365   # 쿠키 만료 기간 "초" 설정.
                      )
        return res

        # vote_result.html 로 이동
        ## Question과 choice들을 조회
        # question = Question.objects.get(pk=question_id)
        # choice_list = question.choice_set.all()
        # return render(
        #     request, 
        #     "polls/vote_result.html", 
        #     {"question":question, "choice_list":choice_list}
        # )



    else: # 보기를 선택하지 않고 투표한 경우.
        # vote_form.html 로 이동. 
        # context value: Question과 그 choice들 + Error Message
        question = Question.objects.get(pk=question_id)
        choice_list = question.choice_set.all()
        return render(
            request, 
            "polls/vote_form.html", 
            {"question":question, "choice_list":choice_list, "error_message":"보기를 선택하고 투표하세요."}
        )


##############################################
# 투표 결과를 보여주는 View
#
# 요청URL: polls/vote_result/<int:question_id>
# View함수: vote_result
# 응답Template: polls/vote_result.html
##############################################
def vote_result(request, question_id):
    question = Question.objects.get(pk=question_id)
    choice_list = question.choice_set.all()
    return render(
        request, 
        "polls/vote_result.html", 
        {"question":question, "choice_list":choice_list}
    )


######################################################################
# 설문 질문 등록
#
# 요청 URL: /polls/vote_create
# View함수: vote_create
##          요청방식: GET - 등록 폼을 응답
##                   POST - 등록 처리 
# 응답: GET - polls/vote_create.html (template)
#       POST- redirect => vote_list View를 요청 (질문목록으로 이동)
######################################################################
# HTTP 요청방식을 조회: request.method (GET, POST, ..)

def vote_create_old(request):
    http_method = request.method
    print(">>>>>> Vote Create: ", http_method)

    if http_method == "GET":
        # 등록폼 template 응답
        return render(request, "polls/vote_create.html")
    elif http_method == "POST":
        # 등록 처리
        ## 1. 요청파라미터들 조회, 검증
        ## 2. 처리 -> DB insert
        ## 3. 응답

        # 요청파라미터 조회 - request.GET, request.POST dictionary 구현체
        ## 조회메소드: get(이름)-조회결과가 한개인 경우. return: str
        ##            getlist(이름)-하나의 이름으로 여러개 값이 넘어오는 경우. return list[str]
        question_text = request.POST.get('question_text') # str
        choice_list = request.POST.getlist('choice_text') # list[str]

        # 요청파라미터 검증
        ## question_text로 넘어온 값이 없거나 (있는데 빈문자열이라면)
        if not question_text or (question_text and not question_text.strip()):
            return render(
                request, 
                "polls/vote_create.html", 
                {
                    "error_message":"질문은 한글자 이상 입력하세요.",
                    "question_text":question_text,
                    "choice_list":choice_list
                }
            )
    
        ## 보기 요청파라미터 검증 - 보기가 두개 미만이라면
        if not choice_list or (choice_list and len([c for c in choice_list if c.strip()])< 2):
            return render(
                request, 
                "polls/vote_create.html", 
                {
                    "error_message":"보기는 두개 이상 입력하세요.",
                    "question_text":question_text,
                    "choice_list":choice_list
                }
            )

        ######## 질문/보기 등록 처리
        try:
            ## transaction 처리 -> 질문과 보기가 모두 insert 되거나 실패하면 모두 insert안되도록 보장
            with transaction.atomic(): # Transaction시작
                # with block을 정상적으로 실행 수 나오면 commit 실행
                #           실행중 오류 발생하면 rollback 실행.(DB의 상태를 시작하기 전 상태로 돌린다.)
                q = Question(question_text=question_text)
                q.save()
                
                for choice_text in choice_list:
                    choice = Choice(choice_text=choice_text, question=q) # id/vote는 자동입력
                    choice.save()

        except Exception as e:
            return render(
                request, 
                "polls/error.html", 
                {"error_message": "설문을 저장하는 도중 에러가 발생했습니다. 관리자에게 문의하세요."}
            )

    ###### 응답: redirect방식 -> 설문 목록이동
    return redirect(reverse("polls:vote_list"))


#######################
# Form을 이용
#######################
from .forms import QuestionForm, ChoiceFormSet, ChoiceForm

@login_required
def vote_create(request):
    if request.method == 'GET':
        # 응답화면 반환
        ## Form을 이용해서 template에 입력 양식을 구현할 경우.
        ## Form객체를 생성, 객체를 context value로 template에게 전달.
        q_form = QuestionForm()
        # c_form = ChoiceForm()
        c_formset = ChoiceFormSet()

        return render(
            request, 
            "polls/vote_create_form.html",
            {"q_form":q_form, "c_formset":c_formset}
        )
    elif request.method == 'POST':
        # 등록 처리
        ## 요청파라미터를 Form을 이용해서 처리.(조회, 검증)
        ## 요청파라미터(request.POST) 를 initializer에 넣어서 객체 생성
        ### 요청파라미터name를 검증하고 검증 통과한 값들을 cleaned_data에 저장. 검증(기본, clean메소드)
        q_form = QuestionForm(request.POST, request.FILES)
        c_formset = ChoiceFormSet(request.POST, request.FILES)
        # 요청파라미터 검증 성공 여부 확인 - 성공: 처리, 실패: 오류처리 페이지로 이동
        ## form.is_valid(): bool -> 검증 성공여부 확인.
        if q_form.is_valid() and c_formset.is_valid():
            # 요청파라미터 값들을 Form에서 조회
            q_text = q_form.cleaned_data['question_text']
            choice_list = []
            for c_form in c_formset:
                choice_list.append(c_form.cleaned_data['choice_text'])
            # DB 저장
            try:
                with transaction.atomic():
                    q = Question(question_text=q_text)
                    q.save()
                    for choice in choice_list:
                        c = Choice(choice_text=choice, question=q)
                        c.save()
            except Exception as e:
                return render(
                    request, 
                    "polls/error.html", 
                    {"error_message": "설문 질문 등록 도중 오류 발생"}
                )
            return redirect(reverse("polls:vote_list"))
        else:
            # 검증 실패 -> form객체를 context value로 해서 다시 vote_create.html로 이동.
            return render(
                request,
                "polls/vote_create_form.html",
                {"q_form":q_form, "c_formset":c_formset} #요청파라미터 가진 Form들
            )