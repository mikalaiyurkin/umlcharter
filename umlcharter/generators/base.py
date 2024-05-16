from abc import ABC

from umlcharter.charts.types import BaseChart


class IChartGenerator(ABC):
    """
    Abstract parent class for the generators. Define the interfaces.
    """

    ref: BaseChart

    def __init__(self, ref: BaseChart):
        self.ref = ref

    def generate_sequence_diagram(self) -> str:
        raise NotImplementedError  # pragma: nocover
