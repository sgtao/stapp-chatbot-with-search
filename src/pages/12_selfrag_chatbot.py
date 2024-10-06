# selfrag_chatbot.py
import streamlit as st


# 関数の定義
def self_rag_response(prompt):
    print(f"prompt: {prompt}")
    response = ["hello"]
    return response


# pageの内容
st.title("SELF-RAG Chatbot")

# チャット履歴
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャット履歴表示
print(st.session_state.messages)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザー入力
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ボットの応答
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # ここでLangChainを使用してSELF-RAG処理を行う
        # 結果をストリーミング表示
        for chunk in self_rag_response(prompt):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # ここでLangChainを使用してSELF-RAG処理を行う
        # 結果をストリーミング表示
        for chunk in self_rag_response(prompt):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )


# 反省トークンと検索結果の表示（オプション）
# with st.expander("Show Reflection Tokens and Retrieved Documents"):
#     st.write(reflection_tokens)
#     st.write(retrieved_documents)
