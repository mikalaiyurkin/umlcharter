import typing
from dataclasses import dataclass, field

from umlcharter.charts.types import BaseChart, Colored, ChartingException
from umlcharter.generators.base import IChartGenerator


class BaseNode:
    graph_ref: typing.Optional["GraphNodeGroup"]

    def __init__(self, graph_ref: typing.Optional["GraphNodeGroup"]):
        self.graph_ref = graph_ref

    def __hash__(self):
        return hash(id(self))

    def __graph_belongs_to(self) -> typing.Dict["BaseNode", typing.List[typing.Tuple["BaseNode", str]]]:
        return self.graph_ref._GraphNodeGroup__inner_graph  # noqa

    def __check_if_interaction_is_possible(self, to: "BaseNode"):
        if to not in self.__graph_belongs_to:
            raise ChartingException("The interaction between the nodes is allowed only within the same group. ")

        if to in [_[0] for _ in self.__graph_belongs_to[to]]:
            raise ChartingException("There is already an established route between these nodes.")

    def go_to(self, to: "BaseNode", text: str = "") -> "BaseNode":
        self.__check_if_interaction_is_possible(to)
        self.__graph_belongs_to[to].append((to, text))
        return to


@dataclass
class Fork(BaseNode):
    pass


@dataclass
class Join(BaseNode):
    pass


@dataclass
class GraphNodeStart(BaseNode):
    pass


@dataclass
class GraphNodeFinish(BaseNode):
    pass


@dataclass
class GraphNode(Colored, BaseNode):
    text: str



class GraphNodeGroup(BaseNode):
    text: str
    start: GraphNodeStart
    finish: GraphNodeFinish
    __inner_graph: typing.Dict[BaseNode, typing.List[typing.Tuple[BaseNode, str]]] = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.start = GraphNodeStart(graph_ref=self)
        self.finish = GraphNodeFinish(graph_ref=self)
        # print(self.start)
        # print(self.finish)
        # self.__inner_graph = {
        #     self.start: [],
        #     self.finish: [],
        # }

    def node(self, title: str, color: typing.Optional[str] = None) -> GraphNode:
        node = GraphNode(graph_ref=self, text=title, _color=color)
        self.__inner_graph[node] = []
        return node

    def group(self, title: str, color: typing.Optional[str] = None) -> "GraphNodeGroup":
        group = GraphNodeGroup(graph_ref=self, text=title, _color=color)
        self.__inner_graph[group] = []
        return group

    # def __validate_inner_graph(self):
    #     pass # TODO


@dataclass
class GraphDiagram(BaseChart):
    """
    A graph that must be rendered to the diagram DSL - depending on the chosen renderer.

    :title: The title of the diagram to display on the top of the diagram
    :generator_cls: the class of the renderer to be used to generate the diagram
    :is_vertical: The boolean flag used to define the rendering orientation of the rendered graph.
        If is set to True, and therefor the orientation of the diagram is set to render the nodes from top to bottom.
        Otherwise, the orientation of the diagram is set to render the nodes from left to right.
        True by default (renders from top to bottom)
    """

    title: str
    generator_cls: typing.Type[IChartGenerator]
    is_vertical: bool = True

    __generator: IChartGenerator = field(init=False)
    __default_group: GraphNodeGroup = field(init=False)

    def __post_init__(self):
        self.__generator = self.generator_cls(self)
        self.__default_group = GraphNodeGroup(graph_ref=None, text=None, _color=None)

    def node(self, title: str, color: typing.Optional[str] = None) -> GraphNode:
        return self.__default_group.node(title, color)

    def group(self, title: str, color: typing.Optional[str] = None) -> GraphNodeGroup:
        return self.__default_group.group(title, color)


if __name__ == '__main__':
    x = GraphDiagram("aaa", type)
    x.node("")