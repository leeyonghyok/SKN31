# account/views.py
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import (
    authenticate, # 사용자 입력 username과 password를 DB에서 조회하는 인증 함수
    login,        # 로그인 처리. 서버 메모리에 로그인한 사용자의 정보(Model)을 저장
    logout,       # 로그아웃 처리. 로그인시 저장한 Model을 제거
    get_user,     # 로그인한 사용자의 저장된 정보(model)을 반환하는 함수.
    update_session_auth_hash # 회원정보 수정 후 수정된 정보를 서버 메모리에 update하는 함수.
)
from django.contrib.auth.forms import (
    AuthenticationForm, # 로그인 입력양식. username, password
    PasswordChangeForm  # 패스워드 변경 화면에서 사용할 입력 양식.
)
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

######################################################
# 가입 처리
#
# 요청 URL: account/create
# View함수: create
#   - GET: 가입양식 화면, POST: 가입 처리
# 응답:
#    - GET: templates/account/create.html
#    - POST: (Redirect) 메인화면 -> (/polls/welcome)
######################################################
def create(request):

    if request.method == "GET":
        # 빈 Form객체를 context value로 전달.
        return render(request, "account/create.html", {"form":CustomUserCreationForm()})
    
    elif request.method == "POST":
        # 요청파라미터 조회 + 검증 -> Form
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid(): # ValidationError가 발생하지 않았으면(검증 통과)
            # DB에 insert -> ModelForm은 save() /insert/update를 처리.
            user = form.save() # ModelForm을 이용해 Insert/Update 처리. 처리한 Model객체를 반환
            print("save후 user:", type(user), user)#user는 insert된 모든 정보를 가지고 있다.

            # 응답
            return redirect(reverse("polls:polls_welcome"))
        else: # 검증시 문제가 발생.
            # context value로 검증 실패한 Form을 넘겨준다.
            return render(request, "account/create.html", {"form":form})

##################################################################
# 로그인 처리
#  요청URL: /account/login
#  View함수: user_login
#      - GET: 로그인 입력 양식화면 응답
#      - POST: 로그인 처리
#  응답: GET - account/login.html, POST: redirect - polls/welcome
##################################################################
def user_login(request):

    if request.method == "GET":
        return render(request, "account/login.html", {"form":AuthenticationForm()})

    elif request.method == "POST":
        # 로그인처리
        ## username/password 조회
        username = request.POST['username']
        password = request.POST["password"]

        ## 인증 - username/password 확인
        ### 일치 - Model반환, 불일치 - None
        user = authenticate(request, username=username, password=password)
        
        if user is not None: # 일치
            # 로그인처리 (메모리-Session에 로그인한 사용자의 Model객체를 저장.)
            login(request, user)

            ## 로그인해야 요청할 수있는 view를 로그인하지 않고 요청한 경우, 로그인 페이지로 이동하면서
            ### next query string을 붙인다. 로그인 후 원래 요청한 페이지로 이동하도록 한다.
            next_url = request.GET.get("next") # url?next=/account/detail
            if next_url is not None:
                return redirect(next_url)
            
            return redirect(reverse("polls:polls_welcome"))
        
        else: # 불일치 - 로그인 form으로 이동
            return render(
                request, 
                "account/login.html", 
                {"form":AuthenticationForm(), "error_message":"아이디나 패스워드를 다시 확인하세요."}
            )


#####################################
# logout처리
# 요청URL: /account/logout
# View함수: user_logout
# 응답: redirect polls:polls_welcome
#####################################
@login_required
def user_logout(request):
    # login() 함수가 처리한 작업을 무효화 (Session에서 user정보를 제거)
    logout(request)
    return redirect(reverse("polls:polls_welcome"))

###############################################
# 로그인한 사용자 정보 조회
# url: /account/detail
# view함수: detail
# 응답: account/detail.html
###############################################
@login_required
def detail(request):
    # get_user(request): 로그인한 User정보를 반환. (Model), template: [request.]user 변수
    user = get_user(request)
    print(type(user), user)
    return render(request, "account/detail.html", {"user":user})

###############################################################
# 사용자정보 변경 처리
# 요청URL: /account/update
# View함수: update
#          GET-수정폼 화면응답, POST-수정 처리
# 응답: GET - 수정폼 페이지 (account/update.html)
#       POST-회원정보조회페이지로 이동(accunt:detail view: redirect)
###############################################################
@login_required
def update(request):
    if request.method == "GET":
        # 수정폼 생성: 수정할 Model객체를 전달. ->화면에 기존 데이터가 입력폼에 나오도록한다.
        form = CustomUserChangeForm(instance=get_user(request))
        return render(request, "account/update.html", {"form":form})
    
    elif request.method == "POST":
        # 요청파라미터 조회 + 검증
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=get_user(request)
        )
        if form.is_valid():
            # DB저장
            user = form.save() # 업데이트된 Model을 반환.
            # Session(로그인 사용자 상태값)에 저장된 User Model을 update된 Model로 변경.
            update_session_auth_hash(request, user)
            # 응답
            return redirect(reverse("account:detail"))
        else: 
            return render(request, "account/update.html", {"form":form})

################################################################
# 패스워드 변경 처리
#
# 요청: /account/password_change
# View함수: password_change
#          GET-변경 폼, POST-변경처리
# 응답:  GET-account/password_change.html, POST-redirect: account:detail 뷰
################################################################
@login_required
def password_change(request):

    if request.method == "GET":
        form = PasswordChangeForm(get_user(request)) #User Model을 넣어서 생성
        return render(request, "account/password_change.html", {"form":form})

    elif request.method == "POST":
        # 요청파라미터 조회 + 검증 -> form
        ## 모델-기존암호 확인목적, 요청파라미터
        form = PasswordChangeForm(get_user(request), request.POST)
        if form.is_valid():
            # DB 저장
            user = form.save()
            update_session_auth_hash(request, user)
            # 응답
            return redirect(reverse("account:detail"))
        else:
            return render(request, "account/password_change.html", {"form":form})

########################################################
# 사용자 탈퇴 처리(삭제) 
#
# 요청 URL: /account/delete
# view함수: user_delete
# 응답    : redirect - 홈페이지 (polls:polls_welcome)
#########################################################
@login_required
def user_delete(request):
    # 로그인한 사용자의 정보를 DB에서 delete -> logout 처리 -> 응답
    user = get_user(request) # Model객체
    user.delete()
    #로그아웃
    logout(request)
    # 응답
    return redirect(reverse("polls:polls_welcome"))