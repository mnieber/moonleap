from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    add,
    create,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    upper0,
)
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactAppConfig
from titan.react_state_pkg.state.resources import State

from . import props
from .props import get_context
from .resources import StateProvider


@create("state-provider", ["component"])
def create_state_provider(term, block):
    base_name = kebab_to_camel(term.data)
    state_provider = StateProvider(name=f"{upper0(base_name)}StateProvider")
    state_provider.add_template_dir(Path(__file__).parent / "templates", get_context)
    add(state_provider, ReactAppConfig(flags=dict(logStateProviders=False)))
    return state_provider


@rule("state")
def state_created(state):
    return [
        create_forward(state.module, has, f"{state.name}:state-provider"),
        create_forward(state, has, f"{state.name}:state-provider"),
    ]


@extend(State)
class ExtendState:
    state_provider = P.child(has, "state-provider")


@extend(StateProvider)
class ExtendStateProvider:
    create_router_configs = MemFun(props.create_router_configs)
    state = P.parent(State, has)
