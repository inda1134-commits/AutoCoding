import os
import streamlit as st
fromlangchain_core.tools import tool
fromlangchain_openai import ChatOpenAI
fromlangchain_anthropic import ChatAnthropic
fromlangchain_google_genai import ChatGoogleGenerativeAI
def init_session():
DEFAULT_SESSION = {
"model_provider": "GPT (OpenAI)",
"api_key": "",
"target_dir": "",
"total_tokens": 0,
"prompt_tokens": 0,
"completion_tokens": 0,
3
"pending_changes": {},
"commit_step": False,
}
for key, value inDEFAULT_SESSION.items():
if keynot inst.session_state:
st.session_state[key] =value
defrender_sidebar():
withst.sidebar:
st.header("📊 Usage")
st.metric("Total Tokens", st.session_state.total_tokens)
st.caption(
f"Input: {st.session_state.prompt_tokens} / "
f"Output: {st.session_state.completion_tokens}"
)
model_list = [
"GPT (OpenAI)",
"Claude (Anthropic)",
"Gemini (Google)",
]
st.session_state.model_provider =st.selectbox(
"LLM 선택",
model_list,
index=model_list.index(st.session_state.model_provider),
key="sidebar_model_provider"
)
st.session_state.api_key=st.text_input(
"API Key",
type="password",
key="sidebar_api_key"
)
target_dir_input =st.text_input(
"작업 폴더",
key="sidebar_target_dir"
)
if st.button("경로 저장", key="save_target_dir"):
st.session_state.target_dir = target_dir_input
st.success("작업 폴더 저장 완료")
4
defbuild_llm():
provider =st.session_state.model_provider
key=st.session_state.api_key
if provider =="GPT (OpenAI)":
returnChatOpenAI(
model="gpt-4o",
temperature=0,
api_key=key,
)
elif provider =="Claude (Anthropic)":
returnChatAnthropic(
model="claude-3-7-sonnet-latest",
temperature=0,
api_key=key,
)
elif provider =="Gemini (Google)":
returnChatGoogleGenerativeAI(
model="gemini-1.5-pro",
temperature=0,
google_api_key=key,
)
@tool
defread_file_content(file_path: str)->str:
"""파일 읽기"""
if not os.path.exists(file_path):
return"파일이 존재하지 않습니다."
withopen(file_path, "r", encoding="utf-8") as f:
return f.read()
@tool
defwrite_file_content(file_path: str, content: str)->str:
"""수정안 임시 저장"""
st.session_state.pending_changes[file_path] =content
return f"수정안 저장 완료: {file_path}"
@tool
deflist_project_files(directory_path: str)->str:
"""프로젝트 파일 목록"""
result = []
5
for root, _, files in os.walk(directory_path):
for file in files:
result.append(os.path.join(root, file))
return "\n".join(result)
@tool
def create_folder(folder_path: str)-> str:
"""폴더 생성"""
os.makedirs(folder_path, exist_ok=True)
return f"폴더 생성 완료: {folder_path}"
@tool
def create_file(file_path: str, content: str)-> str:
"""파일 생성"""
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, "w", encoding="utf-8") as f:
f.write(content)
return f"파일 생성 완료: {file_path}"