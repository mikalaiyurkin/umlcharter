from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.mermaid.sequence_diagram import MermaidSequenceDiagram
from umlcharter.generators.mermaid.graph_diagram import MermaidGraphDiagram


class Mermaid(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return MermaidSequenceDiagram.generate(self.ref)  # noqa

    def generate_graph_diagram(self) -> str:
        return MermaidGraphDiagram.generate(self.ref)  # noqa
