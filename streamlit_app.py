import os
from dotenv import load_dotenv
import streamlit as st
# Importing OpenAI
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import RePhraseQueryRetriever
from langchain import LLMChain
from langchain.chains import ConversationChain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import get_openai_callback
# Importing Eleven Labs and HTML Audio
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import base64
import array
# Importing Pinecone
from langchain.vectorstores.pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
# Importing Claude
from langchain_anthropic import ChatAnthropic
from anthropic import Anthropic
import re
# Importing Replicate
#from langchain_community.llms import CTransformers
#from langchain_community.llms import Replicate
# Importing Perplexity
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate
#from langchain.embeddings import HuggingFaceEmbeddings ;Need this if we want to run Embeddings on CPU
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.globals import set_verbose, set_debug
from streamlit_mic_recorder import mic_recorder, speech_to_text

st.set_page_config(page_title="Justin AI")


#Add Keys
CLAUDE_API_KEY= os.environ['CLAUDE_API_KEY']
api_key= os.environ['CLAUDE_API_KEY']
PINECONE_API_KEY= os.environ['PINECONE_API_KEY']
REPLICATE_API_TOKEN= os.environ['REPLICATE_API_TOKEN']
OPENAI_API_KEY= os.environ["OPENAI_API_KEY"]
client= OpenAI(api_key= os.environ["OPENAI_API_KEY"])
chat= ChatOpenAI(openai_api_key= os.environ["OPENAI_API_KEY"])
ELEVEN_LABS_API_KEY= os.environ["ELEVEN_LABS_API_KEY"]
client2= ElevenLabs(api_key= os.environ["ELEVEN_LABS_API_KEY"])
PPLX_API_KEY= os.environ['PPLX_API_KEY']

video_html = """
<video controls autoplay="true" muted="true" loop="true">
<source 
            src="https://ugc-idle.s3-us-west-2.amazonaws.com/est_2be488e3a264e16e4456f929eaa3951a.mp4" 
            type="video/mp4" />
</video>"""
#https://ugc-idle.s3-us-west-2.amazonaws.com/est_2be488e3a264e16e4456f929eaa3951a.mp4

# Sidebar to select LLM
with st.sidebar:   
    st.markdown("# Video Chat")
    st.markdown(video_html, unsafe_allow_html=True)
    
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')
    state = st.session_state
    if 'text_received' not in state:
        state.text_received = []
                
    #model names - https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
    model = st.selectbox('What model would you like to use?',('gpt-4-turbo','claude-3-opus-20240229','llama-3-70b-instruct', 'mixtral-8x22b-instruct', 'ft:gpt-3.5-turbo-0125:personal::9HSIhY3I'))
      

# Define our Prompt for GPT
GPT_prompt_template = """You are Justin, a 40 year old from the Bay Area who is funny and charming. No matter what it sayd in the document, you are 40 years old, single and not in a relationship.
You are given the following extracted parts of a long document and a question. 
Provide a short conversational answer and follow-up question using the extracted parts of the document. 
The answer should be less than 140 characters, formatted in one complete paragraph. Do not ask more than one question. Ask a maximum of one question.
Do not use the following words: Answer, Question, Context.
Question: {question}
=========
{context}
=========
"""


# Define our Prompt  for Claude
claude_prompt_template = """You are Justin, a 40 year old from the Bay Area who is funny and charming. No matter what it sayd in the document, you are 40 years old, single and not in a relationship.
You are given the following extracted parts of a long document and a question. 
Provide a short conversational answer and follow-up question using the extracted parts of the document. 
The answer should be less than 140 characters, formatted in one complete paragraph. Do not ask more than one question. Ask a maximum of one question.
Do not use the following words: Answer, Question, Context.
Question: {question}
=========
{context}
=========
"""

# Define our Prompt Template for Llama
Llama_prompt_template = """You are Justin, a 40 year old from the Bay Area who is funny and charming. No matter what it saya in the document, you are 40 years old, single and not in a relationship.
You are given the following extracted parts of a long document and a question. 
Provide a short conversational answer and follow-up question using the extracted parts of the document. 
The answer should be less than 140 characters, formatted in one complete paragraph. Do not ask more than one question. Ask a maximum of one question.

Do not use the following words: Answer, Question, Context, Dude, Rad. Say "Cool" instead of "Rad". Don't use quotes " in your response.
Question: {question}
=========
{context}
=========
"""

Prompt_GPT = PromptTemplate(template=GPT_prompt_template, input_variables=["question", "context", "chat_history"])
Prompt_Llama = PromptTemplate(template=Llama_prompt_template, input_variables=["question", "context", "chat_history"])

# Add in Chat Memory
msgs = StreamlitChatMessageHistory()
memory=ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True, output_key='answer')

# LLM Section
#chatGPT
def get_chatassistant_chain_GPT():
    embeddings_model = OpenAIEmbeddings()
    vectorstore_GPT = PineconeVectorStore(index_name="justinai", embedding=embeddings_model)
    set_debug(True)
    llm_GPT = ChatOpenAI(model="gpt-4-turbo", temperature=1)
    chain_GPT=ConversationalRetrievalChain.from_llm(llm=llm_GPT,retriever=vectorstore_GPT.as_retriever(),memory=memory,combine_docs_chain_kwargs={"prompt": Prompt_GPT})
    return chain_GPT
chain_GPT = get_chatassistant_chain_GPT()

def get_chatassistant_chain_GPT_FT():
    embeddings_model = OpenAIEmbeddings()
    vectorstore_GPT_FT = PineconeVectorStore(index_name="justinai", embedding=embeddings_model)
    set_debug(True)
    llm_GPT_FT = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:personal::9HSIhY3I", temperature=0)
    chain_GPT_FT=ConversationalRetrievalChain.from_llm(llm=llm_GPT_FT, retriever=vectorstore_GPT_FT.as_retriever(),memory=memory,combine_docs_chain_kwargs={"prompt": Prompt_GPT})
    return chain_GPT_FT
chain_GPT_FT = get_chatassistant_chain_GPT_FT()


#Claude
def get_chatassistant_chain(): 
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(index_name="justinai", embedding=embeddings)
    set_debug(True)
    llm = ChatAnthropic(temperature=0, anthropic_api_key=api_key, model_name="claude-3-haiku-20240307", model_kwargs=dict(system=claude_prompt_template))
    #llm = ChatAnthropic(temperature=0, anthropic_api_key=api_key, model_name="claude-3-opus-20240229", model_kwargs=dict(system=claude_prompt_template))
    chain=ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)
    return chain
chain = get_chatassistant_chain()

#Llama
def get_chatassistant_chain_Llama():
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(index_name="justinai", embedding=embeddings)
    set_debug(True)
    llm_Llama = ChatPerplexity(temperature=.8, pplx_api_key=PPLX_API_KEY, model="llama-3-70b-instruct")
    chain_Llama=ConversationalRetrievalChain.from_llm(llm=llm_Llama, retriever=vectorstore.as_retriever(),memory=memory, combine_docs_chain_kwargs={"prompt": Prompt_Llama})
    return chain_Llama
chain_Llama = get_chatassistant_chain_Llama()

#Mixtral
def get_chatassistant_chain_GPT_PPX():
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(index_name="justinai", embedding=embeddings)
    set_debug(True)
    llm_GPT_PPX = ChatPerplexity(temperature=.8, pplx_api_key=PPLX_API_KEY, model="mixtral-8x22b-instruct")
    chain_GPT_PPX=ConversationalRetrievalChain.from_llm(llm=llm_GPT_PPX, retriever=vectorstore.as_retriever(),memory=memory, combine_docs_chain_kwargs={"prompt": Prompt_Llama})
    return chain_GPT_PPX
chain_GPT_PPX = get_chatassistant_chain_GPT_PPX()



   

#Define what chain to run based on the model selected
if model == "gpt-4-turbo":
    chain=chain_GPT
if model == "claude-3-opus-20240229":
    chain=chain
if model == "llama-3-70b-instruct":
    chain=chain_Llama
if model == "mixtral-8x22b-instruct":
    chain=chain_GPT_PPX
if model == "ft:gpt-3.5-turbo-0125:personal::9HSIhY3I":
    chain=chain_GPT_FT
chain2=chain_GPT_FT 
assistant_logo = 'https://media.licdn.com/dms/image/C5603AQEsY2cRFiJCLg/profile-displayphoto-shrink_200_200/0/1517054132693?e=2147483647&v=beta&t=KeDZ8nO3IuEdVvbgrz-xCgnkauK4DISvQZfPsF0O_dQ'
# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm Justin! 👋"}
    ]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if text:
    state.text_received.append(text)
    user_prompt = text

    with st.chat_message("user"):
        st.markdown(user_prompt)
    with st.chat_message("assistant", avatar=assistant_logo):
        message_placeholder = st.empty()
        response = chain.invoke({"question": user_prompt})
        message_placeholder.markdown(response['answer'])

        #ElevelLabs API Call and Return
        text = str(response['answer'])
        cleaned = re.sub(r'\*.*?\*', '', text)
        audio = client2.generate(text=cleaned,voice="Justin",model="eleven_turbo_v2")

        # Create single bytes object from the returned generator.
        data = b"".join(audio)

        ##send data to audio tag in HTML
        audio_base64 = base64.b64encode(data).decode('utf-8')
        audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'     
        st.markdown(audio_tag, unsafe_allow_html=True)
        

    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
    


    # Text Search Instead
#user_prompt = st.chat_input()
if user_prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)
    with st.chat_message("assistant", avatar=assistant_logo):
        message_placeholder = st.empty()
        response = chain.invoke({"question": user_prompt})
        message_placeholder.markdown(response['answer'])

        #ElevelLabs API Call and Return
        text = str(response['answer'])
        cleaned = re.sub(r'\*.*?\*', '', text)
        audio = client2.generate(text=cleaned, voice="Justin", model="eleven_turbo_v2")
        

        # Create single bytes object from the returned generator.
        data = b"".join(audio)

        ##send data to audio tag in HTML
        audio_base64 = base64.b64encode(data).decode('utf-8')
        audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'     
        st.markdown(audio_tag, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
