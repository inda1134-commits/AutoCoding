import streamlit as st

st.set_page_config(
    page_title="AI Code Editor + Git Manager",
    layout="wide"
)

st.title("🤖 AI 코드 에디터 & Git 매니저")

st.markdown("""
## 앱 기능 안내

### 1. 이 앱의 기능 (요약)
- 프로젝트 폴더를 선택하여 AI가 코드를 분석
- LLM(OpenAI / Claude / Gemini) 선택 가능
- 코드 수정 자동화
- 변경사항 Diff 검토
- 승인 후 실제 파일 저장
- Git Commit까지 자동 처리
- 신규 코드 생성 및 폴더/파일 자동 생성

---

### 2. `modi_code`
### 코드 수정 및 Git Commit

기존 프로젝트 코드를 분석하고,
필요한 부분을 수정한 뒤
Git Commit까지 진행합니다.

---

### 3. `crea_code.py`
### 요청 코드 작성

요청 사항을 입력하면
AI가 신규 코드 작성 + 폴더 생성 + 파일 생성까지 수행합니다.
""")