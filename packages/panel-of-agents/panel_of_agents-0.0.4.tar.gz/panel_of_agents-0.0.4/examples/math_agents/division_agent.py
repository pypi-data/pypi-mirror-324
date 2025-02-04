from langchain_core.language_models import BaseChatModel
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.decorators import agent_capability


class DivisionAgent(Agent):
    def __init__(self, model: BaseChatModel, max_tries: int = 3):
        personal_biography = "You are an agent that performs division on two numbers."
        public_biography = "Division Agent"

        super().__init__(
            name="Division Agent",
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model,
            max_tries=max_tries
        )

    @agent_capability
    def divide(self, a: float, b: float) -> CapabilityResult:
        if b == 0:
            return CapabilityResult(result="Error: Division by zero", artifact=None)
        result = a / b
        return CapabilityResult(result=result, artifact=None)
