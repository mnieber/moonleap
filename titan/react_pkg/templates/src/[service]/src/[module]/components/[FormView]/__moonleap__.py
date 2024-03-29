from moonleap import u0


def get_helpers(_):
    class Helpers:
        view = _.component
        item = view.item

        def __init__(self):
            pass

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": f"../{u0(_.component.name)}",
        },
        "FormView.tsx.j2": {
            "name": f"{u0(_.component.name)}.tsx",
        },
        "FormView.scss.j2": {
            "name": f"{u0(_.component.name)}.scss",
        },
    }


def get_contexts(_):
    return [
        dict(component=component)
        for component in _.module.components
        if component.meta.term.tag == "form-view"
    ]
