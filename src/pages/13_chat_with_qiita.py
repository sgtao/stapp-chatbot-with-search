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
from langchain.prompts import PromptTemplate

from components.GropApiKey import GropApiKey
from components.ModelSelector import ModelSelector
from functions.GroqAPI import GroqAPI
from functions.QiitaApiItems import QiitaApiItems


def summarize_message(message: str, limit: int) -> str:
    """メッセージを要約する
    Args:
        message (str): オリジナルメッセージ
        limit (int): 上限文字数
    Returns:
        str: 要約した文章
    """
    # PromptTemplateを作成
    prompt_template = PromptTemplate.from_template(
        "以下のメッセージを{limit}文字以内に要約してください。"
        "要約は日本語で行ってください。\n\n"
        "メッセージ: {message}\n\n"
        "要約:"
    )
    # メッセージを先頭の5,000文字に制限
    truncated_message = message[:5000]
    # プロンプトを生成
    prompt = prompt_template.format(message=truncated_message, limit=limit)
    # print(prompt)
    # 通常の回答表示
    llm = GroqAPI(
        api_key=st.session_state.groq_api_key,
        model_name="llama-3.1-8b-instant",
    )
    summarized_message = llm.completion([{"role": "user", "content": prompt}])
    # print("## 要約文：")
    # print(summarized_message)
    return summarized_message


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
            page_size=5,
        )
        article_bodies = []
        for article in articles:
            article_body = article["body"]
            if len(article_body) >= 800:
                article_body = summarize_message(article_body, 800)
            article_bodies.append(f'# {article["title"]}\n{article_body}')
        return article_bodies
    except Exception as e:
        st.warning(f"検索中にエラーが発生しました: {str(e)}")
        return exception_msg


st.set_page_config(page_title="LangChain: Chat with search", page_icon="🔍")
st.title("🔍LangChain: Chat with Qiita search")
page_description = """このページはQiita APIで検索した５つの結果からの回答します。
検索結果は要約することもあるため、すべての情報を利用するとは限りません。
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
    software technology, ICT related fields including computer software,
    web design, artificial intelligence, data analysis, cloud computing,
    cybersecurity, networking, databases and other related topics.
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
