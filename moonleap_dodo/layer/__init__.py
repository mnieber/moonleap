import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    extend,
    kebab_to_camel,
    register_add,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has

from . import props
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=kebab_to_camel(term.data))
    layer.output_path = ".dodo_commands"
    return layer


@rule("layer", has, "layer-group")
def layer_has_layer_group(layer, layer_group):
    layer.layer_configs.add_source(layer_group)


@rule("service", has, "tool")
def service_has_tool(service, tool):
    service.layer_configs.add_source(tool)


@register_add(LayerConfig)
def add_layerconfig(resource, layer_config):
    resource.layer_configs.add(layer_config)


class StoreLayerConfigs:
    layer_configs = P.tree(has, "layer-config")


@extend(Layer)
class ExtendLayer(StoreLayerConfigs, StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    parent_layer_group = P.parent(
        "moonleap_dodo.layergroup.LayerGroup", "contains", "layer"
    )
    layer_groups = P.children(has, "layer-group")
    get_config = MemFun(props.get_config)
