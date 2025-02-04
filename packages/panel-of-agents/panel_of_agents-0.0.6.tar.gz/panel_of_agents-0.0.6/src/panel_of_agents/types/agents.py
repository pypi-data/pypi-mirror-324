from typing import Any, Optional
from pydantic import BaseModel, Field
from .context import Artifact


class AgentVote(BaseModel):
    """A vote on whether the agent is capable of handling the current question"""

    reason: str = Field(description="The reason for the vote")
    vote: int = Field(description="# MUST be one of: 100, 50, 20, 10, 0")


class ModeratorAgentVote(BaseModel):
    """A vote on whether the agent is capable of handling the current question"""

    reason: str = Field(description="The reason for the vote")
    name: str = Field(description="The name of the agent")
    vote: int = Field(description="# MUST be one of: 100, 50, 20, 10, 0")


class ModeratorVote(BaseModel):
    """Votes for all agents in the panel"""

    votes: list[ModeratorAgentVote]


class FunctionParams(BaseModel):
    type: str = Field("object")
    properties: dict
    required: list


class FunctionDesc(BaseModel):
    name: str
    description: str
    parameters: FunctionParams


class Capability(BaseModel):
    type: str = Field("function")
    function: FunctionDesc


class CapabilityResult(BaseModel):
    result: Any
    artifact: Optional[Artifact] = None
