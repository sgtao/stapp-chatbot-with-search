# 11_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey
from components.Message import Message
from components.ModelSelector import ModelSelector
from functions.GroqAPI import GroqAPI


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
# print(st.session_state.messages)
message = Message()
message.display_chat_history()

# ユーザー入力
if prompt := st.chat_input("What is your question?"):

    llm = GroqAPI(
        api_key=groq_api_key.key(),
        model_name=st.session_state.selected_model,
    )

    message.add_display("user", prompt)

    completion = llm.completion(st.session_state.messages)

    message.add_display("assistant", completion)

# 反省トークンと検索結果の表示（オプション）
# with st.expander("Show Reflection Tokens and Retrieved Documents"):
#     st.write(reflection_tokens)
#     st.write(retrieved_documents)
