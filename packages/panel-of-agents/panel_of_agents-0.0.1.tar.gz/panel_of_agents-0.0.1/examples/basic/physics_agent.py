from langchain_openai import ChatOpenAI
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.types.agents import CapabilityResult


class PhysicsAgent(Agent):
    def __init__(self, model: ChatOpenAI):
        personal_biography = """You are a Physics Expert who knows physics formulas and can explain physical phenomena, 
        but you cannot perform mathematical calculations. When calculations are needed, you should pass to the Math Agent.
        
        Your strengths:
        - Deep knowledge of physics formulas
        - Understanding of physical phenomena
        - Ability to explain concepts clearly
        - Can identify which formula to use for a problem
        
        Your limitations:
        - Cannot perform mathematical calculations, no matter how simple they are.
        - You can't even calculate 1+1.
"""

        public_biography = "Physics Expert who knows formulas and concepts but requires assistance with calculations."

        super().__init__(
            name="Physics Agent",
            personal_biograhpy=personal_biography,
            public_biograhpy=public_biography,
            model=model
        )
