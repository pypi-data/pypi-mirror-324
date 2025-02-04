import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_together import ChatTogether
from src.panel_of_agents.moderator import Moderator
from src.panel_of_agents.transmitter import Transmitter
from src.panel_of_agents.context import Context

from examples.content_gen.code_runner import CodeRunner
from examples.content_gen.web_search import WebSearchAgent
from examples.content_gen.content_writer import ContentWriter
from examples.content_gen.file_manager import FileManager
from examples.content_gen.content_research_writer import ContentResearchWriter

# Load environment variables
load_dotenv()

# Initialize the model
better_model = ChatAnthropic(
    model="claude-3-5-sonnet-latest",
    temperature=0.5,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
# better_model = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.5,
#     api_key=os.getenv("OPENAI_API_KEY")
# )
# better_model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-exp",
#     temperature=0.5,
#     api_key=os.getenv("GOOGLE_GENERATIVE_API_KEY")
# )
# better_model = ChatTogether(
#     model="deepseek-ai/DeepSeek-V3",
#     api_key=os.getenv("TOGETHER_API_KEY"),
#     temperature=0.5
# )

# Create the agents
# code_runner = CodeRunner(better_model)
file_manager = FileManager(better_model)
content_research_writer = ContentResearchWriter(better_model)

# Create the panel with Content Research Writer as leader
moderator = Moderator(
    panel_of_agents=[content_research_writer, file_manager],
    leader="Content Research Writer",
    moderator_cast_vote=True,
    # moderator_model=better_model
)

# Create the transmitter
transmitter = Transmitter(moderator)
