from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.graphviz.graph_diagram import GraphvizGraphDiagram


class Graphviz(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        raise NotImplementedError(
            "This generator does not have a sequence diagram support"
        )  # pragma: nocover

    def generate_graph_diagram(self) -> str:
        return GraphvizGraphDiagram.generate(self.ref)  # noqa
