import typing
from dataclasses import dataclass, field

from umlcharter.charts.common import BaseChart, Colored, ChartingException
from umlcharter.generators.base import IChartGenerator


@dataclass
class BaseNode:
    _graph_ref: typing.Optional["Node"]

    @property
    def __graph_belongs_to(
        self,
    ) -> typing.Dict["BaseNode", typing.List[typing.Tuple["BaseNode", str]]]:
        return self._graph_ref._Node__inner_graph  # noqa

    def __check_if_interaction_is_allowed(self, to: "BaseNode"):
        if to not in self.__graph_belongs_to:
            raise ChartingException(
                "You cannot define a link from a node to another one outside of the same level / group"
            )

        for already_existing_routes in self.__graph_belongs_to[self]:
            if already_existing_routes[0] is to:
                raise ChartingException(
                    f"There is already an established link from {self} to {to}."
                )

        if isinstance(self, Start) and isinstance(to, Finish):
            raise ChartingException(
                "The direct link from start to finish is pointless, these are abstract nodes;"
                "there must be some intermediate nodes between them."
            )

        if isinstance(self, Finish):
            raise ChartingException(
                "The 'finish' node can only be the destination and not the starting point"
            )

        if isinstance(to, Start):
            raise ChartingException(
                "The 'start' node can only be the starting point and not the destination"
            )

    def go_to(self, to: "BaseNode", text: str = "") -> "BaseNode":
        self.__check_if_interaction_is_allowed(to)
        self.__graph_belongs_to[self].append((to, text))
        return to


@dataclass
class Fork(BaseNode):
    def __hash__(self):
        return hash(f"{id(self)}")

    def __repr__(self):
        return "Fork"  # pragma: nocover


@dataclass
class Join(BaseNode):
    def __hash__(self):
        return hash(f"{id(self)}")

    def __repr__(self):
        return "Join"  # pragma: nocover


@dataclass
class Condition(BaseNode, Colored):
    def __hash__(self):
        return hash(f"{id(self)}")

    def __repr__(self):
        return "Condition"  # pragma: nocover


@dataclass
class Start(BaseNode):
    def __hash__(self):
        return hash(f"{id(self)}")

    def __repr__(self):
        return "Start"  # pragma: nocover


@dataclass
class Finish(BaseNode):
    def __hash__(self):
        return hash(f"{id(self)}")

    def __repr__(self):
        return "Finish"  # pragma: nocover


@dataclass
class Node(BaseNode, Colored):
    text: str
    start: Start = field(init=False)
    finish: Finish = field(init=False)
    __inner_graph: typing.Dict[BaseNode, typing.List[typing.Tuple[BaseNode, str]]] = (
        field(init=False)
    )

    def is_group(self) -> bool:
        """The node can be a representation of a group / composite state if it contains the other nodes inside it."""
        return (
            len(self.__inner_graph) > 2
        )  # contains anything besides the default start and end nodes

    def is_top_level(self) -> bool:
        return not self._graph_ref

    def __hash__(self):
        return hash(f"{id(self)}")

    def __repr__(self):
        return (
            f"{'Group' if self.is_group() else 'Node'} {self.text}"  # pragma: nocover
        )

    def __post_init__(self):
        super().__post_init__()
        self.start = Start(_graph_ref=self)
        self.finish = Finish(_graph_ref=self)
        self.__inner_graph = {
            self.start: [],
            self.finish: [],
        }

    def __check_if_adding_new_element_is_allowed(self, title: str):
        for nodes in self.__inner_graph:
            if getattr(nodes, "text", None) == title:
                raise ChartingException(
                    f"There must be no nodes in the graph in the same group with the same title '{title}'."
                )

    def node(self, title: str, color: typing.Optional[str] = None) -> "Node":
        self.__check_if_adding_new_element_is_allowed(title)
        node = Node(_graph_ref=self, text=title, _color=color)
        self.__inner_graph[node] = []
        return node

    def fork(self) -> "Fork":
        fork = Fork(_graph_ref=self)
        self.__inner_graph[fork] = []
        return fork

    def join(self) -> "Join":
        join = Join(_graph_ref=self)
        self.__inner_graph[join] = []
        return join

    def condition(self, color: typing.Optional[str] = None) -> "Condition":
        condition = Condition(_graph_ref=self, _color=color)
        self.__inner_graph[condition] = []
        return condition


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
    __base_node: Node = field(init=False)

    def __post_init__(self):
        self.__generator = self.generator_cls(self)
        self.__base_node = Node(_graph_ref=None, text="", _color=None)

    @property
    def start(self) -> Start:
        return self.__base_node.start

    @property
    def finish(self) -> Finish:
        return self.__base_node.finish

    def node(self, title: str, color: typing.Optional[str] = None) -> Node:
        return self.__base_node.node(title, color)

    def fork(self) -> Fork:
        return self.__base_node.fork()

    def join(self) -> Join:
        return self.__base_node.join()

    def condition(self, color: typing.Optional[str] = None) -> Condition:
        return self.__base_node.condition(color)

    def generate(self) -> str:
        return self.__generator.generate_graph_diagram()

    def __repr__(self):
        return f"'{self.title}', {self.generator_cls.__name__}"  # pragma: nocover

    def __str__(self):
        return self.generate()
