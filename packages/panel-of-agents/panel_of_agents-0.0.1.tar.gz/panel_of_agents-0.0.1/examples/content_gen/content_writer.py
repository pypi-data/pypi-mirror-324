from langchain_core.language_models import BaseChatModel
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.decorators import creates_artifact, agent_capability
from src.panel_of_agents.types.agents import *
from src.panel_of_agents.types.context import *


class ContentWriter(Agent):

    def __init__(self, model: BaseChatModel, max_tries: int = 3):
        name = "Content Writer"
        personal_biography = """
        You are an agent that writes content for a variety of media.
        You are able to write content for a variety of media, including but not limited to:
        - Blog posts
        - Social media posts
        - News articles
        - Product descriptions
        - Email newsletters

        Your strengths:
        - Master of the English language.
        - Ability to write in various styles and tones.
        - Ability to write in various languages.
        - Ability to write well formatted markdown file content.

        Your limitations:
        - You are not able to write code.
        - You don't have any knowledge of the world and require provided information to write content on.
        - You can not create files, only content for the files.
        """
        public_biography = """
        An agent that writes content for a variety of media.
        An agent that is able to write content for a variety of media, including but not limited to:
        An agent that can utilize information obtained from research to write content on.
        - Blog posts
        - Social media posts
        - News articles
        - Product descriptions
        - Email newsletters

        An agent that has strengths such as:
        - Mastery of the English language.
        - Ability to write in various styles and tones.
        - Ability to write in various languages.
        - Ability to write well formatted markdown file content.

        An agent that has limitations such as:
        - Not being able to write code.
        - Lacking knowledge of the world and requiring provided information to write content on.
        """
        super().__init__(
            name=name,
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model,
            max_tries=max_tries
        )

    @agent_capability
    def create_content(self, content: str) -> CapabilityResult:
        """
        Generates content based on the provided input string.

        This method takes a string input representing the content to be created
        and returns a CapabilityResult containing the generated content.

        Parameters:
        content (str): The input string that serves as the basis for the content generation.

        Returns:
        CapabilityResult: An object containing the generated content.
        """
        return CapabilityResult(result=content)
