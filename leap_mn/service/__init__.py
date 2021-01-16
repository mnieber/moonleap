import moonleap.resource.props as P
from leap_mn.dockercompose import DockerComposeConfig, StoreDockerComposeConfigs
from leap_mn.project import Project
from leapdodo.layer import LayerConfig, StoreLayerConfigs
from moonleap import StoreOutputPaths, extend, tags

from . import docker_compose_configs as DCC
from . import layer_configs as LC
from .resources import Service


@tags(["service"])
def create_service(term, block):
    service = Service(name=term.data)
    service.output_path = service.name + "/"
    service.layer_configs.add(LayerConfig(body=LC.get_service_options()))
    service.docker_compose_configs.add(
        DockerComposeConfig(
            lambda docker_compose_config: DCC.get_service_options(
                service, docker_compose_config
            )
        )
    )
    service.docker_compose_configs.add(
        DockerComposeConfig(
            lambda docker_compose_config: DCC.get_service_options(
                service, docker_compose_config
            ),
            is_dev=True,
        )
    )
    return service


@extend(Service)
class ExtendService(StoreLayerConfigs, StoreDockerComposeConfigs, StoreOutputPaths):
    src_dir = P.child("has", "src-dir")
    project = P.parent(Project, "has", "service")
