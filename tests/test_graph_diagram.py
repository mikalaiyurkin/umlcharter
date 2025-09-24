from unittest.mock import Mock

import pytest

from umlcharter import GraphDiagram, Mermaid, PlantUML, Graphviz
from umlcharter.charts.common import ChartingException


class TestGraphDiagram:
    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram No Nodes
---
stateDiagram-v2
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram\\nNo Nodes
hide empty description
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram\\nNo Nodes\\n\\n"
    labelloc = t
    layout=dot
}
""",
            ),
        ),
    )
    def test_no_nodes(self, generator_cls, output):
        gd = GraphDiagram("Diagram\nNo Nodes", generator_cls=generator_cls)
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram Only Nodes
---
stateDiagram-v2
state "Node #1" as n2
state "Node #2" as n3
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram Only Nodes
hide empty description
state "Node #1" as n2
state "Node #2" as n3
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram Only Nodes\\n\\n"
    labelloc = t
    layout=dot
    n2 [style = "rounded,filled", shape = "box", label = "Node #1", fillcolor = "lightgrey"]
    n3 [style = "rounded,filled", shape = "box", label = "Node #2", fillcolor = "lightgrey"]
}
""",
            ),
        ),
    )
    def test_only_nodes(self, generator_cls, output):
        gd = GraphDiagram("Diagram Only Nodes", generator_cls=generator_cls)
        gd.node("Node #1")
        gd.node("Node #2")
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram Nodes & Routes
---
stateDiagram-v2
state "Node #1" as n2
state "Node #2" as n3
n2 --> n3 : Hello
n3 --> n2 : Hi!
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram Nodes & Routes
hide empty description
state "Node #1" as n2
state "Node #2" as n3
n2 --> n3 : Hello
n3 --> n2 : Hi!
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram Nodes & Routes\\n\\n"
    labelloc = t
    layout=dot
    n2 [style = "rounded,filled", shape = "box", label = "Node #1", fillcolor = "lightgrey"]
    n3 [style = "rounded,filled", shape = "box", label = "Node #2", fillcolor = "lightgrey"]
    n2 -> n3 [label = "Hello"]
    n3 -> n2 [label = "Hi!"]
}
""",
            ),
        ),
    )
    def test_nodes_with_routes(self, generator_cls, output):
        gd = GraphDiagram("Diagram Nodes & Routes", generator_cls=generator_cls)
        n1 = gd.node("Node #1")
        n2 = gd.node("Node #2")
        n1.go_to(n2, "Hello")
        n2.go_to(n1, "Hi!")
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram Nodes & Routes
---
stateDiagram-v2
state "Node #1" as n2
state "Node #2" as n3
[*] --> n2 : Start!
n2 --> n3 : Hello!
n3 --> n2 : Hi!
n3 --> [*] : Finish!
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram Nodes & Routes
hide empty description
state "Node #1" as n2
state "Node #2" as n3
[*] --> n2 : Start!
n2 --> n3 : Hello!
n3 --> n2 : Hi!
n3 --> [*] : Finish!
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram Nodes & Routes\\n\\n"
    labelloc = t
    layout=dot
    n0 [shape = "circle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    n1 [shape = "doublecircle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    n2 [style = "rounded,filled", shape = "box", label = "Node #1", fillcolor = "lightgrey"]
    n3 [style = "rounded,filled", shape = "box", label = "Node #2", fillcolor = "lightgrey"]
    n0 -> n2 [label = "Start!"]
    n2 -> n3 [label = "Hello!"]
    n3 -> n2 [label = "Hi!"]
    n3 -> n1 [label = "Finish!"]
}
""",
            ),
        ),
    )
    def test_start_and_finish(self, generator_cls, output):
        gd = GraphDiagram("Diagram Nodes & Routes", generator_cls=generator_cls)
        n1 = gd.node("Node #1")
        n2 = gd.node("Node #2")
        start = gd.start
        finish = gd.finish
        start.go_to(n1, "Start!")
        n1.go_to(n2, "Hello!")
        n2.go_to(n1, "Hi!")
        n2.go_to(finish, "Finish!")
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram Nested Groups
---
stateDiagram-v2
state "Group #1" as n2 {
  state "Nested Group #1" as n5 {
    state "Nested Node #1" as n8
  }
  [*] --> n5 : Go deeper!
  n5 --> [*] : It was deep, indeed
}
classDef cd_n2 fill:#769D8F
class n2 cd_n2
state "Group #2" as n9
n2 --> n9 : Inter-group route
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram Nested Groups
hide empty description
state "Group #1" as n2 #769D8F {
  state "Nested Group #1" as n5 #769D8F {
    state "Nested\\nNode #1" as n8 #769D8F
  }
  [*] --> n5 : Go deeper!
  n5 --> [*] : It was deep, indeed
}
state "Group #2" as n9
n2 --> n9 : Inter-group\\nroute
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram Nested Groups\\n\\n"
    labelloc = t
    layout=fdp
    sep=1
    K=2
    overlap=scalexy
    subgraph cluster_n2 {
        label = "Group #1"
        style = "filled"
        fillcolor = "#769D8F"
        n3 [shape = "circle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
        n4 [shape = "doublecircle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
        subgraph cluster_n5 {
            label = "Nested Group #1"
            style = "filled"
            fillcolor = "#769D8F"
            n8 [style = "rounded,filled", shape = "box", label = "Nested\\nNode #1", fillcolor = "#769D8F"]
        }
        n3 -> cluster_n5 [label = "Go deeper!"]
        cluster_n5 -> n4 [label = "It was deep, indeed"]
    }
    n9 [style = "rounded,filled", shape = "box", label = "Group #2", fillcolor = "lightgrey"]
    cluster_n2 -> n9 [label = "Inter-group\\nroute"]
}
""",
            ),
        ),
    )
    def test_nested_nodes(self, generator_cls, output):
        gd = GraphDiagram("Diagram Nested Groups", generator_cls=generator_cls)
        green_color = "769D8F"
        group1 = gd.node("Group #1", color=green_color)
        group2 = gd.node("Group #2")
        nested_group1 = group1.node("Nested Group #1", green_color)
        nested_group1.node("Nested\nNode #1", green_color)
        group1.go_to(group2, "Inter-group\nroute")
        group1.start.go_to(nested_group1, "Go deeper!")
        nested_group1.go_to(group1.finish, "It was deep, indeed")
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram Joins & Forks
---
stateDiagram-v2
state "Short Path" as n2
classDef cd_n2 fill:#769D8F
class n2 cd_n2
state "Long Path #1" as n3
state "Long Path #2" as n4
state "Long Path #3" as n5
classDef cd_n5 fill:#769D8F
class n5 cd_n5
state n6 <<fork>>
state n7 <<join>>
[*] --> n6 : Choose your path
n2 --> n7 : It was easy, ha!
n3 --> n4 : 
n4 --> n5 : ... still going ...
n5 --> n7 : 
n6 --> n2 : Choose the easy one
n6 --> n3 : Choose the hard one
n7 --> [*] : 
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram Joins & Forks
hide empty description
state "Short Path" as n2 #769D8F
state "Long Path #1" as n3
state "Long Path #2" as n4
state "Long Path #3" as n5 #769D8F
state n6 <<fork>>
state n7 <<join>>
[*] --> n6 : Choose your path
n2 --> n7 : It was easy, ha!
n3 --> n4
n4 --> n5 : ... still going ...
n5 --> n7
n6 --> n2 : Choose the easy one
n6 --> n3 : Choose the hard one
n7 --> [*]
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram Joins & Forks\\n\\n"
    labelloc = t
    layout=dot
    n0 [shape = "circle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    n1 [shape = "doublecircle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    n2 [style = "rounded,filled", shape = "box", label = "Short Path", fillcolor = "#769D8F"]
    n3 [style = "rounded,filled", shape = "box", label = "Long Path #1", fillcolor = "lightgrey"]
    n4 [style = "rounded,filled", shape = "box", label = "Long Path #2", fillcolor = "lightgrey"]
    n5 [style = "rounded,filled", shape = "box", label = "Long Path #3", fillcolor = "#769D8F"]
    n6 [style = "filled", fillcolor = "black", shape = "box", label = "", height = 0.1]
    n7 [style = "filled", fillcolor = "black", shape = "box", label = "", height = 0.1]
    n0 -> n6 [label = "Choose your path"]
    n2 -> n7 [label = "It was easy, ha!"]
    n3 -> n4
    n4 -> n5 [label = "... still going ..."]
    n5 -> n7
    n6 -> n2 [label = "Choose the easy one"]
    n6 -> n3 [label = "Choose the hard one"]
    n7 -> n1
}
""",
            ),
        ),
    )
    def test_join_and_fork(self, generator_cls, output):
        gd = GraphDiagram("Diagram Joins & Forks", generator_cls=generator_cls)
        green_color = "769D8F"
        n1 = gd.node("Short Path", green_color)
        n2 = gd.node("Long Path #1")
        n3 = gd.node("Long Path #2")
        n4 = gd.node("Long Path #3", color=green_color)
        fork = gd.fork()
        gd.start.go_to(fork, "Choose your path")
        fork.go_to(n1, "Choose the easy one")
        fork.go_to(n2, "Choose the hard one")
        n2.go_to(n3)
        n3.go_to(n4, "... still going ...")
        join = gd.join()
        n4.go_to(join)
        n1.go_to(join, "It was easy, ha!")
        join.go_to(gd.finish)
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Diagram Conditions
---
stateDiagram-v2
state "Node #1" as n2
state n3 <<choice>>
state "Node (conditional) #2" as n4
[*] --> n2 : Go to first
n2 --> n3 : Make a choice
n3 --> n4 : Need a second one
n3 --> [*] : Nah, try again
n4 --> [*] : 
""",
            ),
            (
                PlantUML,
                """@startuml
title Diagram Conditions
hide empty description
state "Node #1" as n2
state n3 <<choice>>
state "Node (conditional) #2" as n4
[*] --> n2 : Go to first
n2 --> n3 : Make a choice
n3 --> n4 : Need a second one
n3 --> [*] : Nah, try again
n4 --> [*]
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Diagram Conditions\\n\\n"
    labelloc = t
    layout=dot
    n0 [shape = "circle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    n1 [shape = "doublecircle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    n2 [style = "rounded,filled", shape = "box", label = "Node #1", fillcolor = "lightgrey"]
    n3 [style = "filled", fillcolor = "white", shape = "diamond", label = "", height = 0.2, width = 0.2]
    n4 [style = "rounded,filled", shape = "box", label = "Node (conditional) #2", fillcolor = "lightgrey"]
    n0 -> n2 [label = "Go to first"]
    n2 -> n3 [label = "Make a choice"]
    n3 -> n4 [label = "Need a second one"]
    n3 -> n1 [label = "Nah, try again"]
    n4 -> n1
}
""",
            ),
        ),
    )
    def test_condition(self, generator_cls, output):
        gd = GraphDiagram("Diagram Conditions", generator_cls=generator_cls)
        n1 = gd.node("Node #1")
        c1 = gd.condition()
        n2 = gd.node("Node (conditional) #2")
        gd.start.go_to(n1, "Go to first")
        n1.go_to(c1, "Make a choice")
        c1.go_to(n2, "Need a second one")
        n2.go_to(gd.finish)
        c1.go_to(gd.finish, "Nah, try again")
        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """---
title: Complex Diagram With Notes
---
stateDiagram-v2
state "Group" as n2 {
  state "Nested Node" as n5
  note right of n5
Note for the nested node
  end note
}
note right of n2
Note for the group
end note
state "Outer Node" as n6
note right of n6
It is possible to have multiple notes...
end note
note right of n6
...and also split them
in multi lines
end note
state n7 <<fork>>
note right of n7
Note for fork
end note
state n8 <<choice>>
note right of n8
Note for condition
end note
state n9 <<join>>
note right of n9
Note for join
end note
n2 --> n7 : 
n7 --> n8 : 
n7 --> n9 : 
n8 --> n9 : 
n8 --> [*] : 
""",
            ),
            (
                PlantUML,
                """@startuml
title Complex Diagram With Notes
hide empty description
state "Group" as n2 {
  state "Nested Node" as n5
  note right of n5 : Note for the nested node
}
note right of n2 : Note for the group
state "Outer Node" as n6
note right of n6 : It is possible to have multiple notes...
note right of n6 : ...and also split them\\nin multi lines
state n7 <<fork>>
note right of n7 : Note for fork
state n8 <<choice>>
note right of n8 : Note for condition
state n9 <<join>>
note right of n9 : Note for join
n2 --> n7
n7 --> n8
n7 --> n9
n8 --> n9
n8 --> [*]
@enduml
""",
            ),
            (
                Graphviz,
                """digraph umlcharter_graph {
    label = "Complex Diagram With Notes\\n\\n"
    labelloc = t
    layout=fdp
    sep=1
    K=2
    overlap=scalexy
    n1 [shape = "doublecircle", style = "filled", fillcolor = "black", label = "", fixedsize = true, height = 0.2]
    subgraph cluster_n2 {
        label = "Group"
        n5 [style = "rounded,filled", shape = "box", label = "Nested Node", fillcolor = "lightgrey"]
        note0_for_n5 [shape = "note", style="filled", fillcolor="lightyellow", label="Note for the nested node"]
        n5 -> note0_for_n5 [style = "dotted"]
    }
    n6 [style = "rounded,filled", shape = "box", label = "Outer Node", fillcolor = "lightgrey"]
    n7 [style = "filled", fillcolor = "black", shape = "box", label = "", height = 0.1]
    n8 [style = "filled", fillcolor = "white", shape = "diamond", label = "", height = 0.2, width = 0.2]
    n9 [style = "filled", fillcolor = "black", shape = "box", label = "", height = 0.1]
    cluster_n2 -> n7
    note0_for_cluster_n2 [shape = "note", style="filled", fillcolor="lightyellow", label="Note for the group"]
    cluster_n2 -> note0_for_cluster_n2 [style = "dotted"]
    note0_for_n6 [shape = "note", style="filled", fillcolor="lightyellow", label="It is possible to have multiple notes..."]
    n6 -> note0_for_n6 [style = "dotted"]
    note1_for_n6 [shape = "note", style="filled", fillcolor="lightyellow", label="...and also split them\\nin multi lines"]
    n6 -> note1_for_n6 [style = "dotted"]
    n7 -> n8
    n7 -> n9
    note0_for_n7 [shape = "note", style="filled", fillcolor="lightyellow", label="Note for fork"]
    n7 -> note0_for_n7 [style = "dotted"]
    n8 -> n9
    n8 -> n1
    note0_for_n8 [shape = "note", style="filled", fillcolor="lightyellow", label="Note for condition"]
    n8 -> note0_for_n8 [style = "dotted"]
    note0_for_n9 [shape = "note", style="filled", fillcolor="lightyellow", label="Note for join"]
    n9 -> note0_for_n9 [style = "dotted"]
}
""",
            ),
        ),
    )
    def test_complex_with_notes(self, generator_cls, output):
        gd = GraphDiagram("Complex Diagram With Notes", generator_cls=generator_cls)
        group = gd.node("Group")
        nested_node = group.node("Nested Node")
        node = gd.node("Outer Node")
        fork = gd.fork()
        condition = gd.condition()
        join = gd.join()

        group.go_to(fork)
        fork.go_to(condition)
        condition.go_to(join)
        condition.go_to(gd.finish)
        fork.go_to(join)

        group.note("Note for the group")
        nested_node.note("Note for the nested node")
        node.note("It is possible to have multiple notes...")
        node.note("...and also split them\nin multi lines")

        fork.note("Note for fork")
        condition.note("Note for condition")
        join.note("Note for join")

        assert str(gd) == output

    @pytest.mark.parametrize(
        "generator_cls,is_vertical,output",
        (
            (
                Mermaid,
                True,
                """---
title: Diagram Different Orientation
---
stateDiagram-v2
state "Node: #1" as n2
state "Node: #2" as n3
state "Node: #3" as n4
state "Node: #4" as n5
n2 --> n3 : 
n3 --> n4 : 
n4 --> n5 : 
n5 --> n2 : We are rolling yay!
""",
            ),
            (
                Mermaid,
                False,
                """---
title: Diagram Different Orientation
---
stateDiagram-v2
direction LR
state "Node: #1" as n2
state "Node: #2" as n3
state "Node: #3" as n4
state "Node: #4" as n5
n2 --> n3 : 
n3 --> n4 : 
n4 --> n5 : 
n5 --> n2 : We are rolling yay!
""",
            ),
            (
                PlantUML,
                True,
                """@startuml
title Diagram: Different Orientation
hide empty description
state "Node: #1" as n2
state "Node: #2" as n3
state "Node: #3" as n4
state "Node: #4" as n5
n2 --> n3
n3 --> n4
n4 --> n5
n5 --> n2 : We are rolling: yay!
@enduml
""",
            ),
            (
                PlantUML,
                False,
                """@startuml
title Diagram: Different Orientation
hide empty description
state "Node: #1" as n2
state "Node: #2" as n3
state "Node: #3" as n4
state "Node: #4" as n5
n2 -> n3
n3 -> n4
n4 -> n5
n5 -> n2 : We are rolling: yay!
@enduml
""",
            ),
            (
                Graphviz,
                True,
                """digraph umlcharter_graph {
    label = "Diagram: Different Orientation\\n\\n"
    labelloc = t
    layout=dot
    n2 [style = "rounded,filled", shape = "box", label = "Node: #1", fillcolor = "lightgrey"]
    n3 [style = "rounded,filled", shape = "box", label = "Node: #2", fillcolor = "lightgrey"]
    n4 [style = "rounded,filled", shape = "box", label = "Node: #3", fillcolor = "lightgrey"]
    n5 [style = "rounded,filled", shape = "box", label = "Node: #4", fillcolor = "lightgrey"]
    n2 -> n3
    n3 -> n4
    n4 -> n5
    n5 -> n2 [label = "We are rolling: yay!"]
}
""",
            ),
            (
                Graphviz,
                False,
                """digraph umlcharter_graph {
    label = "Diagram: Different Orientation\\n\\n"
    labelloc = t
    layout=dot
    rankdir=LR
    n2 [style = "rounded,filled", shape = "box", label = "Node: #1", fillcolor = "lightgrey"]
    n3 [style = "rounded,filled", shape = "box", label = "Node: #2", fillcolor = "lightgrey"]
    n4 [style = "rounded,filled", shape = "box", label = "Node: #3", fillcolor = "lightgrey"]
    n5 [style = "rounded,filled", shape = "box", label = "Node: #4", fillcolor = "lightgrey"]
    n2 -> n3
    n3 -> n4
    n4 -> n5
    n5 -> n2 [label = "We are rolling: yay!"]
}
""",
            ),
        ),
    )
    def test_orientation(self, generator_cls, is_vertical, output):
        gd = GraphDiagram(
            "Diagram: Different Orientation",
            generator_cls=generator_cls,
            is_vertical=is_vertical,
        )
        n1 = gd.node("Node: #1")
        n2 = gd.node("Node: #2")
        n1.go_to(n2)
        n3 = gd.node("Node: #3")
        n2.go_to(n3)
        n4 = gd.node("Node: #4")
        n3.go_to(n4)
        n4.go_to(n1, "We are rolling: yay!")
        assert str(gd) == output

    def test_invalid_color_string(self):
        gd = GraphDiagram("Invalid color", Mock)
        with pytest.raises(ChartingException):
            gd.node("Invalid color", "red")

    def test_same_titles_on_the_same_level(self):
        gd = GraphDiagram("Same titles", Mock)
        gd.node("Title")
        with pytest.raises(ChartingException):
            gd.node("Title")

    def test_cannot_interact_between_levels(self):
        gd = GraphDiagram("Different levels", Mock)
        outer_node = gd.node("Outer")
        nested_node = gd.node("Group").node("Nested")
        with pytest.raises(ChartingException):
            outer_node.go_to(nested_node)

    def test_cannot_build_same_graph_edge_twice(self):
        gd = GraphDiagram("Duplicated graph edges", Mock)
        n1 = gd.node("Node #1")
        n2 = gd.node("Node #2")
        n1.go_to(n2)
        with pytest.raises(ChartingException):
            n1.go_to(n2)

    def test_cannot_go_to_abstract_start(self):
        gd = GraphDiagram("Start is not a destination", Mock)
        n1 = gd.node("Node #1")
        with pytest.raises(ChartingException):
            n1.go_to(gd.start)

    def test_cannot_go_from_abstract_finish(self):
        gd = GraphDiagram("Finish is not a starting point", Mock)
        n1 = gd.node("Node #1")
        with pytest.raises(ChartingException):
            gd.finish.go_to(n1)

    def test_cannot_directly_link_start_and_finish(self):
        gd = GraphDiagram("Directly link start and finish", Mock)
        with pytest.raises(ChartingException):
            gd.start.go_to(gd.finish)

    @pytest.mark.parametrize("generator_cls", (Mermaid, PlantUML, Graphviz))
    def test_no_cyclic_ref_count(self, generator_cls):
        gd = GraphDiagram(
            "Graph without cyclic references to ensure correct memory management",
            generator_cls=generator_cls,
        )
        node = gd.node("Node")
        fork = gd.fork()
        join = gd.join()
        condition = gd.condition()
        generator = gd._GraphDiagram__generator  # noqa

        for internal_node in (node, fork, join, condition):
            assert internal_node._graph_ref

        assert generator.ref

        del gd

        import gc

        gc.collect()

        for internal_node in (node, fork, join, condition):
            with pytest.raises(
                ReferenceError, match="weakly-referenced object no longer exists"
            ):
                assert internal_node._graph_ref

        with pytest.raises(
            ReferenceError, match="weakly-referenced object no longer exists"
        ):
            assert generator.ref
