import itertools

from umlcharter.charts.sequence_diagram import (
    SequenceDiagram,
    SequenceDiagramParticipant,
    Step,
    ParticipantActivationControl,
    ForwardStep,
    GroupControl,
    LoopControl,
    ConditionControl,
    CaseControl,
    ReturnStep,
    NoteStep,
)


class MermaidSequenceDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        return string.replace("\n", "<br/>")

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: list[
            SequenceDiagramParticipant
        ] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: list[Step] = sequence_diagram._SequenceDiagram__sequence  # noqa

        last_targeted_participant: SequenceDiagramParticipant | None = None
        if participants:
            last_targeted_participant = participants[0]

        # iterate over the color groups, so the groups are not overlapping and separately visible
        group_colors = itertools.cycle(
            [
                # some random colors I've picked
                "rgb(121, 210, 166)",
                "rgb(51, 153, 102)",
                "rgb(153, 221, 255)",
                "rgb(51, 187, 255)",
                "rgb(0, 179, 179)",
                "rgb(184, 184, 148)",
            ]
        )

        first_case = False

        generated = f"sequenceDiagram\nTitle: {sequence_diagram.title}\n"
        for participant in participants:
            generated += f"participant {participant.title}\n"

        for step in sequence:
            if isinstance(step, ParticipantActivationControl):
                if step.is_active:
                    generated += f"activate {step.participant.title}\n"
                else:
                    generated += f"deactivate {step.participant.title}\n"

            if isinstance(step, NoteStep):
                generated += f"note right of {last_targeted_participant.title}: {cls._line_break(step.text)}\n"

            if isinstance(step, GroupControl):
                # NB: the Mermaid does not have the native "group" as Plant UML does, for example,
                # so the reasonable workaround would be here creation of the background rectangle + some note
                if step.is_active:
                    generated += f"rect {next(group_colors)}\n"
                    generated += f"note right of {last_targeted_participant.title}: {cls._line_break(step.text)}\n"
                else:
                    generated += "end\n"

            if isinstance(step, LoopControl):
                if step.is_active:
                    generated += f"loop {cls._line_break(step.how_many_iterations)}\n"
                else:
                    generated += "end\n"

            if isinstance(step, ConditionControl):
                if step.is_active:
                    first_case = True
                else:
                    generated += "end\n"
                    first_case = False

            if isinstance(step, CaseControl):
                if step.is_active:
                    if first_case:
                        generated += f"alt {cls._line_break(step.text)}\n"
                        first_case = False
                    else:
                        generated += f"else {cls._line_break(step.text)}\n"

            if isinstance(step, ForwardStep):
                generated += f"{step.from_participant.title}->>{step.to_participant.title}: {cls._line_break(step.text)}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, ReturnStep):
                generated += f"{step.from_participant.title}-->>{step.to_participant.title}: {cls._line_break(step.text)}\n"

        return generated
