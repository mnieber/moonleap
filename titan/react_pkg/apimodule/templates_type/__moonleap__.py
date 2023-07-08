from moonleap import l0
from titan.types_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        form_field_specs = (
            [x for x in _.form_type_spec.get_field_specs() if "client" in x.has_model]
            if _.form_type_spec
            else []
        )
        item = get_type_reg().get_item(l0(_.type_spec.type_name))

    return Helpers()
