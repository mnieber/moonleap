from dataclasses import dataclass

from moonleap import add, extend, rule, tags
from moonleap.verbs import has
from moonleap_tools.pipdependency import PipDependency
from moonleap_tools.tool import Tool

from . import layer_configs, makefile_rules


@dataclass
class PipCompile(Tool):
    pass


@rule("service", has, "pip-compile")
def service_has_pip_compile(service, pip_compile):
    service.add_template_dir(__file__, "templates_service")


@tags(["pip-compile"])
def create_pip_compile(term, block):
    pip_compile = PipCompile(name="pip-compile")

    add(pip_compile, makefile_rules.get())
    add(pip_compile, layer_configs.get())
    add(pip_compile, PipDependency(["pip-tools"], is_dev=True))

    return pip_compile


@extend(PipCompile)
class ExtendPipCompile:
    pass
