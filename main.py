import streamlit as st
from utilitys import render_sidebar

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
            key="sidebar_api_key"
        )

        target_dir_input = st.text_input(
            "작업 폴더",
            key="sidebar_target_dir"
        )

        if st.button("경로 저장", key="save_target_dir"):
            st.session_state.target_dir = target_dir_input
            st.success("작업 폴더 저장 완료")

        if st.session_state.target_dir:
            st.info(f"📂 {st.session_state.target_dir}")


render_sidebar()

st.title("🤖 AI 코드 에디터 & Git 매니저")

st.markdown("""
## 앱 기능 안내

### 1. 이 앱의 기능 (요약)
- 프로젝트 폴더 선택
- LLM / API Key 공통 관리
- 코드 수정 자동화
- 변경사항 Diff 검토
- 승인 후 실제 파일 저장
- Git Commit 자동 처리
- 신규 코드 생성 및 폴더/파일 생성

---

### 2. Modi Code
### 코드 수정 및 Git Commit

기존 프로젝트 코드를 분석하고 수정 후 Git Commit까지 진행합니다.

---

### 3. Crea Code
### 요청 코드 작성

요청 사항을 입력하면 신규 코드 작성 + 폴더 생성 + 파일 생성까지 수행합니다.
""")