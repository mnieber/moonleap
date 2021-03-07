import moonleap.resource.props as P
from moonleap import (
    Forward,
    MemFun,
    add,
    extend,
    register_add,
    render_templates,
    rule,
    tags,
)
from moonleap.resource.rel import Rel
from moonleap.verbs import has, runs
from moonleap_project.service import Service, service_has_tool_rel
from moonleap_tools.pkgdependency import PkgDependency
from moonleap_tools.tool import StoreMakefileRules, Tool

from . import layer_configs
from .resources import Makefile, MakefileRule  # noqa


@tags(["makefile"])
def create_makefile(term, block):
    makefile = Makefile()

    add(makefile, PkgDependency(["make"], is_dev=True))
    add(makefile, layer_configs.get())

    return makefile


@rule("service", has, "makefile")
def service_has_makefile(service, makefile):
    return service_has_tool_rel(service, makefile)


@rule("makefile", runs, "*", fltr_obj=P.fltr_instance(Tool))
def makefile_running_tool(makefile, tool):
    return Forward(Rel(makefile.service.term, has, tool.term))


@register_add(MakefileRule)
def add_makefile_rule(resource, makefile_rule):
    resource.makefile_rules.add(makefile_rule)


@extend(Makefile)
class ExtendMakefile(StoreMakefileRules):
    render = MemFun(render_templates(__file__))
    service = P.parent(Service, has, "makefile")