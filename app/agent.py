from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import ToolMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_mongodb.agent_toolkit import (
    MONGODB_AGENT_SYSTEM_PROMPT,
)

from langgraph.graph.message import add_messages

from app.tools import llm, tools, tool_map


# ============================================================
# GRAPH STATE
# ============================================================

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]


# ============================================================
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            MONGODB_AGENT_SYSTEM_PROMPT,
        ),

        (
            "system",
            """
            IMPORTANT:

            Always start by checking your memory for relevant
            information before calling any tools.

            Do not re-run tools unless absolutely necessary.

            If you are not able to get enough information using
            the tools, reply with I DON'T KNOW.

            Always wrap _id in quotes when generating queries.

            You have access to the following tools:
            {tool_names}
            """,
        ),

        MessagesPlaceholder(
            variable_name="messages",
        ),
    ]
)


# Fill prompt variables
prompt = prompt.partial(
    top_k=5,
    tool_names=", ".join(
        tool.name for tool in tools
    ),
)


# ============================================================
# LLM WITH TOOLS
# ============================================================

tool_augmented_llm = llm.bind_tools(tools)

llm_with_tools = prompt | tool_augmented_llm


# ============================================================
# AGENT NODE
# ============================================================

def agent_node(state: GraphState):

    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ============================================================
# TOOL NODE
# ============================================================

def tool_node(state: GraphState):

    results = []

    # Get tool calls from latest AI message
    tool_calls = state["messages"][-1].tool_calls

    for tool_call in tool_calls:

        tool_name = tool_call["name"]

        tool = tool_map[tool_name]

        # Execute tool
        observation = tool.invoke(
            tool_call["args"]
        )

        # Store tool response
        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id=tool_call["id"],
            )
        )

    return {
        "messages": results
    }