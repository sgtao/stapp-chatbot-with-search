# 11_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey
from components.Message import Message
from components.ModelSelector import ModelSelector
from functions.GroqAPI import GroqAPI


# sidebar: apikey input
groq_api_key = GropApiKey()
groq_api_key.input_key()

# sidebar: model selector
model = ModelSelector()
st.session_state.selected_model = model.select()

# main pageの内容
st.title("Groq Chatbot")

if groq_api_key.has_key() is False:
    st.error("API-Keyを設定してください")
else:
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

        # completion = llm.completion(st.session_state.messages)
        # message.add_display("assistant", completion)
        response = message.display_stream(
            generater=llm.response_stream(st.session_state.messages)
        )
        message.add("assistant", response)

    # 反省トークンと検索結果の表示（オプション）
    # with st.expander("Show Reflection Tokens and Retrieved Documents"):
    #     st.write(reflection_tokens)
    #     st.write(retrieved_documents)
