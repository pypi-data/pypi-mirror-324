from langchain_openai import ChatOpenAI
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.types.agents import CapabilityResult


class MathAgent(Agent):
    def __init__(self, model: ChatOpenAI):
        personal_biography = """You are a Mathematics Expert who excels at performing calculations when given formulas 
        and values. You don't need to know the physics behind the formulas, just how to compute them accurately.
        
        Your strengths:
        - Expert at mathematical calculations
        - Can work with any formula when variables and values are provided
        - Precise numerical computation
        
        Your limitations:
        - Does not know physics formulas
        - Cannot explain even the simplest physical phenomena
        - Needs complete formula and all values to perform calculations
        - Cannot assume any values or formulas unless explicitly provided"""

        public_biography = "Mathematics Expert who can perform calculations when given formulas and values."

        super().__init__(
            name="Math Agent",
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model
        )
