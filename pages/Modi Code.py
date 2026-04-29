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