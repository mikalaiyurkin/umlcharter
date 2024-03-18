from charter.generators.base import IChartGenerator


class ZenUML(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        raise NotImplementedError("TODO")
