from langgraph.graph import (
    START,
    END,
    StateGraph,
)

from langgraph.prebuilt import tools_condition

from langgraph.checkpoint.mongodb import MongoDBSaver

from app.database import mongodb_client
from app.agent import (
    GraphState,
    agent_node,
    tool_node,
)


# ============================================================
# CREATE GRAPH
# ============================================================

graph = StateGraph(GraphState)


# Add nodes
graph.add_node(
    "agent",
    agent_node,
)

graph.add_node(
    "tools",
    tool_node,
)


# ============================================================
# EDGES
# ============================================================

# START → Agent
graph.add_edge(
    START,
    "agent",
)


# Tools → Agent
graph.add_edge(
    "tools",
    "agent",
)


# Agent → Tools OR END
graph.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)


# ============================================================
# MONGODB CHECKPOINTER
# ============================================================

checkpointer = MongoDBSaver(
    mongodb_client,
)


# ============================================================
# COMPILE
# ============================================================

app = graph.compile(
    checkpointer=checkpointer,
)