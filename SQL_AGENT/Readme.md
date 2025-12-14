SQL AI Agent — README
🚀 Overview

This project implements a SQL AI Agent powered by LangChain and OpenAI that can answer business questions directly from a SQL database.

The agent automatically:
Fetches available tables & schemas
Identifies relevant tables based on the user's question
Generates syntactically correct SQL
Double-checks the SQL for errors using an LLM
Executes the query
Formats a human-friendly response
Streams the explanation and results back to the user

A Streamlit web interface is included so users can ask natural-language questions and see real-time streaming responses.

📂 Project Structure

.
├── Chinook.db                # Sample SQLite database (auto-downloaded)
├── sql_agent.py              # Core agent creation logic (LLM + tools + prompt)
├── app.py                    # Streamlit UI to interact with the agent
├── requirements.txt          # Dependencies
└── README.md                 # This file

🔧 Tech Stack
Python 3.10+
LangChain (agents, toolkits)
OpenAI GPT-4.1
Streamlit (frontend)
SQLite (Chinook database)

🧠 How the SQL Agent Works (Architecture)
1. Load environment variables
Keeps credentials secure and allows clean separation of configuration.

from dotenv import load_dotenv
load_dotenv()

2. Download & initialize the database

The Chinook database is downloaded automatically if not found locally.

import pathlib, requests
url = 
local_path = pathlib.Path("Chinook.db")
if not local_path.exists():
    local_path.write_bytes(requests.get(url).content)

3. Create the LangChain SQL Toolkit

The toolkit exposes SQL actions (inspect schema, run queries, etc.) to the agent.

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

4. System Prompt / Guardrails

Prevents unsafe queries and ensures clean, correct SQL.

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQL query.
Always LIMIT results to at most 5 unless the user asks otherwise.
Do NOT run modification queries.
"""

5. Create the Agent

Combine LLM + tools + system instructions.

from langchain.agents import create_agent
agent = create_agent(model, tools, system_prompt=system_prompt)

6. Stream Responses

The agent streams every message/token in real time.

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values"
):
    print(step["messages"][-1])

7. Streamlit UI for Natural-Language SQL Queries

Run the web interface with:

streamlit run app.py


Inside app.py:

st.title("SQL Agent — Ask Question to Your Database")

user_question = st.text_input("Ask a business question:", 
                              placeholder="e.g., Which genre has the longest tracks?")

if st.button("Run Query"):
    response_area = st.empty()
    streamed_text = ""

    for step in agent.stream(
        {"messages":[{"role": "user", "content": user_question}]},
        stream_mode="values"
    ):
        msg = step["messages"][-1]
        streamed_text += msg.content + "\n"
        response_area.markdown(f"```\n{streamed_text}\n```")

▶️ How to Run the Project
1. Install dependencies
pip install -r requirements.txt

2. Create a .env file
LANGCHAIN_API_KEY=your_key
LANGCHAIN_PROJECT=your_project
OPENAI_API_KEY=your_key
GROQ_API_KEY=...
HF_TOKEN=...

3. Start the Streamlit App
streamlit run app.py
Generate a SQL query with AVG(Milliseconds)LIMIT results

Execute & format response
Stream the output to UI
🛡 Safety & Guardrails
Agent never executes INSERT/UPDATE/DELETE/DDL
All queries are double-checked via LLM
Results auto-limited
DB interactions go through controlled LangChain toolkit methods