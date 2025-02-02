import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from src.panel_of_agents.moderator import Moderator
from src.panel_of_agents.transmitter import Transmitter
from src.panel_of_agents.context import Context
from examples.math_agents.addition_agent import AdditionAgent
from examples.math_agents.subtraction_agent import SubtractionAgent
from examples.math_agents.multiplication_agent import MultiplicationAgent
from examples.math_agents.division_agent import DivisionAgent
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# Initialize the model
# model = ChatOpenAI(
#     model="gpt-4o-mini",
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
max_tries = 10
addition_agent = AdditionAgent(model, max_tries)
subtraction_agent = SubtractionAgent(model, max_tries)
multiplication_agent = MultiplicationAgent(model, max_tries)
division_agent = DivisionAgent(model, max_tries)

# Create the panel with Addition Agent as leader
moderator = Moderator(
    panel_of_agents=[addition_agent, subtraction_agent,
                     multiplication_agent, division_agent],
    leader="Addition Agent",
    moderator_cast_vote=True
)

# Create the transmitter
transmitter = Transmitter(moderator)


def main():
    conversation_history = []
    print("Welcome to the Math Panel of Agents! (Type 'quit' to exit)")

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
