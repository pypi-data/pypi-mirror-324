import pytest
import pytest_asyncio
from faker import Faker
from pytest_mock import mocker, MockerFixture
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import tiktoken
from src.panel_of_agents.types.context import *
from src.panel_of_agents.context import Context

encoding = tiktoken.get_encoding("cl100k_base")


def get_num_tokens(text):
    return len(encoding.encode(text))


def get_tokens(text):

    return [encoding.decode([token]) for token in encoding.encode(text)]


class TestContext:

    def test_empty_current_question(self,):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.current_question == "Hey, I accidentally clicked enter without writing any message, please ignore."

    def test_set_empty_current_question(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.current_question = ""

        # Assert
        assert context.current_question == "Hey, I accidentally clicked enter without writing any message, please ignore."

    def test_set_current_question(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.current_question = "Hello"

        # Assert
        assert context.current_question == "Hello"

    def test_incorrect_type_current_question(self):

        # Arrange
        current_question = 0
        conversation_history = []
        artifacts = {}

        # Act
        with pytest.raises(TypeError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_incorrect_type_current_question(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        with pytest.raises(TypeError):
            context.current_question = 0

    @pytest.mark.parametrize("length", [1, 500, 1000])
    def test_inbounds_current_question(self, length):

        # Arrange
        current_question = " ".join(["word"] * length)
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.current_question == current_question

    # @pytest.mark.parametrize("length", [1001, 10000])
    # def test_out_of_bounds_current_question(self, length):

    #     # Arrange
    #     current_question = " ".join(["word"] * length)
    #     conversation_history = []
    #     artifacts = {}

    #     # Act
    #     with pytest.raises(ValueError):
    #         context = Context(current_question,
    #                           conversation_history, artifacts)

    @pytest.mark.parametrize("length", [1, 500, 1000])
    def test_inbounds_set_current_question(self, length):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.current_question = " ".join(["word"] * length)

        # Assert
        assert context.current_question == " ".join(["word"] * length)

    # @pytest.mark.parametrize("length", [1001, 10000])
    # def test_out_of_bounds_set_current_question(self, length):

    #     # Arrange
    #     current_question = ""
    #     conversation_history = []
    #     artifacts = {}

    #     # Act
    #     context = Context(current_question, conversation_history, artifacts)
    #     with pytest.raises(ValueError):
    #         context.current_question = " ".join(["word"] * length)

    def test_empty_conversation_history(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.conversation_history == []

    def test_set_conversation_history_only_one_message(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        conversation_history.append(message)

        # Act
        with pytest.raises(ValueError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_conversation_history_one_correct_pair(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = AIMessage(test_fake.sentence())
        conversation_history.append(message)
        conversation_history.append(ai_message)

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.conversation_history == conversation_history

    def test_set_conversation_history_one_incorrect_pair(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = HumanMessage(test_fake.sentence())
        conversation_history.append(ai_message)
        conversation_history.append(message)

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_conversation_history_multiple_correct_pairs(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = AIMessage(test_fake.sentence())
        conversation_history.append(message)
        conversation_history.append(ai_message)
        conversation_history.append(message)
        conversation_history.append(ai_message)

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.conversation_history == conversation_history

    def test_set_conversation_history_multiple_incorrect_pairs(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = HumanMessage(test_fake.sentence())
        conversation_history.append(ai_message)
        conversation_history.append(message)
        conversation_history.append(ai_message)
        conversation_history.append(message)

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_conversation_history_mixed_pairs(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = AIMessage(test_fake.sentence())
        conversation_history.append(message)
        conversation_history.append(ai_message)
        conversation_history.append(ai_message)
        conversation_history.append(message)

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_conversation_history_mixed_pairs_long(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = AIMessage(test_fake.sentence())
        for _ in range(30):
            conversation_history.append(message)
            conversation_history.append(ai_message)

        conversation_history.append(ai_message)
        conversation_history.append(message)

        for _ in range(4):
            conversation_history.append(message)
            conversation_history.append(ai_message)

        # Act

        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    @pytest.mark.parametrize("length", [5, 10, 25])
    def test_set_conversation_history_length_inbounds(
        self,
        test_fake: Faker,
        length,
    ):

        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = AIMessage(test_fake.sentence())
        for _ in range(length):
            conversation_history.append(message)
            conversation_history.append(ai_message)

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.conversation_history == conversation_history
        assert len(context.conversation_history) == length * 2

    @pytest.mark.parametrize("length", [26, 50])
    def test_set_conversation_history_length_out_of_bounds(
        self,
        test_fake: Faker,
        length,
    ):

        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = test_fake.sentence()
        ai_message = test_fake.sentence()
        for i in range(length):

            conversation_history.append(HumanMessage(message + " " + str(i)))
            conversation_history.append(AIMessage(ai_message + " " + str(i)))
        start_point = length - 25

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert len(context.conversation_history) == 25 * 2
        assert context.conversation_history == conversation_history[start_point * 2:]

    def test_set_conversation_history_incorrect_type_contents(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = [0]
        artifacts = {}

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_conversation_history_incorrect_type(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = "This is a conversation"
        artifacts = {}

        # Act
        with pytest.raises(TypeError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_conversation_history_odd_number_of_messages(
        self,
        test_fake: Faker,
    ):
        # Arrange
        current_question = "This is a question"
        conversation_history = []
        artifacts = {}
        message = HumanMessage(test_fake.sentence())
        ai_message = AIMessage(test_fake.sentence())
        conversation_history.append(message)
        conversation_history.append(ai_message)
        conversation_history.append(message)

        # Act
        with pytest.raises(ValueError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_empty_artifacts(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.artifacts == {}

    def test_set_artifacts_single(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(0)] = artifact

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.artifacts == artifacts

    def test_set_artifacts_when_conversation_history_empty(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(0)] = artifact

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_artifacts_multiple(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi"),
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(0)] = artifact
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(1)] = artifact

        # Act
        context = Context(current_question, conversation_history, artifacts)

        # Assert
        assert context.artifacts == artifacts

    def test_set_artifacts_length_exceeds_ai_messages(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(0)] = artifact
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(1)] = artifact

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_artifacts_index_exceeds_ai_messages(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(3)] = artifact

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_artifacts_index_matches_conversation_turns(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(1)] = artifact

        # Act
        with pytest.raises(AssertionError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_artifacts_incorrect_key_type(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[0] = artifact

        # Act
        with pytest.raises(TypeError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_artifacts_incorrect_value_type(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(0)] = 0

        # Act
        with pytest.raises(TypeError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_set_artifacts_incorrect_type(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts = "This is not a dictionary"

        # Act
        with pytest.raises(TypeError):
            context = Context(current_question,
                              conversation_history, artifacts)

    def test_update_artifacts_empty(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.update_artifacts(artifact)

        # Assert
        assert context.artifacts != {}

    def test_update_artifacts_previous_artifacts_exist(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifact = Artifact("author", {"key": "value"})
        artifacts = {ConversationTurnIndex(0): artifact}
        new_artifact = Artifact("author", {"key": "value"})

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.update_artifacts(new_artifact)

        # Assert
        assert len(context.artifacts) == 2

    def test_update_artifacts_no_artifact_passed_in(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifact = Artifact("author", {"key": "value"})
        artifacts = {ConversationTurnIndex(0): artifact}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        with pytest.raises(TypeError):
            context.update_artifacts(None)

    def test_update_artifacts_incorrect_type(self):

        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifact = Artifact("author", {"key": "value"})
        artifacts = {ConversationTurnIndex(0): artifact}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        with pytest.raises(TypeError):
            context.update_artifacts(0)

    def test_set_current_action_plan_none(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.current_action_plan = ""

        # Assert
        assert context.current_action_plan == ""

    def test_set_current_action_plan_one_token(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        # Act
        context = Context(current_question, conversation_history, artifacts)
        context.current_action_plan = "Hello"

        # Assert
        assert context.current_action_plan == "Hello"

    def test_set_current_action_plan_valid_stream(self):

        # Arrange
        sample_output = """
        {
        "Action": "get_weather",
        "Parameters": {
        "date": "2024-12-25"
        }
        }"""
        sample_tokens = get_tokens(sample_output)

        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        for token in sample_tokens:
            context.current_action_plan = token

        # Assert
        assert context.current_action_plan == sample_output

    def test_set_current_action_plan_invalid_token_type(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        with pytest.raises(TypeError):
            context.current_action_plan = 0

    def test_get_current_action_plan_empty(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}

        context = Context(current_question, conversation_history, artifacts)

        # Act & Assert
        with pytest.raises(AttributeError):
            current_action_plan = context.get_json_action_plan()

    def test_get_current_action_plan_incomplete(self):

        # Arrange
        sample_output = """
        {
        "Action": "get_weather",
        "Parameters": {
        "date": "2024-12-25"
        """

        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        for token in get_tokens(sample_output):
            context.current_action_plan = token

        # Act & Assert
        with pytest.raises(AttributeError):
            current_action_plan = context.get_json_action_plan()

    def test_get_current_action_plan_complete(self):

        # Arrange
        sample_output = """
        {
        "tool_name": "get_weather",
        "tool_input": {
        "date": "2024-12-25"
        }
        }"""

        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        for token in get_tokens(sample_output):
            context.current_action_plan = token

        # Act
        current_action_plan = context.get_json_action_plan()

        # Assert
        assert isinstance(current_action_plan, ActionPlan)
        assert current_action_plan.tool_name == "get_weather"
        assert current_action_plan.tool_input == {"date": "2024-12-25"}

    def test_get_decision_runs(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        decision_runs = context.decision_runs

        # Assert
        assert decision_runs == 0

    def test_update_decision_runs(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.increment_decision_runs()

        # Assert
        assert context.decision_runs == 1

    def test_update_previous_actions_none(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)
        # add a current action plan
        sample_output = """
        {
        "action_name": "test_action",
        "action_input": {
        "input": "value"
        }
        }
        """
        for token in get_tokens(sample_output):
            context.current_action_plan = token

        # Act
        context.update_previous_actions(author="autho", output=None)

        # Assert
        keys, values = zip(*context.previous_actions.items())
        assert keys[0].index_id == 0
        added_action = values[0]
        assert added_action.action_output == {
            "status": "error",
        }
        assert context.current_action_plan == ""

    def test_update_previous_tools_one(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)
        sample_output = """
        {
        "tool_name": "test_tool",
        "tool_input": {
        "input": "value"
        }
        }
        """
        for token in get_tokens(sample_output):
            context.current_action_plan = token

        action_plan = context.get_json_action_plan()
        # Act
        context.update_previous_actions(
            author="author", output={"key": "value"})

        # Assert
        keys, values = zip(*context.previous_actions.items())
        assert keys[0].index_id == 0
        added_action = values[0]
        assert isinstance(added_action, Action)
        assert added_action.action_name == action_plan.tool_name
        assert added_action.action_input == action_plan.tool_input
        assert added_action.action_output == {"key": "value"}
        assert context.current_action_plan == ""

    def test_update_previous_tool_sets_correct_index_when_existing_tools(self):

        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)
        sample_output = """
        {
        "tool_name": "test_tool",
        "tool_input": {
        "input": "value"
        }
        }
        """
        for token in get_tokens(sample_output):
            context.current_action_plan = token

        context.update_previous_actions(
            author="author", output={"key": "value"})

        # repeat
        for token in get_tokens(sample_output):
            context.current_action_plan = token

        action_plan = context.get_json_action_plan()

        # Act
        context.update_previous_actions(
            author="author", output={"key": "value2"})

        # Assert
        keys, values = zip(*context.previous_actions.items())
        assert len(keys) == 2
        added_action = values[1]
        assert isinstance(added_action, Action)
        assert added_action.action_name == action_plan.tool_name
        assert added_action.action_input == action_plan.tool_input
        assert added_action.action_output == {"key": "value2"}
        assert context.current_action_plan == ""

    def test_set_thinking_out_loud_none(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.thinking_out_loud = ""

        # Assert
        assert context.thinking_out_loud == ""

    def test_set_thinking_out_loud_one_token(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.thinking_out_loud = "Let"

        # Assert
        assert context.thinking_out_loud == "Let"

    def test_set_thinking_out_loud_valid_stream(self):
        # Arrange
        sample_output = "Let me check the weather data for December 25th, 2024"
        sample_tokens = get_tokens(sample_output)
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        for token in sample_tokens:
            context.thinking_out_loud = token

        # Assert
        assert context.thinking_out_loud == sample_output

    def test_set_thinking_out_loud_invalid_token_type(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act & Assert
        with pytest.raises(TypeError):
            context.thinking_out_loud = 0

    def test_set_internal_reasoning_none(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.internal_reasoning = ""

        # Assert
        assert context.internal_reasoning == ""

    def test_set_internal_reasoning_one_token(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.internal_reasoning = "Since"

        # Assert
        assert context.internal_reasoning == "Since"

    def test_set_internal_reasoning_valid_stream(self):
        # Arrange
        sample_output = 'Since we need historical weather data for a specific date, I\'ll use the get_weather function. The date parameter should be formatted as "2024-12-25".'
        sample_tokens = get_tokens(sample_output)
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        for token in sample_tokens:
            context.internal_reasoning = token

        # Assert
        assert context.internal_reasoning == sample_output

    def test_set_internal_reasoning_invalid_token_type(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act & Assert
        with pytest.raises(TypeError):
            context.internal_reasoning = 0

    def test_set_final_output_none(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.final_output = ""

        # Assert
        assert context.final_output == ""

    def test_set_final_output_one_token(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        context.final_output = "Yes"

        # Assert
        assert context.final_output == "Yes"

    def test_set_final_output_valid_stream(self):
        # Arrange
        sample_output = 'Yes, there was light rainfall on December 25th, 2024, with precipitation recorded at 2.3mm during the morning hours between 6 AM and 9 AM.'
        sample_tokens = get_tokens(sample_output)
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        for token in sample_tokens:
            context.final_output = token

        # Assert
        assert context.final_output == sample_output

    def test_set_final_output_invalid_token_type(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act & Assert
        with pytest.raises(TypeError):
            context.final_output = 0

    def test_format_artifacts_empty(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        formatted = context.format_artifacts()

        # Assert
        assert formatted == "No artifacts available"

    def test_format_artifacts_single(self):
        # Arrange
        current_question = ""
        conversation_history = [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ]
        artifacts = {}
        artifact = Artifact("author", {"key": "value"})
        artifacts[ConversationTurnIndex(0)] = artifact
        context = Context(current_question, conversation_history, artifacts)

        # Act
        formatted = context.format_artifacts()

        # Assert
        assert "author" in formatted
        assert "key" in formatted
        assert "value" in formatted

    def test_format_previous_tools_empty(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        formatted = context.format_previous_actions()

        # Assert
        assert formatted == "No previous tool calls"

    def test_format_previous_actions_single(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Add a test action
        action = Action("test_author", "test_action", {
                        "param": "value"}, {"result": "success"})
        context._previous_actions[DecisionRunIndex(0)] = action

        # Act
        formatted = context.format_previous_actions()

        # Assert
        assert "Decision Run 0" in formatted
        assert "test_author" in formatted
        assert "test_action" in formatted
        assert "param" in formatted
        assert "value" in formatted
        assert "result" in formatted
        assert "success" in formatted

    def test_format_custom_props_empty(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act
        formatted = context.format_custom_props("test_agent")

        # Assert
        assert formatted == "No custom properties have been set"

    def test_format_custom_props_single(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        custom_props = {
            "test_agent": [
                CustomProp("test_prop", "A test property", "test_value")
            ]
        }
        context = Context(current_question, conversation_history,
                          artifacts, custom_props=custom_props)

        # Act
        formatted = context.format_custom_props("test_agent")

        # Assert
        assert "1. test_prop" in formatted
        assert "A test property" in formatted
        assert "test_value" in formatted

    def test_get_most_recent_action_no_actions(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Act & Assert
        recent_action = context.get_most_recent_action()
        assert recent_action is None

    def test_get_most_recent_action_single(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Add a test action
        action = Action("test_author", "test_action", {
                        "param": "value"}, {"result": "success"})
        context._previous_actions[DecisionRunIndex(0)] = action

        # Act & Assert
        recent_action = context.get_most_recent_action()
        assert recent_action == action

    def test_get_most_recent_action_multiple(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        # Add multiple test actions
        action1 = Action("test_author1", "test_action1", {
            "param1": "value1"}, {"result1": "success1"})
        action2 = Action("test_author2", "test_action2", {
            "param2": "value2"}, {"result2": "success2"})
        context._previous_actions[DecisionRunIndex(0)] = action1
        context._previous_actions[DecisionRunIndex(1)] = action2

        # Act & Assert
        recent_action = context.get_most_recent_action()
        assert recent_action == action2

    def test_format_action_basic(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        action = Action(
            author="test_author",
            action_name="test_action",
            action_input={"param": "value"},
            action_output={"result": "success"}
        )

        # Act
        formatted = context.format_action(action)

        # Assert
        assert "Author: test_author" in formatted
        assert "Tool: test_action" in formatted
        assert '"param": "value"' in formatted
        assert '"result": "success"' in formatted

    def test_format_action_complex_input_output(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        action = Action(
            author="test_author",
            action_name="test_action",
            action_input={
                "nested": {
                    "param1": "value1",
                    "param2": "value2"
                },
                "list": [1, 2, 3]
            },
            action_output={
                "status": "success",
                "data": {
                    "result1": "value1",
                    "result2": "value2"
                }
            }
        )

        # Act
        formatted = context.format_action(action)

        # Assert
        assert "Author: test_author" in formatted
        assert "Tool: test_action" in formatted
        assert '"nested"' in formatted
        assert '"param1": "value1"' in formatted
        assert '"param2": "value2"' in formatted
        assert '"list"' in formatted
        assert '"status": "success"' in formatted
        assert '"result1": "value1"' in formatted
        assert '"result2": "value2"' in formatted

    def test_format_action_empty_input_output(self):
        # Arrange
        current_question = ""
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        action = Action(
            author="test_author",
            action_name="test_action",
            action_input={},
            action_output={}
        )

        # Act
        formatted = context.format_action(action)

        # Assert
        assert "Author: test_author" in formatted
        assert "Tool: test_action" in formatted
        assert "Input: {}" in formatted
        assert "Result: {}" in formatted
