# 11_groq_chatbot.py
import streamlit as st

from components.GropApiKey import GropApiKey
from components.Message import Message
from components.ModelSelector import ModelSelector
from components.ManageChatbot import ManageChatbot
from functions.GroqAPI import GroqAPI

# Message インスタンスの作成
message = Message("groq_chatbot")


# sidebar: apikey input
groq_api_key = GropApiKey()
groq_api_key.input_key()

# sidebar: model selector
model = ModelSelector()
st.session_state.selected_model = model.select()

# sidebar: save chat history
manage_chatbot = ManageChatbot("groq_chatbot")
manage_chatbot.sidebar_save_clear(message)


# main pageの内容
st.title("Groq Chatbot")

if groq_api_key.has_key() is False:
    st.error("API-Keyを設定してください")
else:
    # ストリーム回答の切り替え
    stream_enabled = st.toggle("ストリーム", value=True)

    # チャット履歴表示
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
                for chunk in llm.response_stream(message.get_messages()):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            message.add("assistant", full_response)
        else:
            # 通常の回答表示
            response = llm.completion(message.get_messages())
            message.add_display("assistant", response)

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
