import moonleap.resource.props as P
from moonleap import StoreOutputPaths, extend, render_templates, rule, tags

from . import props
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    layer.output_path = ".dodo_commands"
    return layer


@rule("layer", "has", "layer-group")
def layer_has_layer_group(layer, layer_group):
    layer.layer_configs.add_source(layer_group)


class StoreLayerConfigs:
    layer_configs = P.tree(
        "has", "layer-config", merge=props.merge, initial=LayerConfig({})
    )


@extend(Layer)
class ExtendLayer(StoreLayerConfigs, StoreOutputPaths):
    render = render_templates(__file__)
    parent_layer_group = P.parent("leapdodo.layergroup.LayerGroup", "contains", "layer")
    layer_groups = P.children("has", "layer-group")
