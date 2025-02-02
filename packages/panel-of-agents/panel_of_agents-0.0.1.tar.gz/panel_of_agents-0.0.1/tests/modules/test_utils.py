import pytest
from langchain_core.messages import HumanMessage, AIMessage
from src.panel_of_agents.utils import get_json_from_string, format_conversation_history, split_with_delimiter


class TestGetJsonFromString:
    def test_valid_json(self):
        # Arrange
        text = 'some text {"key": "value"} more text'

        # Act
        result = get_json_from_string(text)

        # Assert
        assert result == {"key": "value"}

    def test_invalid_json(self):
        # Arrange
        text = 'some text {invalid json} more text'

        # Act
        result = get_json_from_string(text)

        # Assert
        assert result == {}

    def test_no_json(self):
        # Arrange
        text = 'just some regular text'

        # Act
        result = get_json_from_string(text)

        # Assert
        assert result == {}

    def test_nested_json(self):
        # Arrange
        text = 'prefix {"outer": {"inner": "value"}} suffix'

        # Act
        result = get_json_from_string(text)

        # Assert
        assert result == {"outer": {"inner": "value"}}


class TestFormatConversationHistory:
    def test_empty_history(self):
        # Arrange
        messages = []

        # Act
        result = format_conversation_history(messages)

        # Assert
        assert result == "No conversation history"

    def test_single_exchange(self):
        # Arrange
        messages = [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there")
        ]

        # Act
        result = format_conversation_history(messages)

        # Assert
        assert result == "Human: Hello\n\nAssistant: Hi there"

    def test_multiple_exchanges(self):
        # Arrange
        messages = [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there"),
            HumanMessage(content="How are you?"),
            AIMessage(content="I'm doing well!")
        ]

        # Act
        result = format_conversation_history(messages)

        # Assert
        expected = (
            "Human: Hello\n\n"
            "Assistant: Hi there\n\n"
            "Human: How are you?\n\n"
            "Assistant: I'm doing well!"
        )
        assert result == expected


def test_split_with_delimiter():
    # Basic splitting with space
    assert split_with_delimiter("Hello World") == ["Hello ", "World"]

    # Custom delimiter
    assert split_with_delimiter("a,b,c", ",") == ["a,", "b,", "c"]

    # No delimiter in text
    assert split_with_delimiter("Hello") == ["Hello"]

    # Empty string
    assert split_with_delimiter("") == []

    # Multiple consecutive delimiters
    assert split_with_delimiter("Hello  World", " ") == [
        "Hello ", " ", "World"]

    # Delimiter at the end
    assert split_with_delimiter("Hello ", " ") == ["Hello "]

    # Single character delimiter and text
    assert split_with_delimiter("a", " ") == ["a"]

    # Different delimiter
    assert split_with_delimiter("test;string;here", ";") == [
        "test;", "string;", "here"]
