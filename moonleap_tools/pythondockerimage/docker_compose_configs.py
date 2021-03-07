from moonleap_project.dockercompose import DockerComposeConfig


def get(docker_image):
    def get_service_body(service_name):
        body = {}
        volumes = body.setdefault("volumes", [])
        volumes.extend(
            [
                f"{service_name}_site_packages:/usr/local/lib/python3.9/site-packages",
                f"{service_name}_usr_local_bin:/usr/local/bin",
            ]
        )
        return body

    def get_global_body(service_name):
        body = {}
        volumes = body.setdefault("volumes", {})
        volumes[f"{service_name}_site_packages"] = {}
        volumes[f"{service_name}_usr_local_bin"] = {}
        return body

    return DockerComposeConfig(
        get_service_body=lambda x, service_name: get_service_body(service_name),
        get_global_body=lambda x, service_name: get_global_body(service_name),
        is_dev=True,
    )