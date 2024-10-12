from datetime import datetime

import streamlit as st


class Message:
    system_prompt: str = (
        """あなたは聡明なAIです。ユーザの入力に全て日本語で返答を生成してください"""
    )

    def __init__(self, name):
        self.name = name
        self.session_key = f"{name}_message"
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = [
                {
                    "role": "system",
                    "content": self.system_prompt,
                    "timestamp": self.get_timestamp(),
                }
            ]

    def get_name(self):
        return self.name

    def get_timestamp(self):
        # ミリ秒単位までの現在の日時を取得
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S.%f")[:-3]
        return current_time

    def add(self, role: str, content: str):
        st.session_state[self.session_key].append(
            {
                "role": role,
                "content": content,
                "timestamp": self.get_timestamp(),
            }
        )

    def add_display(self, role: str, content: str):
        self.add(role, content)
        with st.chat_message(role):
            st.markdown(content)

    def display_chat_history(self):
        for message in st.session_state[self.session_key]:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def get_messages(self):
        messages = []
        for message in st.session_state[self.session_key]:
            messages.append(
                {
                    "role": message["role"],
                    "content": message["content"],
                }
            )
        return messages

    def messages_history(self):
        return st.session_state[self.session_key]

    def clear_messages(self):
        st.session_state[self.session_key] = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]
