import streamlit as st
from openai import OpenAI

# 비밀번호 설정
PASSWORD = "지니하니"

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# OpenAI API 연결
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 이전 대화 보여주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 채팅창
prompt = st.chat_input("메세지를 입력하세요")

if prompt:
    if not st.session_state.authenticated:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if prompt == PASSWORD:
            st.session_state.authenticated = True
            st.session_state.messages.append({"role": "assistant", "content": "✅ 인증 성공! 조하은에게 무엇이든 물어보세요!"})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "❌ 비밀번호가 틀렸어요. 다시 입력해 주세요."})
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            full_response = ""
            for chunk in stream:
                content = chunk.choices[0].delta.get("content", "")
                full_response += content
                st.write(content, end="")

        st.session_state.messages.append({"role": "assistant", "content": full_response})
