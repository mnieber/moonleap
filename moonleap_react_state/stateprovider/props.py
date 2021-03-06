from moonleap.utils.inflect import plural
from moonleap_react.component.resources import get_component_base_url
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    result = []

    if self.state:
        router_config = create_component_router_config(
            self, wraps=True, url=get_component_base_url(self, self.state.name)
        )
        result.append(router_config)

    return result


def default_props_section(self):
    result = ""

    if self.state:
        result = f"      {self.state.name}State: () => state,\n"
        store_by_item_name = self.state.store_by_item_name
        for item_name, bvrs in self.state.bvrs_by_item_name.items():
            items_name = plural(item_name)

            result += f"      {items_name}: () => state.outputs.{items_name}Display,\n"

            store = store_by_item_name.get(item_name)
            for bvr in bvrs:
                result += bvr.default_props_section(store)
    return result
