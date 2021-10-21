from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, create, extend, register_add, rule
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from titan.tools_pkg.pipdependency import PipRequirement

from . import (
    django_configs,
    docker_compose_configs,
    dodo_layer_configs,
    makefile_rules,
    opt_paths,
    props,
)
from .resources import DjangoApp, DjangoConfig


class StoreDjangoConfigs:
    django_configs = P.tree("django_configs")


@register_add(DjangoConfig)
def add_django_config(resource, django_config):
    resource.django_configs.add(django_config)


base_tags = [
    ("django-app", ["tool"]),
]


@create("django-app")
def create_django(term, block):
    django_app = DjangoApp(name="django-app")
    django_app.add_template_dir(Path(__file__).parent / "templates")
    add(django_app, django_configs.get())
    add(django_app, makefile_rules.get())
    add(django_app, dodo_layer_configs.get())
    add(django_app, opt_paths.static_opt_path)
    add(django_app, PipRequirement(["Django", "django-environ", "django-cors-headers"]))
    add(django_app, PipRequirement(["faker", "pytest-django"], is_dev=True))
    add(django_app, docker_compose_configs.get(is_dev=True))
    add(django_app, docker_compose_configs.get(is_dev=False))
    return django_app


@rule("django-app")
def rule_django_app(django_app):
    if django_app.use_django_extensions:
        add(django_app, PipRequirement(["django-extensions"], is_dev=True))


@extend(DjangoApp)
class ExtendDjangoApp(StoreTemplateDirs):
    config = Prop(props.config)
    get_setting_or = MemFun(props.get_setting_or)
    third_party_apps = Prop(props.third_party_apps)
    local_apps = Prop(props.local_apps)
    cors_urls_regex = Prop(props.cors_urls_regex)
    secret_key = Prop(props.secret_key)
    use_django_extensions = Prop(props.use_django_extensions)
