import os
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# LangSmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("user", "Question: {question}")
    ]
)

# Streamlit UI
st.title("Langchain GenAIapp Powered with Gemma Model")
text_input = st.text_input("What questions would you like to ask?")

# LLM
llm = OllamaLLM(model="gemma:2b")

# Correct parser instance
parser = StrOutputParser()

# Correct chain order → prompt → LLM → parser
chain = prompt | llm | parser

# Run chain
if text_input:
    result = chain.invoke({"question": text_input})
    st.write(result)

