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
        """Some places allow line break as <br/>"""
        return string.replace("\n", "<br/>")

    @staticmethod
    def _remove_line_breaks(string: str) -> str:
        """Some places do not allow line breaks, replace these with just a plane space"""
        return string.replace("\n", " ")

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: list[
            SequenceDiagramParticipant
        ] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: list[Step] = sequence_diagram._SequenceDiagram__sequence  # noqa

        first_case = False
        last_targeted_participant: SequenceDiagramParticipant | None = None
        if participants:
            last_targeted_participant = participants[0]

        aliases = {
            participant: f"p{index + 1}"
            for index, participant in enumerate(participants)
        }

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

        participant_types_map = {
            "default": "participant",
            "actor": "actor",
            "boundary": "participant",
            "control": "participant",
            "entity": "participant",
        }

        generated = f"sequenceDiagram\nTitle: {cls._remove_line_breaks(sequence_diagram.title)}\n"
        for participant in participants:
            generated += f"{participant_types_map[participant.type_]} {aliases[participant]} as {cls._line_break(participant.title)}\n"

        for step in sequence:
            if isinstance(step, ParticipantActivationControl):
                if step.is_active:
                    generated += f"activate {aliases[step.participant]}\n"
                else:
                    generated += f"deactivate {aliases[step.participant]}\n"

            if isinstance(step, ForwardStep):
                generated += f"{aliases[step.from_participant]}->>{aliases[step.to_participant]}: {cls._line_break(step.text)}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, ReturnStep):
                generated += f"{aliases[step.from_participant]}-->>{aliases[step.to_participant]}: {cls._line_break(step.text)}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, GroupControl):
                # NB: the Mermaid does not have the native "group" as Plant UML does, for example,
                # so the reasonable workaround would be here creation of the background rectangle + some note
                if step.is_active:
                    generated += f"rect {next(group_colors)}\n"
                    generated += f"note right of {aliases[last_targeted_participant]}: {cls._line_break(step.text)}\n"
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

            if isinstance(step, NoteStep):
                generated += f"note right of {aliases[last_targeted_participant]}: {cls._line_break(step.text)}\n"

        return generated
