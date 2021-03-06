from moonleap_project.dockercompose import DockerComposeConfig


def get(docker_image):
    def get_service_body(service_name):
        body = {}
        return body

    def get_global_body(service_name):
        body = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: get_service_body(service_name),
        get_global_body=lambda x, service_name: get_global_body(service_name),
        is_dev=True,
    )
