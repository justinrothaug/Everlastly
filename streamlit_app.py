import os
from dotenv import load_dotenv
import streamlit as st
import random
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
with st.sidebar: 
   st.title("Evergrade.AI")  
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

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)


with st.sidebar: 
      message = st.text_input("Enter Everlastly Product 👇", key="4", value = "ZWILLING Twin Kitchen Shears, 8 Inch")
      #st.button('Run🍃', on_click=ProductBOM, key = "121", use_container_width=True)


product_prompt = ("Follow the below steps:\n"+
"*Prioritize sources like Amazon and the Company website*\n"+
"1) Identify the Total Weight of the product.\n"+
"2) Find every material used in creating the product. Do not skip any materials.Materials combined must equal 100%.\n"+
"3) For each material, find both the source country and manufacturing country.\n"+
"4) Find the *estimated % of the total volume for each material. \n"+
"5) Find the density for each material in lb/ft^3. List the source for this data\n"+
"6) Calculate the weight of each material using the following steps:\n"+
"6a) find the Volume-Density by multiplying each material’s volume percentage by that material’s density\n"+
"6b) Calculate the Density-Ratio by dividing that material’s Volume-Density by the total for all Volume-Densities of all materials found in the product\n"+
"6c) Multiply the Density Ratio by the total weight of the product. This should equal the total weight of the product found in Step 1.\n"+                         
"7) Find the Published Carbon Footprint for each Material, expressed as Co2 per Pound\n"+
"8) Multiply the Part Weight of each material by its respective Published Carbon Footprint per pound to get the Carbon Footprint for that Material Part. Then sum these values to estimate the Total Co2 for the Product.\n"+
"Only output in Table format like this:\n"+ 
"UPC Code,Product Name,Material,Source Country, Manufacturing Country,Estimated % in Volume,Material Density, Volume Density, Density Ratio,Weight in Pounds,Published CO2 Carbon Footprint per Pound,Total Carbon Footprint for that Material Part\n"+
"List the Data Source URL links (Amazon, ect.)")

product_prompt2 = ("Follow the below steps:\n"+
"*Prioritize sources like Amazon and the Company website*\n"+
"1) Identify the Total Weight of the product.\n"+
"2) Find every material used in creating the product. Do not skip any materials.Materials combined must equal 100%.\n"+
"3) For each material, find both the source country and manufacturing country.\n"+
"4) Find the *estimated % of the total volume for each material. \n"+
"5) Find the density for each material in lb/ft^3. List the source for this data\n"+
"6) Calculate the weight of each material using the following steps:\n"+
"6a) find the Volume-Density by multiplying each material’s volume percentage by that material’s density\n"+
"6b) Calculate the Density-Ratio by dividing that material’s Volume-Density by the total for all Volume-Densities of all materials found in the product\n"+
"6c) Multiply the Density Ratio by the total weight of the product. This should equal the total weight of the product found in Step 1.\n"+                         
"7) Find the Published Carbon Footprint for each Material, expressed as Co2 per Pound\n"+
"8) Multiply the Part Weight of each material by its respective Published Carbon Footprint per pound to get the Carbon Footprint for that Material Part. Then sum these values to estimate the Total Co2 for the Product.\n"+
"Only output in Table format like this:\n"+ 
"UPC Code,Product Name,Material,Source Country, Manufacturing Country,Estimated % in Volume,Material Density, Volume Density, Density Ratio,Weight in Pounds,Published CO2 Carbon Footprint per Pound,Total Carbon Footprint for that Material Part\n"+
"List the Data Source URL links (Amazon, ect.)")


   

#st.warning(text_input)

def eval_output(message):
     productcard="For the following product:"+message+product_prompt
     template = """You are a helpful assistant in following instructions for {text}. 
     Provide a one sentence explanation """
     system_message_prompt = SystemMessagePromptTemplate.from_template(template)
     human_template = "{text}"
     human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
     chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
     def get_chatassistant_aitopics():
         aitopics = LLMChain(
             llm=ChatPerplexity(model="llama-3.1-sonar-small-128k-online", temperature=0),prompt=chat_prompt,verbose=True)
         return aitopics
     aitopics = get_chatassistant_aitopics()
     response1 = aitopics.run(productcard)

def production_output(message):
     productcard="For the following product:"+message+product_prompt2
     template = """You are a helpful assistant in following instructions for {text}. 
     Provide a one sentence explanation """
     system_message_prompt = SystemMessagePromptTemplate.from_template(template)
     human_template = "{text}"
     human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
     chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
     def get_chatassistant_aitopics():
         aitopics = LLMChain(
             llm=ChatPerplexity(model="llama-3.1-sonar-small-128k-online", temperature=0),prompt=chat_prompt,verbose=True)
         return aitopics
     aitopics = get_chatassistant_aitopics()
     response2 = aitopics.run(productcard)
   
#STREAMLIT APP
#st.title("💬 RealAvatar Arena")
#message = st.text_input("Let's see which AI is better. Write something:")
if message:
    first_one = random.choice([1,2,3,4,5,6])
    if first_one>3:
        response1 = eval_output(message)
        response2 = production_output(message)
    else:
        response1 = production_output(message)
        response2 = eval_output(message)

    col1, col2 = st.columns(2)
    with col1:
        st.success(response1)
        if st.button("Select Bot 1 Response", key='select1'):
            st.session_state.selected = "Bot 1"
    with col2:
        st.success(response2)
        if st.button("Select Bot 2 Response", key='select2'):
            st.session_state.selected = "Bot 2"

    if 'selected' in st.session_state:
        if first_one>3:
            st.success(f"You selected Llama 3.1 70B")
        else:
            st.success(f"You selected Claude 3.5 Sonnet")
           
  #st.warning("Product BOM:  \n"+responsememories)


