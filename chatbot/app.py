from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"    #captures the monitoring results
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") #dashboard to store the monitoring results

#### Prompt Template

prompt = ChatPromptTemplate.from_messages(
    [
     ("system", "As a virtual assistant, please respond to the user queries"),
     ("user", "Question: {question}")
     ]
    )

st.title("OpenAI demo with LangChain")
input_text = st.text_input("Type your queries here")

#OPENAI LLM
llm = ChatOpenAI(model = "gpt-3.5-turbo")
output_parser=StrOutputParser() 
chain = prompt|llm|output_parser #step 1 to give prompt, step 2 to integrate the model a,d step 3 to get the output

if input_text:
    st.write(chain.invoke({'question': input_text}))
