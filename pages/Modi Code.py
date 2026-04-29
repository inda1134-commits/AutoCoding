import os
import difflib
from contextlib import nullcontext

import streamlit as st
from git import Repo, InvalidGitRepositoryError

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.callbacks.manager import get_openai_callback

DEFAULT_SESSION = {
    "model_provider": "GPT (OpenAI)",
    "api_key": "",
    "target_dir": "",
    "total_tokens": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "pending_changes": {},
    "commit_step": False,
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 공통 값 사용
model_provider = st.session_state.model_provider
api_key = st.session_state.api_key
target_dir = st.session_state.target_dir


# ============================================================
# Tools
# ============================================================

@tool
def read_file_content(file_path: str) -> str:
    """파일 읽기"""
    if not os.path.exists(file_path):
        return "파일이 존재하지 않습니다."

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def write_file_content(file_path: str, content: str) -> str:
    """수정안 임시 저장"""
    st.session_state.pending_changes[file_path] = content
    return f"수정안 저장 완료: {file_path}"


@tool
def list_project_files(directory_path: str) -> str:
    """프로젝트 파일 목록"""
    result = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            result.append(os.path.join(root, file))

    return "\n".join(result)


# ============================================================
# LLM Factory
# ============================================================

def build_llm(provider: str, key: str):
    if provider == "GPT (OpenAI)":
        return ChatOpenAI(model="gpt-4o", temperature=0, api_key=key)

    elif provider == "Claude (Anthropic)":
        return ChatAnthropic(
            model="claude-3-7-sonnet-latest",
            temperature=0,
            api_key=key,
        )

    elif provider == "Gemini (Google)":
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            google_api_key=key,
        )


st.title("🛠 코드 수정 및 Git Commit")


user_input = st.text_area("수정 요청")

if st.button("실행"):
    llm = build_llm(model_provider, api_key)

    tools = [
        read_file_content,
        write_file_content,
        list_project_files,
    ]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
프로젝트 구조를 먼저 확인하고
필요한 파일을 읽은 뒤
최소 수정 원칙으로 수정하세요.
반드시 tool을 사용하세요.
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

    callback_ctx = (
        get_openai_callback()
        if model_provider == "GPT (OpenAI)"
        else nullcontext()
    )

    with callback_ctx as cb:
        result = executor.invoke({
            "input": f"경로: {st.session_state.target_dir}\n요청: {user_input}"
        })

        if cb:
            st.session_state.total_tokens += cb.total_tokens
            st.session_state.prompt_tokens += cb.prompt_tokens
            st.session_state.completion_tokens += cb.completion_tokens

    st.write(result["output"])