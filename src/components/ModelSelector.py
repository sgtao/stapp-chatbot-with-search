# ModelSelector.py
import streamlit as st


class ModelSelector:
    """Class for selecting the Groq model"""

    def __init__(self):
        """Define the available models"""
        self.models = ["llama3-8b-8192", "llama3-70b-8192"]

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
