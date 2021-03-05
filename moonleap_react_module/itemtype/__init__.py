import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    add,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    title0,
)
from moonleap.verbs import contains
from moonleap_project.service import service_has_tool_rel
from moonleap_react_module.store import Store
from moonleap_react_view.router import RouterConfig

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    item_type = ItemType(name=kebab_to_camel(term.data))
    return item_type


@rule("store", contains, "item-type")
def store_contains_item_type(store, item_type):
    if not item_type.output_path:
        item_type.output_path = store.module.output_path
        add(
            item_type,
            RouterConfig(
                url=f"/{store.module.name}",
                component_name=f"Load{title0(store.module.name)}Effect",
                module_name=store.module.name,
                wraps=True,
            ),
        )
    return service_has_tool_rel(store.module.service, item_type)


@extend(ItemType)
class ExtendItemType(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    store = P.parent(Store, contains, "item-type")
