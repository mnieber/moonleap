import moonleap.resource.props as P
from moonleap import create_forward, extend, rule
from moonleap.verbs import has, shows
from titan.react_pkg.component import Component
from titan.react_pkg.module import Module


@rule("module", has, "*", fltr_obj=P.fltr_instance(Component))
def module_has_component(module, component):
    module.node_package_configs.add_source(component)
    component.output_paths.add_source(module)


@rule("module", shows, "*", fltr_obj=P.fltr_instance(Component))
def module_shows_component(module, component):
    module_has_component(module, component)
    return create_forward(module, "p-shows", ":component", obj_res=component)


@extend(Module)
class ExtendModule:
    routed_components = P.children("p-shows", "component")