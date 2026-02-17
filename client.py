import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework_ag_ui import AGUIChatClient

load_dotenv()

async def interactive_chat():

    base_url = os.getenv("AGUI_SERVER_URL", "http://localhost:8000/chat")
    print(f"Connecting to: {base_url}\n")

    client = AGUIChatClient(endpoint=base_url)
    agent = Agent(client=client)

    thread = agent.get_new_thread()

    print("Chat started! Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")

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
