import streamlit as st
fromcontextlib import nullcontext
fromlangchain_community.callbacks.manager import get_openai_callback
fromlangchain_classic.agents import AgentExecutor, create_tool_calling_agent
fromlangchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
fromutilitys import (
init_session,
render_sidebar,
build_llm,
read_file_content,
write_file_content,
list_project_files,
)
init_session()
render_sidebar()
st.title("🛠 코드 수정 및 Git Commit"
)
6
user_input =st.text_area("수정 요청")
if st.button("실행"):
llm=build_llm()
tools= [
read_file_content,
write_file_content,
list_project_files,
]
prompt =ChatPromptTemplate.from_messages([
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
agent =create_tool_calling_agent(llm, tools, prompt)
executor =AgentExecutor(
agent=agent,
tools=tools,
verbose=True,
)
callback_ctx= (
get_openai_callback()
if st.session_state.model_provider =="GPT (OpenAI)"
elsenullcontext()
)
withcallback_ctxas cb:
result =executor.invoke({
"input": (
f"프로젝트 경로: {st.session_state.target_dir}\n"
f"요청사항: {user_input}"
)
})
7
if cb:
st.session_state.total_tokens += cb.total_tokens
st.session_state.prompt_tokens += cb.prompt_tokens
st.session_state.completion_tokens += cb.completion_tokens
st.success("작업 완료")
st.write(result["output"])