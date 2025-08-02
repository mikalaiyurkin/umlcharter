from umlcharter.charts.graph_diagram import (
    Node,
    GraphDiagram,
    Start,
    Finish,
    Join,
    Fork,
    Condition,
)


class GraphvizGraphDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        """Some places allow line break as \n"""
        return string.replace("\n", "\\n") or "''"

    @classmethod
    def generate(cls, graph_diagram: GraphDiagram) -> str:
        aliases = {}

        # nb: double line break after the title to add some visual space between the graph title and the graph itself
        generated = f'digraph umlcharter_graph {{\n    label = "{cls._line_break(graph_diagram.title)}\\n\\n"\n    labelloc = t\n'

        # check if we have any nested ("composite") states. If there are such, we have to use alternative layout "fdp"
        #  that produces not so fancy graphs as "dot", and also does not have the control over the direction of the graph.
        base_node: Node = graph_diagram._GraphDiagram__base_node  # noqa
        base_node_inner_graph: dict = base_node._Node__inner_graph  # noqa
        contains_composite_states = False
        for node, _ in base_node_inner_graph.items():
            if isinstance(node, Node) and node.is_group():
                contains_composite_states = True
                break

        if contains_composite_states:
            # set the custom layout and some attributes to ensure the nodes will unlikely clash
            generated += "    layout=fdp\n    sep=1\n    K=2\n    overlap=scalexy\n"
        else:
            generated += "    layout=dot\n"
            if not graph_diagram.is_vertical:
                # we can use default "dot" layout, so we can control direction. Default is top -> bottom
                generated += "    rankdir=LR\n"

        def recursive_graph_generation(
            generated_dsl: str, node_to_process: Node, depth: int
        ) -> str:
            ident = "    " * (depth + 1)
            inner_graph = node_to_process._Node__inner_graph  # noqa
            # iterate once to define if there are incoming routes to finish node within the current subgraph, because it
            #  must be included into the definition of the nodes ONLY if it was really targeted at lest once
            finish_is_in_use = False
            for routes in inner_graph.values():
                for route in routes:
                    to_node, _ = route
                    if isinstance(to_node, Finish):
                        finish_is_in_use = True
                        break

            # now iterate to define the states...
            for node, routes in inner_graph.items():
                node_alias = f"n{len(aliases)}"
                aliases[node] = node_alias

                # nb: start must be added only if there are outgoing links *from* it
                if isinstance(node, Start) and routes:
                    generated_dsl += f'{ident}{node_alias} [shape = "circle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]\n'

                # nb: finish must be added only if there are incoming links *to* it
                if isinstance(node, Finish) and finish_is_in_use:
                    generated_dsl += f'{ident}{node_alias} [shape = "doublecircle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]\n'

                if isinstance(node, (Join, Fork)):
                    generated_dsl += (
                        f'{ident}{node_alias} [style = "filled", fillcolor = "black", shape = "box", label = "", '
                        f'{"height" if graph_diagram.is_vertical else "width"} = 0.1]\n'
                    )

                if isinstance(node, Condition):
                    generated_dsl += f'{ident}{node_alias} [style = "filled", fillcolor = "white", shape = "diamond", label = "", height = 0.2, width = 0.2]\n'

                if isinstance(node, Node):
                    if node.is_group():
                        aliases[node] = f"cluster_{aliases[node]}"
                        generated_dsl += f"{ident}subgraph {aliases[node]} {{\n"
                        if node.text:
                            generated_dsl += (
                                f'{ident}    label = "{cls._line_break(node.text)}"\n'
                            )
                        if node.color:
                            generated_dsl += f'{ident}    style = "filled"\n{ident}    fillcolor = "{node.color.as_hex()}"\n'

                        generated_dsl += (
                            recursive_graph_generation("", node, depth + 1)
                            + f"{ident}}}\n"
                        )

                    else:
                        generated_dsl += (
                            f'{ident}{node_alias} [style = "rounded,filled", shape = "box", label = "{cls._line_break(node.text)}"'
                            + (
                                f', fillcolor = "{node.color.as_hex()}"]\n'
                                if node.color
                                else ', fillcolor = "lightgrey"]\n'
                            )
                        )

            # ...final run is to define the routes between the nodes
            for node, routes in inner_graph.items():
                for route in routes:
                    to_node, route_text = route
                    generated_dsl += (
                        f"{ident}{aliases[node]} -> {aliases[to_node]}"
                        + (
                            f' [label = "{cls._line_break(route_text)}"]'
                            if route_text
                            else ""
                        )
                        + "\n"
                    )

                # there is no native "note" support, because graphviz is for the generic graphs, not for UML
                notes: list[str] = getattr(node, "_notes", [])
                for index, note in enumerate(notes):
                    note_alias = f"note{index}_for_{aliases[node]}"
                    generated_dsl += f'{ident}{note_alias} [shape = "note", style="filled", fillcolor="lightyellow", label="{cls._line_break(note)}"]\n'
                    generated_dsl += (
                        f'{ident}{aliases[node]} -> {note_alias} [style = "dotted"]\n'
                    )

            return generated_dsl

        return recursive_graph_generation(generated, base_node, 0) + "}\n"
