import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


@tool
def create_folder(folder_path: str) -> str:
    """폴더 생성"""
    os.makedirs(folder_path, exist_ok=True)
    return f"폴더 생성 완료: {folder_path}"


@tool
def create_file(file_path: str, content: str) -> str:
    """파일 생성"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"파일 생성 완료: {file_path}"


st.title("✨ 요청 코드 작성")

api_key = st.session_state.api_key
project_path = st.session_state.target_dir

request = st.text_area(
    "요청 사항 입력",
    placeholder="예: FastAPI + PostgreSQL 로그인 API 만들어줘"
)

if st.button("코드 생성"):
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=api_key,
    )

    tools = [
        create_folder,
        create_file,
    ]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
사용자 요청에 따라
반드시 tool을 사용하여
폴더 생성 → 파일 생성까지 수행하세요.
설명만 하지 말고 실제 생성하세요.
""",
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )

    result = executor.invoke({
        "input": f"프로젝트 경로: {project_path}\n요청사항: {request}"
    })

    st.success("생성 완료")
    st.write(result["output"])