import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    Term,
    create,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.resource.forward import create_forward
from moonleap.utils.inflect import plural
from moonleap.verbs import deletes, has, posts, returns
from titan.api_pkg.graphqlapi import GraphqlApi
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList

from . import props
from .resources import Mutation

base_tags = [
    ("mutation", ["api-endpoint"]),
]


rules = [
    (("graphql:api", has, "mutation"), empty_rule()),
    (("mutation", posts, "item"), empty_rule()),
    (("mutation", deletes, "item~list"), empty_rule()),
    (("mutation", returns, "x+item"), empty_rule()),
    (("mutation", returns, "x+item~list"), empty_rule()),
]


@create("mutation")
def create_mutation(term):
    mutation = Mutation(name=kebab_to_camel(term.data))
    return mutation


@rule("mutation", posts, "item")
def mutation_posts_item(mutation, item):
    item_type_term_str = f"{item.meta.term.data}:item~type"
    return [
        create_forward(
            item_type_term_str, has, f"{item.meta.term.data}:item~form-type"
        ),
    ]


@extend(GraphqlApi)
class ExtendGraphqlApi:
    mutations = P.children(has, "mutation")


@extend(Mutation)
class ExtendMutation:
    item_lists_deleted = P.children(deletes, "item~list")
    named_items_returned = P.children(returns, "x+item")
    named_item_lists_returned = P.children(returns, "x+item~list")
    items_posted = P.children(posts, "item")
    posts_item = MemFun(props.posts_item)
    inputs_type_spec = Prop(props.inputs_type_spec)
    outputs_type_spec = Prop(props.outputs_type_spec)


@extend(Item)
class ExtendItem:
    poster_mutations = P.parents("mutation", posts)


@extend(ItemList)
class ExtendItemList:
    deleter_mutations = P.parents("mutation", deletes)
