import streamlit as st
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.set_page_config(
    page_title="AI Code Editor + Git Manager",
    layout="wide"
)

st.title("🤖 AI 코드 에디터 & Git 매니저")


# ============================================================
# 공통 Sidebar
# ============================================================
with st.sidebar:
    st.header("📊 Usage")

    st.metric("Total Tokens", st.session_state.total_tokens)
    st.caption(
        f"Input: {st.session_state.prompt_tokens} / "
        f"Output: {st.session_state.completion_tokens}"
    )

    st.divider()

    st.session_state.model_provider = st.selectbox(
        "LLM 선택",
        [
            "GPT (OpenAI)",
            "Claude (Anthropic)",
            "Gemini (Google)",
        ],
        index=[
            "GPT (OpenAI)",
            "Claude (Anthropic)",
            "Gemini (Google)",
        ].index(st.session_state.model_provider)
    )

    st.session_state.api_key = st.text_input(
        "API Key",
        type="password",
        value=st.session_state.api_key
    )

    st.divider()

    target_dir_input = st.text_input(
        "작업 폴더",
        value=st.session_state.target_dir,
        placeholder="예: C:/Users/yourname/project"
    )

    if st.button("경로 저장"):
        if target_dir_input:
            st.session_state.target_dir = target_dir_input
            st.success("작업 폴더 저장 완료")
        else:
            st.error("경로를 입력해주세요.")

    if st.session_state.target_dir:
        st.info(f"📂 {st.session_state.target_dir}")