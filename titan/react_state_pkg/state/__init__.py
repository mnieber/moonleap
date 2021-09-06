import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    RenderTemplates,
    add,
    extend,
    kebab_to_camel,
    rule,
    tags,
)
from moonleap.verbs import has, provides
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import load_node_package_config

from . import props, react_app_configs
from .resources import State


@tags(["state"])
def create_state(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    add(state, load_node_package_config(__file__))
    return state


@rule("module", has, "state")
def module_has_state(module, state):
    if react_app_configs.config not in module.react_app.react_app_configs.children:
        add(module.react_app, react_app_configs.config)


@extend(Module)
class ExtendModule:
    states = P.children(has, "state")


empty_rules = [
    ("state", provides, "item-list"),
    ("state", provides, "item"),
    ("state", provides, "behavior"),
]


@extend(State)
class ExtendState(RenderTemplates(__file__)):
    behaviors = P.children(provides, "behavior")
    item_lists = P.children(provides, "item-list")
    items = P.children(provides, "item")
    bvrs_by_item_name = Prop(props.bvrs_by_item_name)
    store_by_item_name = Prop(props.store_by_item_name)
    sections = Prop(props.Sections)
    type_import_path = MemFun(props.type_import_path)
