from typing import Union, Dict, Mapping, Any
from enum import Enum
from dataclasses import dataclass


class ArtifactType(Enum):
    INTERNAL = "internal"
    USER = "user"


@dataclass
class Artifact:
    """
    Artifact class to store information about the artifact.
    An artifact is a result of an tool that is required to be persisted across multiple conversation turns.
    """

    author: str
    data: Dict[str, Any]
    artifact_type: ArtifactType = ArtifactType.INTERNAL


@dataclass
class ActionPlan:
    tool_name: str
    tool_input: Dict[str, Any]


@dataclass
class Action:
    author: str
    action_name: str
    action_input: Dict[str, Any]
    action_output: Dict[str, Any]


@dataclass
class CustomProp:
    name: str
    description: str
    value: Any


class Index:

    def __init__(self, index_type: str, index_id: int):
        self.index_type = index_type
        self.index_id = index_id

    def __str__(self):
        return f"{self.index_type}-run-{self.index_id}"

    def __repr__(self):
        return f"{self.index_type}-run-{self.index_id}"


class ConversationTurnIndex(Index):

    def __init__(self, index_id: int):
        super().__init__("conversation", index_id)


class DecisionRunIndex(Index):

    def __init__(self, index_id: int):
        super().__init__("decision", index_id)
