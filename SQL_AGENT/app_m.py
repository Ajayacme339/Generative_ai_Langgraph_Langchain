import os
import streamlit as st
from dotenv import load_dotenv
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------
# Load API keys
# -------------------------
load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# -------------------------
# LLM
# -------------------------
from langchain_openai import ChatOpenAI
import httpx

# Use API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ OPENAI_API_KEY not found in .env file. Please add it.")
    st.stop()


http_client = httpx.Client(verify=False)

model = ChatOpenAI(
    model="gpt-4o-mini", 
    api_key=api_key, 
    temperature=0,
    http_client=http_client
)

# -------------------------
# Database Setup
# -------------------------
from langchain_community.utilities import SQLDatabase

# Connect to Chinook database
db = SQLDatabase.from_uri(
    "sqlite:///Chinook_Sqlite.sqlite",
    sample_rows_in_table_info=3
)

# -------------------------
# Create SQL Agent
# -------------------------
from langchain_community.agent_toolkits import create_sql_agent

agent = create_sql_agent(
    llm=model,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    max_iterations=15,
    max_execution_time=60,
    early_stopping_method="generate"
)

# -------------------------
# Streamlit UI
# -------------------------
st.title("💬 SQL AI Agent — Ask Your Database")

user_question = st.text_input(
    "Ask a business question:",
    placeholder="e.g., Which genre on average has the longest tracks?"
)

if st.button("Run Query"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        st.subheader("🔄 Agent Response")
        with st.spinner("Processing your query..."):
            try:
                response = agent.invoke({"input": user_question})
                st.success("Query completed!")
                st.markdown("**Answer:**")
                st.write(response["output"])
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

