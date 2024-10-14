# 11_groq_chatbot.py
import streamlit as st

from components.ChatParameters import ChatParameters
from components.GropApiKey import GropApiKey
from components.FileUploaders import FileUploaders
from components.Message import Message
from components.ModelSelector import ModelSelector
from components.ManageChatbot import ManageChatbot
from functions.GroqAPI import GroqAPI


# ページの設定
st.set_page_config(page_title="Groq Chatbot", page_icon="💬")


# Message インスタンスの作成
message = Message("groq_chatbot")


# sidebar: apikey input
groq_api_key = GropApiKey()
groq_api_key.input_key()

# sidebar:
# - model selector
# - save chat history
# - setup llm completion parameters
model = ModelSelector()
manage_chatbot = ManageChatbot("groq_chatbot")
chat_parameters = ChatParameters()
with st.sidebar:
    st.subheader("Select a model, etc.")
    st.session_state.selected_model = model.select()
    st.subheader("Save chat history")
    manage_chatbot.sidebar_save_clear(message)
    st.subheader("LLM parameters")
    chat_parameters.system_prompt()
    chat_parameters.tuning_parameters()


file_uploaders = FileUploaders("groq_chatbot")

# main pageの内容
st.title("Groq Chatbot")

if groq_api_key.has_key() is False:
    st.error("input API-Key in sidebar!")
else:
    # 初回チャット時に添付ファイルのアップローダーを表示：
    uploaded_file = None
    if message.has_chat_history() is False:
        st.subheader("Attachment text file or chat history json:")
        col1, col2 = st.columns([1, 1])
        # ファイルアップロード機能
        with col1:
            uploaded_file = file_uploaders.text_file_upload(message)
        # chat_history アップロード機能
        with col2:
            upload_file = file_uploaders.json_chat_history(message)
    # アップロードファイルは手動クリアとなるため、メッセージ表示
    if uploaded_file is not None:
        st.warning("After clear chat, CLEAR upload_file manualy.")

    # ストリーム回答の切り替え
    stream_enabled = st.toggle("streamed completion", value=False)

    # チャット履歴表示
    message.display_chat_history()

    # ユーザー入力
    if prompt := st.chat_input("What is your question?"):
        llm = GroqAPI(
            api_key=groq_api_key.key(),
            model_name=st.session_state.selected_model,
        )

        # 最初の質問投稿時にシステムプロンプト・添付ファイル内容をセットする
        message.append_system_prompts()

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
