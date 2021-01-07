from pathlib import Path

from moonleap.config import config


def _install_templates(module, resource_type, src_class_meta, dest_class_meta):
    templates = src_class_meta.get("templates")
    if templates:
        dest_class_meta["templates"] = str(Path(module.__file__).parent / templates)


def _install_output_dir(module, resource_type, src_class_meta, dest_class_meta):
    dest_class_meta["output_dir"] = src_class_meta.get("output_dir")


def _install_props(module, resource_type, src_class_meta, dest_class_meta):
    for prop_name, prop in src_class_meta.get("props", {}).items():
        if prop.parent_resource_type:
            parent_types = dest_class_meta.setdefault("parent_types", [])
            if prop.parent_resource_type not in parent_types:
                parent_types.append(prop.parent_resource_type)

        if prop.child_resource_type:
            child_types = dest_class_meta.setdefault("child_types", [])
            if prop.child_resource_type not in child_types:
                child_types.append(prop.child_resource_type)

        setattr(resource_type, prop_name, prop.prop)


def install(module):
    for f in [
        f
        for f in module.__dict__.values()
        if callable(f) and f.__module__ == module.__name__
    ]:
        if hasattr(f, "moonleap_create_rule_by_tag"):
            for tag, create_rule in f.moonleap_create_rule_by_tag.items():
                config.create_rule_by_tag[tag] = create_rule

        if hasattr(f, "moonleap_derive_resource"):
            resource_type = f.moonleap_derive_resource
            config.derive_rules_by_resource_type.setdefault(resource_type, [])
            config.derive_rules_by_resource_type[resource_type].append(f)

    meta = module.meta() if callable(module.meta) else module.meta
    for resource_type, src_class_meta in meta.items():
        dest_class_meta = config.meta_by_resource_type.setdefault(resource_type, {})
        _install_output_dir(module, resource_type, src_class_meta, dest_class_meta)
        _install_templates(module, resource_type, src_class_meta, dest_class_meta)
        _install_props(module, resource_type, src_class_meta, dest_class_meta)
