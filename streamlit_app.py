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
PPLX_API_KEY2 = "Bearer "+PPLX_API_KEY

text_input = st.text_input("Enter Everlastly Product 👇", key="4", value = "Lodge 12 Inch Cast Iron Skillet")
prompt = st.text_area("Enter Prompt 👇", key="5", value = "Follow the below steps:"+
"2) Find the materials used in creating the product\n"+
"3) Find the estimated % and weight in pounds for each material.\n"+ 
"4) Calculate the Co2 carbon footprint for each Material.\n"+ 
"5) Multiply the percentage of each material by its respective carbon footprint per pound and then sum these values to estimate the Total Co2 for the Product.\n"+
"Format each step with a Header and the data. Output in CSV format like this: UPC Code,Product Name,Material,Country of Origin,Estimated %,Weight in Pounds,CO2 Carbon Footprint per Pound,Total CO2")

card="For the following product:"+text_input+prompt
                        
template = """You are a helpful assistant in giving a product description for {text}. 
Provide a one sentence explanation """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
def get_chatassistant_aitopics():
    aitopics = LLMChain(
        llm=ChatPerplexity(model="llama-3.1-sonar-small-128k-online", temperature=.8),prompt=chat_prompt,verbose=True)
    return aitopics
aitopics = get_chatassistant_aitopics()

def StartConvo2():
  import requests
  url = "https://api.perplexity.ai/chat/completions"
  payload = {"model": "llama-3.1-sonar-small-128k-online","messages": [{"role": "system","content": "Be as accurate as possible"},{"role": "user","content": card}]}
  headers = {"accept": "application/json", "content-type": "application/json", "authorization": PPLX_API_KEY2}
  response = requests.post(url, json=payload, headers=headers)
  responsetext=response.text
  st.warning("Current Product:  \n"+responsetext)


def StartConvo():
  responsememories = aitopics.run(card)
  st.warning("Current Product:  \n"+responsememories)



st.button('Run', on_click=StartConvo, key = "123", use_container_width=True)
#st.button('Run2', on_click=StartConvo2, key = "121", use_container_width=True)


