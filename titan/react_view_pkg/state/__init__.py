from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import Prop, create, extend, kebab_to_camel, rule, u0
from moonleap.blocks.verbs import has, provides
from moonleap.render.render_mixin import get_root_resource
from titan.react_pkg.reactmodule import ReactModule
from titan.react_view_pkg.pkg.hydrate_state import hydrate_state

from . import props
from .resources import State

base_tags = {"state": ["react-state"]}


@create("state")
def create_state(term):
    name = u0(kebab_to_camel(term.data) + "State")
    state = State(name=name)
    return state


@rule("module", has, "state")
def module_renders_state(module, state):
    module.renders(
        [state],
        state.name,
        lambda state: dict(state=state),
        [Path(__file__).parent / "templates"],
    )

    for container in state.containers:
        state.renders(
            [container],
            container.name,
            lambda state: dict(container=container),
            [Path(__file__).parent / "templates_container"],
        )


@rule("state")
def created_state(state):
    get_root_resource().set_flags(["app/useStates"])
    hydrate_state(state)


@extend(ReactModule)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    state_provider = P.parent("state~provider", provides)
    ts_var = Prop(props.state_ts_var)
