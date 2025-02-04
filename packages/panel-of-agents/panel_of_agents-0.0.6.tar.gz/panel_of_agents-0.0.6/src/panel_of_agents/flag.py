from .types.flag import FlagState


class Flag:
    def __init__(self):
        self._state = FlagState.UNDEFINED

    @property
    def state(self) -> FlagState:
        return self._state

    @state.setter
    def state(self, value: FlagState):
        if not isinstance(value, FlagState):
            raise TypeError("State must be a FlagState enum value")
        self._state = value

    def toggle(self):
        """
        Toggles the flag state according to the following rules:
        - UNDEFINED -> OPEN
        - OPEN -> CLOSED
        - CLOSED -> OPEN
        """
        if self._state == FlagState.UNDEFINED:
            self._state = FlagState.OPEN
        elif self._state == FlagState.OPEN:
            self._state = FlagState.CLOSED
        else:  # CLOSED
            self._state = FlagState.OPEN

    def close(self):
        """
        Explicitly sets the flag state to CLOSED regardless of current state.
        """
        self._state = FlagState.CLOSED

    def is_open(self) -> bool:
        return self._state == FlagState.OPEN

    def is_closed(self) -> bool:
        return self._state == FlagState.CLOSED
