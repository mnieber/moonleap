from titan.typespec.field_spec import get_field_spec_constructor

from .get_generic_field_attrs import get_generic_field_attrs


def get_scalar_field_spec(key, field_spec_value):
    field_attrs = get_generic_field_attrs(key, field_spec_value.split(","))
    parts = field_spec_value.split(",")

    count_is = 0
    for part in parts:
        parts_is = part.split(" = ")
        if len(parts_is) == 2:
            if count_is:
                raise Exception("Only one ' = ' is allowed in a field spec.")
            count_is += 1
            field_attrs["default_value"] = parts_is[1]
            parts.remove(part)
            parts.insert(0, parts_is[0])

    #
    # choices
    #
    for part in parts:
        parts_choice = part.split(" | ")
        if len(parts_choice) > 1:
            field_attrs["choices"] = [(x, x) for x in parts_choice]

    #
    # field_type
    #
    if True:
        if field_attrs["choices"]:
            field_attrs["field_type"] = "string"

        if field_attrs["field_type"] == None:
            field_attrs["field_type"] = (
                "string"
                if "String" in parts
                else "string[]"
                if "String[]" in parts
                else "int[]"
                if "Int[]" in parts
                else "float[]"
                if "Float[]" in parts
                else "uuid"
                if "Id" in parts
                else "uuid[]"
                if "Id[]" in parts
                else "date"
                if "Date" in parts
                else "json"
                if "Json" in parts
                else "boolean"
                if "Boolean" in parts
                else "float"
                if "Float" in parts
                else "url"
                if "Url" in parts
                else "slug"
                if "Slug" in parts
                else "int"
                if "Int" in parts
                else "image"
                if "Image" in parts
                else "markdown"
                if "Markdown" in parts
                else "tags"
                if "Tags" in parts
                else None
            )

        if field_attrs["default_value"] is None:
            if field_attrs["field_type"] == "tags":
                field_attrs["default_value"] = "create_empty_tags"
        else:
            if field_attrs["field_type"] == "boolean":
                field_attrs["default_value"] = (
                    field_attrs["default_value"].lower() == "true"
                )

            if field_attrs["field_type"] == "int":
                field_attrs["default_value"] = int(field_attrs["default_value"])

            if field_attrs["field_type"] == "float":
                field_attrs["default_value"] = float(field_attrs["default_value"])

        if field_attrs["field_type"] is None:
            raise Exception(f"Bad field type: {field_spec_value}")

    #
    # readonly
    #
    if "readonly" in parts:
        field_attrs["readonly"] = True

    #
    # primary key
    #
    if "primary_key" in parts:
        field_attrs["primary_key"] = True
        field_attrs["readonly"] = True
        if field_attrs["field_type"] == "uuid":
            if not field_attrs.get("readonly", None):
                field_attrs["readonly"] = True

    #
    # admin_search
    #
    if "search" in parts:
        field_attrs["admin_search"] = True

    #
    # unique
    #
    if "unique" in parts or field_attrs["field_type"] in ("slug",):
        field_attrs["unique"] = True

    #
    # help
    #
    if "help" in parts:
        field_attrs["help"] = True

    #
    # max length
    #
    if field_attrs["field_type"] in ("string", "slug", "url"):
        max_length = None

        for part in parts:
            try:
                max_length = int(part)
                break
            except ValueError:
                pass

        if max_length:
            field_attrs["max_length"] = max_length
        else:
            if field_attrs["field_type"] == "string":
                field_attrs["field_type"] = "text"
            elif field_attrs["field_type"] == "url":
                field_attrs["max_length"] = 255
            else:
                field_attrs["max_length"] = 80

    #
    # is_slug_src
    #
    if "slug" in parts:
        field_attrs["is_slug_src"] = True

    #
    # field spec
    #
    field_spec = get_field_spec_constructor(field_attrs["field_type"])(**field_attrs)
    return field_spec
