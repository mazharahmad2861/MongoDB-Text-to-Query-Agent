import uuid

from app.graph import app


# ============================================================
# EXECUTE AGENT
# ============================================================

def execute_agent(
    thread_id: str,
    user_input: str,
):

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    print("\n" + "=" * 60)
    print(f"USER: {user_input}")
    print("=" * 60)

    final_response = None

    for step in app.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        },
        config,
        stream_mode="values",
    ):

        message = step["messages"][-1]

        final_response = message

        # Print only AI responses
        if message.type == "ai":
            message.pretty_print()

    return final_response


# ============================================================
# MAIN
# ============================================================

def main():

    # Create a new conversation
    thread_id = str(uuid.uuid4())

    print("\nMongoDB Text-to-Query Agent")
    print(f"Thread ID: {thread_id}")

    # --------------------------------------------------------
    # First question
    # --------------------------------------------------------

    execute_agent(
        thread_id,
        "Which states have the most theaters?",
    )

    # --------------------------------------------------------
    # Second question
    # Same thread = same memory
    # --------------------------------------------------------

    execute_agent(
        thread_id,
        "How many theaters does California have?",
    )

    # --------------------------------------------------------
    # Third question
    # --------------------------------------------------------

    execute_agent(
        thread_id,
        "What about the state with the second most theaters?",
    ) 

    execute_agent(
            thread_id,
            "Find movies with an IMDb rating greater than 9 also mention their release year.",
        )


if __name__ == "__main__":
    main()