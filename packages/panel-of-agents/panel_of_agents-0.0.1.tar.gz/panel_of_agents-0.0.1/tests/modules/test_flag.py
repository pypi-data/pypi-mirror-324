import pytest

from src.panel_of_agents.flag import Flag
from src.panel_of_agents.types.flag import FlagState


def test_flag_initialization():
    flag = Flag()
    assert flag.state == FlagState.UNDEFINED


def test_flag_undefined_to_open():
    # Arrange
    flag = Flag()
    assert flag.state == FlagState.UNDEFINED

    # Act
    flag.toggle()

    # Assert
    assert flag.state == FlagState.OPEN


def test_flag_open_to_close():
    # Arrange
    flag = Flag()
    flag.state = FlagState.OPEN

    # Act
    flag.toggle()

    # Assert
    assert flag.state == FlagState.CLOSED


def test_flag_close_to_open():
    # Arrange
    flag = Flag()
    flag.state = FlagState.CLOSED

    # Act
    flag.toggle()

    # Assert
    assert flag.state == FlagState.OPEN


def test_flag_explicit_close():
    # Arrange
    flag = Flag()
    flag.state = FlagState.OPEN

    # Act
    flag.close()

    # Assert
    assert flag.state == FlagState.CLOSED
    assert flag.is_closed()
