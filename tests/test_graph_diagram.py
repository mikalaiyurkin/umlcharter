from unittest.mock import Mock

import pytest

from umlcharter import GraphDiagram, Mermaid
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
        ),
    )
    def test_nested_nodes(self, generator_cls, output):
        gd = GraphDiagram("Diagram Nested Groups", generator_cls=generator_cls)
        green_color = "769D8F"
        group1 = gd.node("Group #1", color=green_color)
        group2 = gd.node("Group #2")
        nested_group1 = group1.node("Nested Group #1", green_color)
        nested_group1.node("Nested Node #1", green_color)
        group1.go_to(group2, "Inter-group route")
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
        gd = GraphDiagram("Finish is not a strtating point", Mock)
        n1 = gd.node("Node #1")
        with pytest.raises(ChartingException):
            gd.finish.go_to(n1)

    def test_cannot_directly_link_start_and_finish(self):
        gd = GraphDiagram("Directly link start and finish", Mock)
        with pytest.raises(ChartingException):
            gd.start.go_to(gd.finish)
