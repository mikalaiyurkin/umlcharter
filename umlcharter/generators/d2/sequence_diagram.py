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


class D2SequenceDiagram:
    @staticmethod
    def _line_break(string: str) -> str:
        """Some places allow line break as \n"""
        return string.replace("\n", "\\n") or "''"

    @classmethod
    def generate(cls, sequence_diagram: SequenceDiagram) -> str:
        participants: list[
            SequenceDiagramParticipant
        ] = sequence_diagram._SequenceDiagram__participants  # noqa
        sequence: list[Step] = sequence_diagram._SequenceDiagram__sequence  # noqa

        last_targeted_participant: SequenceDiagramParticipant | None = None
        if participants:
            last_targeted_participant = participants[0]

        aliases = {
            participant: f"p{index + 1}"
            for index, participant in enumerate(participants)
        }

        participant_types_map = {
            "default": "",
            "actor": "{shape: person}",
            "boundary": "",
            "control": "",
            "entity": "",
        }

        generated = f"title: {cls._line_break(sequence_diagram.title)} {{\nshape: sequence_diagram\n"
        for participant in participants:
            generated += f"{aliases[participant]}: {cls._line_break(participant.title)} {participant_types_map[participant.type_]}\n"

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
        alt_counter = 1
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
                generated += f"{aliases[step.from_participant]} -> {aliases[step.to_participant]}: {cls._line_break(step.text)}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, ReturnStep):
                generated += f"{aliases[step.from_participant]} -> {aliases[step.to_participant]}: {cls._line_break(step.text)} {{style.stroke-dash: 3}}\n"
                last_targeted_participant = step.to_participant

            if isinstance(step, GroupControl):
                if step.is_active:
                    generated += f"{cls._line_break(step.text)}: {{\n"
                else:
                    generated += "}\n"

            if isinstance(step, LoopControl):
                if step.is_active:
                    generated += f'LOOP {cls._line_break(step.how_many_iterations)}: {{\nstyle: {{\nborder-radius: 50\nfill: "#ffdfbf"\n}}\n'
                else:
                    generated += "}\n"

            if isinstance(step, ConditionControl):
                if step.is_active:
                    generated += (
                        f'alt{alt_counter}: ALT {{\nstyle: {{\nfill: "#ffdfbf"\n}}\n'
                    )
                    alt_counter += 1
                else:
                    generated += "}\n"

            if isinstance(step, CaseControl):
                if step.is_active:
                    generated += f'CASE {cls._line_break(step.text)}: {{\nstyle: {{\nfill: "#f6c5c2"\n}}\n'
                else:
                    generated += "}\n"

            if isinstance(step, NoteStep):
                generated += f'{aliases[last_targeted_participant]}."{cls._line_break(step.text)}"\n'

        return generated + "}\n"
