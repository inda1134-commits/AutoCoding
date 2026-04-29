import streamlit as st

st.set_page_config(
    page_title="AI Code Editor + Git Manager",
    layout="wide"
)

# ============================================================
# 공통 Session State 초기화
# ============================================================
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


# ============================================================
# Sidebar (항상 유지)
# ============================================================
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

    st.session_state.model_provider = st.selectbox(
        "LLM 선택",
        model_list,
        index=model_list.index(st.session_state.model_provider),
        key="sidebar_model_provider"
    )

    st.session_state.api_key = st.text_input(
        "API Key",
        type="password",
        value=st.session_state.api_key,
        key="sidebar_api_key"
    )

    st.divider()

    target_dir_input = st.text_input(
        "작업 폴더",
        value=st.session_state.target_dir,
        key="sidebar_target_dir"
    )

    if st.button("경로 저장", key="save_target_dir"):
        st.session_state.target_dir = target_dir_input
        st.success("작업 폴더 저장 완료")

    if st.session_state.target_dir:
        st.info(f"📂 {st.session_state.target_dir}")