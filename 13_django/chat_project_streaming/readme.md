가상환경
uv venv .venv --python=3.13

활성화
.venv\Script\activate

LIB 설치
uv pip install django langchain langchain-openai python-dotenv

명령팔레트(control + shift + p) 에서 Python Interpreter 를 가상환경으로 설정.


# 장고
- `static` 디렉토리 생성
python manage.py makemigrations
python manage.py migrate

- chatbot_project/ : 설정파일들 저장된 디렉토리
- chat/ : App

python manage.py runserver 

http://127.0.0.1:8000/chat/