from umlcharter.generators.base import IChartGenerator
from umlcharter.generators.sequencediagramorg.sequence_diagram import (
    SequenceDiagramOrgSequenceDiagram,
)


class SequenceDiagramOrg(IChartGenerator):
    def generate_sequence_diagram(self) -> str:
        return SequenceDiagramOrgSequenceDiagram.generate(self.ref)  # noqa

    def generate_graph_diagram(self) -> str:
        raise NotImplementedError(
            "This generator does not have a graph diagram support"
        )  # pragma: nocover
