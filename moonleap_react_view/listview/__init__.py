from moonleap import (
    MemFun,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
)
from moonleap.resource.rel import Forwards
from moonleap.verbs import has

from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    name = kebab_to_camel(term.data)
    list_view = ListView(item_name=name, name=f"{name}ListView")
    return list_view


@rule("list-view", has, "behavior")
def create_container(list_view, behavior):
    module = list_view.module
    return Forwards(
        [
            create_forward(module, has, f"{module.name}:container"),
            create_forward(list_view.module, "has", behavior),
        ]
    )


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
