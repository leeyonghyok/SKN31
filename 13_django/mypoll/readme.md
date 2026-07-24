1. mypoll  프로젝트 디렉토리 생성
2. 가상환경을 생성 (mypoll안에서 생성)
    - `uv venv .venv --python=3.13`
    - 활성화
3. django 설치
    -`uv pip install django`

4. 장고 프로젝트 생성
    - `django-admin startproject config .`
    - `config`: 전체 시스템(proejct)의 설정파일들을 저장할 디렉토리 이름
    - `.`: 디렉토리 생성할 위치 (`.`: 현재 디렉토리)
    - `manage.py`: 장고프로젝트를 관리하는 툴(too) 스크립트
5. 개발서버 실행
    - `python manage.py runserver`
    - Web Browser: `http://127.0.0.1:8000` 
    - 서버종료: `control+c`
6. APP생성
    - `python manage.py startapp APP이름`
    - `python manage.py startapp polls`
    - 생성된 APP을 프로젝트에 등록
        - config/settings.py(프로젝트 설정파일) 열기
        - `INSTALLED_APP=[]` 리스트에 APP이름을 추가.
7. (Project) 관리자 계정
    - `python manage.py migrate` (관리자를 저장할 수 있는 DB 생성)
    - `python manage.py createsuperuser` (관리자 계정 생성)
        - username: 계정명 (admin)
        - email: 이메일주소 (a@a.com)
        - password: 비밀번호 (1111)
    - 관리자 app에 접속
        - 서버실행 후 (`python manage.py runserver`)
        -`http://127.0.0.1:8000/admin`