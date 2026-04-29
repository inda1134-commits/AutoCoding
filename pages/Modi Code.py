import streamlit as st
from contextlib import nullcontext

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks import get_openai_callback

from utilities import (
    init_session,
    render_sidebar,
    build_llm,
    read_file_content,
    write_file_content,
    list_project_files,
)

init_session()
render_sidebar()


st.title("🛠 코드 수정 및 Git Commit")

user_input = st.text_area(
    "수정 요청",
    height=200,
    placeholder="예: 로그인 오류 수정 / 리팩토링 / 기능 추가"
)

if st.button("실행"):
    if not st.session_state.get("target_dir"):
        st.error("작업 폴더를 먼저 설정해주세요.")

    elif not user_input.strip():
        st.error("수정 요청을 입력해주세요.")

    else:
        llm = build_llm()

        tools = [
            read_file_content,
            write_file_content,
            list_project_files,
        ]

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
당신은 숙련된 시니어 소프트웨어 엔지니어입니다.

반드시 tool을 사용하여:
1. 프로젝트 구조를 먼저 파악하고
2. 필요한 파일을 읽고
3. 최소 수정 원칙으로 수정안을 생성하세요.

절대 추측하지 마세요.
""",
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_tool_calling_agent(llm, tools, prompt)

        executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
        )

        callback_ctx = (
            get_openai_callback()
            if st.session_state.model_provider == "GPT (OpenAI)"
            else nullcontext()
        )

        with callback_ctx as cb:
            result = executor.invoke({
                "input": (
                    f"프로젝트 경로: {st.session_state.target_dir}\n"
                    f"요청사항: {user_input}"
                )
            })

            if cb:
                st.session_state.total_tokens += cb.total_tokens
                st.session_state.prompt_tokens += cb.prompt_tokens
                st.session_state.completion_tokens += cb.completion_tokens

        st.success("작업 완료")
        st.write(result.get("output", "응답이 없습니다."))