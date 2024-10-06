# ModelSelector.py
import streamlit as st


class ModelSelector:
    """Class for selecting the Groq model"""

    def __init__(self):
        """Define the available models"""
        self.models = [
            "gemma2-9b-it",
            "gemma-7b-it",
            "llama3-groq-70b-8192-tool-use-preview",
            "llama3-groq-8b-8192-tool-use-preview",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3.2-1b-preview",  # shot token
            "llama-3.2-3b-preview",
            "llama-3.2-11b-vision-preview",
            # "llama-3.2-90b-vision-preview", # NotFoundError yet.
            # "llama-guard-3-8b", # response safe
            # "llava-v1.5-7b-4096-preview", # BadRequestError at chat.
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",  # shot token
        ]

    def select(self):
        """
        Display the model selection form in the sidebar
        Returns:
            st.selectbox of Models
        """
        with st.sidebar:
            st.sidebar.title("ModelSelector")
            return st.selectbox(
                "Select a model:", self.models, label_visibility="collapsed"
            )
