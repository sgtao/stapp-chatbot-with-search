# chat_with_qiita.py
import time

import streamlit as st
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)

# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langchain.tools import Tool

from components.GropApiKey import GropApiKey
from components.ModelSelector import ModelSelector
from functions.QiitaApiItems import QiitaApiItems

st.set_page_config(page_title="LangChain: Chat with search", page_icon="🔍")
st.title("🔍LangChain: Chat with Qiita search")
page_description = """このページはQiita APIで検索した１つの結果からの回答します。
そのため、検索結果外としてないこともあります。
"""
st.info(page_description)

# サイドバーの設定
st.sidebar.title("設定")
# sidebar: apikey input
groq_api_key = GropApiKey()
groq_api_key.input_key()

# - model selector
model = ModelSelector()
with st.sidebar:
    st.subheader("Select a model, etc.")
    st.session_state.selected_model = model.select()

# メイン領域でチャット
if not st.session_state.groq_api_key:
    st.info("Groq API キーを入力してください。")
    st.stop()

# チャット履歴の設定
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs,
    return_messages=True,
    memory_key="chat_history",
    output_key="output",
)

if len(msgs.messages) == 0 or st.sidebar.button("チャット履歴をリセット"):
    msgs.clear()
    msgs.add_ai_message("どのようにお手伝いできますか？")
    st.session_state.steps = {}

# チャット履歴の表示
for msg in msgs.messages:
    st.chat_message("user" if msg.type == "human" else "assistant").write(
        msg.content
    )
# avatars = {"human": "user", "ai": "assistant"}
# for idx, msg in enumerate(msgs.messages):
#     with st.chat_message(avatars[msg.type]):
#         # Render intermediate steps if any were saved
#         for step in st.session_state.steps.get(str(idx), []):
#             if step[0].tool == "_Exception":
#                 continue
#             with st.status(
#                 f"**{step[0].tool}**: {step[0].tool_input}", state="complete"
#             ):
#                 st.write(step[0].log)
#                 st.write(step[1])
#         st.write(msg.content)


# カスタム検索ツールの定義
def custom_search(query: str) -> str:
    exception_msg = """申し訳ありませんが、現在検索サービスにアクセスできません。
    別の方法で質問にお答えしますので、もう一度お試しください。
    """
    try:
        qiit_items = QiitaApiItems()
        # print(f"search query is {query}")
        time.sleep(1)  # レートリミット対策として1秒待機
        # search = DuckDuckGoSearchRun()
        # return search.run(query)
        # search = DuckDuckGoSearchResults()
        # return search.invoke(query)
        articles = qiit_items.get_articles(
            params={"query": query},
            page_size=1,
        )
        article_bodies = []
        for article in articles:
            article_bodies.append(
                {
                    "title": article["title"],
                    "body": article["body"],
                }
            )
        return article_bodies
    except Exception as e:
        st.warning(f"検索中にエラーが発生しました: {str(e)}")
        return exception_msg


# ユーザー入力
if prompt := st.chat_input("質問を入力してください"):
    st.chat_message("user").code(prompt)

    # LLMとエージェントの設定
    llm = ChatGroq(
        temperature=0,
        model=st.session_state.selected_model,
        api_key=st.session_state.groq_api_key,
    )
    # カスタム検索ツールの作成
    # tools = [DuckDuckGoSearchRun(name="Search")]
    search_description = """useful for answering questions about
    software technology, web design, AI, and other ICT fields.
    """
    search_tool = Tool(
        name="Search", func=custom_search, description=search_description
    )
    tools = [search_tool]

    chat_agent = ConversationalChatAgent.from_llm_and_tools(
        llm=llm, tools=tools
    )
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )

    # 応答の生成と表示
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(
            st.container(), expand_new_thoughts=False
        )
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        response = executor.invoke(prompt, cfg)
        st.write(response["output"])
        st.session_state.steps[str(len(msgs.messages) - 1)] = response[
            "intermediate_steps"
        ]
