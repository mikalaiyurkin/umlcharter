import typing

from umlcharter.charts.sequence_diagram import (
    SequenceDiagram,
    SequenceDiagramParticipant,
    SequenceDiagramParticipantGroup,
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


class SequenceDiagramOrgSequenceDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        """Some places allow line break as \n"""
        return string.replace("\n", "\\n")

    @staticmethod
    def _remove_line_breaks(string: str) -> str:
        """Some places do not allow line breaks, replace these with just a plane space"""
        return string.replace("\n", " ")

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: typing.Dict[
            SequenceDiagramParticipantGroup, typing.List[SequenceDiagramParticipant]
        ] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: typing.List[Step] = (
            sequence_diagram._SequenceDiagram__sequence  # noqa
        )

        first_case = False
        last_targeted_participant: SequenceDiagramParticipant | None = None
        aliases = {}
        aliases_counter = 1

        participant_types_map = {
            "default": "participant",
            "actor": "actor",
            "boundary": "boundary",
            "control": "control",
            "entity": "entity",
        }

        generated = f"title {cls._line_break(sequence_diagram.title)}\n"
        for group, group_participants in participants.items():
            if group.title:
                generated += (
                    f"participantgroup{group.color.as_hex() if group.color else ''} "
                    f"**{cls._line_break(group.title)}**\n"
                )

            for participant in group_participants:
                # define initial last targeted participant
                if not last_targeted_participant:
                    last_targeted_participant = participant

                aliases[participant] = f"p{aliases_counter}"
                aliases_counter += 1

                generated += (
                    f'{participant_types_map[participant.type_]} "{cls._line_break(participant.title)}" as '
                    f"{aliases[participant]}"
                )
                generated += (
                    f"{participant.color.as_hex() if participant.color else ''}\n"
                )

            if group.title:
                generated += "end\n"

        for step in sequence:
            if isinstance(step, ParticipantActivationControl):
                if step.is_active:
                    generated += f"activate {aliases[step.participant]}{step.color.as_hex() if step.color else ''}\n"
                else:
                    generated += f"deactivate {aliases[step.participant]}\n"

            if isinstance(step, ForwardStep):
                generated += (
                    f"{aliases[step.from_participant]}->{aliases[step.to_participant]}: "
                    f"{cls._line_break(step.text)}\n"
                )
                last_targeted_participant = step.to_participant

            if isinstance(step, ReturnStep):
                generated += (
                    f"{aliases[step.from_participant]}-->{aliases[step.to_participant]}: "
                    f"{cls._line_break(step.text)}\n"
                )
                last_targeted_participant = step.to_participant

            if isinstance(step, GroupControl):
                if step.is_active:
                    generated += (
                        f"group{step.color.as_hex() if step.color else ''} "
                        f"[{cls._remove_line_breaks(step.text)}]\n"
                    )
                else:
                    generated += "end\n"

            if isinstance(step, LoopControl):
                if step.is_active:
                    generated += (
                        f"loop{step.color.as_hex() if step.color else ''} "
                        f"{cls._remove_line_breaks(step.how_many_iterations)}\n"
                    )
                else:
                    generated += "end\n"

            if isinstance(step, ConditionControl):
                if step.is_active:
                    generated += f"alt{step.color.as_hex() if step.color else ''}"
                    first_case = True
                else:
                    generated += "end\n"
                    first_case = False

            if isinstance(step, CaseControl):
                if step.is_active:
                    if first_case:
                        generated += f" {cls._remove_line_breaks(step.text)}\n"
                        first_case = False
                    else:
                        generated += f"else {cls._remove_line_breaks(step.text)}\n"

            if isinstance(step, NoteStep):
                generated += (
                    f"note right of {aliases[last_targeted_participant]}{step.color.as_hex() if step.color else ''}: "
                    f"{cls._line_break(step.text)}\n"
                )

        return generated
