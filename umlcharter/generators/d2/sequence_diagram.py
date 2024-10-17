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


class D2SequenceDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        """Some places allow line break as \n"""
        return string.replace("\n", "\\n") or "''"

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: typing.Dict[
            SequenceDiagramParticipantGroup, typing.List[SequenceDiagramParticipant]
        ] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: typing.List[Step] = (
            sequence_diagram._SequenceDiagram__sequence  # noqa
        )

        last_targeted_participant: SequenceDiagramParticipant | None = None
        aliases = {}
        aliases_counter = 1

        participant_types_map = {
            "default": "",
            "actor": "person",
            "boundary": "",
            "control": "",
            "entity": "",
        }

        generated = f"title: {cls._line_break(sequence_diagram.title)} {{\nshape: sequence_diagram\n"
        for _, group_participants in participants.items():
            for participant in group_participants:
                # define initial last targeted participant
                if not last_targeted_participant:
                    last_targeted_participant = participant

                aliases[participant] = f"p{aliases_counter}"
                aliases_counter += 1

                generated += (
                    f"{aliases[participant]}: {cls._line_break(participant.title)} "
                )
                if participant.color or participant_types_map[participant.type_]:
                    generated += "{\n"
                    if participant.color:
                        generated += (
                            f'style: {{fill: "{participant.color.as_hex()}" \n'
                            f'stroke:"{participant.color.as_hex()}" }}\n'
                        )
                    if participant_types_map[participant.type_]:
                        generated += (
                            f"shape: {participant_types_map[participant.type_]}\n"
                        )
                    generated += "}"
                generated += "\n"

        # NB! In D2 the logic of "activation" phases or "spans" works a bit differently, compared to the other DSLs.
        # You have to know that the participant will be activated
        # BEFORE the flow goes under the new participant control.
        # To align the activation representation with the other DSLs, we have to
        # 1. Check if the step is `ForwardStep` to the participant X
        # 2. If right after the `ForwardStep` participant X is activated -
        #   swap these `ForwardStep` & `ParticipantActivationControl`
        new_seq = sequence.copy()
        len_sequence = len(new_seq)
        for index, step in enumerate(new_seq):
            if (
                isinstance(step, ForwardStep)
                and (index + 1) < len_sequence
                and isinstance(new_seq[index + 1], ParticipantActivationControl)
                and new_seq[index + 1].is_active is True
                and step.to_participant is new_seq[index + 1].participant
            ):
                new_seq[index], new_seq[index + 1] = new_seq[index + 1], new_seq[index]

        activation_counter = 0
        custom_element_counter = 1
        for step in new_seq:
            if isinstance(step, ParticipantActivationControl):
                if step.is_active:
                    aliases[step.participant] += f".{activation_counter}"
                    activation_counter += 1
                else:
                    aliases[step.participant] = ".".join(
                        aliases[step.participant].split(".")[:-1]
                    )

            if isinstance(step, ForwardStep):
                generated += (
                    f"{aliases[step.from_participant]} -> "
                    f"{aliases[step.to_participant]}: {cls._line_break(step.text)}\n"
                )
                last_targeted_participant = step.to_participant

            if isinstance(step, ReturnStep):
                generated += (
                    f"{aliases[step.from_participant]} -> "
                    f"{aliases[step.to_participant]}: {cls._line_break(step.text)} {{style.stroke-dash: 3}}\n"
                )
                last_targeted_participant = step.to_participant

            if isinstance(step, NoteStep):
                generated += f'{aliases[last_targeted_participant]}."{cls._line_break(step.text)}"\n'

            if isinstance(step, GroupControl):
                if step.is_active:
                    generated += f"group{custom_element_counter}: \[GROUP\] {cls._line_break(step.text)}: {{"
                    if step.color:
                        generated += f'\nstyle: {{\nfill: "{step.color.as_hex()}" \n}}'
                    generated += "\n"
                    custom_element_counter += 1
                else:
                    generated += "}\n"

            if isinstance(step, LoopControl):
                if step.is_active:
                    generated += f"loop{custom_element_counter}: \[LOOP\] {cls._line_break(step.how_many_iterations)}: {{"
                    if step.color:
                        generated += f'\nstyle: {{\nfill: "{step.color.as_hex()}" \n}}'
                    generated += "\n"
                    custom_element_counter += 1
                else:
                    generated += "}\n"

            if isinstance(step, ConditionControl):
                if step.is_active:
                    generated += f"alt{custom_element_counter}: \[ALT\] {{"
                    if step.color:
                        generated += f'\nstyle: {{\nfill: "{step.color.as_hex()}" \n}}'
                    generated += "\n"
                    custom_element_counter += 1
                else:
                    generated += "}\n"

            if isinstance(step, CaseControl):
                if step.is_active:
                    generated += f"case{custom_element_counter}: \[CASE\] {cls._line_break(step.text)}: {{"
                    if step.color:
                        generated += f'\nstyle: {{\nfill: "{step.color.as_hex()}" \n}}'
                    generated += "\n"
                    custom_element_counter += 1
                else:
                    generated += "}\n"

        return generated + "}\n"
