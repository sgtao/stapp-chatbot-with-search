import json

import streamlit as st
import chardet


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


class FileUploaders:
    def __init__(self, name):
        self.name = name
        self.session_key = f"{name}_message"
        st.session_state.filename = f"{name}.json"
        if self.session_key not in st.session_state:
            st.error(
                "FileUploaders need st.session_state.[session_key]_message."
            )

    def text_file_upload(self, message):
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
                st.session_state.disabled_edit_params = True
            else:
                st.error("ファイルの内容を正しく読み取れませんでした。")

    def json_chat_history(self, message):
        uploaded_file = st.file_uploader(
            "You can upload an previous chat history",
            type=("json"),
            disabled=st.session_state.disabled_edit_params,
        )
        if message.has_chat_history() is False and uploaded_file is not None:
            # message.アップロードされたファイルは手動でクリア
            chat_history_messages = json.load(uploaded_file)
            message.set_whole_messages(chat_history_messages)
            st.session_state.disabled_edit_params = True
