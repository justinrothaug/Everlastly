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

st.set_page_config(page_title="Evergrade.Arena", layout="wide")

#Add Keys
PPLX_API_KEY= os.environ['PPLX_API_KEY']
PPLX_API_KEY2 = "Bearer "+PPLX_API_KEY

header = st.container()
header.title("Evergrade.Arena")
#with st.sidebar: 
   #st.title("Evergrade.AI")  
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
      message = st.text_input("Enter Evergrade Product 👇", key="4", value = "ZWILLING Twin Kitchen Shears, 8 Inch")
      eval = st.toggle("Evaluation Mode", value=True)
      tentimes = st.toggle("Run 10 Times", value=False)
      showwork = st.toggle("Show Work", value=True)



product_prompt = ("Follow the below steps:\n"+
   "*Prioritize sources like Amazon and the Company website.* If the source is Amazon, prioritize sections like 'Product Information', 'Product Overview' and 'From the manufacturer' for any details.\n"+
   "1) Find the Total Weight of the product in pounds using several sources (including amazon.com where it can be found under 'item weight') to make sure it's correct.\n"+
   "2) Identify all Materials used in creating the product and also estimate the percentage of total volume of each Material for that product (called Material Percentage). Analyze closely all product images and accompanying product texts to determine Materials and Material Percentage. Do not skip any materials. Material Percentage percentages combined must equal 100%.\n"+
   "3) For each Material, identify the Material Source Country defined as the most likely single country where the material is first sourced and processed based on research that shows where most of that Material is being sourced for manufacturing.\n"+
   "4) Next find the Country of Origin defined as the country where the product was manufactured.\n"+
   "5) Find the published Density for each Material in lb/ft^3 (called Material Density). List the source for this data\n"+
   "6) Calculate the Part Weight of each Material using the following steps:\n"+
   "6a) find the Volume-Density by multiplying each Material’s Material Percentage by that Material’s Material Density\n"+
   "6b) Calculate the Density-Ratio by dividing that Material’s Volume-Density by the total for all Volume-Densities of all Materials found in the product\n"+
   "6c) Calculate the Part Weight by multiplying the Density-Ratio by the Total Weight of the product. The sum of all Part Weights should equal the Total Weight of the product found in Step 1.\n"+                         
   "7) Find the generally accepted carbon footprint for each Material (called the Published Material Carbon Footprint), expressed as both Kg Co2/Pound and Kg Co2/kg\n"+
   "8) Multiply the Part Weight of each material by its respective Published Material Carbon Footprint per pound to get the Material/Product Total Co2. Then sum all Material/Product Total Co2 values to get the Product Co2 Total for the product.\n"+
   "Only output in Table format like this:\n"+ 
   "UPC Code,Product Name, Material,Material Source Country, Country of Origin, Material Percentage, Material Density, Volume-Density, Density-Ratio,Part Weight in Pounds,Published Carbon Footprint per Pound, Published Carbon Footprint per Kg, Material/Product Total Co2, Product Co2 Total.\n"+
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

if showwork:
   output = ""
else:
   output = "DO NOT DISPLAY STEPS 1-8 IN THE OUTPUT. ONLY DISPLAY THE TABLE"
   



#st.warning(text_input)

def eval_output(message):
     productcard="For the following product: "+message+product_prompt
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
     return response1


def production_output(message):
     productcard="For the following product: "+message+product_prompt2
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
     return response2
   
if message:
   if eval:
      response1 = eval_output(message+output)
      response2 = production_output(message+output)
      st.success(response1)
      st.success(response2)
   if tentimes:
      response1 = eval_output(message+output)
      response2 = eval_output(message+output)
      response3 = eval_output(message+output)
      response4 = eval_output(message+output)
      response5 = eval_output(message+output)
      response6 = eval_output(message+output)
      response7 = eval_output(message+output)
      response8 = eval_output(message+output)
      response9 = eval_output(message+output)
      response10 = eval_output(message+output)
      st.success(response1)
      st.success(response2)
      st.success(response3) 
      st.success(response4) 
      st.success(response5) 
      st.success(response6) 
      st.success(response7) 
      st.success(response8) 
      st.success(response9) 
      st.success(response10) 



#with st.sidebar:
#   st.button('Run🍃', on_click=ProductBOM, key = "121", use_container_width=True)
   

   
   




