import moonleap.resource.props as P
from moonleap import add_source, extend, rule
from moonleap.verbs import has, runs
from moonleap_project.dockercompose.resources import DockerCompose


@rule("service", has, "tool")
def service_has_tool(service, tool):
    add_source(
        [service, "docker_compose_configs"],
        tool,
        "The :service receives docker compose configs from a :tool",
    )


@extend(DockerCompose)
class ExtendDockerCompose:
    services = P.children(runs, "service")
