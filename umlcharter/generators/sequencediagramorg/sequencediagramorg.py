from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.sequencediagramorg.sequence_diagram import (
    SequenceDiagramOrgSequenceDiagram,
)


class SequenceDiagramOrg(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return SequenceDiagramOrgSequenceDiagram.generate(self.ref)  # noqa
