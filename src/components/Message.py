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
                }
            ]

    def get_name(self):
        return self.name

    def add(self, role: str, content: str):
        st.session_state[self.session_key].append(
            {"role": role, "content": content}
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
        return st.session_state[self.session_key]

    def clear_messages(self):
        st.session_state[self.session_key] = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]
