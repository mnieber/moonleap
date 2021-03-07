from moonleap import add, rule, tags
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_tools.pipdependency import PipRequirement

from . import opt_paths
from .resources import Pudb


@tags(["pudb"])
def create_pudb(term, block):
    pudb = Pudb()

    add(pudb, PipRequirement(["pudb", "ipython"], is_dev=True))
    add(pudb, opt_paths.pudb_opt_path)
    add(pudb, opt_paths.ipython_opt_path)

    return pudb


@rule("service", has, "pudb")
def service_has_pudb(service, pudb):
    return service_has_tool_rel(service, pudb)