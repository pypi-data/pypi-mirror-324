from typing import List, Generator
import logging

from .flag import Flag
from .context import Context
from .moderator import Moderator
from .types.flag import FlagState
from .utils import split_with_delimiter

logging.basicConfig(
    filename="transmitter.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.info("Transmitter initialized")

logger = logging.getLogger(__name__)


class Transmitter:
    def __init__(self, moderator: Moderator):
        self._thinking_out_loud = Flag()
        self._internal_reasoning = Flag()
        self._final_output = Flag()
        self._current_action_plan = Flag()
        self._moderator = moderator
        self.raw_feed = ""
        self.current_decision_run = 0

    def _close_all_flags_except(self, exception_flag: Flag = None):
        """
        Closes all flags except the specified flag.

        Args:
            exception_flag (Flag, optional): Flag to keep in its current state
        """
        flags = [
            self._thinking_out_loud,
            self._internal_reasoning,
            self._final_output,
            self._current_action_plan,
        ]

        for flag in flags:
            if flag is not exception_flag:
                flag.close()

    def accumulate(self, token: str, context: Context) -> str:
        if context.decision_runs > self.current_decision_run:
            # self.raw_feed += f"\n\n***** decision-run-{self.current_decision_run} END *****\n\n"
            self.current_decision_run = context.decision_runs
            self.raw_feed = ""
            context.clear_action_plan()

        # Normalize emoji variations
        token = token.replace("🛠️", "🛠")
        self.raw_feed += token

        logger.info(f"Accumulating token: {token}")

        tokens = split_with_delimiter(token)
        logger.info(f"Tokens: {tokens}")

        def _accumulate(processed_token: str, tokens: List[str]):
            if not tokens:
                return processed_token

            head = tokens[0]

            if "🚨" in head:
                self._close_all_flags_except(self._thinking_out_loud)
                self._thinking_out_loud.toggle()
                return _accumulate(processed_token, tokens[1:])
            elif "🤖" in head:
                self._close_all_flags_except(self._internal_reasoning)
                self._internal_reasoning.toggle()
                return _accumulate(processed_token, tokens[1:])
            elif "🛠" in head:
                self._close_all_flags_except(self._current_action_plan)
                self._current_action_plan.toggle()
                return _accumulate(processed_token, tokens[1:])
            elif "📢" in head:
                self._close_all_flags_except(self._final_output)
                self._final_output.toggle()
                if self._final_output.is_closed():
                    context.conversation_turn_finished = True
                return _accumulate(processed_token, tokens[1:])

            if self._thinking_out_loud.is_open():
                context.thinking_out_loud = head
                processed_token += head
                return _accumulate(processed_token, tokens[1:])
            elif self._internal_reasoning.is_open():
                context.internal_reasoning = head
                return _accumulate(processed_token, tokens[1:])
            elif self._current_action_plan.is_open():
                context.current_action_plan = head
                return _accumulate(processed_token, tokens[1:])
            elif self._final_output.is_open():
                context.final_output = head
                processed_token += head
                return _accumulate(processed_token, tokens[1:])
            else:
                return _accumulate(processed_token, tokens[1:])

        processed_token = _accumulate("", tokens)
        return processed_token

        # Handle opening and closing of thinking out loud
        # if "🚨" in token:
        #     token = token.replace("🚨", "")
        #     if not (token and self._thinking_out_loud.is_open()):
        #         self._close_all_flags_except(self._thinking_out_loud)
        #         self._thinking_out_loud.toggle()

        # # Handle opening and closing of internal reasoning
        # if "🤖" in token:
        #     token = token.replace("🤖", "")
        #     if not (token and self._internal_reasoning.is_open()):
        #         self._close_all_flags_except(self._internal_reasoning)
        #         self._internal_reasoning.toggle()

        # # Handle opening and closing of current action plan
        # if "🛠" in token:
        #     token = token.replace("🛠", "").strip()
        #     if not (token and self._current_action_plan.is_open()):
        #         self._close_all_flags_except(self._current_action_plan)
        #         self._current_action_plan.toggle()
        #     # if token:
        #     #     context.current_action_plan = token

        # # Handle opening and closing of final output
        # if "📢" in token:
        #     token = token.replace("📢", "").strip()
        #     self._close_all_flags_except(self._final_output)
        #     self._final_output.toggle()
        #     if self._final_output.is_closed():
        #         context.conversation_turn_finished = True
        #         # self.raw_feed += f"\n\n***** decision-run-{context.decision_runs} END *****\n\n"

        # # Accumulate tokens based on which flag is open
        # if self._thinking_out_loud.is_open():
        #     context.thinking_out_loud = token
        #     return token
        # elif self._internal_reasoning.is_open():
        #     context.internal_reasoning = token
        #     return None
        # elif self._current_action_plan.is_open():
        #     context.current_action_plan = token
        #     return None
        # elif self._final_output.is_open():
        #     context.final_output = token
        #     return token

        # return token

    def clear(self):
        """
        Clears all flags and raw feed to prepare for a new conversation turn.
        """
        self._thinking_out_loud.close()
        self._internal_reasoning.close()
        self._final_output.close()
        self._current_action_plan.close()
        self.raw_feed = ""

    async def ainvoke_moderator(self, context: Context, stream: bool = False):
        """
        Asynchronously invoke the moderator's execution process.

        Args:
            context (Context): The current context object
            stream (bool): Whether to stream the tokens or return final output

        Yields:
            If stream=True: Processed tokens from the moderator's execution
        Returns:
            If stream=False: The final output once conversation is finished
        """
        self.clear()  # Clear state at start of new invocation
        if stream:
            async for token in self._moderator.aexecute(context):
                processed_token = self.accumulate(token, context)
                if processed_token:
                    yield processed_token
        else:
            async for token in self._moderator.aexecute(context):
                self.accumulate(token, context)
            if context.conversation_turn_finished:
                yield context.final_output

    def invoke_moderator(self, context: Context, stream: bool = False):
        """
        Synchronously invoke the moderator's execution process.

        Args:
            context (Context): The current context object
            stream (bool): Whether to stream the tokens or return final output

        Yields:
            If stream=True: Processed tokens from the moderator's execution
        Returns:
            If stream=False: The final output once conversation is finished
        """
        self.clear()  # Clear state at start of new invocation
        if stream:
            for token in self._moderator.execute(context):
                processed_token = self.accumulate(token, context)
                if processed_token:
                    yield processed_token
        else:
            for token in self._moderator.execute(context):
                self.accumulate(token, context)
            if context.conversation_turn_finished:
                yield context.final_output
