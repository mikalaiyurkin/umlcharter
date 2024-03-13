from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field

from charter.generators.base import IChartGenerator
from charter.charts.types import BaseChart


class Step:
    pass


@dataclass
class Control(Step):
    is_active: bool


@dataclass
class LoopControl(Control):
    how_many_iterations: str | None = None


@dataclass
class GroupControl(Control):
    text: str | None = None


@dataclass
class CaseControl(Control):
    text: str | None = None


@dataclass
class ConditionControl(Control):
    pass


@dataclass
class ParticipantActivationControl(Control):
    participant: "SequenceDiagramParticipant"


@dataclass
class SequenceStep(Step):
    text: str | None
    from_participant: "SequenceDiagramParticipant"
    to_participant: "SequenceDiagramParticipant"


@dataclass
class SequenceDiagramParticipant:
    sequence_ref: "SequenceDiagram"
    title: str

    def __add_step(self, step: SequenceStep | ParticipantActivationControl):
        self.sequence_ref._SequenceDiagram__add_step(step)  # noqa

    def do(self, text: str, to: "SequenceDiagramParticipant"):
        self.__add_step(SequenceStep(text=text, from_participant=self, to_participant=to))

    @contextmanager
    def activate(self):
        """
        Explicitly activate the participant in the diagram on start of the context manager and ends on its exit.
        Can be used to activate the participant *before* it will participate in any activity
        """
        self.__add_step(ParticipantActivationControl(is_active=True, participant=self))
        yield None
        self.__add_step(ParticipantActivationControl(is_active=False, participant=self))

    def __hash__(self):
        return hash(self.title)


@dataclass
class SequenceDiagram(BaseChart):
    """
    A sequence of the steps that must be rendered to the diagram DSL - depending on the chosen renderer.

    :title: The title of the diagram to display on the top of the diagram
    :renderer_cls: the class of the renderer to be used to generate the diagram
    :auto_activation: The flag used to track whether the participant should be activated every time it
        has evoked the action to another participant.
        Once the control flow has returned back and the initial active participant was the target of the action, the
        active participant must be deactivated.
        True by default.
    """
    title: str
    generator_cls: type[IChartGenerator]
    auto_activation: bool = True

    __participants: list[SequenceDiagramParticipant] = field(init=False)
    __sequence: list[Step] = field(init=False)
    __auto_activation_stack: dict[SequenceDiagramParticipant: int] = field(init=False)
    __generator: IChartGenerator = field(init=False)
    __inside_condition: bool = field(init=False)

    def __post_init__(self):
        self.__participants = []
        self.__sequence = []
        self.__inside_condition = False
        self.__auto_activation_stack = defaultdict(int)
        self.__generator = self.generator_cls(self)

    def participant(self, title: str) -> SequenceDiagramParticipant:
        # NB: every participant must have a unique name
        if title in [_.title for _ in self.__participants]:
            raise AssertionError(f"Sequence diagram already contains participant {title}. "
                                 f"All participants must have unique titles.")
        participant = SequenceDiagramParticipant(title=title, sequence_ref=self)
        self.__participants.append(participant)
        return participant

    @contextmanager
    def loop(self, how_many_iterations: str) -> None:
        """
        Explicitly mark the following sequence of steps as performed in the loop
        """
        self.__add_step(LoopControl(is_active=True, how_many_iterations=how_many_iterations))
        yield None
        self.__add_step(LoopControl(is_active=False))

    @contextmanager
    def group(self, text: str) -> None:
        """
        Explicitly mark the following sequence of steps as performed in the group
        """
        self.__add_step(GroupControl(is_active=True, text=text))
        yield None
        self.__add_step(GroupControl(is_active=False))

    @contextmanager
    def condition(self) -> None:
        """
        Explicitly mark the following sequence of steps as performed within some logical "if - else" block
        """
        self.__add_step(ConditionControl(is_active=True))
        self.__inside_condition = True
        yield
        self.__add_step(ConditionControl(is_active=False))
        self.__inside_condition = False

    @contextmanager
    def case(self, text: str):
        """
        Explicitly mark the following sequence of steps as performed within the specific condition
        """
        self.__add_step(CaseControl(is_active=True, text=text))
        yield
        self.__add_step(CaseControl(is_active=False))

    def __add_step(self, step: Step):
        if self.__inside_condition:
            # explicitly require the "CaseControl" to always happen right after the "ConditionControl"
            previous_step = self.__sequence[-1]
            if isinstance(previous_step, ConditionControl) and previous_step.is_active:

                if not isinstance(step, CaseControl):
                    raise AssertionError("After `with .condition()` the next step must be always `with .case()` "
                                         "with the definition of the condition. "
                                         "Please check the examples from the project repo.")
        else:
            # do not allow "CaseControl" being used outside of the condition
            if isinstance(step, CaseControl):
                raise AssertionError("Context manager `with .case()` cannot be used separately outside of the "
                                     "`with .condition()` context manager. "
                                     "Please check the examples from the project repo.")

        if self.auto_activation and isinstance(step, SequenceStep):
            # If auto_activation is enabled, every time we add a regular step, the activation must be started
            # and every time the flow returns to the activated participant, its activation must be ended.
            self.__auto_activation_stack[step.to_participant] += 1
            self.__sequence.append(step)
            self.__sequence.append(ParticipantActivationControl(is_active=True, participant=step.to_participant))
            if step.from_participant in self.__auto_activation_stack:
                self.__auto_activation_stack[step.from_participant] -= 1
                self.__sequence.append(ParticipantActivationControl(is_active=False, participant=step.from_participant))
                if not self.__auto_activation_stack[step.from_participant]:
                    del self.__auto_activation_stack[step.from_participant]
        else:
            self.__sequence.append(step)

    def generate(self) -> str:
        return self.__generator.generate_sequence_diagram()
