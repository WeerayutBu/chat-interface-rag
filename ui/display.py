import streamlit as st
from utils import get_api_response
import json

def display_sidebar():
    # Model selection
    model_options = ["gpt-4o-mini", "gpt-4o"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

def display_chat_interface():
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("Query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get API response
        with st.spinner("Generating response..."):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)
            if response:
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})

                with st.chat_message("assistant"):
                    st.markdown(response['answer'])

                with st.expander("Details"):
                    st.subheader("Context")
                    st.code(json.dumps(response["facts"], indent=2, ensure_ascii=False), language="json")

                    st.subheader("History")
                    st.code(json.dumps(response["history"], indent=2, ensure_ascii=False), language="json")

                    st.subheader("Model Used")
                    st.code(response["model"])

                    st.subheader("Session ID")
                    st.code(response["session_id"])
            else:
                st.error("Failed to get a response from the API. Please try again.")
