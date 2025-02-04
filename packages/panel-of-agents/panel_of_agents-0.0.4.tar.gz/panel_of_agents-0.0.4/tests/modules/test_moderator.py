from typing import Any
import pytest
import pytest_asyncio
from pytest_mock import MockFixture
from langchain_openai import ChatOpenAI
import json

from src.panel_of_agents.agents import Agent
from src.panel_of_agents.moderator import Moderator
from src.panel_of_agents.context import Context
from tests.modules.test_agent import NoCapabilityAgent, OneCapabilityAgent, get_tokens


@pytest.fixture
def single_agent_vote_mock(mocker: MockFixture):
    mocker.patch(
        "src.panel_of_agents.agents.Agent._invoke",
        return_value="""{
        "reason": "Single agent vote",
        "vote": 100
        }"""
    )


@pytest.fixture
def multiple_agent_votes_mock(mocker: MockFixture):
    responses = iter([
        """{
            "reason": "First agent vote",
            "vote": 75
        }""",
        """{
            "reason": "Second agent vote",
            "vote": 85
        }""",
        """{
            "reason": "Third agent vote",
            "vote": 95
        }"""
    ])

    mocker.patch(
        "src.panel_of_agents.agents.Agent._invoke",
        side_effect=lambda *args: next(responses)
    )


@pytest_asyncio.fixture
async def multiple_agent_votes_async_mock(mocker: MockFixture):
    responses = iter([
        """{
            "reason": "First agent vote",
            "vote": 75
        }""",
        """{
            "reason": "Second agent vote",
            "vote": 85
        }""",
        """{
            "reason": "Third agent vote",
            "vote": 95
        }"""
    ])

    mocker.patch(
        "src.panel_of_agents.agents.Agent._ainvoke",
        side_effect=lambda *args: next(responses)
    )


class TestModeratorInitialization:
    def test_init_rejects_empty_panel(self):
        # Arrange
        panel = []
        leader = "leader"

        # Act & Assert
        with pytest.raises(ValueError, match="Panel must contain at least one agent"):
            moderator = Moderator(panel, leader)

    def test_init_rejects_non_list_panel(self):
        # Arrange
        panel = "not a list"
        leader = "leader"

        # Act & Assert
        with pytest.raises(TypeError, match="Panel must be a list"):
            moderator = Moderator(panel, leader)

    def test_init_rejects_non_agent_items(self):
        # Arrange
        panel = ["not an agent", 123]
        leader = "leader"

        # Act & Assert
        with pytest.raises(TypeError, match="All panel members must be instances of Agent"):
            moderator = Moderator(panel, leader)

    def test_init_rejects_invalid_leader(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent]
        leader = "nonexistent_leader"

        # Act & Assert
        with pytest.raises(ValueError, match="Leader must be the name of one of the agents in the panel"):
            moderator = Moderator(panel, leader)

    def test_init_single_agent_panel(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent]
        leader = "Test Agent"

        # Act
        moderator = Moderator(panel, leader)

        # Assert
        assert len(moderator.panel_of_agents) == 1
        assert "Test Agent" in moderator.panel_of_agents
        assert moderator.panel_of_agents["Test Agent"] == agent
        # Verify peer information is empty for single agent
        assert "No peers to choose from" in agent.passing_clause

    def test_init_multiple_agent_panel(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent3 = NoCapabilityAgent(
            "Agent Three",
            "Personal Bio 3",
            "Public Bio 3",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2, agent3]
        leader = "Agent One"

        # Act
        moderator = Moderator(panel, leader)

        # Assert
        assert len(moderator.panel_of_agents) == 3
        assert all(name in moderator.panel_of_agents for name in [
                   "Agent One", "Agent Two", "Agent Three"])

        # Check peer information for each agent
        for agent in panel:
            peer_info = {}
            for peer in panel:
                if peer.name != agent.name:  # Don't include self
                    peer_info[peer.name] = peer.public_biograhpy

            # Verify the peer information is in the agent's passing clause
            for peer_name, peer_bio in peer_info.items():
                assert peer_name in agent.passing_clause
                assert peer_bio in agent.passing_clause

            # Verify agent's own bio is not in their peer information
            assert agent.public_biograhpy not in agent.passing_clause


class TestModeratorVoting:
    @pytest.fixture
    def single_agent_vote_mock(self, mocker: MockFixture):
        mocker.patch(
            "src.panel_of_agents.agents.Agent._invoke",
            return_value="""{
            "reason": "Single agent vote",
            "vote": 100
            }"""
        )

    @pytest.fixture
    def multiple_agent_votes_mock(self, mocker: MockFixture):
        responses = iter([
            """{
                "reason": "First agent vote",
                "vote": 75
            }""",
            """{
                "reason": "Second agent vote",
                "vote": 85
            }""",
            """{
                "reason": "Third agent vote",
                "vote": 95
            }"""
        ])

        mocker.patch(
            "src.panel_of_agents.agents.Agent._invoke",
            side_effect=lambda *args: next(responses)
        )

    def test_single_agent_voting(self, single_agent_vote_mock):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent]
        leader = "Test Agent"
        moderator = Moderator(panel, leader)
        context = Context("test question", [], {})

        # Act
        votes = moderator.conduct_sync_vote(context)

        # Assert
        assert len(votes) == 1
        assert votes["Test Agent"] == 100

    def test_multiple_agent_voting(self, multiple_agent_votes_mock):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent3 = NoCapabilityAgent(
            "Agent Three",
            "Personal Bio 3",
            "Public Bio 3",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2, agent3]
        leader = "Agent One"
        moderator = Moderator(panel, leader)
        context = Context("test question", [], {})

        # Act
        votes = moderator.conduct_sync_vote(context)

        # Assert
        assert len(votes) == 3
        assert votes["Agent One"] == 75
        assert votes["Agent Two"] == 85
        assert votes["Agent Three"] == 95


class TestModeratorWinnerSelection:
    def test_select_winner_single_vote(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent]
        leader = "Test Agent"
        moderator = Moderator(panel, leader)
        votes = {"Test Agent": 50}

        # Act
        winner = moderator.select_winner(votes)

        # Assert
        assert winner == "Test Agent"

    def test_select_winner_all_zeros_returns_leader(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2]
        leader = "Agent One"
        moderator = Moderator(panel, leader)
        votes = {"Agent One": 0, "Agent Two": 0}

        # Act
        winner = moderator.select_winner(votes)

        # Assert
        assert winner == "Agent One"

    def test_select_winner_all_hundred_with_leader(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2]
        leader = "Agent Two"
        moderator = Moderator(panel, leader)
        votes = {"Agent One": 100, "Agent Two": 100}

        # Act
        winner = moderator.select_winner(votes)

        # Assert
        assert winner == "Agent Two"

    def test_select_winner_all_hundred_without_leader(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Beta Agent",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        leader_agent = NoCapabilityAgent(
            "Leader Agent",
            "Leader Bio",
            "Leader Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2, leader_agent]
        leader = "Leader Agent"
        moderator = Moderator(panel, leader)
        votes = {"Agent One": 100, "Beta Agent": 100, "Leader Agent": 0}

        # Act
        winner = moderator.select_winner(votes)

        # Assert
        assert winner == "Agent One"  # Alphabetically first wins ties

    def test_select_winner_clear_winner(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2]
        leader = "Agent One"
        moderator = Moderator(panel, leader)
        votes = {"Agent One": 75, "Agent Two": 90}

        # Act
        winner = moderator.select_winner(votes)

        # Assert
        assert winner == "Agent Two"


class TestModeratorAgentSwitching:

    def test_switch_agent_returns_correct_agent(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2]
        leader = "Agent One"
        moderator = Moderator(panel, leader)

        # Act
        switched_agent = moderator.switch_agent("Agent Two")

        # Assert
        assert switched_agent == agent2


class TestModeratorAsyncVoting:

    @pytest.mark.asyncio
    async def test_single_agent_async_voting(self, single_agent_vote_mock):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent]
        leader = "Test Agent"
        moderator = Moderator(panel, leader)
        context = Context("test question", [], {})

        # Act
        votes = await moderator.conduct_async_vote(context)

        # Assert
        assert len(votes) == 1
        assert votes["Test Agent"] == 100

    @pytest.mark.asyncio
    async def test_multiple_agent_async_voting(self, multiple_agent_votes_async_mock):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent3 = NoCapabilityAgent(
            "Agent Three",
            "Personal Bio 3",
            "Public Bio 3",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2, agent3]
        leader = "Agent One"
        moderator = Moderator(panel, leader)
        context = Context("test question", [], {})

        # Act
        votes = await moderator.conduct_async_vote(context)

        # Assert
        assert len(votes) == 3
        assert votes["Agent One"] == 75
        assert votes["Agent Two"] == 85
        assert votes["Agent Three"] == 95


class TestModeratorExecute:

    @pytest.fixture
    def agent_decide_mock(self, mocker: MockFixture, request):
        # Response pattern 1: Only until action plan
        action_plan_response = """🚨 Let me check the weather data for December 25th, 2024 🚨
        🤖 Since we need historical weather data for a specific date, I'll use the get_weather function. The date parameter should be formatted as "2024-12-25". 🤖
        🛠️
        {
        "action_name": "get_weather",
        "action_input": {
        "date": "2024-12-25"
        }
        }
        🛠️"""

        # Response pattern 2: Only final output
        final_output_response = """📢 Yes, there was light rainfall on December 25th, 2024, with precipitation recorded at 2.3mm during the morning hours between 6 AM and 9 AM. 📢"""

        # Response pattern 3: Pass to another agent
        pass_action_response = """🚨 I need to pass this task to Agent Two who has more expertise 🚨
        🤖 Preparing to delegate this task to a more qualified agent 🤖
        🛠️
        {
        "action_name": "pass",
        "action_input": {
        "nominee": "Agent Two",
        "reason": "Better expertise for this task"
        }
        }
        🛠️"""

        response_patterns = {
            'action_plan': action_plan_response,
            'final_output': final_output_response,
            'pass_action': pass_action_response
        }

        # Get the requested pattern or default to full response
        pattern = getattr(request, 'param', 'action_plan')
        response = response_patterns[pattern]
        response = get_tokens(response)

        def mock_decide(question: str, chain: Any):
            for token in response:
                yield token

        mocker.patch(
            "src.panel_of_agents.agents.Agent._stream_chunks",
            side_effect=mock_decide
        )

    @pytest.fixture
    def agent_adecide_mock(self, mocker: MockFixture):
        response = """🚨 Let me check the weather data for December 25th, 2024 🚨
        🤖 Since we need historical weather data for a specific date, I'll use the get_weather function. The date parameter should be formatted as "2024-12-25". 🤖
        🛠️
        {
        "action_name": "get_weather",
        "action_input": {
        "date": "2024-12-25"
        }
        }
        🛠️
        📢 Yes, there was light rainfall on December 25th, 2024, with precipitation recorded at 2.3mm during the morning hours between 6 AM and 9 AM. 📢"""
        response = get_tokens(response)

        async def mock_adecide(question: str, chain: Any):
            for token in response:
                yield token
        mocker.patch(
            "src.panel_of_agents.agents.Agent._astream_chunks",
            side_effect=mock_adecide
        )

    # @pytest.mark.parametrize('agent_decide_mock', ['action_plan'], indirect=True)
    # def test_execute_action_plan_only(self, agent_decide_mock):
    #     # Arrange
    #     agent = OneCapabilityAgent(
    #         "Test Agent",
    #         "Personal Bio",
    #         "Public Bio",
    #         ChatOpenAI(model="gpt-4o-mini")
    #     )
    #     agent.max_tries = 2  # Set max tries to 2
    #     panel = [agent]
    #     leader = "Test Agent"
    #     moderator = Moderator(panel, leader)
    #     context = Context("test question", [], {})
    #     context.target_agent = "Test Agent"

    #     # Act
    #     for token in moderator.execute(context):
    #         if "🛠️" in token:  # Start of action plan
    #             context.current_action_plan = ""  # Reset for new plan
    #         elif context.current_action_plan is not None:
    #             context.current_action_plan += token

    #     # Assert
    #     assert context.decision_runs == 2  # Reached max tries
    #     assert len(context.previous_actions) == 2  # Two actions recorded

    #     # Verify both actions were weather queries
    #     actions = list(context.previous_actions.values())
    #     for action in actions:
    #         assert action.action_name == "get_weather"
    #         assert action.action_input == {"date": "2024-12-25"}

    # @pytest.mark.parametrize('agent_decide_mock', ['final_output'], indirect=True)
    # def test_execute_final_output_only(self, agent_decide_mock):
    #     # Arrange
    #     agent = OneCapabilityAgent(
    #         "Test Agent",
    #         "Personal Bio",
    #         "Public Bio",
    #         ChatOpenAI(model="gpt-4o-mini")
    #     )
    #     panel = [agent]
    #     leader = "Test Agent"
    #     moderator = Moderator(panel, leader)
    #     context = Context("test question", [], {})
    #     context.target_agent = "Test Agent"

    #     # Act
    #     window_count = 0
    #     for token in moderator.execute(context):
    #         if "📢" in token:  # Changed from 🪟
    #             window_count += 1
    #             if window_count == 2:  # Second response emoji means closing
    #                 context.conversation_turn_finished = True
    #                 break
    #         elif context.final_output is not None:
    #             context.final_output += token

    #     # Assert
    #     assert context.conversation_turn_finished == True
    #     assert "light rainfall" in context.final_output
    #     assert "2.3mm" in context.final_output

    # @pytest.mark.parametrize('agent_decide_mock', ['pass_action'], indirect=True)
    # def test_execute_pass_action(self, agent_decide_mock):
    #     # Arrange
    #     agent1 = OneCapabilityAgent(
    #         "Agent One",
    #         "Personal Bio 1",
    #         "Public Bio 1",
    #         ChatOpenAI(model="gpt-4o-mini")
    #     )
    #     agent2 = OneCapabilityAgent(
    #         "Agent Two",
    #         "Personal Bio 2",
    #         "Public Bio 2",
    #         ChatOpenAI(model="gpt-4o-mini")
    #     )
    #     panel = [agent1, agent2]
    #     leader = "Agent One"
    #     moderator = Moderator(panel, leader)
    #     context = Context("test question", [], {})
    #     context.target_agent = "Agent One"

    #     # Act
    #     for token in moderator.execute(context):
    #         if "🛠️" in token:  # Start of action plan
    #             context.current_action_plan = ""  # Reset for new plan
    #         elif context.current_action_plan is not None:
    #             context.current_action_plan += token

    #     # Assert
    #     assert len(context.previous_actions) == 1
    #     action = list(context.previous_actions.values())[0]
    #     assert action.action_name == "pass"
    #     assert action.action_input["nominee"] == "Agent Two"
    #     assert "expertise" in action.action_input["reason"].lower()

    def test_format_voting_prompt(self):
        # Arrange
        agent1 = NoCapabilityAgent(
            "Agent One",
            "Personal Bio 1",
            "Public Bio 1",
            ChatOpenAI(model="gpt-4o-mini")
        )
        agent2 = NoCapabilityAgent(
            "Agent Two",
            "Personal Bio 2",
            "Public Bio 2",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent1, agent2]
        leader = "Agent One"
        moderator = Moderator(panel, leader)
        context = Context("test", [], {})

        # Act
        prompt = moderator._format_voting_prompt(context)

        # Assert
        assert prompt is not None
        # Verify prompt content
        prompt_content = prompt.messages[0].content
        assert "Agent One" in prompt_content
        assert "Agent Two" in prompt_content
        assert "Public Bio 1" in prompt_content
        assert "Public Bio 2" in prompt_content

    def test_format_voting_prompt_preserves_template(self):
        # Arrange
        agent = NoCapabilityAgent(
            "Test Agent",
            "Personal Bio",
            "Public Bio",
            ChatOpenAI(model="gpt-4o-mini")
        )
        panel = [agent]
        leader = "Test Agent"
        moderator = Moderator(panel, leader)
        context = Context("test", [], {})
        original_prompt = moderator.moderator_voting_prompt

        # Act
        prompt1 = moderator._format_voting_prompt(context)
        prompt2 = moderator._format_voting_prompt(context)

        # Assert
        assert moderator.moderator_voting_prompt == original_prompt
        assert prompt1.messages[0].content == prompt2.messages[0].content
