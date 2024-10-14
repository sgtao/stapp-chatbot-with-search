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
            # disabled_edit_params is updated at Message.has_chat_history
            st.session_state.disabled_edit_params = False

        if "change_llm_params" not in st.session_state:
            # change_llm_params are used at GroqAPI._response
            st.session_state.change_llm_params = False
            st.session_state.max_tokens = 8000
            st.session_state.temperature = 1.0
            st.session_state.top_p = 1.0

    def system_prompt(self):
        """sidebar: setup system prompt"""
        # SYSTEM_PROMPTの編集
        if st.checkbox(
            "use SYSTEM PROMPT",
            value=False,
        ):
            st.session_state.use_system_prompt = True
            st.session_state.system_prompt = st.text_area(
                "Edit SYSTEM_PROMPT before chat",
                value=st.session_state.system_prompt,
                height=100,
                # disabled=(not st.session_state.no_chat_history),
                disabled=(st.session_state.disabled_edit_params),
            )
        else:
            st.session_state.use_system_prompt = False

    def tuning_parameters(self):
        with st.expander("Tuning Parameters?", expanded=False):
            # Parameterの調整
            max_tokens = st.slider(
                "max_tokens",
                min_value=1000,
                max_value=8000,
                value=st.session_state.max_tokens,
                step=1000,
            )
            temperature = st.slider(
                "temperature",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.temperature,
                step=0.1,
            )
            top_p = st.slider(
                "top_p",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.top_p,
                step=0.1,
            )
            # update session_state
            st.session_state.change_llm_params = True
            st.session_state.max_tokens = max_tokens
            st.session_state.temperature = temperature
            st.session_state.top_p = top_p
