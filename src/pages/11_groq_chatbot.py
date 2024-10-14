# 11_groq_chatbot.py
import streamlit as st
import chardet

from components.ChatParameters import ChatParameters
from components.GropApiKey import GropApiKey
from components.Message import Message
from components.ModelSelector import ModelSelector
from components.ManageChatbot import ManageChatbot
from functions.GroqAPI import GroqAPI


# ファイルの内容を読み取り、UTF-8に変換する関数
def read_and_convert_to_utf8(file):
    content = file.read()
    detected = chardet.detect(content)
    encoding = detected["encoding"]

    if encoding.lower() != "utf-8":
        try:
            content = content.decode(encoding).encode("utf-8").decode("utf-8")
        except UnicodeDecodeError:
            st.error(
                f"ファイルの文字コード（{encoding}）を正しく変換できませんでした。"
            )
            return None
    else:
        content = content.decode("utf-8")

    return content


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


# main pageの内容
st.title("Groq Chatbot")

if groq_api_key.has_key() is False:
    st.error("input API-Key in sidebar!")
else:
    # カラムを作成
    col1, col2 = st.columns([1, 1])
    uploaded_file = None
    # ファイルアップロード機能
    with col1:
        col1.subheader("Attach. text file:")
        uploaded_file = st.file_uploader(
            "Before 1st chat, You can upload an article",
            type=("txt", "md"),
            disabled=st.session_state.disabled_edit_params,
        )
        if message.has_chat_history() is False and uploaded_file is not None:
            # ファイルの内容を読み取り、UTF-8に変換する
            file_content = read_and_convert_to_utf8(uploaded_file)
            if file_content is not None:
                # ファイルの内容をmessageリストに追加
                message.append_system_prompts()
                message.add(
                    "system",
                    f"以下はアップロードされたファイルの内容です：\n\n{file_content}",
                )
            else:
                st.error("ファイルの内容を正しく読み取れませんでした。")

    # chat_history アップロード機能
    with col2:
        col2.subheader("Attach. past chat:")
        uploaded_file = st.file_uploader(
            "You can upload an previous chat history",
            type=("json"),
            disabled=st.session_state.disabled_edit_params,
        )
        if message.has_chat_history() is False and uploaded_file is not None:
            import json

            # message.アップロードされたファイルは手動でクリア
            chat_history_messages = json.load(uploaded_file)
            message.set_whole_messages(chat_history_messages)
            st.session_state.disabled_edit_params = True

    if uploaded_file is not None:
        # アップロードされたファイルは手動でクリア
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
