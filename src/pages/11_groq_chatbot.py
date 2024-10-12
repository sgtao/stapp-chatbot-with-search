# 11_groq_chatbot.py
import json
from datetime import datetime

import streamlit as st

from components.GropApiKey import GropApiKey
from components.Message import Message
from components.ModelSelector import ModelSelector
from functions.GroqAPI import GroqAPI


# 『保存』ボタン：
def save_chat_history():
    # チャット履歴
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 現在の日時を取得してファイル名を生成
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{current_time}_chatbot.json"

    # チャット履歴をダウンロードするボタン
    if st.checkbox(
        "Save chat history?",
        # disabled=(not st.session_state.no_chat_history),
        # disabled=("messages" not in st.session_state),
        value=False,
        # expanded=True,
    ):
        # チャット履歴をJSONに変換
        chat_history = st.session_state.messages
        chat_json = json.dumps(chat_history, ensure_ascii=False, indent=2)
        # define collection_name
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{current_time}_chatbot.json"
        st.download_button(
            label="Download as json",
            data=chat_json,
            file_name=filename,
            mime="application/json",
        )


# チャット履歴
if "messages" not in st.session_state:
    st.session_state.messages = []

# sidebar: apikey input
groq_api_key = GropApiKey()
groq_api_key.input_key()

# sidebar: model selector
model = ModelSelector()
st.session_state.selected_model = model.select()

# sidebar: save chat history
with st.sidebar:
    # カラムを作成
    col1, col2 = st.columns([2, 1])
    # 会話履歴保存ボタン
    with col1:
        save_chat_history()
    # 会話履歴クリアボタン
    with col2:
        if st.button("クリア"):
            st.session_state.messages = []
            st.rerun()

# main pageの内容
st.title("Groq Chatbot")

if groq_api_key.has_key() is False:
    st.error("API-Keyを設定してください")
else:
    # ストリーム回答の切り替え
    stream_enabled = st.toggle("ストリーム", value=True)

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

        if stream_enabled:
            # ストリーミングレスポンスの表示
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in llm.response_stream(st.session_state.messages):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        else:
            # 通常の回答表示
            completion = llm.completion(st.session_state.messages)
            message.add_display("assistant", completion)
            full_response = completion

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        # 最後のメッセージまでスクロール
        st.markdown(
            """
            <script>
                const chatContainer =
                  window.parent.document.querySelector(".chat-container");
                chatContainer.scrollTop = chatContainer.scrollHeight;
            </script>
            """,
            unsafe_allow_html=True,
        )
