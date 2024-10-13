# ModelSelector.py
import streamlit as st


class ChatParameters:
    """Class for Chat Completion Setup Module"""

    default_sys_prompt = """あなたは聡明なAIです。
    ユーザの入力に全て日本語で返答を生成してください"""

    def __init__(self):
        """Define the default system prompt"""
        if "system_prompt" not in st.session_state:
            st.session_state.use_system_prompt = False
            st.session_state.system_prompt: str = self.default_sys_prompt
            st.session_state.disabled_edit_params = False

    def system_prompt(self):
        """sidebar: setup system prompt"""
        with st.sidebar:
            # SYSTEM_PROMPTの編集
            if st.checkbox(
                "use SYSTEM PROMPT",
                value=False,
            ):
                st.session_state.use_system_prompt = True
                with st.expander("Edit SYSTEM_PROMPT?", expanded=False):
                    st.session_state.system_prompt = st.text_area(
                        "Edit SYSTEM_PROMPT before chat",
                        value=st.session_state.system_prompt,
                        height=100,
                        # disabled=(not st.session_state.no_chat_history),
                        disabled=(st.session_state.disabled_edit_params),
                    )
            else:
                st.session_state.use_system_prompt = False
