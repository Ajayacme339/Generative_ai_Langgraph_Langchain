import os
import streamlit as st
from dotenv import load_dotenv

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
model = ChatOpenAI(model="gpt-4.1")

# -------------------------
# Database Setup
# -------------------------
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

# Make sure Chinook.db exists
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query.
Always LIMIT results to at most 5 unless user asks otherwise.
Double check your query.
Do NOT run modification queries.
"""

# -------------------------
# Create SQL Agent
# -------------------------
from langchain.agents import create_agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
)

# -------------------------
# Streamlit UI
# -------------------------
st.title("💬 SQL Agent — Ask Your Database")

user_question = st.text_input(
    "Ask a question about the Chinook database:",
    placeholder="e.g., Which genre on average has the longest tracks?"
)

if st.button("Run Query"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        st.subheader("🔄 Agent Response (Streaming)")
        response_area = st.empty()   # Placeholder for streaming text
        streamed_text = ""

        # Stream agent's response as tokens
        for step in agent.stream(
            {"messages": [{"role": "user", "content": user_question}]},
            stream_mode="values",
        ):
            msg = step["messages"][-1]
            streamed_text += msg.content + "\n"
            response_area.markdown(f"```\n{streamed_text}\n```")

