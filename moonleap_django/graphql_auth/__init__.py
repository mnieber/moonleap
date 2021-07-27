from moonleap import add, extend, rule, tags
from moonleap.verbs import uses
from moonleap_project.service import Tool
from moonleap_tools.pipdependency import PipRequirement

from . import django_configs


class GraphqlAuth(Tool):
    pass


@tags(["graphql-auth"])
def create_graphql_auth(term, block):
    graphql_auth = GraphqlAuth(name="graphql-auth")
    add(graphql_auth, django_configs.get())
    add(
        graphql_auth,
        PipRequirement(
            [
                "git+git://github.com/mnieber/django-graphql-auth@feature/"
                + "return-activation-token#egg=django-graphql-auth"
            ]
        ),
    )
    return graphql_auth


@rule("service", uses, "graphql-auth")
def service_uses_graphql_auth(service, graphql_auth):
    pass


@extend(GraphqlAuth)
class ExtendGraphqlAuth:
    pass