import typing
from dataclasses import dataclass, field


class ChartingException(Exception):
    pass


@dataclass
class Color:
    color: str

    def __post_init__(self):
        """
        Color must be strictly a 6-character hex string
        """
        try:
            if not (
                len(self.color) == 6 and int(self.color, 16) > 0
            ):  # it is fine without regular expr
                raise AssertionError
        except AssertionError:
            raise ChartingException(
                "Color must be strictly a 6-character hex string. "
                f"The value '{self.color}' is not a such."
            )

    def as_hex(self) -> str:
        return f"#{self.color}"


@dataclass
class Colored:
    """
    Used to assign the color to the component of the diagram.
    """

    _color: typing.Optional[str]
    color: typing.Optional[Color] = field(init=False)

    def __post_init__(self):
        self.color = Color(self._color) if self._color else None


class BaseChart:
    """
    Base class for all the charts
    """
