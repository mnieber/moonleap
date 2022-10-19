from moonleap.typespec.type_spec import TypeSpec
from moonleap.utils.case import l0


def update_or_create_type_spec(
    type_spec_store, type_name, parts, module_name, parent_type_spec
):
    type_spec = type_spec_store.get(type_name, default=None)
    if not type_spec:
        type_spec = TypeSpec(type_name=type_name, field_specs=[])
        type_spec_store.setdefault(type_name, type_spec)

    # Update module name
    if module_name:
        if type_spec.module_name and type_spec.module_name != module_name:
            raise Exception(
                f"Type {type_spec.type_name} is defined in two modules: "
                + f"{type_spec.module_name} and {module_name}"
            )
        type_spec.module_name = module_name

    if "is_sorted" in parts:
        type_spec.is_sorted = True

    if "entity" in parts:
        type_spec.is_entity = True

    if "extract_gql_fields" in parts:
        type_spec.extract_gql_fields = True

    # Register parent
    if parent_type_spec:
        type_spec_store.register_parent_child(
            parent_type_spec.type_name, type_spec.type_name
        )

    return type_spec