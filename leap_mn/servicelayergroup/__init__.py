from leap_mn.layer import LayerConfig
from leap_mn.layergroup import LayerGroup
from moonleap import tags


def create_dial_config(layer_group):
    return {
        "default": {
            str(i + 1): f"dodo {layer.name}"
            for i, layer in enumerate(layer_group.layers)
        },
        "shift": {
            str(i + 1): r"${/ROOT/src_dir}/" + ("" if i == 0 else layer.name)
            for i, layer in enumerate(layer_group.layers)
        },
    }


@tags(["service-layer-group"])
def create_service_layer_group(term, block):
    layer_group = LayerGroup(name="server")
    return [layer_group, LayerConfig("dial", lambda x: create_dial_config(layer_group))]


meta = {}