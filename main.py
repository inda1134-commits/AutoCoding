import streamlit as st
from utilities import init_session, render_sidebar

st.set_page_config(
    page_title="AI Code Editor + Git Manager",
    layout="wide"
)

# 공통 session 초기화
init_session()

# 모든 페이지 공통 sidebar
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