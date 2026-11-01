from langchain_openai import ChatOpenAI
from langchain_mongodb.agent_toolkit.toolkit import (
    MongoDBDatabaseToolkit,
)

from app.database import db
from app.config import MODEL_NAME


# Initialize LLM
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
)


# Create MongoDB toolkit
toolkit = MongoDBDatabaseToolkit(
    db=db,
    llm=llm,
)


# Get MongoDB tools
tools = toolkit.get_tools()


# Map tool names → tool objects
tool_map = {
    tool.name: tool
    for tool in tools
}