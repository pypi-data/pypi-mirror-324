from langchain_core.language_models import BaseChatModel
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.decorators import agent_capability


class AdditionAgent(Agent):
    def __init__(self, model: BaseChatModel, max_tries: int = 3):
        personal_biography = "You are an agent that performs addition on two numbers."
        public_biography = "Addition Agent"

        super().__init__(
            name="Addition Agent",
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model,
            max_tries=max_tries
        )

    @agent_capability
    def add(self, a: float, b: float) -> CapabilityResult:
        result = a + b
        return CapabilityResult(result=result, artifact=None)
