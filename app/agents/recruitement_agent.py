from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

from langchain.agents import (

    AgentExecutor,
    create_react_agent
)

from langchain import hub

from app.agents.tools import (
    autonomous_resume_evaluator_tool
)

# -----------------------------------
# Load LLM
# -----------------------------------

llm = ChatGroq(

    model_name="llama-3.1-8b-instant",

    temperature=0
)

# -----------------------------------
# Tools
# -----------------------------------

tools = [

    autonomous_resume_evaluator_tool
]

# -----------------------------------
# Prompt
# -----------------------------------

prompt = hub.pull(

    "hwchase17/react"
)

# -----------------------------------
# Create Agent
# -----------------------------------

agent = create_react_agent(

    llm,
    tools,
    prompt
)

# -----------------------------------
# Agent Executor
# -----------------------------------

recruitment_agent = AgentExecutor(

    agent=agent,

    tools=tools,

    verbose=True,

    handle_parsing_errors=True
)