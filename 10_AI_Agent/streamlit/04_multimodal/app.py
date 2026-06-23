###################################################################################
# - chat_input에서 파일 첨부 받기
#   - accept_file(bool | str): True - 첨부가능, "multiple": 여러 파일 첨부가능
#    >> prompt = st.chat_input(placeholder="User:", accept_file=True)  
#
# - st.chat_input의 반환타입인 ChatInputValue의 attributes:
#   - ChatInputValue.text : 텍스트 입력
#   - ChatInputValue.files : 첨부파일을 List에 담아서 반환.
#     - 첨부파일은 UploadFile 타입
#
# - UploadFile attributes:
#     - name(str):  파일 명
#     - getvalue(): bytes - 첨부파일을 bytes로 반환.
###################################################################################

import streamlit as st
from langchain_openai import ChatOpenAI
import utils
from dotenv import load_dotenv

st.title("멀티 모달리티 챗봇")

@st.cache_resource
def get_model():
    load_dotenv()
    return ChatOpenAI(model="gpt-5-mini")

model = get_model()

################################################################
#  session state에 message history를 저장할 list 추가.
################################################################
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

###################################
# 기존 대화 내역(chat_history) 출력
###################################
for message_dict in st.session_state['chat_history']:
    with st.chat_message(message_dict['role']):
        st.write(message_dict['content'])

###################################
# chat_input 생성 (입력폼)
###################################
prompt = st.chat_input(
    placeholder="User:",
    accept_file=True  # 한개 파일을 첨부 가능. accept_file="multiple": 여러파일 첨부 가능
    # , file_type=["txt", "md", "pdf", "jpg", "png", "bmp"] # 첨부 가능한 파일의 확장자들 지정
)
#####################################
# 사용자 입력 처리 (텍스트 + 첨부파일)
#####################################
if prompt is not None:
    text_message = prompt.text  # 입력된 text
    attach_files = prompt.files # list[UploadFile]: 첨부파일
    mime_type = None
    bytes_data = None
    filename = None
    if attach_files: #첨부된 파일이 있다면
        bytes_data = attach_files[0].getvalue() # 첨부파일을 읽어서 bytes로 반환.
        mime_type = utils.get_file_mimetype(bytes_data)
        filename = attach_files[0].name # 첨부파일의 이름 조회

    messages = utils.get_human_message(
        text_message=text_message,
        bytes_data=bytes_data,
        mime_type=mime_type,
        filename=filename,
        history=st.session_state['chat_history']
    )

    # chat history에 사용자 입력을 추가, 화면에 출력
    st.session_state['chat_history'].append(
        {"role":"user", "content":text_message}
    )
    with st.chat_message("user"):
        st.write(text_message)

    # LLM 모델에게 prompt 전송, 응답 출력 (streaming)
    with st.chat_message("ai"):
        generator = model.stream(messages)
        full_message = st.write_stream(generator)

    # AI응답(full_message) 를 chat history에 저장
    st.session_state['chat_history'].append(
        {"role":"ai", "content":full_message}
    )
# cd  streamlit\04_multimodal
# streamlit run app.py