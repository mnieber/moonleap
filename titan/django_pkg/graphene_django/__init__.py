import moonleap.resource.props as P
from moonleap import MemFun, add, create_forward, extend, rule, tags
from moonleap.verbs import has, uses
from titan.project_pkg.service import Service, Tool
from titan.tools_pkg.pipdependency import PipRequirement

from . import django_configs, props


class GrapheneDjango(Tool):
    pass


@tags(["graphene-django"])
def create_graphene_django(term, block):
    graphene_django = GrapheneDjango(name="graphene-django")
    add(graphene_django, django_configs.get())
    add(graphene_django, PipRequirement(["graphene-django"]))
    return graphene_django


@rule("service", uses, "graphene-django")
def service_uses_graphene_django(service, graphene_django):
    return create_forward(service.django_app, has, "api:module")


@extend(GrapheneDjango)
class ExtendGrapheneDjango:
    render = MemFun(props.render)
    service = P.parent(Service, has)
    p_section_graphene_fields = MemFun(props.p_section_graphene_fields)
    p_section_exclude = MemFun(props.p_section_exclude)
    p_section_mutation_fields = MemFun(props.p_section_mutation_fields)
    p_section_query_base_types = MemFun(props.p_section_query_base_types)
    p_section_form_values = MemFun(props.p_section_form_values)
    p_section_item_list_query = MemFun(props.p_section_item_list_query)
    p_section_form_mutation = MemFun(props.p_section_form_mutation)
    p_section_post_item_mutation = MemFun(props.p_section_post_item_mutation)