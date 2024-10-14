# GroqAPI.py
import streamlit as st
from groq import Groq


class GroqAPI:
    """GroqAPI クラス：
    Groq APIとのインターフェースを提供します。
    このクラスは、Groq APIを使用して自然言語処理タスクを実行するための
    メソッドを提供します。

    Attributes:
        client (Groq): Groq APIクライアントインスタンス
        model_name (str): 使用するモデルの名前
    """

    def __init__(self, api_key: str, model_name: str):
        # self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def _response(self, message, stream=False):
        if (
            "change_llm_params" in st.session_state
            and st.session_state.change_llm_params
        ):
            return self.client.chat.completions.create(
                model=self.model_name,
                messages=message,
                max_tokens=st.session_state.max_tokens,
                temperature=st.session_state.temperature,
                top_p=st.session_state.top_p,
                stream=stream,
                stop=None,
            )
        else:
            return self.client.chat.completions.create(
                model=self.model_name,
                messages=message,
                max_tokens=4096,
                temperature=1.0,
                top_p=1.0,
                stream=stream,
                stop=None,
            )

    def completion(self, message):
        """Groq APIにPrompt messageを送信し、レスポンスを取得します。
        Args:
            message: APIに送信するメッセージ
        Return:
            str: レスポンスの各チャンク
        """
        response = self._response(message, stream=False)
        completion_content = response.choices[0].message.content
        return completion_content

    def response_stream(self, message):
        """Groq APIにストリーミングで送信し、レスポンスを取得します。
        Args:
            message: APIに送信するメッセージ
        Yields:
            str: レスポンスの各チャンク

        利用例：
          llm = GroqAPI(st.session_state.selected_model)
          with st.chat_message("assistant"):
              message_placeholder = st.empty()
              full_response = ""
              for chunk in llm.response_stream(st.session_state.messages):
                  full_response += chunk
                  message_placeholder.markdown(full_response + "▌")
              message_placeholder.markdown(full_response)
          st.session_state.messages.append(
              {"role": "assistant", "content": full_response}
          )
        """
        response = self._response(message, stream=True)
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
