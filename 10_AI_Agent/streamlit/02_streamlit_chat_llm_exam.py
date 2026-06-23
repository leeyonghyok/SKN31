# 02_streamlit_chat_llm_exam.py
# GPT 모델과 연동한 chatbot

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import streamlit as st 
from dotenv import load_dotenv

@st.cache_resource
def get_model():
    # 처음 호출 될 때 객체를 생성해서 반환하고 반환한 객체를 cache에 저장한다. 
    #   다음 부터는 cache에 저장한 객체를 반환
    load_dotenv()
    return ChatOpenAI(model="gpt-5.4-nano")

def get_prompt_template():

    return ChatPromptTemplate.from_messages(
        [
            {"role":"system", "content":"당신은 유능한 AI Assistant입니다."},
            MessagesPlaceholder(variable_name="history", optional=True),
            {"role":"user", "content":"{query}"}
            
        ]
    )

def add_message(role, content):
    """받은 role과 content를 message로 만들어서 session_state에 저장"""
    st.session_state['chat_history'].append(
        {"role":role, "content":content}
    )

model = get_model()
prompt = get_prompt_template()

# 처음 실행될 때 session_state에 대화내역을 저장할 리스트 추가.
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []


st.title("챗봇 서비스")

# 프롬프트 입력을 위한  chat_input 생성.
user_input = st.chat_input("User:")
if user_input:
    # AI에게 요청
    query = prompt.invoke(
        {"query":user_input, "history":st.session_state['chat_history']}
    )
    try:
        response = model.invoke(query)
        # 질문 - 답변 를 chat_history에 저장.
        add_message("user", user_input)
        add_message("ai", response.content)
    except Exception as e:
        st.error(f"응답 생성 도중에 오류가 발생했습니다. {e}")

## 출력
for message_dict in st.session_state['chat_history']:
    with st.chat_message(message_dict['role']):
        st.write(message_dict['content'])

# uv pip install torchvision
# streamlit run 02_streamlit_chat_llm_exam.py

