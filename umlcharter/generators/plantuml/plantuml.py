from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.plantuml.sequence_diagram import PlantUMLSequenceDiagram


class PlantUML(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return PlantUMLSequenceDiagram.generate(self.ref)  # noqa
