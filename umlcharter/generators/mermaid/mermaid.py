from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.mermaid.sequence_diagram import MermaidSequenceDiagram


class Mermaid(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return MermaidSequenceDiagram.generate(self.ref)  # noqa
