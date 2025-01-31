import json
from dataclasses import dataclass
from typing import Any, Union

from ..lib import Result
from .errors import Error, ErrorKind


@dataclass
class Arg:
    """Class representing a typed argument with its associated value.

    Attributes:
        type (int): The argument type
        value (Any): The argument value

    Examples:
        >>> text_arg = Arg(Arg.TEXT, "Hello")
        >>> int_arg = Arg(Arg.INT, 42)
        >>> bool_arg = Arg(Arg.BOOL, True)
        >>> vec_arg = Arg(Arg.VEC_TEXT, ["a", "b", "c"])
        >>> opt_text_arg = Arg(Arg.OPT_TEXT, "optional")
        >>> opt_value_arg = Arg(Arg.OPT_VALUE, {"key": "value"})
    """

    type: int
    value: Any

    # Supported argument types
    TEXT = 1  # For strings
    INT = 2  # For integers
    BOOL = 3  # For booleans
    VEC_TEXT = 4  # For string lists
    OPT_TEXT = 5  # For optional strings
    OPT_VALUE = 6  # For optional complex values (dict/list)

    def __init__(self, arg_type: int, value: Any = None):
        """Initialize a new argument with its type and value.

        Args:
            arg_type (int): The argument type
            value (Any, optional): The argument value. Defaults to None.

        Examples:
            >>> text_arg = Arg(Arg.TEXT, "Hello")
            >>> int_arg = Arg(Arg.INT, 42)
        """
        self.type = arg_type
        self.value = value

    @classmethod
    def from_str(cls, s: str) -> "Arg":
        """Create an argument from a string by automatically determining its type.

        Args:
            s (str): The string to convert

        Returns:
            Arg: A new Arg instance

        Examples:
            >>> Arg.from_str("42")        # Arg(INT, 42)
            >>> Arg.from_str("0xFF")      # Arg(INT, 255)
            >>> Arg.from_str("true")      # Arg(BOOL, True)
            >>> Arg.from_str("hello")     # Arg(TEXT, "hello")
        """
        if s.startswith("0x"):
            return cls(cls.INT, int(s, 16))

        try:
            if int(s):
                return cls(cls.INT, int(s))
        except ValueError:
            pass

        if s == "true":
            return cls(cls.BOOL, True)
        elif s == "false":
            return cls(cls.BOOL, False)

        return cls(cls.TEXT, s)

    def to_string(self) -> Result[str, Error]:
        """Convert the argument to a string.

        Returns:
            str: String representation of the argument

        Examples:
            >>> Arg(Arg.TEXT, "hello").to_string()           # "hello"
            >>> Arg(Arg.INT, 42).to_string()                 # "42"
            >>> Arg(Arg.BOOL, True).to_string()              # "true"
            >>> Arg(Arg.VEC_TEXT, ["a","b"]).to_string()     # "a,b"
            >>> Arg(Arg.OPT_VALUE, {"x":1}).to_string()      # '{"x":1}'
        """
        if self.type == self.TEXT:
            return Result.Ok(self.value)

        if self.type == self.INT:
            return Result.Ok(str(self.value))

        if self.type == self.BOOL:
            return Result.Ok("true" if self.value else "false")

        if self.type == self.VEC_TEXT:
            return Result.Ok(",".join(self.value))

        if self.type == self.OPT_TEXT:
            return Result.Ok(self.value if self.value else "")

        if self.type == self.OPT_VALUE:
            return Result.Ok(json.dumps(self.value))

        return Result.Err(
            Error(0, ErrorKind.BAD_REQUEST, f"Invalid argument type: {self.type}")
        )

    def to_int(self) -> Result[int, Error]:
        """Convert the argument to an integer if its type is INT.

        Returns:
            int: The integer value

        Raises:
            ValueError: If the type is not INT

        Example:
            >>> Arg(Arg.INT, 42).to_int()  # 42
        """
        if self.type == self.INT:
            return Result.Ok(self.value)

        return Result.Err(
            Error(0, ErrorKind.BAD_REQUEST, f"Invalid argument type: {self.type}")
        )

    def to_bool(self) -> Result[bool, Error]:
        """Convert the argument to a boolean if its type is BOOL.

        Returns:
            bool: The boolean value

        Raises:
            ValueError: If the type is not BOOL

        Example:
            >>> Arg(Arg.BOOL, True).to_bool()  # True
        """
        if self.type == self.BOOL:
            return Result.Ok(self.value)

        return Result.Err(
            Error(0, ErrorKind.BAD_REQUEST, f"Invalid argument type: {self.type}")
        )

    def to_vec_text(self) -> Result[list[str], Error]:
        """Convert the argument to a list of strings if its type is VEC_TEXT.

        Returns:
            list[str]: The list of strings

        Raises:
            ValueError: If the type is not VEC_TEXT

        Example:
            >>> Arg(Arg.VEC_TEXT, ["a", "b"]).to_vec_text()  # ["a", "b"]
        """
        if self.type == self.VEC_TEXT:
            return Result.Ok(self.value)

        return Result.Err(
            Error(0, ErrorKind.BAD_REQUEST, f"Invalid argument type: {self.type}")
        )

    def to_opt_text(self) -> Result[str, Error]:
        """Convert the argument to an optional string if its type is OPT_TEXT.

        Returns:
            str | None: The string or None

        Raises:
            ValueError: If the type is not OPT_TEXT

        Examples:
            >>> Arg(Arg.OPT_TEXT, "hello").to_opt_text()  # "hello"
            >>> Arg(Arg.OPT_TEXT, None).to_opt_text()     # None
        """
        if self.type == self.OPT_TEXT:
            return Result.Ok(self.value)

        return Result.Err(
            Error(0, ErrorKind.BAD_REQUEST, f"Invalid argument type: {self.type}")
        )

    def to_opt_value(self) -> Result[Union[dict, list], Error]:
        """Convert the argument to an optional complex value if its type is OPT_VALUE.

        Returns:
            Union[dict, list, None]: The complex value or None

        Raises:
            ValueError: If the type is not OPT_VALUE

        Examples:
            >>> Arg(Arg.OPT_VALUE, {"x": 1}).to_opt_value()  # {"x": 1}
            >>> Arg(Arg.OPT_VALUE, [1, 2]).to_opt_value()    # [1, 2]
            >>> Arg(Arg.OPT_VALUE, None).to_opt_value()      # None
        """
        if self.type == self.OPT_VALUE:
            return Result.Ok(self.value)

        return Result.Err(
            Error(0, ErrorKind.BAD_REQUEST, f"Invalid argument type: {self.type}")
        )
