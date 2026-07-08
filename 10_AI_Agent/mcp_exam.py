
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

async def main():
    # MultiServerMCPClient 객체 생성 -> MCP 서버와 연결 + MCP 툴들을 langchain tool로 변경
    # 연결할 MCP 서버들 설정. dict[str: 서버이름, dict]
    client = MultiServerMCPClient(
        {
            "time":{
                "transport":"stdio",
                "command":"python",
                "args":["-m","mcp_server_time"]
            },
            "filesystem": {
                "transport":"stdio",    
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    os.getcwd() # server-filesystem이 사용할 수 있는 디렉토리
                ]
            },
            "playwright": {
                "transport":"stdio",  
                "command": "npx",
                "args": [
                    "@playwright/mcp@latest"
                ]
            }
        }

    )
    # langchain too list로 변환
    tools = await client.get_tools()
    print("툴개수:", len(tools))
    # agent 생성
    agent = create_agent(
        model=ChatOpenAI(model="gpt-5.4-mini"),
        tools=tools,
        system_prompt="당신은 유능한 AI Assistant입니다. 필요한 경우 도구들을 이용해서 답변하세요."
    )
    print(">>> 종료하려면 !quit를 입력하세요.<<<")
    while True:
        query = input(">>>질문:")
        if query == '!quit':
            print(">>>종료<<<")
            break
        res = await agent.ainvoke({
            "messages":[
                ("human", query)
            ]
        })
        print("<<<답변:")
        print(res['messages'][-1].content)
        print("---")
if __name__ == "__main__":
    asyncio.run(main())
