from typing import List, Dict, AsyncGenerator, Generator
import asyncio
from langchain_core.language_models import BaseChatModel
from .agents import Agent
from .context import Context
from .types.agents import AgentVote, ModeratorVote
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import ValidationError
import json
from .utils import format_conversation_history, get_json_from_string


class Moderator:
    moderator_voting_prompt = """
        ### MODERATOR VOTING DIRECTIVE
        WARNING: THIS IS A VOTE-ONLY TASK. ANY NON-JSON OUTPUT WILL BE REJECTED.

        TASK:
        Given the `conversation_history`, Select the SINGLE MOST APPROPRIATE capability level for each agent that matches their ability to continue the conversation.
        Conversation history is PROVIDED FOR CONTEXT ONLY.

        CAPABILITY LEVELS:
        100 points: COMPLETE SOLVER
        - Can independently handle the ENTIRE query from start to finish
        - Has ALL required functions and domain knowledge
        - NO assistance needed from other agents

        50 points: INITIATOR 
        - Can provide initial information required for completion of the task 
        - Can execute initial action required for completion of the task
        - Cannot complete the entire task alone

        20 points: FINALIZER
        - Cannot initiate or process independently
        - Can execute final action required for completion of the task
        - Can deliver final output
        - Requires complete input from others

        10 points: SUPPORT AGENT
        - Cannot work independently on task
        - Can assist other agents' processing
        - Has supplementary functions/knowledge
        - Role is purely supportive

        0 points: NO CAPABILITY
        - Lacks required functions
        - Missing domain knowledge
        - Cannot meaningfully contribute

        VOTING GUIDELINES:
        - No 2 agents can have the same vote value

        PANEL COMPOSITION:
        {panel_info}

        REQUIRED OUTPUT FORMAT:
        {{
            "votes": [
                {{
                    "reason" : "reason for agent1 vote", 
                    "name": "agent_name1", 
                    "vote": number # MUST be one of: 100, 50, 20, 10, 0
                }},  
                {{
                    "reason" : "reason for agent2 vote",
                    "name": "agent_name2", 
                    "vote": number # MUST be one of: 100, 50, 20, 10, 0
                }},
                ...
            ]
        }}

        CONVERSATION HISTORY:
        {conversation_history}

        CURRENT QUESTION:
        {question}
        """

    def __init__(
        self,
        panel_of_agents: List[Agent],
        leader: str,
        moderator_cast_vote: bool = False,
        moderator_model: BaseChatModel = None,
    ):
        # Check if panel is a list
        if not isinstance(panel_of_agents, list):
            raise TypeError("Panel must be a list")

        # Check if panel is empty
        if len(panel_of_agents) == 0:
            raise ValueError("Panel must contain at least one agent")

        # Check if all items are Agent instances
        if not all(isinstance(agent, Agent) for agent in panel_of_agents):
            raise TypeError("All panel members must be instances of Agent")

        # Convert list to dictionary for easier access
        self.panel_of_agents = {agent.name: agent for agent in panel_of_agents}

        # Check if leader exists in panel
        if leader not in self.panel_of_agents:
            raise ValueError(
                "Leader must be the name of one of the agents in the panel"
            )

        self.leader = leader
        self.moderator_cast_vote = moderator_cast_vote

        # Set peer information for each agent
        for agent in panel_of_agents:
            peer_info = {}
            for peer in panel_of_agents:
                if peer.name != agent.name:  # Don't include self
                    peer_info[peer.name] = peer.public_biograhpy
            agent.set_peer_information(peer_info)

        self.moderator_model = moderator_model

    def conduct_sync_vote(self, context: Context) -> Dict[str, int]:
        """
        Conducts a synchronous vote among all agents in the panel.

        Args:
            context (Context): The current context object containing the question and history

        Returns:
            Dict[str, int]: Dictionary mapping agent names to their vote scores
        """
        votes = {}

        # If only one agent, return max vote (100) by default
        if len(self.panel_of_agents) == 1:
            agent = list(self.panel_of_agents.values())[0]
            votes[agent.name] = 100
            return votes

        # Get votes from all agents
        for agent_name, agent in self.panel_of_agents.items():
            vote_result = agent.vote(context)
            if not isinstance(vote_result, AgentVote):
                vote_result = get_json_from_string(vote_result)
                vote_result = AgentVote(**vote_result)
            votes[agent_name] = vote_result.vote

        return votes

    async def conduct_async_vote(self, context: Context) -> Dict[str, int]:
        """
        Conducts an asynchronous vote among all agents in the panel.

        Args:
            context (Context): The current context object containing the question and history

        Returns:
            Dict[str, int]: Dictionary mapping agent names to their vote scores
        """
        votes = {}

        # If only one agent, return max vote (100) by default
        if len(self.panel_of_agents) == 1:
            agent = list(self.panel_of_agents.values())[0]
            votes[agent.name] = 100
            return votes

        # Create tasks for all agent votes
        async def get_agent_vote(agent_name: str, agent: Agent) -> tuple[str, int]:
            vote_result = await agent.avote(context)
            if not isinstance(vote_result, AgentVote):
                vote_result = get_json_from_string(vote_result)
                vote_result = AgentVote(**vote_result)
            vote = vote_result.vote
            return agent_name, vote

        tasks = [
            get_agent_vote(agent_name, agent)
            for agent_name, agent in self.panel_of_agents.items()
        ]

        # Wait for all votes to complete
        vote_results = await asyncio.gather(*tasks)
        votes = dict(vote_results)

        return votes

    def _format_voting_prompt(self, context: Context) -> ChatPromptTemplate:
        """
        Format the voting prompt with panel information and conversation history.

        Args:
            context (Context): The current context containing the conversation history

        Returns:
            ChatPromptTemplate: Formatted prompt template for voting
        """
        # Format panel information
        panel_info = []
        for agent_name, agent in self.panel_of_agents.items():
            panel_info.append(f"Agent: {agent_name}\n{agent.public_biograhpy}")
        formatted_panel_info = "\n\n".join(panel_info)

        formatted_history = format_conversation_history(context.conversation_history)

        return ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=self.moderator_voting_prompt.format(
                        panel_info=formatted_panel_info,
                        conversation_history=formatted_history,
                        question=context.current_question,
                    )
                ),
                ("user", "{question}"),
            ]
        )

    def cast_vote(self, context: Context) -> Dict[str, int]:
        """
        Cast votes for each panel member based on their capabilities.

        Args:
            context (Context): The current context containing the question

        Returns:
            Dict[str, int]: Dictionary mapping agent names to their vote scores
        """
        prompt = self._format_voting_prompt(context)

        # Use leader's model for voting with structured output
        leader_agent = (
            self.panel_of_agents[self.leader]
            if self.moderator_model is None
            else self.moderator_model
        )
        structured_model = leader_agent.model.with_structured_output(ModeratorVote)
        chain = prompt | structured_model

        try:
            response = leader_agent._invoke(chain, "CAST YOUR VOTE")
            # Convert ModeratorVote to dictionary of agent names to vote values
            return {vote.name: vote.vote for vote in response.votes}
        except (ValidationError, AttributeError, KeyError) as e:
            # Return 0 votes for all agents on error
            return {agent: 0 for agent in self.panel_of_agents}

    async def acast_vote(self, context: Context) -> Dict[str, int]:
        """
        Cast votes for each panel member based on their capabilities asynchronously.

        Args:
            context (Context): The current context containing the question

        Returns:
            Dict[str, int]: Dictionary mapping agent names to their vote scores
        """
        prompt = self._format_voting_prompt(context)

        # Use leader's model for voting with structured output
        leader_agent = (
            self.panel_of_agents[self.leader]
            if self.moderator_model is None
            else self.moderator_model
        )
        structured_model = leader_agent.model.with_structured_output(ModeratorVote)
        chain = prompt | structured_model

        try:
            response = await leader_agent._ainvoke(chain, "CAST YOUR VOTE")
            # Convert ModeratorVote to dictionary of agent names to vote values
            return {vote.name: vote.vote for vote in response.votes}
        except (ValidationError, AttributeError, KeyError) as e:
            # Return 0 votes for all agents on error
            return {agent: 0 for agent in self.panel_of_agents}

    def select_winner(self, votes: Dict[str, int]) -> str:
        """
        Selects the winning agent based on votes.

        Args:
            votes (Dict[str, int]): Dictionary mapping agent names to their vote scores

        Returns:
            str: Name of the winning agent
        """
        # If only one vote, return that agent
        if len(votes) == 1:
            return list(votes.keys())[0]

        # Get the maximum vote value
        max_vote = max(votes.values())

        # If all votes are 0, return the leader
        if max_vote == 0:
            return self.leader

        # Get all agents with the maximum vote
        max_voters = [name for name, vote in votes.items() if vote == max_vote]

        # If all votes are 100 and leader is among max voters, return leader
        if max_vote == 100 and self.leader in max_voters:
            return self.leader

        # If all votes are 100 and leader is not among max voters, return alphabetically first
        if max_vote == 100:
            return min(max_voters)

        # Return the agent with the highest vote
        return max(votes.items(), key=lambda x: x[1])[0]

    def switch_agent(self, agent_name: str) -> Agent:
        """
        Switches to a specified agent in the panel.

        Args:
            agent_name (str): Name of the agent to switch to

        Returns:
            Agent: The requested agent instance
        """
        return self.panel_of_agents[agent_name]

    def execute(self, context: Context) -> Generator[str, None, None]:
        """
        Execute the agent selection and decision process synchronously.

        Args:
            context (Context): The current context object

        Yields:
            str: Tokens from the selected agent's decision process
        """
        # Handle undirected queries
        if context.target_agent is None:
            votes = (
                self.cast_vote(context)
                if self.moderator_cast_vote
                else self.conduct_sync_vote(context)
            )
            winner = self.select_winner(votes)
            context.target_agent = winner

        finished = False

        while not finished:
            selected_agent = self.switch_agent(context.target_agent)
            # Check if max tries exceeded
            if context.decision_runs > selected_agent.max_tries:
                break

            # Stream tokens from agent's decision process
            for token in selected_agent.decide(context):
                yield token

            finished = context.conversation_turn_finished
            if finished:
                break

            # Execute action and update context
            selected_agent.call_action(context)

            # Handle agent passing

    async def aexecute(self, context: Context) -> AsyncGenerator[str, None]:
        """
        Execute the agent selection and decision process asynchronously.

        Args:
            context (Context): The current context object

        Yields:
            str: Tokens from the selected agent's decision process
        """
        # Handle undirected queries
        if context.target_agent is None:
            votes = await (
                self.acast_vote(context)
                if self.moderator_cast_vote
                else self.conduct_async_vote(context)
            )
            winner = self.select_winner(votes)
            context.target_agent = winner
            selected_agent = self.panel_of_agents[winner]
        else:
            # Handle directed queries
            selected_agent = self.switch_agent(context.target_agent)

        finished = False

        while not finished:
            # Check if max tries exceeded
            if context.decision_runs > selected_agent.max_tries:
                break

            # Stream tokens from agent's decision process
            async for token in selected_agent.adecide(context):
                yield token

            finished = context.conversation_turn_finished
            if finished:
                break

            # Execute action and update context
            await selected_agent.acall_action(context)
