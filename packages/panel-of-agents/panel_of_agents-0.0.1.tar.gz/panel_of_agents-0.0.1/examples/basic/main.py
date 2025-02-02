import os
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from src.panel_of_agents.moderator import Moderator
from src.panel_of_agents.transmitter import Transmitter
from src.panel_of_agents.context import Context
from examples.basic.physics_agent import PhysicsAgent
from examples.basic.math_agent import MathAgent
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# Initialize the model
# model = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0.5,
#     api_key=os.getenv("OPENAI_API_KEY")
# )
model = ChatAnthropic(
    model="claude-3-5-haiku-latest",
    temperature=0.5,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
# model = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     temperature=0.5,
#     api_key=os.getenv("GOOGLE_GENERATIVE_API_KEY")
# )
# Create the agents
physics_agent = PhysicsAgent(model)

math_agent = MathAgent(model)

# Create the panel with Physics Agent as leader
moderator = Moderator(
    panel_of_agents=[physics_agent, math_agent],
    leader="Physics Agent"
)

# Create the transmitter
transmitter = Transmitter(moderator)

# Comment out Gradio-specific code
# def process_question(message, history):
#     # Convert chat history to LangChain message format
#     formatted_history = []
#     for entry in history:
#         if entry["role"] == "user":
#             formatted_history.append(HumanMessage(content=entry["content"]))
#         elif entry["role"] == "assistant":
#             formatted_history.append(AIMessage(content=entry["content"]))
#
#     # Create new context for each interaction
#     context = Context(
#         current_question=message,
#         conversation_history=formatted_history,
#         artifacts={}
#     )
#
#     full_response = ""
#     for token in transmitter.invoke_moderator(context, stream=True):
#         if token:
#             full_response += token
#             yield full_response

# # Create Gradio interface
# demo = gr.ChatInterface(
#     fn=process_question,
#     type="messages",
#     title="Physics and Math Panel of Agents",
# )

# Add new terminal-based chat loop


def main():
    conversation_history = []
    print("Welcome to the Physics and Math Panel of Agents! (Type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break

        context = Context(
            current_question=user_input,
            conversation_history=conversation_history,
            artifacts={}
        )

        print("\nAssistant: ", end="", flush=True)
        full_response = ""
        for token in transmitter.invoke_moderator(context, stream=True):
            if token:
                print(token, end="", flush=True)
                full_response += token

        conversation_history.append(HumanMessage(content=user_input))
        conversation_history.append(AIMessage(content=transmitter.raw_feed))
        print()  # New line after response


if __name__ == "__main__":
    main()
