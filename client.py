# These imports set up asynchronous execution, environment configuration, and the AG-UI client integration.

import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework_ag_ui import AGUIChatClient #(AG-UI activity protocol)

load_dotenv()

async def interactive_chat():
    # Backend Endpoint Configuration
    base_url = os.getenv("AGUI_SERVER_URL", "http://localhost:8000/chat")
    print(f"Connecting to: {base_url}\n")

    # AG-UI Client Initialization
    client = AGUIChatClient(endpoint=base_url)
    agent = Agent(client=client)

    thread = agent.get_new_thread() # creates conversational thread so that it can maintain context across multiple users

    print("Chat started! Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")
        #  Each update represents an activity emitted by the agent.
        # As soon as text is available, it is rendered immediately
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        try:
            print("Agent: ", end="", flush=True)

            stream = agent.run(user_message, thread=thread)

            async for update in stream:
                if update.text:
                    print(update.text, end="", flush=True)

            print("\n")

        except Exception as e:
            print("Error:", e)
            print()


def main():
    asyncio.run(interactive_chat())


if __name__ == "__main__":
    main()
