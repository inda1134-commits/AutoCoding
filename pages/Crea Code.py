import streamlit as st
from contextlib import nullcontext
from langchain_community.callbacks.manager import get_openai_callback
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from utilitys import init_session, render_sidebar, build_llm, create_folder, create_file


init_session()
render_sidebar()

st.title("✨ 요청 코드 작성")

request = st.text_area(
    "요청 사항 입력",
    placeholder="예: FastAPI + PostgreSQL 로그인 API 만들어줘"
)


if st.button("코드 생성"):
    llm = build_llm()

    tools = [
        create_folder,
        create_file,
    ]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
사용자 요청에 따라
반드시 tool을 사용하여
폴더 생성 → 파일 생성까지 수행하세요.
설명만 하지 말고 실제 생성하세요.
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
                f"요청사항: {request}"
            )
        })

        if cb:
            st.session_state.total_tokens += cb.total_tokens
            st.session_state.prompt_tokens += cb.prompt_tokens
            st.session_state.completion_tokens += cb.completion_tokens

    st.success("생성 완료")
    st.write(result["output"])