from umlcharter.charts.graph_diagram import (
    Node,
    Start,
    Finish,
    Condition,
    Join,
    Fork,
    GraphDiagram,
)


class MermaidGraphDiagram:
    @staticmethod
    def _remove_line_breaks(string: str) -> str:
        """Some places do not allow line breaks, replace these with just a plane space"""
        return string.replace("\n", " ")

    @classmethod
    def generate(cls, sequence_diagram: GraphDiagram) -> str:
        aliases = {}

        generated = f"---\ntitle: {cls._remove_line_breaks(sequence_diagram.title)}\n---\nstateDiagram-v2\n"
        if not sequence_diagram.is_vertical:
            # default direction is top -> bottom, specify if it is not default
            generated += "direction LR\n"

        def recursive_graph_generation(
            generated_dsl: str, node_to_process: Node
        ) -> str:
            inner_graph = node_to_process._Node__inner_graph  # noqa
            # iterate once to define the states first...
            for node, routes in inner_graph.items():
                if isinstance(node, Start) or isinstance(node, Finish):
                    aliases[node] = "[*]"
                else:
                    node_alias = f"n{len(aliases)}"
                    aliases[node] = node_alias
                    if isinstance(node, Condition):
                        generated_dsl += f"state {node_alias} <<choice>>\n"
                    if isinstance(node, Join):
                        generated_dsl += f"state {node_alias} <<join>>\n"
                    if isinstance(node, Fork):
                        generated_dsl += f"state {node_alias} <<fork>>\n"
                    if isinstance(node, Node):
                        if node.is_group():
                            generated_dsl += (
                                f'state "{node.text}" as {node_alias} '
                                f'{{\n{recursive_graph_generation("", node)}\n}}\n'
                            )
                        else:
                            generated_dsl += f'state "{node.text}" as {node_alias}\n'
            # second run is to define the routes between the nodes
            for node, routes in inner_graph.items():
                for route in routes:
                    to_node, route_text = route
                    generated_dsl += f"{aliases[node]} --> {aliases[to_node]} : {cls._remove_line_breaks(route_text)}\n"

            return generated_dsl

        base_node: Node = sequence_diagram._GraphDiagram__base_node  # noqa
        return recursive_graph_generation(generated, base_node)
