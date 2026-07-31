from dotenv import load_dotenv

from django.shortcuts import render
from django.http import StreamingHttpResponse

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import traceback

load_dotenv()


def get_chain():
    """LangChain 체인을 초기화"""

    prompt = ChatPromptTemplate(
        messages=[
            {
                "role": "system", 
                "content": ("당신은 다양한 분야에 대해 전문적인 조언을 할 수 있는 유능한 인공지능 Assistant입니다."
                            "사용자의 질문에 대해 친절한 톤으로 답변해 주세요."
                            "답변의 난이도가 질문에 명시되어 있지 않은 경우, 해당 주제를 처음 접하는 사람도 이해할 수 있도록 단계적으로 차근차근 쉽게 설명해 주세요."
                            "확실하지 않은 내용은 단정하지 말고 그 한계를 명확히 밝혀 주세요.")
            },
            MessagesPlaceholder(variable_name="history"),
            {"role": "user", "content": "{input}"}
        ]
    )
    chat = ChatOpenAI(model_name="gpt-5.4-mini")
    return prompt | chat

def index(request):
    return render(request, 'chat/index.html')

def stream_chat(request):
    message = request.GET.get('message', '')
    if not message:
        # StreamingHttpResponse(iterable/generator, content_type="text/event-stream")
        ## iterable이 값을 제공할 때 마다 응답.
        return StreamingHttpResponse("data: [ERROR] 메세지를 입력하세요.\n\n", content_type='text/event-stream')

    if 'message_history' not in request.session:
        request.session['message_history'] = []
        request.session.modified = True
        request.session.save()

    # 답변 처리 generator
    # def gen():

    #     yield 값1

    #     yield 값2

    #     yield 값3
    # g = gen() #객체 생성
    # next(g)
    # for v in g:


    def event_stream():
        try:
            # Session에서 지금까지의 대화 내역 조회
            message_history = request.session.get('message_history', [])

            chat = get_chain() #llm chain
            ai_message = ""  # LLM 모델이 stream방식으로 출력하는 응답을 모아 저장할 변수
            
            print(f"현재 히스토리: {len(message_history)}개 메시지")
            for chunk in chat.stream({"input": message, "history": message_history}):
                content = chunk.content.replace('\n', '<br>')
                if content:
                    ai_message += content
                    yield f"data: {content}\n\n"
            
            message_history.append(HumanMessage(content=message))
            message_history.append(AIMessage(content=ai_message.replace('<br>', '\n')))
            
            trimmed_msg = trim_messages(
                message_history,
                max_tokens=20,
                strategy="last",
                token_counter=len,
                start_on="human",
                end_on=("human", "ai"),
                include_system=True
            )
            
            message_history_to_save = []
            for msg in trimmed_msg:
                if isinstance(msg, HumanMessage):
                    message_history_to_save.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    message_history_to_save.append({"role": "assistant", "content": msg.content})
            
            request.session['message_history'] = message_history_to_save
            request.session.modified = True
            request.session.save()
            
            print(f"저장된 히스토리: {len(message_history_to_save)}개 메시지")
            yield "data: [DONE]\n\n" # client에게 보내는 답변 완료 flag값.

        except Exception as e:
            traceback.print_exc()
            yield f"data: [ERROR] {str(e)}\n\n" # client에게 보내는 ERROR 표시

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream') # iterable
    response['Cache-Control'] = 'no-cache'
    # 응답정보의 Head의 Cach-Control을 no-cache 설정. 응답데이터를 웹브라우저가 저장하지 않게 하기.
   
    return response

