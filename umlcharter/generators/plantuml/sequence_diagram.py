import typing

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


class PlantUMLSequenceDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        """Some places allow line break as \n"""
        return string.replace("\n", "\\n")

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: typing.Dict[
            typing.Optional[str], typing.List[SequenceDiagramParticipant]
        ] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: typing.List[
            Step
        ] = sequence_diagram._SequenceDiagram__sequence  # noqa

        first_case = False
        deactivation_just_has_happened_for_step: SequenceDiagramParticipant | None = (
            None
        )
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

        generated = f"@startuml\ntitle: {cls._line_break(sequence_diagram.title)}\n"
        for group_title, group_participants in participants.items():
            if group_title:
                generated += f'box "{cls._line_break(group_title)}"\n'

            for participant in group_participants:
                # define initial last targeted participant
                if not last_targeted_participant:
                    last_targeted_participant = participant

                aliases[participant] = f"p{aliases_counter}"
                aliases_counter += 1

                generated += f'{participant_types_map[participant.type_]} "{cls._line_break(participant.title)}" as {aliases[participant]}\n'

            if group_title:
                generated += "end box\n"

        for step in sequence:
            if isinstance(step, ParticipantActivationControl):
                if step.is_active:
                    # NB! The magic of PlantUML:
                    # you cannot activate the participant right after you have deactivated it,
                    # so you have to place something in between.
                    # Luckily, PlantUML supports invisible messages we can use as separator to split the sequence
                    if (
                        deactivation_just_has_happened_for_step
                        and step.participant == deactivation_just_has_happened_for_step
                    ):
                        generated += f"{aliases[step.participant]} -[hidden]-> {aliases[step.participant]}\n"
                    generated += f"activate {aliases[step.participant]}\n"
                    deactivation_just_has_happened_for_step = None
                else:
                    generated += f"deactivate {aliases[step.participant]}\n"
                    deactivation_just_has_happened_for_step = step.participant

            if isinstance(step, ForwardStep):
                generated += f"{aliases[step.from_participant]}->{aliases[step.to_participant]}: {cls._line_break(step.text)}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, ReturnStep):
                generated += f"{aliases[step.from_participant]}-->{aliases[step.to_participant]}: {cls._line_break(step.text)}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, GroupControl):
                if step.is_active:
                    generated += f"group {cls._line_break(step.text)}\n"
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

        return generated + "@enduml\n"
