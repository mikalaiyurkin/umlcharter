from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.d2.sequence_diagram import D2SequenceDiagram


class D2(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return D2SequenceDiagram.generate(self.ref)  # noqa

    def generate_graph_diagram(self) -> str:
        raise NotImplementedError(
            "This generator does not have a graph diagram support"
        )  # pragma: nocover
