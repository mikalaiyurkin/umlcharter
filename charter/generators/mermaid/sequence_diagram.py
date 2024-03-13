import itertools

from charter.charts.sequence_diagram import (
    SequenceDiagram,
    SequenceDiagramParticipant,
    Step,
    ParticipantActivationControl,
    SequenceStep,
    GroupControl,
    LoopControl,
    ConditionControl,
    CaseControl
)


class MermaidSequenceDiagram:

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: list[SequenceDiagramParticipant] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: list[Step] = sequence_diagram._SequenceDiagram__sequence  # noqa

        last_targeted_participant: SequenceDiagramParticipant | None = None
        if participants:
            last_targeted_participant = participants[0]

        # iterate over the color groups, so the groups are not overlapping and separately visible
        group_colors = itertools.cycle([
            # some random colors I've picked
            "rgb(121, 210, 166, 0.5)",
            "rgb(51, 153, 102, 0.5)",
            "rgb(153, 221, 255, 0.5)",
            "rgb(51, 187, 255, 0.5)",
            "rgb(0, 179, 179, 0.5)",
            "rgb(184, 184, 148, 0.5)",
        ])

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

            if isinstance(step, GroupControl):
                # NB: the Mermaid does not have the native "group" as Plant UML does, for example,
                # so the reasonable workaround would be here creation of the background rectangle + some note
                if step.is_active:
                    generated += f"rect {next(group_colors)}\n"
                    generated += f"note right of {last_targeted_participant.title}: {step.text}\n"
                else:
                    generated += "end\n"

            if isinstance(step, LoopControl):
                if step.is_active:
                    generated += f"loop {step.how_many_iterations}\n"
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
                        generated += f"alt {step.text}\n"
                        first_case = False
                    else:
                        generated += f"else {step.text}\n"

            if isinstance(step, SequenceStep):
                generated += f"{step.from_participant.title}->>{step.to_participant.title}: {step.text}\n"
                last_targeted_participant = step.to_participant

        return generated
