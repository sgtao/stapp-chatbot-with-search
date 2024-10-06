# GropApiKey.py
import os
import streamlit as st


class GropApiKey:
    def __init__(self):
        self.api_key = ""
        # API-KEYのプリセット確認
        if "groq_api_key" in st.session_state:
            self.api_key = st.session_state.groq_api_key
        elif os.getenv("GROQ_API_KEY"):
            st.session_state.groq_api_key = os.getenv("GROQ_API_KEY")
            self.api_key = st.session_state.groq_api_key
        else:
            self.api_key = ""

    def input_key(self):
        # API-KEY入力部品
        with st.sidebar:
            # API-KEYの設定
            st.session_state.groq_api_key = st.text_input(
                "Groq API Key",
                key="api_key",
                type="password",
                placeholder="gsk_...",
                value=self.api_key,
            )
            st.markdown("[Get an Groq API key](https://console.groq.com/keys)")
