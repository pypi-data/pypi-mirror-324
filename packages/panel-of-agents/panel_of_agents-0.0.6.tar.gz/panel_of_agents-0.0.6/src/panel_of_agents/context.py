import json
from typing import List, Union, Dict, Any
from collections import OrderedDict

from pydantic import ValidationError
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from .types.context import (
    Artifact,
    Action,
    ConversationTurnIndex,
    DecisionRunIndex,
    ActionPlan,
    CustomProp,
)


class Context:

    def __init__(
        self,
        current_question: Union[str, None],
        conversation_history: List[Union[HumanMessage, AIMessage]],
        artifacts: OrderedDict[ConversationTurnIndex, Artifact],
        target_agent: Union[str, None] = None,
        custom_props: Dict[str, List[CustomProp]] = {},
    ):
        if not isinstance(custom_props, dict):
            raise TypeError("custom_props must be a dictionary")

        for props in custom_props.values():
            if not all(isinstance(prop, CustomProp) for prop in props):
                raise TypeError(
                    "All items in custom_props must be instances of CustomProp"
                )

        self.current_question = current_question
        self._original_question = current_question
        self.conversation_history = conversation_history
        self.artifacts = artifacts
        if not isinstance(target_agent, (str, type(None))):
            raise TypeError("target_agent must be a string or None")
        self.target_agent = target_agent
        self._current_action_plan: str = ""
        self._previous_actions: Dict[DecisionRunIndex, Action] = {}
        self._decision_runs = 0
        self._thinking_out_loud: str = ""
        self._internal_reasoning: str = ""
        self._final_output: str = ""
        self._conversation_turn_finished = False
        self._custom_props: Dict[str, List[CustomProp]] = custom_props

    @property
    def current_question(self) -> str:
        return self._current_question

    @current_question.setter
    def current_question(self, value: str):
        if not isinstance(value, str):
            raise TypeError("current_question must be a string")

        if value == "":
            self._current_question = "Hey, I accidentally clicked enter without writing any message, please ignore."
        else:
            # word_count = len(value.split())
            # if word_count > 1000:
            #     raise ValueError(
            #         "current_question must be less than 1000 words")
            self._current_question = value

    @property
    def conversation_history(self) -> List[Union[HumanMessage, AIMessage]]:
        return self._conversation_history

    @conversation_history.setter
    def conversation_history(self, value: List[Union[HumanMessage, AIMessage]]):
        if not isinstance(value, list):
            raise TypeError("conversation_history must be a list")

        len_items = len(value)
        assert all(
            isinstance(x, (HumanMessage, AIMessage)) for x in value
        ), "conversation_history must be a list of HumanMessage or AIMessage"
        if len_items == 1:
            raise ValueError(
                "conversation_history must have at least 2 messages, if not empty"
            )

        if len_items % 2 != 0:
            raise ValueError(
                "conversation_history must have an even number of messages"
            )

        even_indices = range(0, len_items, 2)
        odd_indices = range(1, len_items, 2)

        assert all(
            isinstance(value[i], HumanMessage) for i in even_indices
        ), "conversation_history must have HumanMessage at even indices"
        assert all(
            isinstance(value[i], AIMessage) for i in odd_indices
        ), "conversation_history must have AIMessage at odd indices"

        if len_items > 25 * 2:
            # get the last 25x2 messages
            value = value[-25 * 2 :]
        self._conversation_history = value

    @property
    def artifacts(self) -> OrderedDict[ConversationTurnIndex, Artifact]:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, value: Dict[ConversationTurnIndex, Artifact]):
        if not isinstance(value, (dict, OrderedDict)):
            raise TypeError("artifacts must be a dict")

        artifact_length = len(value)
        if artifact_length == 0:
            self._artifacts = OrderedDict()
            return

        assert (
            artifact_length <= len(self.conversation_history) / 2
        ), "There must only be as many artifacts as there are conversation turns"

        ordered_artifacts = OrderedDict()
        for key, content in value.items():
            if not isinstance(key, ConversationTurnIndex):
                raise TypeError("Keys of artifacts must be ConversationTurnIndex")
            if not isinstance(content, Artifact):
                raise TypeError("contents of artifacts must be of type Artifact")

            if key.index_id >= len(self.conversation_history) / 2:
                raise AssertionError(
                    "The index_id of the artifact can not exceed or match the number of conversation turns"
                )
            ordered_artifacts[key] = content

        self._artifacts = ordered_artifacts

    def update_artifacts(self, artifact: Artifact):
        """
        Updates artifacts within a decision run.
        """

        if not isinstance(artifact, Artifact):
            raise TypeError("artifact must be of type Artifact")
        if not artifact:
            return

        # if len(self.conversation_history) == 0:
        #     raise AssertionError(
        #         "Can not add an artifact without a conversation turn")

        # if len(self.artifacts) >= len(self.conversation_history) / 2:
        #     raise AssertionError(
        #         "Can not add more artifacts than conversation turns")

        index = DecisionRunIndex(len(self.artifacts))
        self.artifacts[index] = artifact

    def get_json(self, output):

        start_index = output.find("{")
        end_index = output.rfind("}") + 1
        payload = output[start_index:end_index]
        payload = payload.replace("\n", "")
        payload = payload.replace("\r", "")
        payload = payload.replace("\t", "")
        try:
            json_output = json.loads(payload)
        except json.JSONDecodeError as e:
            print("Error decoding JSON: ", payload, e)
            return {}

        return json_output

    @property
    def current_action_plan(self) -> str:

        return self._current_action_plan

    def get_json_action_plan(self) -> ActionPlan:
        try:
            json_string = self._current_action_plan
            start_index = json_string.find("{")
            end_index = json_string.rfind("}") + 1
            json_string = json_string[start_index:end_index]
            json_string = json_string.replace("\n", "")
            json_string = json_string.replace("\r", "")
            json_string = json_string.replace("\t", "")
            json_string = json_string.strip()
            json_data = json.loads(json_string)

            return ActionPlan(**json_data)

        except json.JSONDecodeError:
            print("Error decoding JSON: ", self._current_action_plan)
            raise AttributeError("current_action_plan is not JSON serializable")
        except (KeyError, TypeError, ValidationError) as e:
            raise KeyError(f"Invalid action plan structure: {str(e)}")
        except Exception as e:
            raise AttributeError(f"Unexpected error creating action plan: {str(e)}")

    @current_action_plan.setter
    def current_action_plan(self, value: str):
        if not isinstance(value, str):
            raise TypeError("current_action_plan must be a string")

        self._current_action_plan += value

    @current_action_plan.deleter
    def current_action_plan(self):
        self._current_action_plan = ""

    @property
    def decision_runs(self) -> int:
        return self._decision_runs

    def increment_decision_runs(self):
        self._decision_runs += 1

    @property
    def previous_actions(self) -> Dict[DecisionRunIndex, Action]:
        return self._previous_actions

    def update_previous_actions(self, author: str, output: Union[dict, None]):
        if not isinstance(author, str):
            raise TypeError("author must be a string")

        action_plan_index = len(self.previous_actions)
        index = DecisionRunIndex(action_plan_index)
        try:
            current_action_plan = self.get_json_action_plan()
        except Exception:
            current_action_plan = ActionPlan(tool_name="", tool_input={})

        tool_name = current_action_plan.tool_name
        tool_input = current_action_plan.tool_input

        if output is None:
            output = {
                "status": "error",
            }

        action = Action(author, tool_name, tool_input, output)
        # clear the current action plan
        del self.current_action_plan

        self.previous_actions[index] = action
        self.increment_decision_runs()

    def clear_action_plan(self):
        del self.current_action_plan

    @property
    def thinking_out_loud(self) -> str:
        return self._thinking_out_loud

    @thinking_out_loud.setter
    def thinking_out_loud(self, value: str):
        if not isinstance(value, str):
            raise TypeError("thinking_out_loud must be a string")
        self._thinking_out_loud += value

    @thinking_out_loud.deleter
    def thinking_out_loud(self):
        self._thinking_out_loud = ""

    @property
    def internal_reasoning(self) -> str:
        return self._internal_reasoning

    @internal_reasoning.setter
    def internal_reasoning(self, value: str):
        if not isinstance(value, str):
            raise TypeError("internal_reasoning must be a string")
        self._internal_reasoning += value

    @internal_reasoning.deleter
    def internal_reasoning(self):
        self._internal_reasoning = ""

    @property
    def final_output(self) -> str:
        return self._final_output

    @final_output.setter
    def final_output(self, value: str):
        if not isinstance(value, str):
            raise TypeError("final_output must be a string")
        self._final_output += value

    @final_output.deleter
    def final_output(self):
        self._final_output = ""

    @property
    def conversation_turn_finished(self) -> bool:
        return self._conversation_turn_finished

    @conversation_turn_finished.setter
    def conversation_turn_finished(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("conversation_turn_finished must be a bool")
        self._conversation_turn_finished = value

    @conversation_turn_finished.deleter
    def conversation_turn_finished(self):
        self._conversation_turn_finished = False

    @property
    def custom_props(self) -> List[CustomProp]:
        return self._custom_props

    @custom_props.setter
    def custom_props(self, value: List[CustomProp]):
        if not isinstance(value, list):
            raise TypeError("custom_props must be a list")
        self._custom_props = value

    def format_custom_props(self, agent_name: str) -> str:
        """Format custom props for the specified agent with name, description and value."""
        if not self._custom_props or agent_name not in self._custom_props:
            return "No custom properties have been set"

        props = self._custom_props[agent_name]
        if not props:
            return "No custom properties have been set"

        formatted_props = []
        for i, prop in enumerate(props, 1):
            formatted_props.append(
                f"{i}. {prop.name}\n"
                f"   Description: {prop.description}\n"
                f"   Value: {prop.value}"
            )

        return "\n".join(formatted_props)

    def format_previous_actions(self) -> str:
        """Returns formatted string of previous actions"""
        if not self._previous_actions:
            return "No previous tool calls"

        formatted = []
        for index, action in self._previous_actions.items():
            formatted.append(
                f"Decision Run {index.index_id}:\n"
                f"- Author: {action.author}\n"
                f"- Tool: {action.action_name}\n"
                f"- Input: {json.dumps(action.action_input, indent=2)}\n"
                f"- Result: {json.dumps(action.action_output, indent=2)}"
            )
        return "\n\n".join(formatted)

    def format_artifacts(self) -> str:
        """Returns formatted string of all artifacts"""
        if not self._artifacts:
            return "No artifacts available"

        formatted = []
        for key, artifact in self._artifacts.items():
            formatted.append(
                f"{key}:\n"
                f"Author: {artifact.author}\n"
                f"Data: {json.dumps(artifact.data, indent=2)}"
            )
        return "\n\n".join(formatted)

    def get_most_recent_action(self) -> Action:
        if not self._previous_actions:
            return None
        return list(self._previous_actions.values())[-1]

    def format_action(self, action: Action) -> str:
        return f"Author: {action.author} | Tool: {action.action_name} | Input: {json.dumps(action.action_input, indent=2)} | Result: {json.dumps(action.action_output, indent=2)}"
