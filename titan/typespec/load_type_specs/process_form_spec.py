def process_form_spec(type_reg, form_type_spec):
    existing_form_type_spec = type_reg.get(form_type_spec.type_name, default=None)
    if existing_form_type_spec:
        for field_spec in form_type_spec.field_specs:
            existing_form_type_spec.add_field_spec(field_spec)
        form_type_spec = existing_form_type_spec

        if existing_form_type_spec.module_name and form_type_spec.module_name:
            if existing_form_type_spec.module_name != form_type_spec.module_name:
                raise Exception(
                    f"Form type {form_type_spec.type_name} is defined in two modules: "
                    + f"{existing_form_type_spec.module_name} and {form_type_spec.module_name}"
                )
        if not existing_form_type_spec.module_name:
            existing_form_type_spec.module_name = form_type_spec.module_name
    else:
        type_reg.setdefault(form_type_spec.type_name, form_type_spec)
