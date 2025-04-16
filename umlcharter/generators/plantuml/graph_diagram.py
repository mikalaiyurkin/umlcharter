from umlcharter.charts.graph_diagram import (
    Node,
    Start,
    Finish,
    Condition,
    Join,
    Fork,
    GraphDiagram,
)


class PlantUMLGraphDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        """Some places allow line break as \n"""
        return string.replace("\n", "\\n")

    @classmethod
    def generate(cls, graph_diagram: GraphDiagram) -> str:
        aliases = {}
        generated = f"@startuml\ntitle {cls._line_break(graph_diagram.title)}\nhide empty description\n"

        def recursive_graph_generation(
            generated_dsl: str, node_to_process: Node, depth: int
        ) -> str:
            ident = " " * depth
            inner_graph = node_to_process._Node__inner_graph  # noqa
            # iterate once to define the states first...
            for node, routes in inner_graph.items():
                if isinstance(node, Start) or isinstance(node, Finish):
                    aliases[node] = "[*]"
                else:
                    node_alias = f"n{len(aliases)}"
                    aliases[node] = node_alias
                    if isinstance(node, Condition):
                        generated_dsl += f"{ident}state {node_alias} <<choice>>\n"
                    if isinstance(node, Join):
                        generated_dsl += f"{ident}state {node_alias} <<join>>\n"
                    if isinstance(node, Fork):
                        generated_dsl += f"{ident}state {node_alias} <<fork>>\n"
                    if isinstance(node, Node):
                        if node.is_group():
                            generated_dsl += (
                                f'{ident}state "{cls._line_break(node.text)}" as {node_alias}{" " + node.color.as_hex() if node.color else ""} '
                                f'{{\n{recursive_graph_generation("", node, depth + 2)}{ident}}}\n'
                            )
                        else:
                            generated_dsl += f'{ident}state "{cls._line_break(node.text)}" as {node_alias}{" " + node.color.as_hex() if node.color else ""}\n'

                    notes: list[str] = getattr(node, "_notes", [])
                    for note in notes:
                        generated_dsl += (
                            f"{ident}note {'right' if graph_diagram.is_vertical else 'bottom'} "
                            f"of {node_alias} : {cls._line_break(note)}\n"
                        )

            # ...second run is to define the routes between the nodes
            for node, routes in inner_graph.items():
                for route in routes:
                    to_node, route_text = route
                    generated_dsl += (
                        f"{ident}{aliases[node]} {'-->' if graph_diagram.is_vertical else '->'} "
                        f"{aliases[to_node]}{' : ' + cls._line_break(route_text) if route_text else ''}\n"
                    )

            return generated_dsl

        base_node: Node = graph_diagram._GraphDiagram__base_node  # noqa
        return recursive_graph_generation(generated, base_node, 0) + "@enduml\n"
