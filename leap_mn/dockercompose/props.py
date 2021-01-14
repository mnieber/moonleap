import ramda as R
from moonleap.prop import Prop
from moonleap.utils.merge_into_config import merge_into_config

from .resources import DockerComposeConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return DockerComposeConfig(body=new_body)


def merge_configs(configs):
    merged = R.reduce(merge, DockerComposeConfig(body={}), configs)
    return merged.get_body()


def docker_compose_config_prop(is_dev=False):
    def get_value(self):
        return merge_configs(
            self.docker_compose_configs
            + [x.docker_compose_config for x in self.docker_compose_config_sources]
        )

    return Prop(get_value)
