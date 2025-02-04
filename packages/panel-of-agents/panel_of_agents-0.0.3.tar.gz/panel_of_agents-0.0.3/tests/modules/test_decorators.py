import pytest
from src.panel_of_agents.decorators import agent_capability, panel_capability, creates_artifact
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.types.context import Artifact


@agent_capability
def agent_capability_only() -> CapabilityResult:
    return CapabilityResult(result="Hello, World!", artifact=None)


@panel_capability
def panel_capability_only():
    return "Hello, World!"


@panel_capability
@agent_capability
def agent_capability_and_panel_capability() -> CapabilityResult:
    return CapabilityResult(result="Hello, World!", artifact=None)


@agent_capability
@creates_artifact(description="This is a toy artifact")
def agent_capability_creates_artifact() -> CapabilityResult:
    """
    This is a test function.
    """
    return CapabilityResult(
        result="Hello, World!",
        artifact=Artifact(author="test", data={"message": "Hello, World!"})
    )


def test_agent_capability():
    assert hasattr(agent_capability_only, "is_agent_capability")
    assert agent_capability_only.is_agent_capability is True
    result = agent_capability_only()
    assert isinstance(result, CapabilityResult)
    assert result.result == "Hello, World!"
    assert result.artifact is None


def test_panel_capability():
    assert hasattr(panel_capability_only, "is_panel_capability")
    assert panel_capability_only.is_panel_capability is True


def test_agent_and_panel_capability():
    assert hasattr(agent_capability_and_panel_capability,
                   "is_agent_capability")
    assert agent_capability_and_panel_capability.is_agent_capability is True
    assert hasattr(agent_capability_and_panel_capability,
                   "is_panel_capability")
    assert agent_capability_and_panel_capability.is_panel_capability is True
    result = agent_capability_and_panel_capability()
    assert isinstance(result, CapabilityResult)


def test_creates_artifact():
    assert "This function creates an artifact. Artifact Description: This is a toy artifact" in agent_capability_creates_artifact.__doc__
    result = agent_capability_creates_artifact()
    assert isinstance(result, CapabilityResult)
    assert isinstance(result.artifact, Artifact)
    assert result.artifact.author == "test"
    assert result.artifact.data == {"message": "Hello, World!"}


def test_agent_capability_wrong_return_type():
    with pytest.raises(TypeError):
        @agent_capability
        def wrong_return() -> str:
            return "This should fail"


def test_agent_capability_wrong_return_value():
    @agent_capability
    def wrong_value() -> CapabilityResult:
        return "This should fail"  # Not returning CapabilityResult

    with pytest.raises(TypeError):
        wrong_value()
