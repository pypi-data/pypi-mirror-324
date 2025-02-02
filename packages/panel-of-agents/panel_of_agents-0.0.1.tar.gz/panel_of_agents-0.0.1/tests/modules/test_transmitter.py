from collections import OrderedDict

import pytest
import pytest_asyncio
from pytest_mock import MockFixture
from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, AIMessage

from src.panel_of_agents.context import Context
from src.panel_of_agents.transmitter import Transmitter
from src.panel_of_agents.types.flag import FlagState
from src.panel_of_agents.types.context import ActionPlan
from src.panel_of_agents.moderator import Moderator
from tests.modules.test_agent import NoCapabilityAgent, get_tokens


@pytest.fixture
def sample_context() -> Context:
    return Context(
        current_question="What is the capital of France?",
        conversation_history=[HumanMessage(content="Hello, how are you?"), AIMessage(
            content="I'm fine, thank you!")],
        artifacts=OrderedDict(),
        target_agent="moderator"
    )


@pytest.fixture
def basic_moderator():
    agent = NoCapabilityAgent(
        "Test Agent",
        "Personal Bio",
        "Public Bio",
        ChatOpenAI(model="gpt-4o-mini")
    )
    return Moderator([agent], "Test Agent")


@pytest.fixture
def transmitter(basic_moderator):
    return Transmitter(moderator=basic_moderator)


class TestTransmitterAccumulate:

    def test_accumulate_thinking_out_loud_flag_open(self, sample_context: Context, transmitter):
        # Act
        result = transmitter.accumulate("🚨", sample_context)

        # Assert
        assert transmitter._thinking_out_loud.is_open()

    def test_accumulate_thinking_out_loud_when_flag_open(self, sample_context: Context, transmitter):
        # Arrange
        _ = transmitter.accumulate("🚨", sample_context)

        # Act
        result = transmitter.accumulate("token", sample_context)

        # Assert
        assert result == "token"
        assert transmitter._thinking_out_loud.is_open()
        assert sample_context.thinking_out_loud == "token"

    def test_accumulate_thinking_out_loud_when_flag_open_stream(self, sample_context: Context, transmitter):
        # Arrange
        _ = transmitter.accumulate("🚨", sample_context)

        # Act
        token_stream = "This is a stream of tokens"
        for token in token_stream.split():
            token = token + " "
            result = transmitter.accumulate(token, sample_context)
            assert result == token
            assert transmitter._thinking_out_loud.is_open()

        assert sample_context.thinking_out_loud.strip() == token_stream

    def test_accumulate_thinking_out_loud_when_flag_closed(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("🚨", sample_context)

        # Act
        result = transmitter.accumulate("🚨", sample_context)

        # Assert
        assert transmitter._thinking_out_loud.is_open() == False

    def test_accumulate_internal_reasoning_flag_open(self, sample_context: Context, transmitter):
        # Arrange

        # Act
        result = transmitter.accumulate("🤖", sample_context)

        # Assert
        assert result == ""
        assert transmitter._internal_reasoning.is_open()

    def test_accumulate_internal_reasoning_when_flag_open(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("🤖", sample_context)

        # Act
        result = transmitter.accumulate("token", sample_context)

        # Assert
        assert result == ""
        assert transmitter._internal_reasoning.is_open()
        assert sample_context.internal_reasoning == "token"

    def test_accumulate_internal_reasoning_when_flag_open_stream(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("🤖", sample_context)

        # Act
        token_stream = "Since we need historical weather data for a specific date, I'll use the get_weather function."
        for token in token_stream.split():
            token = token + " "
            result = transmitter.accumulate(token, sample_context)
            assert transmitter._internal_reasoning.is_open()

        assert sample_context.internal_reasoning.strip() == token_stream

    def test_accumulate_current_action_plan_flag_open(self, sample_context: Context, transmitter):
        # Arrange

        # Act
        result = transmitter.accumulate("🛠️", sample_context)

        # Assert
        assert result == ""
        assert transmitter._current_action_plan.is_open()

    def test_accumulate_current_action_plan_when_flag_open(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("🛠️", sample_context)

        # Act
        result = transmitter.accumulate("{", sample_context)

        # Assert
        assert result == ""
        assert transmitter._current_action_plan.is_open()
        assert sample_context.current_action_plan == "{"

    def test_accumulate_current_action_plan_when_flag_open_stream(self, sample_context: Context, transmitter):

        # Act
        action_plan = """
        🛠 {"tool_name": "get_weather", "tool_input": {"date": "2024-12-25"}} 🛠
        """
        for token in action_plan.split():
            result = transmitter.accumulate(token, sample_context)

        # Verify the accumulated action plan is valid
        action_plan_obj = sample_context.get_json_action_plan()
        assert action_plan_obj.tool_name == "get_weather"
        assert action_plan_obj.tool_input == {"date": "2024-12-25"}

    def test_accumulate_final_output_flag_open(self, sample_context: Context, transmitter):
        # Arrange

        # Act
        result = transmitter.accumulate("📢", sample_context)

        # Assert
        assert transmitter._final_output.is_open()

    def test_accumulate_final_output_when_flag_open(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("📢", sample_context)

        # Act
        result = transmitter.accumulate("token", sample_context)

        # Assert
        assert result == "token"
        assert transmitter._final_output.is_open()
        assert sample_context.final_output == "token"

    def test_accumulate_final_output_when_flag_open_stream(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("📢", sample_context)

        # Act
        token_stream = "Yes, there was light rainfall on December 25th, 2024."
        for token in token_stream.split():
            token = token + " "
            result = transmitter.accumulate(token, sample_context)
            assert result == token
            assert transmitter._final_output.is_open()

        assert sample_context.final_output.strip() == token_stream

    def test_accumulate_internal_reasoning_when_flag_closed(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("🤖", sample_context)

        # Act
        result = transmitter.accumulate("🤖", sample_context)

        # Assert
        assert transmitter._internal_reasoning.is_open() == False

    def test_accumulate_current_action_plan_when_flag_closed(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("🛠️", sample_context)

        # Act
        result = transmitter.accumulate("🛠️", sample_context)

        # Assert
        assert transmitter._current_action_plan.is_open() == False

    def test_accumulate_final_output_when_flag_closed(self, sample_context: Context, transmitter):
        # Arrange

        _ = transmitter.accumulate("📢", sample_context)

        # Act
        result = transmitter.accumulate("📢", sample_context)

        # Assert
        assert transmitter._final_output.is_open() == False

    def test_special_token_closes_other_flags(self, sample_context: Context, transmitter):
        # Open thinking out loud flag
        _ = transmitter.accumulate("🚨", sample_context)
        assert transmitter._thinking_out_loud.is_open()

        # When opening internal reasoning, thinking out loud should close
        _ = transmitter.accumulate("🤖", sample_context)
        assert not transmitter._thinking_out_loud.is_open()
        assert transmitter._internal_reasoning.is_open()

        # When opening action plan, internal reasoning should close
        _ = transmitter.accumulate("🛠️", sample_context)
        assert not transmitter._internal_reasoning.is_open()
        assert transmitter._current_action_plan.is_open()

        # When opening final output, action plan should close
        _ = transmitter.accumulate("📢", sample_context)
        assert not transmitter._current_action_plan.is_open()
        assert transmitter._final_output.is_open()

    def test_clear_state_on_new_invocation(self, sample_context: Context, transmitter):
        # Arrange - Set some initial state
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        transmitter.accumulate("Some thinking", sample_context)
        transmitter.raw_feed = "Some raw feed content"
        assert transmitter._thinking_out_loud.is_open()
        assert transmitter.raw_feed != ""


class TestTransmitterAccumulateComplex:
    def test_opening_thinking_flag_text_after(self, sample_context: Context, transmitter):
        token = "🚨 Some text after"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert transmitter._thinking_out_loud.is_open()
        assert sample_context.thinking_out_loud == "Some text after"

    def test_closing_thinking_flag_text_before(self, sample_context: Context, transmitter):
        # Arrange
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        token = "Some text before 🚨"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert sample_context.thinking_out_loud == "Some text before "

    def test_opening_thinking_flag_text_in_between(self, sample_context: Context, transmitter):
        token = "🚨 Some text in between 🚨"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert sample_context.thinking_out_loud == "Some text in between "

    def test_closing_alert_flag_closing_processing_flag_open(self, sample_context: Context, transmitter):
        # Arrange
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        token = "🚨 🤖"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert transmitter._internal_reasoning.is_open()

    def test_text_before_closing_alert_flag_internal_reasoning_flag_opens(self, sample_context: Context, transmitter):
        # Arrange
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        token = "Starting process 🚨 🤖"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert transmitter._internal_reasoning.is_open()
        assert "Starting process" in sample_context.thinking_out_loud

    def test_closing_alert_flag_internal_reasoning_flag_opens_text_after(self, sample_context: Context, transmitter):
        # Arrange
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        token = "🚨 🤖 Some text after"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert transmitter._internal_reasoning.is_open()
        assert "Some text after" in sample_context.internal_reasoning

    def test_text_before_closing_alert_flag_internal_reasoning_flag_opens_text_after(self, sample_context: Context, transmitter):
        # Arrange
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        token = "Starting process 🚨 🤖 Some text after"

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert transmitter._internal_reasoning.is_open()
        assert "Starting process" in sample_context.thinking_out_loud
        assert "Some text after" in sample_context.internal_reasoning

    def test_closing_alert_flag_tool_call_opening_text_after(self, sample_context: Context, transmitter):
        # Arrange
        transmitter.accumulate("🚨", sample_context)  # Open thinking
        token = """ 🚨

🛠 {"
"""

        # Act
        result = transmitter.accumulate(token, sample_context)

        # Assert
        assert not transmitter._thinking_out_loud.is_open()
        assert transmitter._current_action_plan.is_open()
        assert "{" in sample_context.current_action_plan


class TestTransmitterStreaming:
    @pytest.fixture
    def mock_moderator_thinking_reasoning_action(self, mocker: MockFixture):
        responses = """🚨 Let me check that for you 🚨
        🤖 I'll need to use the weather API to get this information 🤖
        🛠️ {
            "tool_name": "get_weather",
            "tool_input": {
                "date": "2024-12-25"
            }
        } 🛠️"""

        def mock_execute(context):
            # Split while preserving spaces
            tokens = []
            current_token = ""
            for char in responses:
                if char.isspace():
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    tokens.append(char)
                else:
                    current_token += char
            if current_token:
                tokens.append(current_token)

            for token in tokens:
                yield token

        mocker.patch(
            "src.panel_of_agents.moderator.Moderator.execute",
            side_effect=mock_execute
        )

        return responses

    @pytest.fixture
    def mock_moderator_reasoning_final(self, mocker: MockFixture):
        responses = """🤖 Based on the weather data I retrieved, I can provide an answer 🤖
        📢 Yes, it was raining on December 25th, 2024 with 2.3mm of precipitation. 📢"""

        def mock_execute(context):
            # Split while preserving spaces
            tokens = []
            current_token = ""
            for char in responses:
                if char.isspace():
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    tokens.append(char)
                else:
                    current_token += char
            if current_token:
                tokens.append(current_token)

            for token in tokens:
                yield token

        mocker.patch(
            "src.panel_of_agents.moderator.Moderator.execute",
            side_effect=mock_execute
        )

        return responses

    def test_stream_thinking_reasoning_action(self, mock_moderator_thinking_reasoning_action):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        moderator = Moderator([agent], "Test Agent")
        transmitter = Transmitter(moderator)
        context = Context("What's the weather?", [], {})

        # Act
        accumulated_action = ""
        for token in transmitter.invoke_moderator(context, stream=True):
            if token and context.current_action_plan is not None:
                accumulated_action += token

        # Assert
        assert context.thinking_out_loud.strip() == "Let me check that for you"
        assert "I'll need to use the weather API" in context.internal_reasoning
        assert '"tool_name": "get_weather"' in context.current_action_plan
        assert '"date": "2024-12-25"' in context.current_action_plan
        assert context.conversation_turn_finished == False
        assert context.get_json_action_plan() is not None

    def test_stream_reasoning_final_output(self, mock_moderator_reasoning_final):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        moderator = Moderator([agent], "Test Agent")
        transmitter = Transmitter(moderator)
        context = Context("What's the weather?", [], {})

        # Act & Assert with streaming
        accumulated_output = ""
        for token in transmitter.invoke_moderator(context, stream=True):
            if token and context.final_output is not None:
                accumulated_output += token

        assert "Based on the weather data" in context.internal_reasoning
        assert "2.3mm of precipitation" in accumulated_output

    def test_no_stream_final_output(self, mock_moderator_reasoning_final):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        moderator = Moderator([agent], "Test Agent")
        transmitter = Transmitter(moderator)
        context = Context("What's the weather?", [], {})

        # Act
        final_output = next(
            transmitter.invoke_moderator(context, stream=False))

        # Assert
        assert "2.3mm of precipitation" in final_output
        assert context.conversation_turn_finished == True


class TestTransmitterAsyncStreaming:
    @pytest.fixture
    def mock_moderator_thinking_reasoning_action(self, mocker: MockFixture):
        responses = """🚨 Let me check that for you 🚨
        🤖 I'll need to use the weather API to get this information 🤖
        🛠️ {
            "tool_name": "get_weather",
            "tool_input": {
                "date": "2024-12-25"
            }
        } 🛠️"""

        async def mock_execute(context):
            # Split while preserving spaces
            tokens = []
            current_token = ""
            for char in responses:
                if char.isspace():
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    tokens.append(char)
                else:
                    current_token += char
            if current_token:
                tokens.append(current_token)

            for token in tokens:
                yield token

        mocker.patch(
            "src.panel_of_agents.moderator.Moderator.aexecute",
            side_effect=mock_execute
        )

        return responses

    @pytest.fixture
    def mock_moderator_reasoning_final(self, mocker: MockFixture):
        responses = """🤖 Based on the weather data I retrieved, I can provide an answer 🤖
        📢 Yes, it was raining on December 25th, 2024 with 2.3mm of precipitation. 📢"""

        async def mock_execute(context):
            # Split while preserving spaces
            tokens = []
            current_token = ""
            for char in responses:
                if char.isspace():
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    tokens.append(char)
                else:
                    current_token += char
            if current_token:
                tokens.append(current_token)

            for token in tokens:
                yield token

        mocker.patch(
            "src.panel_of_agents.moderator.Moderator.aexecute",
            side_effect=mock_execute
        )

        return responses

    @pytest.mark.asyncio
    async def test_stream_thinking_reasoning_action(self, mock_moderator_thinking_reasoning_action):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        moderator = Moderator([agent], "Test Agent")
        transmitter = Transmitter(moderator)
        context = Context("What's the weather?", [], {})

        # Act
        accumulated_action = ""
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            if token and context.current_action_plan is not None:
                accumulated_action += token

        # Assert
        assert context.thinking_out_loud.strip() == "Let me check that for you"
        assert "I'll need to use the weather API" in context.internal_reasoning
        assert '"tool_name": "get_weather"' in context.current_action_plan
        assert '"date": "2024-12-25"' in context.current_action_plan
        assert context.conversation_turn_finished == False
        assert context.get_json_action_plan() is not None

    @pytest.mark.asyncio
    async def test_stream_reasoning_final_output(self, mock_moderator_reasoning_final):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        moderator = Moderator([agent], "Test Agent")
        transmitter = Transmitter(moderator)
        context = Context("What's the weather?", [], {})

        # Act & Assert with streaming
        accumulated_output = ""
        async for token in transmitter.ainvoke_moderator(context, stream=True):
            if token and context.final_output is not None:
                accumulated_output += token

        assert "Based on the weather data" in context.internal_reasoning
        assert "2.3mm of precipitation" in accumulated_output

    @pytest.mark.asyncio
    async def test_no_stream_final_output(self, mock_moderator_reasoning_final):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        moderator = Moderator([agent], "Test Agent")
        transmitter = Transmitter(moderator)
        context = Context("What's the weather?", [], {})

        # Act
        final_output = None
        async for output in transmitter.ainvoke_moderator(context, stream=False):
            final_output = output

        # Assert
        assert "2.3mm of precipitation" in final_output
        assert context.conversation_turn_finished == True
