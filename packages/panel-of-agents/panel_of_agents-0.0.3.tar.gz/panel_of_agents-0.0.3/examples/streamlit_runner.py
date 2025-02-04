import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from src.panel_of_agents.context import Context
from examples.content_gen.main import transmitter
# from examples.math_agents.main import transmitter
st.title("Panel of Agents Runner")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Enter your message"):
    conversation_history = [
        HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(
            content=msg["raw_feed" if "raw_feed" in msg else "content"])
        for msg in st.session_state.messages
    ]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    context = Context(
        current_question=prompt,
        conversation_history=conversation_history,
        artifacts={},
        target_agent="Content Research Writer"
    )
    with st.chat_message("assistant"):
        token_stream = transmitter.invoke_moderator(context, stream=True)
        display_response = st.write_stream(token_stream)
    st.session_state.messages.append(
        {"role": "assistant", "content": display_response,
            "raw_feed": transmitter.raw_feed}
    )
