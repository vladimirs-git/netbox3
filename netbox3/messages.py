"""Messages. Processing info/warning/error messages."""

from __future__ import annotations

import logging
from typing import List, Union

from vhelpers import vstr


class Msg:
    """Message."""

    def __init__(self, level: str, name: str, text: str):
        """Init Message.

        :param level: "example", "info", "warning", "error".
        :param name: Header.
        :param text: Body.
        """
        self.level = level
        self.name = name
        self.text = text

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.line()}>"

    def line(self) -> str:
        """Return line of message, ready for print."""
        line = f"{self.level.upper()}: "
        line += f": {self.name}: " if self.name else ""
        line += f"{self.text}"
        return line


class Messages:
    """Messages. Processing info/warning/error messages."""

    def __init__(self, name: str = ""):
        """Init Messages.

        :param name: Default header for all messages.
        """
        self.name = str(name)
        self.items: List[Msg] = []

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        params = vstr.repr_params(
            msgs=len(self.items),
            info=len([o for o in self.items if o.level == "info"]),
            warning=len([o for o in self.items if o.level == "warning"]),
            error=len([o for o in self.items if o.level == "error"]),
        )
        return f"<{name}: {params}>"

    def clear(self) -> None:
        """Delete all messages."""
        self.items = []

    def add(self, level: str, name: str, text: str) -> None:
        """Add message to messages."""
        message = Msg(level=level, name=name, text=text)
        self.items.append(message)

    def info(self, text: str) -> None:
        """Add INFO to messages."""
        message = Msg(level="info", name=self.name, text=text)
        self.items.append(message)

    def warning(self, text: str) -> None:
        """Add WARNING to messages."""
        message = Msg(level="warning", name=self.name, text=text)
        self.items.append(message)

    def error(self, text: str) -> None:
        """Add ERROR to messages."""
        message = Msg(level="error", name=self.name, text=text)
        self.items.append(message)

    def update(self, msgs: Union[Messages, List[Messages]]) -> None:
        """Extend other Messages data to self.messages."""
        msgs = msgs if isinstance(msgs, list) else [msgs]
        for msg in msgs:
            for msg_ in msg.items:
                if msg_ not in self.items:
                    self.items.append(msg_)

    def is_warnings(self) -> bool:
        """Return True if in messages has error or warning."""
        if [o for o in self.items if o.level in ["error", "warning"]]:
            return True
        return False

    def is_error(self) -> bool:
        """Return True if in messages has error."""
        if [o for o in self.items if o.level in ["error"]]:
            return True
        return False

    def count(self) -> int:
        """Return count of messages."""
        return len(self.items)

    def logging(self) -> None:
        """Log all messages."""
        for msg in self.items:
            line = f"{msg.name}: " if msg.name else ""
            line += f"{msg.text}"
            try:
                logger_o = getattr(logging, msg.level)
            except AttributeError:
                logger_o = getattr(logging, "warning")
                line = f"{msg.level.upper()}: {line}"
            logger_o(line)

    def line(self) -> str:
        """Return all messages as string."""
        return "; ".join([o.line() for o in self.items])

    def print(self) -> None:
        """Print all messages."""
        for msg in self.items:
            print(msg.line())
