import json
from typing import List, Dict, Any, Union
from langchain_core.messages import HumanMessage, AIMessage


def get_json_from_string(text: str) -> Dict[str, Any]:
    """
    Extracts JSON from a string, handling potential formatting issues.

    Args:
        text (str): String containing JSON data

    Returns:
        Dict[str, Any]: Parsed JSON data or empty dict if parsing fails
    """
    try:
        # Find the first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            return {}

        # Extract and parse the JSON
        json_str = text[start : end + 1]
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return {}


def format_conversation_history(messages: List[Union[HumanMessage, AIMessage]]) -> str:
    """
    Formats conversation history into a simple string format.

    Args:
        messages (List[Union[HumanMessage, AIMessage]]): List of conversation messages

    Returns:
        str: Formatted conversation history
    """
    if not messages:
        return "No conversation history"

    formatted = []
    for msg in messages:
        prefix = "Human: " if isinstance(msg, HumanMessage) else "Assistant: "
        formatted.append(f"{prefix}{msg.content}")

    return "\n\n".join(formatted)


def split_with_delimiter(text: str, delimiter: str = " ") -> List[str]:
    """
    Splits a string into segments, keeping the delimiter at the end of each segment.
    Similar to str.split() but preserves the delimiter.

    Args:
        text (str): The text to split
        delimiter (str): The character to split on (defaults to space)

    Returns:
        List[str]: List of segments, each ending with the delimiter (except possibly the last)

    Examples:
        >>> split_with_delimiter("Hello World")
        ['Hello ', 'World']
        >>> split_with_delimiter("a,b,c", ",")
        ['a,', 'b,', 'c']
        >>> split_with_delimiter("Hello")
        ['Hello']
        >>> split_with_delimiter("Hello  World", " ")
        ['Hello ', ' ', 'World']
    """
    if not text:
        return []

    segments = []
    current_segment = ""
    for char in text:
        current_segment += char
        if char == delimiter or char == "\n":
            segments.append(current_segment)
            current_segment = ""
    if current_segment:  # Add any remaining text
        segments.append(current_segment)
    return segments
