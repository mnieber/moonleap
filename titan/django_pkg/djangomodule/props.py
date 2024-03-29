from moonleap import u0
from moonleap.utils import chop_suffix
from moonleap.utils.case import sn
from titan.types_pkg.typeregistry import get_type_reg


def module_path(self):
    return sn(self.name)


def get_module_by_name(django_app, module_name, default="__notset__"):
    for x in django_app.modules:
        if x.name == module_name:
            return x

    if default == "__notset__":
        raise KeyError(f"No module named {module_name}")

    return default


def item_django_module(item):
    return item.item_list.django_module if item.item_list else None


def type_spec_django_module(type_spec):
    type_name = (
        chop_suffix(type_spec.type_name, "Form")
        if type_spec.is_form
        else type_spec.type_name
    )
    for item in get_type_reg().items:
        if u0(item.type_name) == type_name:
            return item_django_module(item)
    return None
