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

st.set_page_config(page_title="Evergrade.AI", layout="wide")

#Add Keys
PPLX_API_KEY= os.environ['PPLX_API_KEY']
PPLX_API_KEY2 = "Bearer "+PPLX_API_KEY

header = st.container()
header.title("Evergrade.AI")

#################################################################################################################################################
### Custom CSS for the sticky header#########
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: dove gray;
        z-index: 999;
    }
    .fixed-header {
        border-bottom: 1px solid black;
    }
</style>
    """,
    unsafe_allow_html=True
)


with st.sidebar: 
      text_input = st.text_input("Enter Everlastly Product 👇", key="4", value = "Lodge 12 Inch Cast Iron Skillet")

      product_prompt = st.text_area("Product & BOM 👇", key="5", value = "Follow the below steps:\n"+
      "1) Find the materials used in creating the product.\n"+
      "2) Find the estimated % and weight in pounds for each material.\n"+ 
      "3) Calculate the Co2 carbon footprint for each Material (Co2 per Pound).\n"+ 
      "4) Multiply the percentage of each material by its respective carbon footprint per pound and then sum these values to estimate the Total Co2 for the Product.\n"+
      "Hide the above steps. Only output in Table format like this:\n"+ 
      "UPC Code,Product Name,Material,Country of Origin,Estimated %,Weight in Pounds,CO2 Carbon Footprint per Pound,Total CO2\n"+
      "List the Data Source URL links (Amazon, ect.)")


      category_prompt = st.text_area("Category 👇", key="3", value = "Follow the below steps:"+
      "Create a excel style table of product categories based on the Amazon listing,  using the following formatting as a guide: \n"+
      "Department, Category, Subcategory, Specific Category. \n"+ 
      "Add a final column that shows the type of product within the specific category by analyzing the different product types available.")
      
      lifespan_prompt = st.text_area("Lifespan 👇", key="2", value = "Follow the below steps:\n"+
      "List the general types of skillets and frypans, then estimate their lifespan in one number of years where lifetime is equal to 100 years, and display results in an table format including a column that displays the specific product category.")



productcard="For the following product:"+text_input+product_prompt
categorycard="For the following product:"+text_input+category_prompt
lifespancard="For the following: "+lifespan_prompt
      

def ProductBOM():

  st.warning(text_input)

    
  template = """You are a helpful assistant in following instructions for {text}. 
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
  responsememories = aitopics.run(productcard)
  st.warning("Product BOM:  \n"+responsememories)


#def category():
  template = """You are a helpful assistant in following instructions for {text}. 
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
  responsememories = aitopics.run(categorycard)
  st.warning("Product Category:  \n"+responsememories)

#def lifespan():
  template = """You are a helpful assistant in following instructions for {text}. 
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
  responsememories = aitopics.run(lifespancard)
  st.warning("Product Lifespan:  \n"+responsememories)



with st.sidebar: 
    st.button('Run', on_click=ProductBOM, key = "121", use_container_width=True)
    #st.button('Run category', on_click=category, key = "122", use_container_width=True)
    #st.button('Run lifespan', on_click=lifespan, key = "123", use_container_width=True)








#Test output from API directly:
def StartConvo2():
  import requests
  url = "https://api.perplexity.ai/chat/completions"
  payload = {"model": "llama-3.1-sonar-small-128k-online","messages": [{"role": "system","content": "Be as accurate as possible"},{"role": "user","content": card}]}
  headers = {"accept": "application/json", "content-type": "application/json", "authorization": PPLX_API_KEY2}
  response = requests.post(url, json=payload, headers=headers)
  responsetext=response.text
  st.warning("Current Product:  \n"+responsetext)
#st.button('Run2', on_click=StartConvo2, key = "120", use_container_width=True)


