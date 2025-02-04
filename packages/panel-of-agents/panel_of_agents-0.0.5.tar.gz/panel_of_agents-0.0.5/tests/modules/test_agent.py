import os

from dotenv import load_dotenv
import pytest
import pytest_asyncio
from pytest_mock import mocker, MockFixture
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
import tiktoken

from src.panel_of_agents.agents import Agent, AgentVote
from src.panel_of_agents.decorators import agent_capability, creates_artifact
from src.panel_of_agents.types.context import Artifact, CustomProp, Action, DecisionRunIndex, ConversationTurnIndex, ArtifactType
from src.panel_of_agents.types.agents import CapabilityResult
from src.panel_of_agents.context import Context
from src.panel_of_agents.utils import split_with_delimiter


load_dotenv()


def get_tokens(text):
    return split_with_delimiter(text, " ")


class NoCapabilityAgent(Agent):
    def __init__(self, name: str, personal_biograhpy: str, public_biograhpy: str, model: ChatOpenAI):
        super().__init__(name, personal_biograhpy, public_biograhpy, model)

    def get_response(self, context):
        return "Hello, World!"


class OneCapabilityAgent(Agent):
    def __init__(self, name: str, personal_biograhpy: str, public_biograhpy: str, model: ChatOpenAI):
        super().__init__(name, personal_biograhpy, public_biograhpy, model)

    @agent_capability
    def sample_capability_one(self, greeting: str) -> CapabilityResult:
        """This is a capability which returns a greeting."""
        return CapabilityResult(
            result=f"{greeting}, World!",
            artifact=None
        )


class MultipleCapabilityAgent(Agent):
    def __init__(self, name: str, personal_biograhpy: str, public_biograhpy: str, model: ChatOpenAI):
        super().__init__(name, personal_biograhpy, public_biograhpy, model)

    @agent_capability
    def sample_capability_one(self, greeting: str) -> CapabilityResult:
        """This is a capability which returns a greeting."""
        return CapabilityResult(
            result=f"{greeting}, World!",
            artifact=None
        )

    @agent_capability
    def sample_capability_two(self, greeting: str, exclamations: int) -> CapabilityResult:
        """This is another capability which returns a greeting with exclamations."""
        return CapabilityResult(
            result=f"{greeting}, World{'!' * exclamations}",
            artifact=None
        )


class ErroneousFunctionAgent(Agent):
    def __init__(self,
                 name="Error Agent",
                 personal_biograhpy="This is an agent that will raise an error.",
                 public_biograhpy="This is an agent that will raise an error.",
                 model=ChatOpenAI(model="gpt-4o-mini"),
                 max_tries=3
                 ):
        super().__init__(name, personal_biograhpy, public_biograhpy, model, max_tries)

    @agent_capability
    def erroneous_function(self, greeting: str) -> CapabilityResult:
        """This is a capability which raises an error."""
        raise RuntimeError("This is an error.")


class ArtifactCapabilityAgent(Agent):
    def __init__(self, name: str, personal_biograhpy: str, public_biograhpy: str, model: ChatOpenAI):
        super().__init__(name, personal_biograhpy, public_biograhpy, model)

    @agent_capability
    @creates_artifact(description="This is a toy artifact")
    def sample_capability_with_artifact(self, greeting: str) -> CapabilityResult:
        """This is a capability which returns a greeting and creates an artifact."""
        return CapabilityResult(
            result=f"{greeting}, World!",
            artifact=Artifact(author="test", data={"message": "Hello, World!"})
        )


@pytest.fixture
def test_voting_invoke(mocker: MockFixture):
    mocker.patch(
        "src.panel_of_agents.agents.Agent._invoke",
        return_value=AgentVote(
            reason="I can do this",
            vote=10
        )
    )


@pytest.fixture
def test_erroneous_voting_invoke(mocker: MockFixture):
    mocker.patch(
        "src.panel_of_agents.agents.Agent._invoke",
        return_value="This is not JSON"
    )


@pytest.fixture
def test_incorrect_params_voting_invoke(mocker: MockFixture):
    mocker.patch(
        "src.panel_of_agents.agents.Agent._invoke",
        return_value="""{
        "incorrect": "parameters",
        "are": "present" 
        }"""
    )


class TestAgentInitialization:
    def test_agent_init_rejects_incorrect_model_type(self):
        # Arrange
        name = "Test Agent"
        personal_biograhpy = "This is a test agent."
        public_biograhpy = "This is a test agent."
        model = "This is not a model."

        # Act
        with pytest.raises(TypeError):
            agent = Agent(
                name=name,
                personal_biograhpy=personal_biograhpy,
                public_biograhpy=public_biograhpy,
                model=model,
            )

    def test_agent_init_accepts_correct_model_type(self):
        # Arrange
        name = "Test Agent"
        personal_biograhpy = "This is a test agent."
        public_biograhpy = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")

        # Act
        agent = Agent(
            name=name,
            personal_biograhpy=personal_biograhpy,
            public_biograhpy=public_biograhpy,
            model=model,
        )

        # Assert
        assert agent.name == name
        assert agent.personal_biograhpy == personal_biograhpy
        assert agent.public_biograhpy == public_biograhpy
        assert agent.model == model

    def test_agent_no_capabilities(self):
        # Arrange
        name = "Test Agent"
        personal_biograhpy = "This is a test agent."
        public_biograhpy = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")

        # Act
        agent = NoCapabilityAgent(
            name=name,
            personal_biograhpy=personal_biograhpy,
            public_biograhpy=public_biograhpy,
            model=model
        )

        # Assert
        assert len(agent.actions) == 1  # Only has pass_agent capability

    def test_agent_one_capability(self):
        # Arrange
        name = "Test Agent"
        personal_biograhpy = "This is a test agent."
        public_biograhpy = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")

        # Act
        agent = OneCapabilityAgent(
            name=name,
            personal_biograhpy=personal_biograhpy,
            public_biograhpy=public_biograhpy,
            model=model
        )

        # Assert
        # Has pass_agent + one custom capability
        assert len(agent.actions) == 2

    def test_agent_multiple_capabilities(self):
        # Arrange
        name = "Test Agent"
        personal_biograhpy = "This is a test agent."
        public_biograhpy = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")

        # Act
        agent = MultipleCapabilityAgent(
            name=name,
            personal_biograhpy=personal_biograhpy,
            public_biograhpy=public_biograhpy,
            model=model
        )

        # Assert
        # Has pass_agent + two custom capabilities
        assert len(agent.actions) == 3


class TestAgentVoting:
    def test_vote_correct_json(self, test_voting_invoke):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        result = agent.vote(context)

        # Assert
        assert result.vote == 10

    # def test_vote_erroneous_json(self, test_erroneous_voting_invoke):
    #     # Arrange
    #     agent = NoCapabilityAgent(
    #         "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
    #     context = Context("test", [], {})

    #     # Act
    #     result = agent.vote(context)

    #     # Assert
    #     assert isinstance(result, dict)
    #     assert result["vote"] == 0

    # def test_vote_incorrect_parameters(self, test_incorrect_params_voting_invoke):
    #     # Arrange
    #     agent = NoCapabilityAgent(
    #         "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
    #     context = Context("test", [], {})

    #     # Act
    #     result = agent.vote(context)

    #     # Assert
    #     assert isinstance(result, dict)
    #     assert result["vote"] == 0

    def test_repeated_voting_keeps_the_prompt_the_same(self, test_voting_invoke):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        original_prompt = agent.voting_prompt

        # Act
        result = agent.vote(context)
        result = agent.vote(context)
        result = agent.vote(context)

        # Assert
        assert agent.voting_prompt == original_prompt
        assert result.vote == 10


class TestPeerInformation:
    def test_set_peer_information_no_peers(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))

        # Act
        agent.set_peer_information({})

        # Assert
        assert "no peers to choose from" in agent.passing_clause.lower()

    def test_set_peer_information_one_peer(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        peers = {"Peer1": "Bio1"}

        # Act
        agent.set_peer_information(peers)

        # Assert
        assert "Peer1" in agent.passing_clause
        assert "Bio1" in agent.passing_clause

    def test_set_peer_information_multiple_peers(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        peers = {"Peer1": "Bio1", "Peer2": "Bio2"}

        # Act
        agent.set_peer_information(peers)

        # Assert
        assert all(peer in agent.passing_clause
                   for peer in [
                       "Peer1", "Peer2"])
        assert all(bio in agent.passing_clause for bio in [
                   "Bio1", "Bio2"])

    def test_set_peer_information_incorrect_input_type(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))

        # Act & Assert
        with pytest.raises(TypeError):
            agent.set_peer_information("not a dict")

    def test_set_peer_information_incorrect_content_type(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))

        # Act & Assert
        with pytest.raises(TypeError):
            agent.set_peer_information({1: 2})


class TestPromptPreparation:
    def test_prepare_prompt_decision_turn_one(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        context._decision_runs = 0

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert agent.initial_decision_state in prompt

    def test_prepare_prompt_decision_turn_middle(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        context._decision_runs = 1

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert agent.continued_prompt_state in prompt

    def test_prepare_prompt_decision_turn_max(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        context._decision_runs = agent.max_tries

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert agent.finishing_prompt_state in prompt

    def test_prepare_prompt_in_panel_true(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        prompt = agent.prepare_prompt(context, in_panel=True)

        # Assert
        assert "PASS CONDITIONS" in prompt

    def test_prepare_prompt_in_panel_false(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        prompt = agent.prepare_prompt(context, in_panel=False)

        # Assert
        assert "PASS CONDITIONS" not in prompt

    def test_prepare_prompt_includes_artifacts(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        context.update_artifacts(Artifact("author", {"key": "artifact"}))

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert "artifact" in prompt

    def test_prepare_prompt_includes_custom_props(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {}, custom_props={
            "Test": [CustomProp("test_prop", "A test property", "test_value")]
        })

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert "test_prop" in prompt
        assert "A test property" in prompt
        assert "test_value" in prompt

    def test_prepare_prompt_includes_multiple_custom_props(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {}, custom_props={
            "Test": [CustomProp("prop1", "First property", "value1"),
                     CustomProp("prop2", "Second property", 123)]
        })

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert "prop1" in prompt
        assert "First property" in prompt
        assert "value1" in prompt
        assert "prop2" in prompt
        assert "Second property" in prompt
        assert "123" in prompt

    def test_prepare_prompt_empty_custom_props(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})  # No custom_props provided

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        # assert "Custom properties provide additional context" in prompt
        assert "No custom properties have been set" in prompt

    def test_prepare_prompt_includes_formatted_artifacts(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        context.update_artifacts(Artifact("author", {"key": "artifact"}))

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert "author" in prompt
        assert "key" in prompt
        assert "artifact" in prompt

    # def test_prepare_prompt_includes_formatted_previous_actions(self):
    #     # Arrange
    #     agent = NoCapabilityAgent(
    #         "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
    #     context = Context("test", [], {})
    #     action = Action("test_author", "test_action", {
    #                     "param": "value"}, {"result": "success"})
    #     context._previous_actions[DecisionRunIndex(0)] = action

    #     # Act
    #     prompt = agent.prepare_prompt(context)

    #     # Assert
    #     assert "Decision Run 0" in prompt
    #     assert "test_author" in prompt
    #     assert "test_action" in prompt
    #     assert "param" in prompt
    #     assert "value" in prompt
    #     assert "result" in prompt
    #     assert "success" in prompt

    def test_prepare_prompt_includes_formatted_custom_props(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {}, custom_props={
            "Test": [CustomProp("test_prop", "A test property", "test_value")]
        })

        # Act
        prompt = agent.prepare_prompt(context)

        # Assert
        assert "1. test_prop" in prompt
        assert "A test property" in prompt
        assert "test_value" in prompt


class TestChainBuilding:
    def test_build_chain_creates_runnable(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        prompt = agent.prepare_prompt(context, in_panel=False)

        # Act
        chain = agent.build_chain(context, prompt)

        # Assert
        assert isinstance(chain, Runnable)

    def test_build_chain_includes_conversation_history(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [
            HumanMessage("Hello"),
            AIMessage("Hi")
        ], {})
        prompt = agent.prepare_prompt(context, in_panel=False)

        # Act
        chain = agent.build_chain(context, prompt)

        # Assert
        assert isinstance(chain, Runnable)


class TesttoolCalling:
    def test_call_tool_erroneous_json(self):
        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = NoCapabilityAgent(name, pub_bio, personal_bio, model)

        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
        {
            "tool_name": "sample_capability_one"
            "tool_input": {
                "greeting": "Hello"
            }
        }
        """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output == {
            "status": "error-json",
        }

    def test_call_tool_unknown_function(self):
        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = NoCapabilityAgent(name, pub_bio, personal_bio, model)

        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
            {
                "tool_name": "nonexistent_function",
                "tool_input": {
                    "greeting": "Hello"
                }
            }
            """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output == {
            "status": "error-function-not-found",
        }

    def test_call_tool_incorrect_tool_keys(self):
        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = NoCapabilityAgent(name, pub_bio, personal_bio, model)

        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
        {
            "tool_name": "sample_capability_one",
            "incorrect_key": {
                "greeting": "Hello"
            }
        }
        """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output == {
            "status": "error-incorrect-keys",
        }

    def test_call_tool_execution_error(self):
        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = ErroneousFunctionAgent()
        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
        {
            "tool_name": "erroneous_function",
            "tool_input": {
                "greeting": "will_cause_error"
            }
        }
        """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output == {
            "status": "error-function-error",
        }

    def test_call_tool_invalid_parameters(self):
        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = OneCapabilityAgent(name, pub_bio, personal_bio, model)
        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
        {
            "tool_name": "sample_capability_one",
            "tool_input": {
                "invalid_param": "wrong_parameter",
                "another_wrong": "not_valid"
            }
        }
        """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output == {
            "status": "error-invalid-parameters",
        }

    def test_call_tool_successful(self):

        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = NoCapabilityAgent(name, pub_bio, personal_bio, model)

        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
        {
            "tool_name": "sample_capability_one",
            "tool_input": {
                "greeting": "Hello"
            }
        }
        """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output is not None

    def test_call_tool_with_artifact(self):
        # Arrange
        name = "Test Agent"
        pub_bio = "This is a test agent."
        personal_bio = "This is a test agent."
        model = ChatOpenAI(model="gpt-4o-mini")
        agent = ArtifactCapabilityAgent(name, pub_bio, personal_bio, model)

        current_question = "Hello, World!"
        conversation_history = []
        artifacts = {}
        context = Context(current_question, conversation_history, artifacts)

        sample_json = """
        {
            "tool_name": "sample_capability_with_artifact",
            "tool_input": {
                "greeting": "Hello"
            }
        }
        """

        for token in get_tokens(sample_json):
            context.current_action_plan = token

        assert context.current_action_plan != ""

        # Act
        agent.call_action(context)

        # Assert
        assert context.current_action_plan == ""
        assert len(context.previous_actions) == 1
        past_action = context.previous_actions[list(
            context.previous_actions.keys())[0]]
        assert past_action.action_output["status"] == "success"
        assert past_action.action_output["result"] == "Hello, World!"
        assert len(context.artifacts) == 1
        artifact = context.artifacts[list(context.artifacts.keys())[0]]
        assert artifact.author == "test"
        assert artifact.data == {"message": "Hello, World!"}


class TestDynamicPrompt:

    def test_prepare_dynamic_prompt_no_pass(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        result = agent.prepare_dynamic_prompt(
            context, "sample_capability_one", {}, {"status": "success"}, None)

        # Assert
        assert result is False
        assert "sample_capability_one" in context.current_question

    @pytest.mark.parametrize("runs", [1, 2, 3])
    def test_prepare_dynamic_prompt_correct_state_update(self, runs):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        state_clauses = [
            agent.continued_prompt_state,
            agent.continued_prompt_state,
            agent.finishing_prompt_state
        ]
        matching_state = state_clauses[runs - 1]
        context._decision_runs = runs - 1

        # Act
        _ = agent.prepare_dynamic_prompt(
            context, "state_capability_test", {}, {"status": "success"}, None)

        # Assert
        assert matching_state in context.current_question

    def test_prepare_dynamic_prompt_pass(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("Test", [], {})

        # Act
        result = agent.prepare_dynamic_prompt(context, "pass_agent", {
                                              "nominee": "Test2", "agent_message": "Here you go Test2!"}, {"status": "success"}, None)

        # Assert
        assert result is True
        assert context.target_agent == "Test2"
        assert "Here you go Test2!" in context.current_question
        assert context.current_action_plan == ""
        assert context.decision_runs == 1
        assert context.previous_actions == {}

    def test_prepare_dynamic_prompt_with_user_artifact(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        result = agent.prepare_dynamic_prompt(
            context,
            "sample_capability_one",
            {},
            {"status": "success"},
            Artifact(author="test", data={
                     "message": "Hello, World!"}, artifact_type=ArtifactType.USER)
        )

        # Assert
        assert result is False
        assert "The previous tool call created an artifact, please make sure to explain the artifact in the response." in context.current_question

    def test_prepare_dynamic_prompt_with_internal_artifact(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        result = agent.prepare_dynamic_prompt(
            context, "sample_capability_one", {}, {"status": "success"}, Artifact(author="test", data={"message": "Hello, World!"}, artifact_type=ArtifactType.INTERNAL))

        # Assert
        assert result is False
        assert "The previous tool call created an artifact, please make sure to explain the artifact in the response." not in context.current_question

    def test_format_voting_prompt(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})

        # Act
        chain = agent._format_voting_prompt(context)

        # Assert
        assert chain is not None
        # Verify the chain components
        # ChatPromptTemplate and structured output model
        assert len(chain.steps) == 3

    def test_format_voting_prompt_preserves_template(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test", "Bio", "Public Bio", ChatOpenAI(model="gpt-4o-mini"))
        context = Context("test", [], {})
        original_prompt = agent.voting_prompt

        # Act
        chain = agent._format_voting_prompt(context)
        chain2 = agent._format_voting_prompt(context)

        # Assert
        assert agent.voting_prompt == original_prompt
