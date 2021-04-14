from moonleap import (MemFun, add, extend, kebab_to_camel, render_templates,
                      rule, tags)
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.nodepackage import load_node_package_config

from .resources import Picker


@tags(["picker"])
def create_frame(term, block):
    name = kebab_to_camel(term.data)
    picker = Picker(basename=name, name=f"{name}Picker")
    add(picker, load_node_package_config(__file__))
    return picker


@rule("panel", has, "picker")
def panel_has_picker(panel, picker):
    picker.output_paths.add_source(panel)
    picker.react_base_path = panel.react_base_path


@extend(Picker)
class ExtendPicker:
    render = MemFun(render_templates(__file__))
