import pytest

from umlcharter import SequenceDiagram, Mermaid, PlantUML


class TestSequenceDiagram:
    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Empty
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Empty
@enduml
""",
            ),
        ),
    )
    def test_no_participants(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Empty", generator_cls=generator_cls)
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Only Participants
participant p1 as First
participant p2 as Second
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Only Participants
participant "First" as p1
participant "Second" as p2
@enduml
""",
            ),
        ),
    )
    def test_only_participants(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Only Participants", generator_cls=generator_cls)
        sd.participant("First")
        sd.participant("Second")
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,auto_activation,output",
        (
            (
                Mermaid,
                True,
                """sequenceDiagram
Title: Diagram Interaction and Auto Activation
participant p1 as First<br/>Participant
participant p2 as Second<br/>Participant
participant p3 as Third<br/>Participant
participant p4 as Fourth<br/>Participant
activate p1
p1->>p2: Go to second
activate p2
p2-->>p1: Return to first
deactivate p2
deactivate p1
activate p1
p1->>p3: Go to third
activate p3
p3->>p4: Go to fourth
activate p4
p4->>p4: Go to self
p4-->>p3: Return to third
deactivate p4
p3-->>p1: Return to first
deactivate p3
deactivate p1
""",
            ),
            (
                Mermaid,
                False,
                """sequenceDiagram
Title: Diagram Interaction and Auto Activation
participant p1 as First<br/>Participant
participant p2 as Second<br/>Participant
participant p3 as Third<br/>Participant
participant p4 as Fourth<br/>Participant
p1->>p2: Go to second
p2-->>p1: Return to first
p1->>p3: Go to third
p3->>p4: Go to fourth
p4->>p4: Go to self
p4-->>p3: Return to third
p3-->>p1: Return to first
""",
            ),
            (
                PlantUML,
                True,
                """@startuml
title: Diagram Interaction\\nand Auto Activation
participant "First\\nParticipant" as p1
participant "Second\\nParticipant" as p2
participant "Third\\nParticipant" as p3
participant "Fourth\\nParticipant" as p4
activate p1
p1->p2: Go to second
activate p2
p2-->p1: Return to first
deactivate p2
deactivate p1
p1 -[hidden]-> p1
activate p1
p1->p3: Go to third
activate p3
p3->p4: Go to fourth
activate p4
p4->p4: Go to self
p4-->p3: Return to third
deactivate p4
p3-->p1: Return to first
deactivate p3
deactivate p1
@enduml
""",
            ),
            (
                PlantUML,
                False,
                """@startuml
title: Diagram Interaction\\nand Auto Activation
participant "First\\nParticipant" as p1
participant "Second\\nParticipant" as p2
participant "Third\\nParticipant" as p3
participant "Fourth\\nParticipant" as p4
p1->p2: Go to second
p2-->p1: Return to first
p1->p3: Go to third
p3->p4: Go to fourth
p4->p4: Go to self
p4-->p3: Return to third
p3-->p1: Return to first
@enduml
""",
            ),
        ),
    )
    def test_simple_interaction_and_auto_activation(
        self, generator_cls, auto_activation, output
    ):
        sd = SequenceDiagram(
            "Diagram Interaction\nand Auto Activation",
            generator_cls=generator_cls,
            auto_activation=auto_activation,
        )
        first = sd.participant("First\nParticipant")
        second = sd.participant("Second\nParticipant")
        third = sd.participant("Third\nParticipant")
        fourth = sd.participant("Fourth\nParticipant")

        first.go_to(second, "Go to second").return_to(first, "Return to first")

        first.go_to(third, "Go to third").go_to(fourth, "Go to fourth").go_to(
            fourth, "Go to self"
        ).return_to(third, "Return to third").return_to(first, "Return to first")
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Manual Activation
participant p1 as First
participant p2 as Second
activate p1
p1->>p2: Go to second
activate p2
p2->>p2: Go to self
p2-->>p1: Return to first
deactivate p2
deactivate p1
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Interaction and Manual Activation
participant "First" as p1
participant "Second" as p2
activate p1
p1->p2: Go to second
activate p2
p2->p2: Go to self
p2-->p1: Return to first
deactivate p2
deactivate p1
@enduml
""",
            ),
        ),
    )
    def test_simple_interaction_and_manual_activation(self, generator_cls, output):
        sd = SequenceDiagram(
            "Diagram Interaction and Manual Activation",
            generator_cls=generator_cls,
            auto_activation=False,
        )
        first = sd.participant("First")
        second = sd.participant("Second")

        with first.activate():
            first.go_to(second, "Go to second")
            with second.activate():
                second.go_to(second, "Go to self")
                second.return_to(first, "Return to first")

        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Grouping
participant p1 as First
participant p2 as Second
participant p3 as Third
rect rgb(121, 210, 166)
note right of p1: Group enclosing everything
activate p1
p1->>p2: Go to second
activate p2
rect rgb(51, 153, 102)
note right of p2: Group enclosing interaction<br/>between second and third
p2->>p3: Go to third
activate p3
p3-->>p2: Return to second
deactivate p3
end
p2-->>p1: Return to first
deactivate p2
deactivate p1
end
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Interaction and Grouping
participant "First" as p1
participant "Second" as p2
participant "Third" as p3
group Group enclosing everything
activate p1
p1->p2: Go to second
activate p2
group Group enclosing interaction\nbetween second and third
p2->p3: Go to third
activate p3
p3-->p2: Return to second
deactivate p3
end
p2-->p1: Return to first
deactivate p2
deactivate p1
end
@enduml
""",
            ),
        ),
    )
    def test_grouping(self, generator_cls, output):
        sd = SequenceDiagram(
            "Diagram Interaction and Grouping", generator_cls=generator_cls
        )

        first = sd.participant("First")
        second = sd.participant("Second")
        third = sd.participant("Third")

        with sd.group("Group enclosing everything"):
            first.go_to(second, "Go to second")
            with sd.group("Group enclosing interaction\nbetween second and third"):
                second.go_to(third, "Go to third").return_to(second, "Return to second")
            second.return_to(first, "Return to first")
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Loops
participant p1 as First
participant p2 as Second
loop Infinite loop
activate p1
p1->>p2: Send request to second
activate p2
loop Repeat<br/>until available
p2->>p2: Check internal state
end
p2-->>p1: Return response
deactivate p2
deactivate p1
end
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Interaction and Loops
participant "First" as p1
participant "Second" as p2
loop Infinite loop
activate p1
p1->p2: Send request to second
activate p2
loop Repeat\\nuntil available
p2->p2: Check internal state
end
p2-->p1: Return response
deactivate p2
deactivate p1
end
@enduml
""",
            ),
        ),
    )
    def test_loop(self, generator_cls, output):
        sd = SequenceDiagram(
            "Diagram Interaction and Loops", generator_cls=generator_cls
        )

        first = sd.participant("First")
        second = sd.participant("Second")

        with sd.loop("Infinite loop"):
            first.go_to(second, "Send request to second")
            with sd.loop("Repeat\nuntil available"):
                second.go_to(second, "Check internal state")
            sd.return_("Return response")

        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Conditions
participant p1 as Viewer
participant p2 as Drama
participant p3 as Comedy
activate p1
p1->>p1: What would I like to watch today?
deactivate p1
alt Want a drama
activate p1
p1->>p2: Watch drama
activate p2
p2-->>p1: Tears and sadness
deactivate p2
deactivate p1
else Want a comedy
activate p1
p1->>p3: Watch comedy
activate p3
p3-->>p1: Laugh a lot
deactivate p3
deactivate p1
end
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Interaction and Conditions
participant "Viewer" as p1
participant "Drama" as p2
participant "Comedy" as p3
activate p1
p1->p1: What would I like to watch today?
deactivate p1
alt Want a drama
p1 -[hidden]-> p1
activate p1
p1->p2: Watch drama
activate p2
p2-->p1: Tears and sadness
deactivate p2
deactivate p1
else Want a comedy
p1 -[hidden]-> p1
activate p1
p1->p3: Watch comedy
activate p3
p3-->p1: Laugh a lot
deactivate p3
deactivate p1
end
@enduml
""",
            ),
        ),
    )
    def test_condition(self, generator_cls, output):
        sd = SequenceDiagram(
            "Diagram Interaction and Conditions",
            generator_cls=generator_cls,
            auto_activation=False,
        )

        viewer = sd.participant("Viewer")
        drama = sd.participant("Drama")
        comedy = sd.participant("Comedy")

        with viewer.activate():
            viewer.go_to(viewer, "What would I like to watch today?")
        with sd.condition():
            with sd.case("Want a drama"):
                with viewer.activate():
                    viewer.go_to(drama, "Watch drama")
                    with drama.activate():
                        drama.return_to(viewer, "Tears and sadness")
            with sd.case("Want a comedy"):
                with viewer.activate():
                    viewer.go_to(comedy, "Watch comedy")
                    with comedy.activate():
                        comedy.return_to(viewer, "Laugh a lot")
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Notes
participant p1 as Batman
participant p2 as Bandit
note right of p1: Batman is throwing<br/>a batarang at the bandit
activate p1
p1->>p2: Pheeeeeeu!
activate p2
note right of p2: Batman has missed!
p2-->>p1: A bad day<br/>for the Gotham :(
deactivate p2
deactivate p1
note right of p1: Batman is sad now
""",
            ),
            (
                PlantUML,
                """@startuml
title: Diagram Interaction and Notes
participant "Batman" as p1
participant "Bandit" as p2
note right of p1: Batman is throwing\\na batarang at the bandit
activate p1
p1->p2: Pheeeeeeu!
activate p2
note right of p2: Batman has missed!
p2-->p1: A bad day\\nfor the Gotham :(
deactivate p2
deactivate p1
note right of p1: Batman is sad now
@enduml
""",
            ),
        ),
    )
    def test_note(self, generator_cls, output):
        sd = SequenceDiagram(
            "Diagram Interaction and Notes",
            generator_cls,
        )

        batman = sd.participant("Batman")
        bandit = sd.participant("Bandit")

        sd.note("Batman is throwing\na batarang at the bandit")
        batman.go_to(bandit, "Pheeeeeeu!")
        sd.note("Batman has missed!")
        sd.return_("A bad day\nfor the Gotham :(")
        sd.note("Batman is sad now")
        print(sd)
        assert str(sd) == output
