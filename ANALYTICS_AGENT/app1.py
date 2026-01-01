import streamlit as st
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from dotenv import load_dotenv
import openpyxl
import xlrd
import xlsxwriter
import xlwt
import xlutils


load_dotenv()

if 'df' not in st.session_state:
    st.session_state.df = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'messages' not in st.session_state:
    st.session_state.messages = []



st.set_page_config(page_title="Excel/CSV/Text Analytics Agent", layout="wide")
st.title("Excel / CSV / Text Analytics Agent")


uploaded_file = st.sidebar.file_uploader("Please Upload a CSV/Excel/Text file", type=["csv", "xlsx", "xls", "txt"])

#### Create DataFrame
if uploaded_file is not None:
    if uploaded_file.type == "text/csv":
        st.session_state.df = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        st.session_state.df = pd.read_excel(uploaded_file)
    st.write("Preview of Dataset")
    st.dataframe(st.session_state.df.head(5))
    
    #### Create Agent
    if st.session_state.df is not None and not st.session_state.df.empty:
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        st.session_state.agent = create_pandas_dataframe_agent(
            llm,
            st.session_state.df,
            verbose=True,
            agent_type="tool-calling",
            allow_dangerous_code=True,
        handle_parsing_errors=True
        )


#### Chat with Agent
if 'agent' in st.session_state and st.session_state.agent is not None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt = st.chat_input("Please ask your question to the agent")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking.."):
                response = st.session_state.agent.run(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
    elif not prompt:
        st.warning("Please enter a question.")
    else:
        st.warning("Please upload a CSV/Excel/Text file first.")
