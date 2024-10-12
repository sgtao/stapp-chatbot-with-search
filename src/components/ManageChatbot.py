import json
from datetime import datetime

import streamlit as st


class ManageChatbot:
    def __init__(self, name):
        self.name = name

    # 『保存』ボタン：
    def save_message(self, message):
        if self.name != message.get_name():
            st.error("diffence session_state name")
            return

        # 現在の日時を取得してファイル名を生成
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{current_time}_{message.get_name()}.json"

        # チャット履歴をダウンロードするボタン
        if st.checkbox("Save chat history?", value=False):
            # チャット履歴をJSONに変換
            chat_history = message.messages_history()
            chat_json = json.dumps(chat_history, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download as json",
                data=chat_json,
                file_name=filename,
                mime="application/json",
            )

    def sidebar_save_clear(self, message):
        with st.sidebar:
            # カラムを作成
            col1, col2 = st.columns([2, 1])
            # 会話履歴保存ボタン
            with col1:
                self.save_message(message)

            # 会話履歴クリアボタン
            with col2:
                if st.button("クリア"):
                    message.clear_messages()
                    st.rerun()
