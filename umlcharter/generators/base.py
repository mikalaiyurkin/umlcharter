from abc import ABC

from umlcharter.charts.common import BaseChart


class IChartGenerator(ABC):
    """
    Abstract parent class for the generators. Defines the interfaces.
    """

    ref: BaseChart

    def __init__(self, ref: BaseChart):
        self.ref = ref

    def generate_sequence_diagram(self) -> str:
        raise NotImplementedError  # pragma: nocover

    def generate_graph_diagram(self) -> str:
        raise NotImplementedError  # pragma: nocover
