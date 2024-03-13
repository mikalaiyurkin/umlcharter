import pytest

from charter import SequenceDiagram, Mermaid


class TestSequenceDiagram:

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (
                Mermaid,
                """sequenceDiagram
Title: Diagram Empty
"""
            ),
        )
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
"""
            ),
        )
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
First->>Second: Go to second
activate Second
First->>Third: Go to third
activate Third
Second->>First: Return to first
activate First
deactivate Second
Third->>Fourth: Go to fourth
activate Fourth
deactivate Third
Fourth->>Fourth: Go to self
activate Fourth
deactivate Fourth
Fourth->>First: Return to first
activate First
deactivate Fourth
"""
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
First->>Third: Go to third
Second->>First: Return to first
Third->>Fourth: Go to fourth
Fourth->>Fourth: Go to self
Fourth->>First: Return to first
"""
            ),
        )
    )
    def test_simple_interaction_and_auto_activation(self, generator_cls, auto_activation, output):
        sd = SequenceDiagram("Diagram Interaction and Auto Activation", generator_cls=generator_cls, auto_activation=auto_activation)
        first = sd.participant("First")
        second = sd.participant("Second")
        third = sd.participant("Third")
        fourth = sd.participant("Fourth")

        first.do("Go to second", to=second)
        first.do("Go to third", to=third)
        second.do("Return to first", to=first)
        third.do("Go to fourth", to=fourth)
        fourth.do("Go to self", to=fourth)
        fourth.do("Return to first", to=first)
        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (Mermaid, """sequenceDiagram
Title: Diagram Interaction and Manual Activation
participant First
participant Second
activate First
First->>Second: Go to second
activate Second
Second->>Second: Go to self
Second->>First: Return to first
deactivate Second
deactivate First
"""),
        )
    )
    def test_simple_interaction_and_manual_activation(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Interaction and Manual Activation", generator_cls=generator_cls, auto_activation=False)
        first = sd.participant("First")
        second = sd.participant("Second")

        with first.activate():
            first.do("Go to second", second)
            with second.activate():
                second.do("Go to self", second)
                second.do("Return to first", first)

        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
            (Mermaid, """sequenceDiagram
Title: Diagram Interaction and Grouping
participant First
participant Second
participant Third
rect rgb(121, 210, 166, 0.5)
note right of First: Group enclosing everything
First->>Second: Go to second
activate Second
rect rgb(51, 153, 102, 0.5)
note right of Second: Group enclosing interaction between second and third
Second->>Third: Go to third
activate Third
deactivate Second
Third->>Second: Return to second
activate Second
deactivate Third
end
Second->>First: Return to first
activate First
deactivate Second
end
"""),
        ),
    )
    def test_grouping(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Interaction and Grouping", generator_cls=generator_cls)

        first = sd.participant("First")
        second = sd.participant("Second")
        third = sd.participant("Third")

        with sd.group("Group enclosing everything"):
            first.do("Go to second", second)
            with sd.group("Group enclosing interaction between second and third"):
                second.do("Go to third", third)
                third.do("Return to second", second)
            second.do("Return to first", first)
        assert sd.generate() == output

    @pytest.mark.parametrize(
        "generator_cls,output",
        (
                (Mermaid, """sequenceDiagram
Title: Diagram Interaction and Loops
participant First
participant Second
loop Infinite loop
First->>Second: Send request to second
activate Second
loop Repeat until available
Second->>Second: Check internal state
activate Second
deactivate Second
end
Second->>First: Return response
activate First
deactivate Second
end
"""),
        ),
    )
    def test_loop(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Interaction and Loops", generator_cls=generator_cls)

        first = sd.participant("First")
        second = sd.participant("Second")

        with sd.loop("Infinite loop"):
            first.do("Send request to second", second)
            with sd.loop("Repeat until available"):
                second.do("Check internal state", second)
            second.do("Return response", first)

        assert sd.generate() == output

    @pytest.mark.parametrize(
            "generator_cls,output",
            (
                    (Mermaid, """sequenceDiagram
Title: Diagram Interaction and Conditions
participant First
participant Second
participant Third
activate First
First->>First: Self-check
deactivate First
alt Found something interesting
activate First
First->>Second: Call second
activate Second
Second->>First: Return something interesting
deactivate Second
deactivate First
else Nothing interesting
activate First
First->>Third: Call third
activate Third
Third->>First: Return something boring
deactivate Third
deactivate First
end
"""),
            ),
    )
    def test_condition(self, generator_cls, output):
        sd = SequenceDiagram("Diagram Interaction and Conditions", generator_cls=generator_cls, auto_activation=False)

        first = sd.participant("First")
        second = sd.participant("Second")
        third = sd.participant("Third")

        with first.activate():
            first.do("Self-check", first)
        with sd.condition():
            with sd.case("Found something interesting"):
                with first.activate():
                    first.do("Call second", second)
                    with second.activate():
                        second.do("Return something interesting", first)
            with sd.case("Nothing interesting"):
                with first.activate():
                    first.do("Call third", third)
                    with third.activate():
                        third.do("Return something boring", first)
        assert sd.generate() == output
