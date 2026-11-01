# MongoDB Text-to-Query Agent

An **AI-powered text-to-query agent** that allows users to interact with a MongoDB database using natural language.

Instead of manually writing MongoDB queries, users can ask questions such as:

> "Which states have the most theaters?"

The agent uses an LLM to understand the question, select the appropriate MongoDB tools, generate and validate queries, execute them against the database, and return a natural-language response.

The project is built using **LangGraph, LangChain, OpenAI, MongoDB, and MongoDBSaver**.

---

## 🚀 Features

- 🗣️ **Natural-language database queries**
- 🤖 **LLM-powered agent**
- 🔧 **MongoDB tool calling**
- 🔍 **Automatic schema discovery**
- ✅ **MongoDB query validation**
- 📊 **MongoDB aggregation/query execution**
- 🔄 **LangGraph agent orchestration**
- 🧠 **Short-term conversational memory**
- 💾 **MongoDB-backed checkpointing**
- 🧵 **Thread-based conversations**
- 🔁 **Multi-turn conversations**

---

## 🏗️ Architecture

```text
┌─────────────────────┐
│       MongoDB       │
│                     │
│    sample_mflix     │
│                     │
│    Checkpoints      │
└──────────▲──────────┘
           │
     MongoDBSaver
           │
           |
         User
           │
    Natural-language question
           ▼
┌────────────────────────────────────────┐
│              LangGraph                 │
│                                        │
│   ┌──────────────────────────────┐     │
│   │          Agent / LLM         │     │
│   │                              │     │
│   │   Understand → Decide        │     │
│   └──────────────┬───────────────┘     │
│                  │                     │
│             Tool Call                  │
│                  ▼                     │
│   ┌──────────────────────────────┐     │
│   │       MongoDB Tools          │     │
│   │                              │     │
│   │  • List Collections          │     │
│   │  • Get Schema                │     │
│   │  • Check Query               │     │
│   │  • Execute Query             │     │
│   └──────────────┬───────────────┘     │
└──────────────────┼─────────────────────┘
                   │
                   ▼
                MongoDB
                   │
                   ▼
               Query Result
                   │
                   ▼
                 Agent
                   │
                   ▼
             Final Answer
```

---

## 🔄 How It Works

The agent follows this workflow:

```text
User Question
      ↓
LLM Agent
      ↓
Understand the question
      ↓
Identify relevant collection
      ↓
Inspect database schema
      ↓
Generate MongoDB query
      ↓
Validate query
      ↓
Execute query
      ↓
Retrieve results
      ↓
LLM generates final response
      ↓
User
```

For multi-turn conversations, LangGraph checkpoints the conversation state in MongoDB.

```text
Question 1
    ↓
Agent
    ↓
Checkpoint
    ↓
MongoDB
    ↓
Question 2
    ↓
Same thread_id
    ↓
Previous context restored
    ↓
Agent
    ↓
Answer
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| MongoDB Atlas | Database |
| PyMongo | MongoDB connection |
| OpenAI | LLM |
| LangChain | LLM and tool integration |
| LangGraph | Agent orchestration |
| MongoDB Toolkit | MongoDB tools for the agent |
| MongoDBSaver | Persistent short-term memory |
| Pydantic | Data validation |

---

## 🛠️ MongoDB Agent Tools

The MongoDB toolkit provides the agent with several tools.

### 1. `mongodb_list_collections`

Lists the collections available in the database.

```text
Agent → list collections → MongoDB
```

Useful when the agent needs to determine where relevant information is stored.

---

### 2. `mongodb_schema`

Retrieves information about a collection's schema and sample documents.

```text
Agent → schema → MongoDB
```

This helps the LLM understand field names and data structure.

---

### 3. `mongodb_query_checker`

Checks the generated MongoDB query before execution.

```text
Generated Query
      ↓
Query Checker
      ↓
Valid Query
```

---

### 4. `mongodb_query`

Executes the MongoDB query.

```text
MongoDB Query
      ↓
MongoDB
      ↓
Results
```

---

## 🧠 Agent Architecture

The agent can be understood using three components:

### LLM

The LLM decides what action should be taken.

### Tools

Tools allow the LLM to interact with MongoDB.

### State

State stores the messages and intermediate results during the graph execution.

---

## 🔗 LangGraph Workflow

The LangGraph workflow contains two main nodes:

```text
START
  ↓
Agent
  ↓
Tool required?
 ┌───────┴───────┐
 ↓               ↓
YES              NO
 ↓               ↓
Tools            END
 ↓
Agent
 ↓
Tool required?
 ↓
...
```

### Agent Node

The agent node sends the current conversation to the LLM.

```python
def agent_node(state):
    messages = state["messages"]

    result = llm_with_tools.invoke(messages)

    return {
        "messages": [result]
    }
```

### Tool Node

The tool node executes the tool requested by the LLM.

```python
def tool_node(state):
    tool_calls = state["messages"][-1].tool_calls

    ...
```

The result is then returned to the agent.

---

## 🧠 Short-Term Memory

The project uses:

```python
MongoDBSaver
```

to persist LangGraph checkpoints in MongoDB.

```python
checkpointer = MongoDBSaver(mongodb_client)

app = graph.compile(
    checkpointer=checkpointer
)
```

### Thread ID

Each conversation has a unique `thread_id`.

```python
thread_id = str(uuid.uuid4())
```

The same `thread_id` allows the agent to continue an existing conversation.

```text
Thread A
 ├── Question 1
 ├── Answer 1
 ├── Question 2
 └── Answer 2

Thread B
 ├── Question 1
 └── Answer 1
```

Different thread IDs maintain separate conversations.

---

## 📁 Project Structure

```text
text-to-query-agent/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
└── app/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── tools.py
    ├── agent.py
    ├── graph.py
    └── main.py
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `config.py` | Environment variables and configuration |
| `database.py` | MongoDB connection |
| `tools.py` | MongoDB toolkit and tools |
| `agent.py` | Prompt, agent node, and tool node |
| `graph.py` | LangGraph workflow and checkpointing |
| `main.py` | Run the application |
| `.env` | API keys and MongoDB URI |
| `requirements.txt` | Python dependencies |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mazharahmad2861/MongoDB-Text-to-Query-Agent

cd text-to-query-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/
OPENAI_API_KEY=your_openai_api_key
```



## ▶️ Run the Project

From the project root:

```bash
python -m app.main
```

The application creates a new conversation thread and executes multiple questions using the same thread.

Example:

```text
MongoDB Text-to-Query Agent

Thread ID: 8d4e...

USER: Which states have the most theaters?

...

USER: How many theaters does California have?

...

USER: What about the state with the second most theaters?

...
```

---

## 💬 Example Questions

You can ask questions such as:

```text
Which states have the most theaters?
```

```text
How many theaters does California have?
```

```text
What are the top 5 highest-rated movies?
```

```text
Which directors have made more than 20 movies?
```

```text
What are the most common movie genres?
```

The agent determines the appropriate MongoDB operations dynamically.

---

## 🔍 Example MongoDB Aggregation

A question such as:

```text
Give me the top 5 directors by average IMDb rating,
who have made at least 20 movies.
```

can be represented by an aggregation pipeline:

```python
[
    {"$unwind": "$directors"},

    {
        "$group": {
            "_id": "$directors",
            "filmCount": {"$sum": 1},
            "avgRating": {"$avg": "$imdb.rating"}
        }
    },

    {
        "$match": {
            "filmCount": {"$gte": 20}
        }
    },

    {
        "$sort": {
            "avgRating": -1
        }
    },

    {
        "$limit": 5
    }
]
```

The important point is that the user does **not** need to manually write this query.

---

## 🎯 Key Concepts Learned

This project covers:

- MongoDB fundamentals
- MongoDB Query API
- MongoDB aggregation pipelines
- `$match`
- `$group`
- `$sort`
- `$limit`
- `$project`
- `$unwind`
- LLM tool calling
- Prompt engineering
- Text-to-query systems
- AI agents
- LangChain
- LangGraph
- Graph state
- Agent/tool nodes
- Conditional routing
- Checkpointing
- Short-term agent memory
- Thread-based conversations
- MongoDB-backed memory

---

## 📚 Key Learnings

### Before the agent

```text
User
 ↓
Developer manually writes query
 ↓
MongoDB
 ↓
Result
```

### After the agent

```text
User
 ↓
LLM
 ↓
Tool selection
 ↓
Query generation
 ↓
Query validation
 ↓
MongoDB
 ↓
Result
 ↓
LLM
 ↓
Natural-language answer
```

### With memory

```text
User
 ↓
Agent
 ↓
MongoDB
 ↓
Checkpoint
 ↓
Same thread
 ↓
Previous conversation restored
 ↓
Agent continues conversation
```

---

## 🚀 Future Improvements

Possible extensions to this project include:

- Add a FastAPI backend
- Build a Streamlit chat interface
- Add authentication
- Add query-cost protection
- Add more MongoDB collections
- Add query-result visualization
- Add long-term memory
- Add human approval before executing queries
- Add query caching
- Add error handling and retries
- Add MongoDB Atlas Vector Search
- Add RAG capabilities
- Add evaluation and tracing
- Deploy using Docker
- Deploy on AWS
- Add CI/CD with GitHub Actions

---

## 📌 Project Takeaway

This project demonstrates how an LLM can be connected to a real database through tools and orchestrated using LangGraph.

The core architecture is:

```text
LLM
 +
Tools
 +
State
 +
LangGraph
 +
MongoDB
 +
Memory
 =
Text-to-Query Agent
```



---

