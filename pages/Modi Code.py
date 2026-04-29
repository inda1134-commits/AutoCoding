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


# ============================================================
# Session Init
# ============================================================

DEFAULT_SESSION = {
    "total_tokens": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "pending_changes": {},
    "commit_step": False,
    "target_dir": "",
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.header("📊 Usage")

    st.metric("Total Tokens", st.session_state.total_tokens)
    st.caption(
        f"Input: {st.session_state.prompt_tokens} / "
        f"Output: {st.session_state.completion_tokens}"
    )

    st.divider()

    model_provider = st.selectbox(
        "LLM 선택",
        [
            "GPT (OpenAI)",
            "Claude (Anthropic)",
            "Gemini (Google)",
        ]
    )

    api_key = st.session_state.api_key

    st.divider()

    target_dir_input = st.text_input(
        "작업할 프로젝트 경로",
        value=st.session_state.target_dir
    )

if st.button("경로 저장"):
    if os.path.exists(target_dir_input):
        st.session_state.target_dir = target_dir_input
        st.success("경로 저장 완료")
    else:
        st.error("존재하지 않는 경로입니다.")