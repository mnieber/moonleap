import moonleap.resource.props as P
from moonleap import add, add_src, add_src_inv, extend, rule
from moonleap.verbs import configured_by, has, runs
from titan.dodo_pkg.layer import StoreLayerConfigs
from titan.project_pkg.service import Service

from . import dodo_layer_configs

rules = [
    (("service", configured_by, "layer"), add_src_inv("dodo_layer_configs")),
    (("service", has + runs, "tool"), add_src("dodo_layer_configs")),
]


@rule("service")
def service_created(service):
    add(service, dodo_layer_configs.get_service_options(service))


@rule("service", has, "dockerfile")
def service_has_dockerfile(service, dockerfile):
    add(service, dodo_layer_configs.get_docker_options(service))


@extend(Service)
class ExtendService(StoreLayerConfigs):
    layer = P.child(configured_by, "layer")
