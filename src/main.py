import streamlit as st

"""
# Welcome to stapp-chatbot-with-search apps!

- This application use Groq-API.
  - so, [Get an Groq API key](https://console.groq.com/keys)
"""

# サイドバーのページに移動
st.page_link("pages/11_groq_chatbot.py", label="Go to Groq Chatbot", icon="💬")
st.page_link(
    "pages/12_chat_with_search.py",
    label="Go to LangChain: Chat with search",
    icon="🦜"
)
