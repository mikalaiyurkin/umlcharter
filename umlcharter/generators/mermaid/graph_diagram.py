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
        """
        Some places do not allow line breaks, replace these with just a plane space.
        Also, these places do not allow ':' symbol
        """
        return string.replace("\n", " ").replace(":", "")

    @classmethod
    def generate(cls, sequence_diagram: GraphDiagram) -> str:
        aliases = {}

        generated = f"---\ntitle: {cls._remove_line_breaks(sequence_diagram.title)}\n---\nstateDiagram-v2\n"
        if not sequence_diagram.is_vertical:
            # default direction is top -> bottom, specify if it is not default
            generated += "direction LR\n"

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
                                f'{ident}state "{node.text}" as {node_alias} '
                                f'{{\n{recursive_graph_generation("", node, depth + 2)}{ident}}}\n'
                            )
                        else:
                            generated_dsl += (
                                f'{ident}state "{node.text}" as {node_alias}\n'
                            )
                        if node_to_process.is_top_level() and node.color:
                            # NB: mermaid does not support styling for the nodes inside composite states ("groups") yet.
                            # So the styling will be applied ONLY to the nodes on the most top level of the graph
                            class_def = f"cd_{node_alias}"
                            generated_dsl += (
                                f"{ident}classDef {class_def} fill:{node.color.as_hex()}\n"
                                f"{ident}class {node_alias} {class_def}\n"
                            )
                notes: list[str] = getattr(node, "_notes", [])
                for note in notes:
                    generated_dsl += (
                        f"{ident}note right of {node_alias}\n{note}\n{ident}end note\n"
                    )

            # ...second run is to define the routes between the nodes
            for node, routes in inner_graph.items():
                for route in routes:
                    to_node, route_text = route
                    generated_dsl += f"{ident}{aliases[node]} --> {aliases[to_node]} : {cls._remove_line_breaks(route_text)}\n"

            return generated_dsl

        base_node: Node = sequence_diagram._GraphDiagram__base_node  # noqa
        return recursive_graph_generation(generated, base_node, 0)
