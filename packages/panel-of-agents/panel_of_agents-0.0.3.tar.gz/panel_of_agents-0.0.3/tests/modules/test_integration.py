from typing import Any, Generator

import pytest
from pytest_mock import MockFixture
import pytest_asyncio

from langchain_openai import ChatOpenAI

from src.panel_of_agents.transmitter import Transmitter
from src.panel_of_agents.moderator import Moderator
from src.panel_of_agents.context import Context
from src.panel_of_agents.agents import Agent
from src.panel_of_agents.types.context import Action, DecisionRunIndex, ConversationTurnIndex

from tests.modules.test_agent import MultipleCapabilityAgent, OneCapabilityAgent, get_tokens


class ResponseCycler:
    def __init__(self):
        self.current = 0
        self.responses = {
            "simple": """📢 This is a simple response without any tool calls or passes 📢""",

            "tool_and_output": [
                """🚨 Let me use my capability 🚨
                🛠️
                {
                "tool_name": "sample_capability_one",
                "tool_input": {
                "greeting": "Hello"
                }
                }
                🛠️""",
                """📢 The greeting function returned: Hello, World! 📢"""
            ],

            "pass_and_output": [
                """🚨 I should pass this to Agent Two 🚨
                🛠️
                {
                "tool_name": "pass_agent",
                "tool_input": {
                "nominee": "Agent Two",
                "reason": "They are better suited for this task",
                "agent_message": "Please handle this request"
                }
                }
                🛠️""",
                """📢 I've passed this task to Agent Two 📢"""
            ],

            "pass_tool_output": [
                """🚨 I need to pass this to Agent Two 🚨
                🛠️
                {
                "tool_name": "pass_agent",
                "tool_input": {
                "nominee": "Agent Two",
                "reason": "They have the right capability",
                "agent_message": "Please handle this request"
                }
                }
                🛠️""",
                """🚨 Let me use my capability 🚨
                🛠️
                {
                "tool_name": "sample_capability_one",
                "tool_input": {
                "greeting": "Hello"
                }
                }
                🛠️""",
                """📢 The greeting function returned: Hello, World! 📢"""
            ],

            "tool_pass_output": [
                """🚨 Let me try my capability first 🚨
                🛠️
                {
                "tool_name": "sample_capability_one",
                "tool_input": {
                "greeting": "Hello"
                }
                }
                🛠️""",
                """🚨 After that attempt, I should pass to Agent Two 🚨
                🛠️
                {
                "tool_name": "pass_agent",
                "tool_input": {
                "nominee": "Agent Two",
                "reason": "They can handle the next part better",
                "agent_message": "I tried a greeting, please continue"
                }
                }
                🛠️""",
                """📢 Task completed after passing to Agent Two 📢"""
            ]
        }

    def get_next_response(self, target: str = "simple") -> str:
        if isinstance(self.responses[target], list):
            response = self.responses[target][self.current]
            self.current = (self.current + 1) % len(self.responses[target])
        else:
            response = self.responses[target]
        return response


@pytest.fixture
def agent_decide_mock(mocker: MockFixture, request):
    cycler = ResponseCycler()
    pattern = getattr(request, 'param', 'simple')

    def mock_stream_chunks(question: str, chain: Any) -> Generator[str, None, None]:
        response = get_tokens(cycler.get_next_response(pattern))
        yield from response

    mocker.patch(
        "src.panel_of_agents.agents.Agent._stream_chunks",
        side_effect=mock_stream_chunks
    )


@pytest_asyncio.fixture
async def agent_decide_mock_async(mocker: MockFixture, request):
    cycler = ResponseCycler()
    pattern = getattr(request, 'param', 'simple')

    async def mock_stream_chunks_async(question: str, chain: Any) -> Generator[str, None, None]:
        response = get_tokens(cycler.get_next_response(pattern))
        for token in response:
            yield token

    mocker.patch(
        "src.panel_of_agents.agents.Agent._astream_chunks",
        side_effect=mock_stream_chunks_async
    )


class TestExecuteTargetAgent:

    @pytest.mark.parametrize('agent_decide_mock', ['simple'], indirect=True)
    def test_execute_single_response(self, agent_decide_mock):
        # Arrange
        agent = OneCapabilityAgent(
            "Test Agent", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent], "Test Agent")
        context = Context("test question", [], {})
        context.target_agent = "Test Agent"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        for token in transmitter.invoke_moderator(context, stream=True):
            response += token

        # Assert
        assert response == "This is a simple response without any tool calls or passes "
        assert context.conversation_turn_finished == True
        assert context.final_output == "This is a simple response without any tool calls or passes "
        assert context.decision_runs == 0

    @pytest.mark.parametrize('agent_decide_mock', ['tool_and_output'], indirect=True)
    def test_execute_tool_and_output(self, agent_decide_mock):
        # Arrange
        agent = OneCapabilityAgent(
            "Test Agent", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent], "Test Agent")
        context = Context("test question", [], {})
        context.target_agent = "Test Agent"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        for token in transmitter.invoke_moderator(context, stream=True):
            response += token

        # Assert
        assert len(context.previous_actions) == 1
        keys, values = zip(*context.previous_actions.items())
        assert keys[0].index_id == 0
        assert values[0].action_name == "sample_capability_one"
        assert values[0].action_input == {"greeting": "Hello"}
        assert values[0].action_output == {
            "result": "Hello, World!", "status": "success"}
        assert context.conversation_turn_finished == True
        assert context.thinking_out_loud == "Let me use my capability "
        assert context.final_output == "The greeting function returned: Hello, World! "
        assert context.decision_runs == 1

    @pytest.mark.parametrize('agent_decide_mock', ['pass_and_output'], indirect=True)
    def test_execute_pass_and_output(self, agent_decide_mock):
        # Arrange
        agent_one = OneCapabilityAgent(
            "Agent One", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        agent_two = OneCapabilityAgent(
            "Agent Two", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent_one, agent_two], "Agent One")
        context = Context("test question", [], {})
        context.target_agent = "Agent One"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        for token in transmitter.invoke_moderator(context, stream=True):
            response += token

        # Assert
        assert context.target_agent == "Agent Two"  # Target agent changed
        assert context.thinking_out_loud == "I should pass this to Agent Two "
        assert context.final_output == "I've passed this task to Agent Two "
        # assert context.decision_runs == 1
        assert len(context.previous_actions) == 0

    @pytest.mark.parametrize('agent_decide_mock', ['pass_tool_output'], indirect=True)
    def test_execute_pass_tool_output(self, agent_decide_mock):
        # Arrange
        agent_one = OneCapabilityAgent(
            "Agent One", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        agent_two = OneCapabilityAgent(
            "Agent Two", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent_one, agent_two], "Agent One")
        context = Context("test question", [], {})
        context.target_agent = "Agent One"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        for token in transmitter.invoke_moderator(context, stream=True):
            response += token

        # Assert
        assert context.target_agent == "Agent Two"  # Target agent changed
        assert len(context.previous_actions) == 1
        keys, values = zip(*context.previous_actions.items())
        # Second action was tool call by Agent Two
        assert values[0].action_name == "sample_capability_one"
        assert values[0].action_input == {"greeting": "Hello"}
        assert values[0].action_output == {
            "result": "Hello, World!", "status": "success"}
        assert context.final_output == "The greeting function returned: Hello, World! "

    @pytest.mark.parametrize('agent_decide_mock', ['tool_pass_output'], indirect=True)
    def test_execute_tool_pass_output(self, agent_decide_mock):
        # Arrange
        agent_one = OneCapabilityAgent(
            "Agent One", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        agent_two = OneCapabilityAgent(
            "Agent Two", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent_one, agent_two], "Agent One")
        context = Context("test question", [], {})
        context.target_agent = "Agent One"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        for token in transmitter.invoke_moderator(context, stream=True):
            response += token

        # Assert
        assert context.target_agent == "Agent Two"  # Target agent changed
        assert len(context.previous_actions) == 1
        keys, values = zip(*context.previous_actions.items())
        # First action was tool call
        assert values[0].action_name == "sample_capability_one"
        assert values[0].action_input == {"greeting": "Hello"}
        assert values[0].action_output == {
            "result": "Hello, World!", "status": "success"}
        assert context.final_output == "Task completed after passing to Agent Two "


class TestExecuteTargetAgentAsync:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('agent_decide_mock_async', ['simple'], indirect=True)
    async def test_execute_single_response_async(self, agent_decide_mock_async):
        # Arrange
        agent = OneCapabilityAgent(
            "Test Agent", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent], "Test Agent")
        context = Context("test question", [], {})
        context.target_agent = "Test Agent"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            response += token

        # Assert
        assert response == "This is a simple response without any tool calls or passes "
        assert context.conversation_turn_finished == True
        assert context.final_output == "This is a simple response without any tool calls or passes "
        assert context.decision_runs == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize('agent_decide_mock_async', ['tool_and_output'], indirect=True)
    async def test_execute_tool_and_output_async(self, agent_decide_mock_async):
        # Arrange
        agent = OneCapabilityAgent(
            "Test Agent", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent], "Test Agent")
        context = Context("test question", [], {})
        context.target_agent = "Test Agent"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            response += token

        # Assert
        assert len(context.previous_actions) == 1
        keys, values = zip(*context.previous_actions.items())
        assert keys[0].index_id == 0
        assert values[0].action_name == "sample_capability_one"
        assert values[0].action_input == {"greeting": "Hello"}
        assert values[0].action_output == {
            "result": "Hello, World!", "status": "success"}
        assert context.conversation_turn_finished == True
        assert context.thinking_out_loud == "Let me use my capability "
        assert context.final_output == "The greeting function returned: Hello, World! "
        assert context.decision_runs == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize('agent_decide_mock_async', ['pass_and_output'], indirect=True)
    async def test_execute_pass_and_output_async(self, agent_decide_mock_async):
        # Arrange
        agent_one = OneCapabilityAgent(
            "Agent One", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        agent_two = OneCapabilityAgent(
            "Agent Two", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent_one, agent_two], "Agent One")
        context = Context("test question", [], {})
        context.target_agent = "Agent One"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            response += token

        # Assert
        assert context.target_agent == "Agent Two"  # Target agent changed
        assert context.thinking_out_loud == "I should pass this to Agent Two "
        assert context.final_output == "I've passed this task to Agent Two "
        assert len(context.previous_actions) == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize('agent_decide_mock_async', ['pass_tool_output'], indirect=True)
    async def test_execute_pass_tool_output_async(self, agent_decide_mock_async):
        # Arrange
        agent_one = OneCapabilityAgent(
            "Agent One", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        agent_two = OneCapabilityAgent(
            "Agent Two", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent_one, agent_two], "Agent One")
        context = Context("test question", [], {})
        context.target_agent = "Agent One"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            response += token

        # Assert
        assert context.target_agent == "Agent Two"  # Target agent changed
        assert len(context.previous_actions) == 1
        keys, values = zip(*context.previous_actions.items())
        assert values[0].action_name == "sample_capability_one"
        assert values[0].action_input == {"greeting": "Hello"}
        assert values[0].action_output == {
            "result": "Hello, World!", "status": "success"}
        assert context.final_output == "The greeting function returned: Hello, World! "

    @pytest.mark.asyncio
    @pytest.mark.parametrize('agent_decide_mock_async', ['tool_pass_output'], indirect=True)
    async def test_execute_tool_pass_output_async(self, agent_decide_mock_async):
        # Arrange
        agent_one = OneCapabilityAgent(
            "Agent One", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        agent_two = OneCapabilityAgent(
            "Agent Two", "Personal Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        moderator = Moderator([agent_one, agent_two], "Agent One")
        context = Context("test question", [], {})
        context.target_agent = "Agent One"
        transmitter = Transmitter(moderator)
        response = ""

        # Act
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            response += token

        # Assert
        assert context.target_agent == "Agent Two"  # Target agent changed
        assert len(context.previous_actions) == 1
        keys, values = zip(*context.previous_actions.items())
        assert values[0].action_name == "sample_capability_one"
        assert values[0].action_input == {"greeting": "Hello"}
        assert values[0].action_output == {
            "result": "Hello, World!", "status": "success"}
        assert context.final_output == "Task completed after passing to Agent Two "
