from unittest.mock import Mock

import pytest

from umlcharter import SequenceDiagram, Mermaid, PlantUML, D2, SequenceDiagramOrg


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
            (
                D2,
                """title: Diagram Empty {
shape: sequence_diagram
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Empty
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
            (
                D2,
                """title: Diagram Only Participants {
shape: sequence_diagram
p1: First 
p2: Second 
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Only Participants
participant "First" as p1
participant "Second" as p2
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
            (
                D2,
                True,
                """title: Diagram Interaction\\nand Auto Activation {
shape: sequence_diagram
p1: First\\nParticipant 
p2: Second\\nParticipant 
p3: Third\\nParticipant 
p4: Fourth\\nParticipant 
p1.0 -> p2.1: Go to second
p2.1 -> p1.0: Return to first {style.stroke-dash: 3}
p1.2 -> p3.3: Go to third
p3.3 -> p4.4: Go to fourth
p4.4 -> p4.4: Go to self
p4.4 -> p3.3: Return to third {style.stroke-dash: 3}
p3.3 -> p1.2: Return to first {style.stroke-dash: 3}
}
""",
            ),
            (
                D2,
                False,
                """title: Diagram Interaction\\nand Auto Activation {
shape: sequence_diagram
p1: First\\nParticipant 
p2: Second\\nParticipant 
p3: Third\\nParticipant 
p4: Fourth\\nParticipant 
p1 -> p2: Go to second
p2 -> p1: Return to first {style.stroke-dash: 3}
p1 -> p3: Go to third
p3 -> p4: Go to fourth
p4 -> p4: Go to self
p4 -> p3: Return to third {style.stroke-dash: 3}
p3 -> p1: Return to first {style.stroke-dash: 3}
}
""",
            ),
            (
                SequenceDiagramOrg,
                True,
                """title Diagram Interaction\\nand Auto Activation
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
""",
            ),
            (
                SequenceDiagramOrg,
                False,
                """title Diagram Interaction\\nand Auto Activation
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
            (
                D2,
                """title: Diagram Interaction and Manual Activation {
shape: sequence_diagram
p1: First 
p2: Second 
p1.0 -> p2.1: Go to second
p2.1 -> p2.1: Go to self
p2.1 -> p1.0: Return to first {style.stroke-dash: 3}
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Interaction and Manual Activation
participant "First" as p1
participant "Second" as p2
activate p1
p1->p2: Go to second
activate p2
p2->p2: Go to self
p2-->p1: Return to first
deactivate p2
deactivate p1
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
group Group enclosing interaction\\nbetween second and third
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
            (
                D2,
                """title: Diagram Interaction and Grouping {
shape: sequence_diagram
p1: First 
p2: Second 
p3: Third 
Group enclosing everything: {
p1.0 -> p2.1: Go to second
Group enclosing interaction\\nbetween second and third: {
p2.1 -> p3.2: Go to third
p3.2 -> p2.1: Return to second {style.stroke-dash: 3}
}
p2.1 -> p1.0: Return to first {style.stroke-dash: 3}
}
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Interaction and Grouping
participant "First" as p1
participant "Second" as p2
participant "Third" as p3
group [Group enclosing everything]
activate p1
p1->p2: Go to second
activate p2
group [Group enclosing interaction between second and third]
p2->p3: Go to third
activate p3
p3-->p2: Return to second
deactivate p3
end
p2-->p1: Return to first
deactivate p2
deactivate p1
end
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
            (
                D2,
                """title: Diagram Interaction and Loops {
shape: sequence_diagram
p1: First 
p2: Second 
LOOP Infinite loop: {
style: {
border-radius: 50
fill: "#ffdfbf"
}
p1.0 -> p2.1: Send request to second
LOOP Repeat\\nuntil available: {
style: {
border-radius: 50
fill: "#ffdfbf"
}
p2.1 -> p2.1: Check internal state
}
p2.1 -> p1.0: Return response {style.stroke-dash: 3}
}
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Interaction and Loops
participant "First" as p1
participant "Second" as p2
loop Infinite loop
activate p1
p1->p2: Send request to second
activate p2
loop Repeat until available
p2->p2: Check internal state
end
p2-->p1: Return response
deactivate p2
deactivate p1
end
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
            (
                D2,
                """title: Diagram Interaction and Conditions {
shape: sequence_diagram
p1: Viewer 
p2: Drama 
p3: Comedy 
p1.0 -> p1.0: What would I like to watch today?
alt1: ALT {
style: {
fill: "#ffdfbf"
}
CASE Want a drama: {
style: {
fill: "#f6c5c2"
}
p1.1 -> p2.2: Watch drama
p2.2 -> p1.1: Tears and sadness {style.stroke-dash: 3}
}
CASE Want a comedy: {
style: {
fill: "#f6c5c2"
}
p1.3 -> p3.4: Watch comedy
p3.4 -> p1.3: Laugh a lot {style.stroke-dash: 3}
}
}
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Interaction and Conditions
participant "Viewer" as p1
participant "Drama" as p2
participant "Comedy" as p3
activate p1
p1->p1: What would I like to watch today?
deactivate p1
alt Want a drama
activate p1
p1->p2: Watch drama
activate p2
p2-->p1: Tears and sadness
deactivate p2
deactivate p1
else Want a comedy
activate p1
p1->p3: Watch comedy
activate p3
p3-->p1: Laugh a lot
deactivate p3
deactivate p1
end
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
            (
                D2,
                """title: Diagram Interaction and Notes {
shape: sequence_diagram
p1: Batman 
p2: Bandit 
p1."Batman is throwing\\na batarang at the bandit"
p1.0 -> p2.1: Pheeeeeeu!
p2.1."Batman has missed!"
p2.1 -> p1.0: A bad day\\nfor the Gotham :( {style.stroke-dash: 3}
p1."Batman is sad now"
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Diagram Interaction and Notes
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
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Empty Transitions between Participants
participant p1 as First
participant p2 as Second
activate p1
p1->>p2: 
activate p2
p2-->>p1: 
deactivate p2
deactivate p1
""",
            ),
            (
                PlantUML,
                """@startuml
title: Empty Transitions between Participants
participant "First" as p1
participant "Second" as p2
activate p1
p1->p2: 
activate p2
p2-->p1: 
deactivate p2
deactivate p1
@enduml
""",
            ),
            (
                D2,
                """title: Empty Transitions between Participants {
shape: sequence_diagram
p1: First 
p2: Second 
p1.0 -> p2.1: ''
p2.1 -> p1.0: '' {style.stroke-dash: 3}
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Empty Transitions between Participants
participant "First" as p1
participant "Second" as p2
activate p1
p1->p2: 
activate p2
p2-->p1: 
deactivate p2
deactivate p1
""",
            ),
        ),
    )
    def test_empty_transitions(self, generator_cls, output):
        sd = SequenceDiagram("Empty Transitions between Participants", generator_cls)
        first = sd.participant("First")
        second = sd.participant("Second")

        first.go_to(second).return_to(first)
        assert str(sd) == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Participant types, according to ECB
actor p1 as Actor
participant p2 as Boundary
participant p3 as Control
participant p4 as Entity
activate p1
p1->>p2: Do something
activate p2
p2->>p3: Do something
activate p3
p3->>p4: Do something
activate p4
p4-->>p3: Return
deactivate p4
p3-->>p2: Return
deactivate p3
p2-->>p1: Return
deactivate p2
deactivate p1
""",
            ),
            (
                PlantUML,
                """@startuml
title: Participant types, according to ECB
actor "Actor" as p1
boundary "Boundary" as p2
control "Control" as p3
entity "Entity" as p4
activate p1
p1->p2: Do something
activate p2
p2->p3: Do something
activate p3
p3->p4: Do something
activate p4
p4-->p3: Return
deactivate p4
p3-->p2: Return
deactivate p3
p2-->p1: Return
deactivate p2
deactivate p1
@enduml
""",
            ),
            (
                D2,
                """title: Participant types, according to ECB {
shape: sequence_diagram
p1: Actor {shape: person}
p2: Boundary 
p3: Control 
p4: Entity 
p1.0 -> p2.1: Do something
p2.1 -> p3.2: Do something
p3.2 -> p4.3: Do something
p4.3 -> p3.2: Return {style.stroke-dash: 3}
p3.2 -> p2.1: Return {style.stroke-dash: 3}
p2.1 -> p1.0: Return {style.stroke-dash: 3}
}
""",
            ),
            (
                SequenceDiagramOrg,
                """title Participant types, according to ECB
actor "Actor" as p1
boundary "Boundary" as p2
control "Control" as p3
entity "Entity" as p4
activate p1
p1->p2: Do something
activate p2
p2->p3: Do something
activate p3
p3->p4: Do something
activate p4
p4-->p3: Return
deactivate p4
p3-->p2: Return
deactivate p3
p2-->p1: Return
deactivate p2
deactivate p1
""",
            ),
        ),
    )
    def test_ecb_types_for_participants(self, generator_cls, output):
        sd = SequenceDiagram("Participant types, according to ECB", generator_cls)
        actor = sd.participant("Actor").as_actor()
        boundary = sd.participant("Boundary").as_boundary()
        control = sd.participant("Control").as_control()
        entity = sd.participant("Entity").as_entity()

        actor.go_to(boundary, "Do something").go_to(control, "Do something").go_to(
            entity, "Do something"
        )
        entity.return_to(control, "Return").return_to(boundary, "Return").return_to(
            actor, "Return"
        )

        assert str(sd) == output

    def test_same_participants(self):
        sd = SequenceDiagram("Same participants", Mock)

        sd.participant("Same")
        with pytest.raises(AssertionError):
            sd.participant(
                "Same"
            )  # it is forbidden to have multiple participants with the same label

    def test_forbid_return_when_not_auto_activated(self):
        sd = SequenceDiagram(
            "Return without auto-activation", Mock, auto_activation=False
        )

        first = sd.participant("First")
        second = sd.participant("Second")

        first.go_to(second)
        with pytest.raises(AssertionError):
            sd.return_()

    def test_forbid_return_to_nowhere(self):
        sd = SequenceDiagram("Return to nowhere", Mock)

        with pytest.raises(AssertionError):
            sd.return_()

    def test_force_case_after_condition(self):
        sd = SequenceDiagram("Violated order of condition and case #1", Mock)
        first = sd.participant("First")
        second = sd.participant("Second")

        with pytest.raises(AssertionError):
            with sd.condition():
                first.go_to(second, "Do smth")

    def test_force_case_inside_condition(self):
        sd = SequenceDiagram("Violated order of condition and case #2", Mock)

        with pytest.raises(AssertionError):
            with sd.case("A case"):
                pass

    @pytest.mark.parametrize(
        "callable_", ("as_actor", "as_boundary", "as_control", "as_entity")
    )
    def test_force_participant_type_being_set_only_once(self, callable_):
        sd = SequenceDiagram("Participant type can be set only once", Mock)

        a = sd.participant("Someone")
        a.type_ = "SET TO SOMETHING ELSE BUT NOT DEFAULT"
        with pytest.raises(AssertionError):
            getattr(a, callable_)()

    @pytest.mark.parametrize(
        "from_,to_",
        (
            ("actor", "actor"),
            ("actor", "control"),
            ("actor", "entity"),
            ("boundary", "boundary"),
            ("boundary", "entity"),
            ("control", "actor"),
            ("entity", "actor"),
            ("entity", "boundary"),
        ),
    )
    def test_only_certain_forward_interactions_are_available(self, from_, to_):
        sd = SequenceDiagram("Not available interactions", Mock)

        a = sd.participant("a")
        b = sd.participant("b")

        a.type_ = from_
        b.type_ = to_

        with pytest.raises(AssertionError):
            a.go_to(b, "Do something")

    @pytest.mark.parametrize(
        "from_,to_",
        (
            ("actor", "actor"),
            ("actor", "control"),
            ("actor", "entity"),
            ("boundary", "boundary"),
            ("boundary", "entity"),
            ("control", "actor"),
            ("entity", "actor"),
            ("entity", "boundary"),
        ),
    )
    def test_only_certain_return_interactions_are_available(self, from_, to_):
        sd = SequenceDiagram("Not available interactions", Mock)

        a = sd.participant("a")
        b = sd.participant("b")

        a.type_ = from_
        b.type_ = to_

        with pytest.raises(AssertionError):
            a.return_to(b, "Do something")
