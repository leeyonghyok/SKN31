
4.



    - `manage.py`: 장고프로젝트를 관리하는 tool script
5. 개발server 실행
    - `python manage.py runserver`
    - web browser: http://127.0.0.1:8000
    - server 종료: `ctrl + c`
6. APP 생성
    -`python manage.py startapp 앱이름`
    -`python manage.py startapp polls`
    - 생성된 APP을 프로젝트에 등록
        - config/settings.py (프로젝트 설정파일) 열기
        - `installed_app=[]` 리스트에 app 이름을 추가
7. (Project) 관리자 계정
    - `python manage.py migrate` (관리자를 저장할 수 있는 DB 생성)
    - `python manage.py createsuperuser`
        - username: 계정명(admin)
        - email: 이메일주소(a@a.com)
        - password: 비밀번호(1111)
    - 관리자 app에 접속
        - 서버 실행 후 (`python manage.py runserver`)
        -`http://127.0.0.1:8000/admin`