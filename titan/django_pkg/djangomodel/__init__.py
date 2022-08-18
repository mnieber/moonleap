import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, rule
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import contains, has, provides

from .import_type_spec import import_type_spec
from .resources import DjangoModel

rules = [
    (("module", contains + provides, "item~list"), empty_rule()),
    (("module", has, "django-model"), empty_rule()),
]

base_tags = [("module", ["django-module"])]


@create("django-model")
def create_django_model(term):
    django_model = DjangoModel(name=kebab_to_camel(term.data), kebab_name=term.data)
    return django_model


@rule("django-model", provides, "item~list")
def django_model_provides_item_list(django_model, item_list):
    import_type_spec(item_list.item.type_spec, django_model)


@extend(DjangoModel)
class ExtendDjangoModel:
    item_list = P.child(provides, "item~list")
    module = P.parent("module", has)
