import pytest

from umlcharter import SequenceDiagram, Mermaid


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
        ),
    )
    def test_no_participants(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Empty", generator_cls=generator_cls)
        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Only Participants
participant First
participant Second
""",
            ),
        ),
    )
    def test_only_participants(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Only Participants", generator_cls=generator_cls)
        sd.participant("First")
        sd.participant("Second")
        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,auto_activation,output",
        (
            (
                Mermaid,
                True,
                """sequenceDiagram
Title: Diagram Interaction and Auto Activation
participant First
participant Second
participant Third
participant Fourth
activate First
First->>Second: Go to second
activate Second
Second-->>First: Return to first
deactivate Second
deactivate First
activate First
First->>Third: Go to third
activate Third
Third->>Fourth: Go to fourth
activate Fourth
Fourth->>Fourth: Go to self
Fourth-->>Third: Return to third
deactivate Fourth
Third-->>First: Return to first
deactivate Third
deactivate First
""",
            ),
            (
                Mermaid,
                False,
                """sequenceDiagram
Title: Diagram Interaction and Auto Activation
participant First
participant Second
participant Third
participant Fourth
First->>Second: Go to second
Second-->>First: Return to first
First->>Third: Go to third
Third->>Fourth: Go to fourth
Fourth->>Fourth: Go to self
Fourth-->>Third: Return to third
Third-->>First: Return to first
""",
            ),
        ),
    )
    def test_simple_interaction_and_auto_activation(
        self, generator_cls, auto_activation, output
    ):
        sd = SequenceDiagram(
            "Diagram Interaction and Auto Activation",
            generator_cls=generator_cls,
            auto_activation=auto_activation,
        )
        first = sd.participant("First")
        second = sd.participant("Second")
        third = sd.participant("Third")
        fourth = sd.participant("Fourth")

        first.go_to(second, "Go to second").return_to(first, "Return to first")

        first.go_to(third, "Go to third").go_to(fourth, "Go to fourth").go_to(
            fourth, "Go to self"
        ).return_to(third, "Return to third").return_to(first, "Return to first")
        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Manual Activation
participant First
participant Second
activate First
First->>Second: Go to second
activate Second
Second->>Second: Go to self
Second-->>First: Return to first
deactivate Second
deactivate First
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

        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Grouping
participant First
participant Second
participant Third
rect rgb(121, 210, 166)
note right of First: Group enclosing everything
activate First
First->>Second: Go to second
activate Second
rect rgb(51, 153, 102)
note right of Second: Group enclosing interaction between second and third
Second->>Third: Go to third
activate Third
Third-->>Second: Return to second
deactivate Third
end
Second-->>First: Return to first
deactivate Second
deactivate First
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
            with sd.group("Group enclosing interaction between second and third"):
                second.go_to(third, "Go to third").return_to(second, "Return to second")
            second.return_to(first, "Return to first")
        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Loops
participant First
participant Second
loop Infinite loop
activate First
First->>Second: Send request to second
activate Second
loop Repeat until available
Second->>Second: Check internal state
end
Second-->>First: Return response
deactivate Second
deactivate First
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
            with sd.loop("Repeat until available"):
                second.go_to(second, "Check internal state")
            sd.return_("Return response")

        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Interaction and Conditions
participant Viewer
participant Drama
participant Comedy
activate Viewer
Viewer->>Viewer: What would I like to watch today?
deactivate Viewer
alt Want a drama
activate Viewer
Viewer->>Drama: Watch drama
activate Drama
Drama-->>Viewer: Tears and sadness
deactivate Drama
deactivate Viewer
else Want a comedy
activate Viewer
Viewer->>Comedy: Watch comedy
activate Comedy
Comedy-->>Viewer: Laugh a lot
deactivate Comedy
deactivate Viewer
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
        assert sd.generate() == output
