from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.plantuml.sequence_diagram import PlantUMLSequenceDiagram
from umlcharter.generators.plantuml.graph_diagram import PlantUMLGraphDiagram


class PlantUML(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return PlantUMLSequenceDiagram.generate(self.ref)  # noqa

    def generate_graph_diagram(self) -> str:
        return PlantUMLGraphDiagram.generate(self.ref)  # noqa
