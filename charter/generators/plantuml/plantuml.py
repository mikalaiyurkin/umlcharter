from charter.generators.base import IChartGenerator


class PlantUML(IChartGenerator):

    def generate_sequence_diagram(self) -> str:
        raise NotImplementedError("TODO")
