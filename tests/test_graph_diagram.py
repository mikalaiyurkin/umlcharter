import pytest

from umlcharter import GraphDiagram, Mermaid


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
        sd = GraphDiagram("Diagram\nNo Nodes", generator_cls=generator_cls)
        assert str(sd) == output

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
        sd = GraphDiagram("Diagram Only Nodes", generator_cls=generator_cls)
        sd.node("Node #1")
        sd.node("Node #2")
        assert str(sd) == output

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
        sd = GraphDiagram("Diagram Nodes & Routes", generator_cls=generator_cls)
        n1 = sd.node("Node #1")
        n2 = sd.node("Node #2")
        n1.go_to(n2, "Hello")
        n2.go_to(n1, "Hi!")
        assert str(sd) == output

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
        sd = GraphDiagram("Diagram Nodes & Routes", generator_cls=generator_cls)
        n1 = sd.node("Node #1")
        n2 = sd.node("Node #2")
        start = sd.start
        finish = sd.finish
        start.go_to(n1, "Start!")
        n1.go_to(n2, "Hello!")
        n2.go_to(n1, "Hi!")
        n2.go_to(finish, "Finish!")
        assert str(sd) == output

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
state "Group #2" as n9
n2 --> n9 : Inter-group route
""",
            ),
        ),
    )
    def test_nested_nodes(self, generator_cls, output):
        sd = GraphDiagram("Diagram Nested Groups", generator_cls=generator_cls)
        group1 = sd.node("Group #1")
        group2 = sd.node("Group #2")
        nested_group1 = group1.node("Nested Group #1")
        nested_group1.node("Nested Node #1")
        group1.go_to(group2, "Inter-group route")
        group1.start.go_to(nested_group1, "Go deeper!")
        nested_group1.go_to(group1.finish, "It was deep, indeed")
        assert str(sd) == output

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
state "Long Path #1" as n3
state "Long Path #2" as n4
state "Long Path #3" as n5
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
        sd = GraphDiagram("Diagram Joins & Forks", generator_cls=generator_cls)
        n1 = sd.node("Short Path")
        n2 = sd.node("Long Path #1")
        n3 = sd.node("Long Path #2")
        n4 = sd.node("Long Path #3")
        fork = sd.fork()
        sd.start.go_to(fork, "Choose your path")
        fork.go_to(n1, "Choose the easy one")
        fork.go_to(n2, "Choose the hard one")
        n2.go_to(n3)
        n3.go_to(n4, "... still going ...")
        join = sd.join()
        n4.go_to(join)
        n1.go_to(join, "It was easy, ha!")
        join.go_to(sd.finish)
        assert str(sd) == output

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
        sd = GraphDiagram("Diagram Conditions", generator_cls=generator_cls)
        n1 = sd.node("Node #1")
        c1 = sd.condition()
        n2 = sd.node("Node (conditional) #2")
        sd.start.go_to(n1, "Go to first")
        n1.go_to(c1, "Make a choice")
        c1.go_to(n2, "Need a second one")
        n2.go_to(sd.finish)
        c1.go_to(sd.finish, "Nah, try again")
        assert str(sd) == output

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
state "Node #1" as n2
state "Node #2" as n3
state "Node #3" as n4
state "Node #4" as n5
n2 --> n3 : 
n3 --> n4 : 
n4 --> n5 : 
n5 --> n2 : We are rolling
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
state "Node #1" as n2
state "Node #2" as n3
state "Node #3" as n4
state "Node #4" as n5
n2 --> n3 : 
n3 --> n4 : 
n4 --> n5 : 
n5 --> n2 : We are rolling
""",
            ),
        ),
    )
    def test_orientation(self, generator_cls, is_vertical, output):
        sd = GraphDiagram(
            "Diagram Different Orientation",
            generator_cls=generator_cls,
            is_vertical=is_vertical,
        )
        n1 = sd.node("Node #1")
        n2 = sd.node("Node #2")
        n1.go_to(n2)
        n3 = sd.node("Node #3")
        n2.go_to(n3)
        n4 = sd.node("Node #4")
        n3.go_to(n4)
        n4.go_to(n1, "We are rolling")
        assert str(sd) == output
