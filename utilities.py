import os
import streamlit as st

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


def init_session():
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
            

def render_sidebar():
    with st.sidebar:
        st.header("📊 Usage")

        st.metric("Total Tokens", st.session_state.total_tokens)
        st.caption(
            f"Input: {st.session_state.prompt_tokens} / "
            f"Output: {st.session_state.completion_tokens}"
        )

        st.divider() 

        model_list = [
            "GPT (OpenAI)",
            "Claude (Anthropic)",
            "Gemini (Google)",
        ]

        current_model = st.session_state.get("model_provider", "GPT (OpenAI)")
        if current_model not in model_list:
            current_model = "GPT (OpenAI)"

        st.session_state.model_provider = st.selectbox(
            "LLM 선택",
            model_list,
            index=model_list.index(current_model),
            key="sidebar_model_provider"
        )

        st.session_state.api_key = st.text_input(
            "API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            key="sidebar_api_key"
        )

        target_dir_input = st.text_input(
            "작업 폴더",
            value=st.session_state.target_dir, # 직접 참조
            key="sidebar_target_dir"
        )

        if st.button("경로 저장"):
            # 버튼 클릭 시 확실하게 저장
            st.session_state.target_dir = target_dir_input
            st.success("경로가 저장되었습니다.")

        if st.session_state.get("target_dir"):
            st.info(f"📂 {st.session_state.target_dir}")

def build_llm():
    provider = st.session_state.get("model_provider", "GPT (OpenAI)")
    api_key = st.session_state.get("api_key", "")

    if not api_key:
        raise ValueError("API Key를 입력해주세요.")

    if provider == "GPT (OpenAI)":
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=api_key,
        )

    elif provider == "Claude (Anthropic)":
        return ChatAnthropic(
            model="claude-3-7-sonnet-latest",
            temperature=0,
            api_key=api_key,
        )

    elif provider == "Gemini (Google)":
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            google_api_key=api_key,
        )

    raise ValueError("지원하지 않는 LLM입니다.")

@tool
def read_file_content(file_path: str) -> str:
    """파일의 전체 내용을 읽습니다."""
    try:
        if not os.path.exists(file_path):
            return f"오류: 파일이 존재하지 않습니다 -> {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        return f"오류: {str(e)}"


@tool
def write_file_content(file_path: str, content: str) -> str:
    """파일 수정안을 세션에 임시 저장합니다."""
    st.session_state.pending_changes[file_path] = content
    return f"수정안 저장 완료: {file_path}"


@tool
def list_project_files(directory_path: str) -> str:
    """프로젝트 전체 파일 목록 반환"""
    if not os.path.exists(directory_path):
        return f"오류: '{directory_path}' 경로가 존재하지 않습니다. 절대 경로를 사용해 주세요."

    collected = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if not file.startswith("."):
                collected.append(os.path.join(root, file))

    return "\n".join(collected) if collected else "파일이 없습니다."


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