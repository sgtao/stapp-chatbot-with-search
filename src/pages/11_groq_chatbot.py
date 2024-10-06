# 11_groq_chatbot.py
import streamlit as st
from groq import Groq

from components.GropApiKey import GropApiKey
from components.Message import Message
from components.ModelSelector import ModelSelector


# 関数の定義
def self_rag_response(prompt):
    print(f"prompt: {prompt}")
    response = ["hello"]
    return response


def model_select():
    models = ["llama3-8b-8192", "llama3-70b-8192"]
    with st.sidebar:
        st.sidebar.title("model select:")
        return st.selectbox("", models)


class GroqAPI:
    def __init__(self, model_name: str):
        # self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.client = Groq(api_key=st.session_state.groq_api_key)
        self.model_name = model_name

    def _response(self, message):
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
        for chunk in self._response(message):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


# sidebar: apikey input
groq_api_key = GropApiKey()
groq_api_key.input_key()

# sidebar: model selector
model = ModelSelector()
st.session_state.selected_model = model.select()

# main pageの内容
st.title("Groq Chatbot")

# チャット履歴
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴表示
print(st.session_state.messages)
message = Message()
message.display_chat_history()

# ユーザー入力
if prompt := st.chat_input("What is your question?"):

    llm = GroqAPI(st.session_state.selected_model)

    message.add_display("user", prompt)

    completion = llm.completion(st.session_state.messages)

    message.add_display("assistant", completion)

# 反省トークンと検索結果の表示（オプション）
# with st.expander("Show Reflection Tokens and Retrieved Documents"):
#     st.write(reflection_tokens)
#     st.write(retrieved_documents)
