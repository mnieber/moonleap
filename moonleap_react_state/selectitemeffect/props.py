from moonleap_react_view.router import RouterConfig
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    return [RouterConfig(component=self, url="")]
