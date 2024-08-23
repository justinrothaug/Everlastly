import os
from dotenv import load_dotenv
import streamlit as st

# Importing Perplexity
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Everlastly")


#Add Keys
PPLX_API_KEY= os.environ['PPLX_API_KEY']


title = st.text_input("Product Search", "Everlastly")
st.write("The current product title is", title)
