import typing
from contextlib import contextmanager
from dataclasses import dataclass, field
from itertools import chain

from umlcharter.charts.types import BaseChart, Color, ChartingException
from umlcharter.generators.base import IChartGenerator


@dataclass
class Colored:
    """
    Used to assign the color to the component of the sequence diagram.
    """

    _color: typing.Optional[str]
    color: typing.Optional[Color] = field(init=False)

    def __post_init__(self):
        self.color = Color(self._color) if self._color else None


class Step:
    pass


@dataclass
class Control(Step):
    is_active: bool


@dataclass
class LoopControl(Colored, Control):
    how_many_iterations: typing.Union[str, None] = None


@dataclass
class GroupControl(Colored, Control):
    text: typing.Union[str, None] = None


@dataclass
class CaseControl(Colored, Control):
    text: typing.Union[str, None] = None


@dataclass
class ConditionControl(Colored, Control):
    pass


@dataclass
class ParticipantActivationControl(Colored, Control):
    participant: "SequenceDiagramParticipant"


@dataclass
class ForwardStep(Step):
    text: str
    from_participant: "SequenceDiagramParticipant"
    to_participant: "SequenceDiagramParticipant"


@dataclass
class ReturnStep(Step):
    text: str
    from_participant: "SequenceDiagramParticipant"
    to_participant: "SequenceDiagramParticipant"


@dataclass
class NoteStep(Colored, Step):
    text: str


@dataclass
class SequenceDiagramParticipant(Colored):
    sequence_ref: "SequenceDiagram"
    title: str
    type_: typing.Literal["actor", "boundary", "control", "entity", "default"] = field(
        init=False, default="default"
    )

    def __check_can_set_type(self):
        if self.type_ != "default":
            raise ChartingException(
                f"The type of the participant must be set only once. The current type is '{self.type_}'"
            )

    def as_actor(self):
        self.__check_can_set_type()
        self.type_ = "actor"
        return self

    def as_boundary(self):
        self.__check_can_set_type()
        self.type_ = "boundary"
        return self

    def as_control(self):
        self.__check_can_set_type()
        self.type_ = "control"
        return self

    def as_entity(self):
        self.__check_can_set_type()
        self.type_ = "entity"
        return self

    def __check_if_interaction_is_possible(self, to: "SequenceDiagramParticipant"):
        """
        The check is based on the purpose of the participant, according to the ECB.
        https://en.wikipedia.org/wiki/Entity-control-boundary

        If the type of the participant is not "default" then only the specific interactions are available:

        - Actors may only know and communicate with boundaries.
        - Boundaries may communicate with actors and controls only.
        - Controls may know and communicate with boundaries and entities, and if needed other controls.
        - Entities may only know about other entities but could communicate also with controls.

        |          | default | actor | boundary | control | entity |
        ------------------------------------------------------------
        | default  |    v    |   v   |     v    |    v    |   v    |
        | actor    |    v    |       |     v    |         |        |
        | boundary |    v    |   v   |          |    v    |        |
        | control  |    v    |       |     v    |    v    |   v    |
        | entity   |    v    |       |          |    v    |   v    |
        """
        allowed = (
            {"default", "default"},
            {"default", "actor"},
            {"default", "boundary"},
            {"default", "control"},
            {"default", "entity"},
            {"actor", "boundary"},
            {"boundary", "control"},
            {"control", "control"},
            {"control", "entity"},
            {"entity", "entity"},
        )

        if {self.type_, to.type_} not in allowed:
            raise ChartingException(
                f"The interaction between '{self.type_}' to '{to.type_}' is not allowed. "
                f"Please correct the types of the participants or remove the use of the types "
                f"if you do not really care about it."
            )

    def __add_step(
        self, step: typing.Union[ForwardStep, ReturnStep, ParticipantActivationControl]
    ):
        self.sequence_ref._SequenceDiagram__add_step(step)  # noqa

    def go_to(
        self, to: "SequenceDiagramParticipant", text: str = ""
    ) -> "SequenceDiagramParticipant":
        self.__check_if_interaction_is_possible(to)
        self.__add_step(ForwardStep(text, from_participant=self, to_participant=to))
        return to

    def return_to(
        self, to: "SequenceDiagramParticipant", text: str = ""
    ) -> "SequenceDiagramParticipant":
        self.__check_if_interaction_is_possible(to)
        self.__add_step(ReturnStep(text, from_participant=self, to_participant=to))
        return to

    @contextmanager
    def activate(self, color: typing.Optional[str] = None):
        """
        Explicitly activate the participant in the diagram on start of the context manager and ends on its exit.
        Can be used to activate the participant *before* it will participate in any activity
        """
        self.__add_step(
            ParticipantActivationControl(is_active=True, participant=self, _color=color)
        )
        yield None
        self.__add_step(
            ParticipantActivationControl(
                is_active=False, participant=self, _color=color
            )
        )

    def __hash__(self):
        return hash(self.title)

    def __repr__(self):
        return f"Participant ({self.title})"  # pragma: nocover


@dataclass
class SequenceDiagramParticipantGroup(Colored):
    """
    Container used to visually join (group, encompass, box) participants.
    """

    title: typing.Optional[str]

    def __hash__(self):
        return hash(self.title)


@dataclass
class SequenceDiagram(BaseChart):
    """
    A sequence of the steps that must be rendered to the diagram DSL - depending on the chosen renderer.

    :title: The title of the diagram to display on the top of the diagram
    :generator_cls: the class of the renderer to be used to generate the diagram
    :auto_activation: The flag used to track whether the participant should be activated every time it
        has evoked the action to another participant.
        Once the control flow has returned back and the initial active participant was the target of the action, the
        active participant must be deactivated.
        True by default.
    """

    title: str
    generator_cls: typing.Type[IChartGenerator]
    auto_activation: bool = True

    __participants: typing.Dict[
        SequenceDiagramParticipantGroup, typing.List[SequenceDiagramParticipant]
    ] = field(init=False)
    __sequence: typing.List[Step] = field(init=False)
    __auto_activation_stack: typing.List[
        typing.Union[
            typing.Tuple[SequenceDiagramParticipant, SequenceDiagramParticipant],
            typing.Tuple[None, SequenceDiagramParticipant],
        ]
    ] = field(init=False)
    __generator: IChartGenerator = field(init=False)
    __inside_condition: bool = field(init=False)
    __default_group: SequenceDiagramParticipantGroup = field(init=False)

    def __post_init__(self):
        self.__default_group = SequenceDiagramParticipantGroup(title=None, _color=None)
        self.__participants = {self.__default_group: []}
        self.__sequence = []
        self.__inside_condition = False
        self.__auto_activation_stack = []
        self.__generator = self.generator_cls(self)

    def participant(
        self, title: str, color: typing.Optional[str] = None
    ) -> SequenceDiagramParticipant:
        # NB: every participant must have a unique name
        all_registered_participant_titles = [
            _.title for _ in chain.from_iterable(self.__participants.values())
        ]
        if title in all_registered_participant_titles:
            raise ChartingException(
                f"Sequence diagram already contains participant {title}. "
                f"All participants must have unique titles."
            )
        participant = SequenceDiagramParticipant(
            title=title, sequence_ref=self, _color=color
        )
        # add the participant to the default group
        if self.__default_group not in self.__participants:
            self.__participants[self.__default_group] = []
        self.__participants[self.__default_group].append(participant)
        return participant

    def group_participants(
        self,
        title: str,
        *participants: SequenceDiagramParticipant,
        color: typing.Optional[str] = None,
    ) -> None:
        """
        Visually join (group, encompass, box) participants to emphasize the connections or similarities between them.

        NB 1: the name of this new group must be unique.
        NB 2: every participant can participate in one group only
        """
        all_registered_groups = [_.title for _ in self.__participants]
        if not title or title in all_registered_groups:
            raise ChartingException(
                "The given name of the named group of joint participants "
                "must be unique and not empty."
            )

        for participant in participants:
            if participant not in self.__participants.get(self.__default_group, []):
                raise ChartingException(
                    f"The participant {participant.title} does not belong to the default group "
                    "and therefor cannot be moved to the named one."
                )

        # remove the mentioned participants from the default group and put them to the new one
        self.__participants[self.__default_group] = [
            participant
            for participant in self.__participants.get(self.__default_group, [])
            if participant not in participants
        ]
        # there must be no empty groups
        if not self.__participants.get(self.__default_group):
            self.__participants.pop(self.__default_group, None)

        self.__participants[
            SequenceDiagramParticipantGroup(title=title, _color=color)
        ] = list(participants)

    def note(self, text: str, color: typing.Optional[str] = None) -> None:
        """
        Add the note plate with the given text somewhere inside the diagram
        """
        self.__add_step(NoteStep(text=text, _color=color))

    @contextmanager
    def loop(
        self, how_many_iterations: str, color: typing.Optional[str] = None
    ) -> None:
        """
        Explicitly mark the following sequence of steps as performed in the loop
        """
        self.__add_step(
            LoopControl(
                is_active=True, how_many_iterations=how_many_iterations, _color=color
            )
        )
        yield None
        self.__add_step(LoopControl(is_active=False, _color=color))

    def return_(self, text: str = ""):
        if not self.auto_activation:
            raise ChartingException(
                "The method .return_() can be used only when diagram have been initialized"
                "with `auto_activation=True`. "
                "Please initialize the diagram with `auto_activation=True` "
                "or explicitly use .return_to() for the participant objects."
            )
        try:
            previously_active_participant = self.__auto_activation_stack[-1]
        except IndexError:
            raise ChartingException(
                "Sequence diagram stack does not hold the previous participant to return to."
            )
        self.__add_step(
            ReturnStep(
                text,
                from_participant=previously_active_participant[1],
                to_participant=previously_active_participant[0],
            )
        )

    @contextmanager
    def group(self, text: str, color: typing.Optional[str] = None) -> None:
        """
        Explicitly mark the following sequence of steps as performed in the group
        """
        self.__add_step(GroupControl(is_active=True, text=text, _color=color))
        yield None
        self.__add_step(GroupControl(is_active=False, _color=color))

    @contextmanager
    def condition(self, color: typing.Optional[str] = None) -> None:
        """
        Explicitly mark the following sequence of steps as performed within some logical "if - else" block
        """
        self.__add_step(ConditionControl(is_active=True, _color=color))
        self.__inside_condition = True
        yield
        self.__add_step(ConditionControl(is_active=False, _color=color))
        self.__inside_condition = False

    @contextmanager
    def case(self, text: str, color: typing.Optional[str] = None):
        """
        Explicitly mark the following sequence of steps as performed within the specific condition
        """
        self.__add_step(CaseControl(is_active=True, text=text, _color=color))
        yield
        self.__add_step(CaseControl(is_active=False, _color=color))

    def __add_step(self, step: Step):
        if self.__inside_condition:
            # explicitly require the "CaseControl" to always happen right after the "ConditionControl"
            previous_step = self.__sequence[-1]
            if isinstance(previous_step, ConditionControl) and previous_step.is_active:
                if not isinstance(step, CaseControl):
                    raise ChartingException(
                        "After `with .condition()` the next step must be always `with .case()` "
                        "with the definition of the condition. "
                        "Please check the examples from the project repo."
                    )
        else:
            # do not allow "CaseControl" being used outside the condition
            if isinstance(step, CaseControl):
                raise ChartingException(
                    "Context manager `with .case()` cannot be used separately outside of the "
                    "`with .condition()` context manager. "
                    "Please check the examples from the project repo."
                )

        if self.auto_activation:
            # If auto_activation is enabled,
            # every time we add a regular step transferring the control to another participant,
            # the activation must be started.
            # And every time the flow returns to the previously activated participant, its activation must be ended.

            if isinstance(step, ForwardStep):
                if not self.__auto_activation_stack:
                    # If stack is empty, the very first participant starting the flow must be activated as well.
                    self.__auto_activation_stack.append((None, step.from_participant))
                    self.__sequence.append(
                        ParticipantActivationControl(
                            is_active=True,
                            participant=step.from_participant,
                            _color=None,
                        )
                    )

                self.__sequence.append(step)

                if (
                    self.__auto_activation_stack
                    and step.to_participant != self.__auto_activation_stack[-1][-1]
                ):
                    # If the flow has been passed to the participant that is not currently considered as active,
                    # then activate it.
                    self.__auto_activation_stack.append(
                        (step.from_participant, step.to_participant)
                    )
                    self.__sequence.append(
                        ParticipantActivationControl(
                            is_active=True, participant=step.to_participant, _color=None
                        )
                    )

            elif isinstance(step, ReturnStep):
                self.__sequence.append(step)

                if (
                    self.__auto_activation_stack
                    and (step.to_participant, step.from_participant)
                    == self.__auto_activation_stack[-1]
                ):
                    # If we are passing the flow back exactly to the participant,
                    # that previously has passed the control to us -
                    # deactivate the current participant.
                    self.__auto_activation_stack.pop()
                    self.__sequence.append(
                        ParticipantActivationControl(
                            is_active=False,
                            participant=step.from_participant,
                            _color=None,
                        )
                    )

                if self.__auto_activation_stack == [(None, step.to_participant)]:
                    # If we have returned back to the very first participant
                    # that has started the stack of the calls, then also deactivate it.
                    self.__auto_activation_stack.pop()
                    self.__sequence.append(
                        ParticipantActivationControl(
                            is_active=False,
                            participant=step.to_participant,
                            _color=None,
                        )
                    )
            else:
                self.__sequence.append(step)
        else:
            self.__sequence.append(step)

    def generate(self) -> str:
        return self.__generator.generate_sequence_diagram()

    def __repr__(self):
        return f"'{self.title}', {self.generator_cls.__name__}"  # pragma: nocover

    def __str__(self):
        return self.generate()
