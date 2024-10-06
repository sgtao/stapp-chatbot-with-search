# GroqAPI.py
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

    def _response(self, message):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            stream=False,
            stop=None,
        )

    def _response_stream(self, message):
        """Groq APIに非ストリーミングで送信し、レスポンスを取得します。
        Args:
            message: APIに送信するメッセージ

        Returns:
            APIからのレスポンス
        """
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            # stream=True,
            stream=False,
            stop=None,
        )

    def completion(self, message):
        response = self._response(message)
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
              msg_place = st.empty()
              full_response = ""
              # ここでLangChainを使用してSELF-RAG処理を行う
              # 結果をストリーミング表示
              for chunk in llm.response_stream(prompt):
                  full_response += chunk
                  msg_place.markdown(full_response + "▌")
              msg_place.markdown(full_response)
        """
        for chunk in self._response_stream(message):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
