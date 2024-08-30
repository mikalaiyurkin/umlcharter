from dataclasses import dataclass


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
                raise ValueError
        except ValueError:
            raise AssertionError(
                "Color must be strictly a 6-character hex string. "
                f"The value '{self.color}' is not a such."
            )

    def as_hex(self) -> str:
        return f"#{self.color}"


class BaseChart:
    """
    Base class for all the charts
    """
