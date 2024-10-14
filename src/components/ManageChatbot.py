import json
from datetime import datetime

import streamlit as st


# ファイル名を生成するcallback関数
def generate_filename():
    # 現在の日時を取得してファイル名を生成
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    # self.filename = f"{current_time}_{message.get_name()}.json"
    st.session_state.filename = f"{current_time}_chat_history.json"


class ManageChatbot:
    def __init__(self, name):
        self.name = name
        self.session_key = f"{name}_message"
        st.session_state.filename = f"{name}.json"
        if self.session_key not in st.session_state:
            st.error(
                "ManageChatbot need st.session_state.[session_key]_message."
            )

    # 『保存』ボタン：
    def save_message(self, message):
        if self.name != message.get_name():
            st.error("diffence session_state name")
            return

        # チャット履歴をダウンロードするボタン
        # if st.checkbox(
        #     "Save chat history?",
        #     key="save_checkbox",
        #     value=st.session_state.checked_save,
        # ):
        with st.expander("Save chat ?", expanded=False):
            st.write("maybe need to DL twice...")
            # 現在の日時を取得してファイル名を生成
            # current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
            # filename = f"{current_time}_{message.get_name()}.json"
            pad = f"{message.get_name()}.json"
            # チャット履歴をJSONに変換
            chat_history = message.messages_history()
            chat_json = json.dumps(chat_history, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download as json",
                data=chat_json,
                # file_name=filename,
                file_name=f"{datetime.now().strftime("%Y%m%d-%H%M%S")}_{pad}",
                mime="application/json",
            )

    def sidebar_save_clear(self, message):
        # カラムを作成
        col1, col2 = st.columns([2, 1])
        # 会話履歴保存ボタン
        with col1:
            self.save_message(message)

        # 会話履歴クリアボタン
        with col2:
            if st.button("クリア"):
                message.clear_messages()
                # 話履歴クリア後、チェックボックスをFalseに戻す
                st.session_state.checked_save = False
                st.rerun()
