from typing import Callable

from tinysmith.orchestrator.state import State

TransitionFunction = Callable[[None|str, State], None]
