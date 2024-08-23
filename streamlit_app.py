import os
from dotenv import load_dotenv
import streamlit as st

# Importing Perplexity
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains import     ConversationalRetrievalChain
from langchain.prompts.chat import (ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate,)
from langchain.chains import LLMChain, ConversationChain

st.set_page_config(page_title="Everlastly")


#Add Keys
PPLX_API_KEY= os.environ['PPLX_API_KEY']


text_input = st.text_input("Enter Everlastly Product 👇", key="4")
prompt = st.text_input("Enter Prompt 👇", key="5")

card=prompt+text_input
                        

template = """You are a helpful assistant in giving a product description for {text}. 
Provide a one sentence explanation """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
def get_chatassistant_aitopics():
    aitopics = LLMChain(
        llm=ChatPerplexity(model="llama-3.1-sonar-huge-128k-online", temperature=.8),prompt=chat_prompt,verbose=True)
    return aitopics
aitopics = get_chatassistant_aitopics()

responsememories = aitopics.run(card)
st.warning("Current Product:  \n"+responsememories)
