import magic
import base64
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

def get_file_mimetype(bytes_data: bytes) -> str:
    """파일을 bytes 타입으로 받아서 그 파일의 mime-type을 반환한다.
    Args:
        bytes_data (bytes) - 마임타입을 확인할 파일
    Returs
        str - 파일의 타입을 mime-type으로 반환
    """

    return magic.from_buffer(bytes_data, mime=True)


def get_human_message(
        text_message: str, bytes_data:bytes=None, mime_type:str=None, 
        filename:str=None, history:list=None) -> list[BaseMessage]:
    """사용자 메시지와 선택적(Optional) 파일 첨부를 포함한 LangChain 메시지 리스트를 생성한다.
    대화 히스토리와 현재 사용자의 텍스트 메시지, 그리고 선택적으로 이미지나 PDF 등의 파일을 Base64로 인코딩하여 멀티모달 메시지 형태로 변환한다.

    Args:
        text_message (str): 사용자가 입력한 텍스트 메시지.
        bytes_data (bytes, optional): 첨부 파일의 바이트 데이터. Defaults to None.
        mime_type (str, optional): 첨부 파일의 MIME 타입 (예: 'image/png', 'application/pdf'). 
            Defaults to None.
        filename (str, optional): 첨부 파일의 이름. OpenAI PDF 전송 시 필요. 
            Defaults to None.
        history (list, optional): 이전 대화 히스토리. 각 항목은 'role'과 'message' 키를 
            포함하는 딕셔너리. Defaults to None.
        list: HumanMessage와 AIMessage 객체로 구성된 LangChain 메시지 리스트.
            마지막 항목은 현재 사용자 입력과 첨부 파일(있는 경우)을 포함한 HumanMessage.
    Returns
        list[BaseMessage] - LLM에게 전송할 Message 리스트
    """
    # LLM에게 전달할 메세지들을 순서대로 담을 list
    # chat_history 메세지들, 현재 User Message
    messages = [] 
    for msg in history: #history: list[dict] dict key: role, content (OpenAI 형식)
        if msg['role'] == "user":
            messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'ai':
            messages.append(AIMessage(content=msg['content']))

    # 현재 사용자 입력 메세지를 messages list에 추가
    content = [
        {"type":"text", "text":text_message}
    ]
    # 첨부파일이 있을 경우 content에 추가.
    if bytes_data is not None:
        d_type = "image" if "image" in mime_type else "file" # type 값 조회
        base64_data = base64.b64encode(bytes_data).decode("utf-8")
        content.append({
            "type":d_type, 
            "source_type":"base64",
            "data":base64_data,
            "mime_type":mime_type,
            "filename":filename 
        })

    messages.append(HumanMessage(content=content))
    return messages