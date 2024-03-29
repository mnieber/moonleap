from moonleap import create, create_forward, kebab_to_camel, parts_to_camel, u0
from moonleap.spec.verbs import has

from .resources import Behavior, is_exposed_bvr  # noqa: F401

base_tags = {}


@create("addition:bvr")
def create_addition_behavior(term):
    return Behavior(
        name="Addition",
        has_param=True,
    )


@create("deletion:bvr")
def create_deletion_behavior(term):
    return Behavior(
        name="Deletion",
        has_param=False,
    )


@create("drag-and-drop:bvr")
def create_drag_and_drop_behavior(term):
    return Behavior(
        name="DragAndDrop",
        has_param=False,
    )


@create("edit:bvr")
def create_edit_behavior(term):
    return Behavior(
        name="Edit",
        has_param=False,
    )


@create("filtering:bvr")
def create_filtering_behavior(term):
    return Behavior(
        name="Filtering",
        has_param=False,
    )


@create("highlight:bvr")
def create_highlight_behavior(term):
    return Behavior(
        name="Highlight",
        has_param=True,
    )


@create("hovering:bvr")
def create_hovering_behavior(term):
    return Behavior(
        name="Hovering",
        has_param=False,
    )


@create("insertion:bvr")
def create_insertion_behavior(term):
    return Behavior(
        name="Insertion",
        has_param=True,
    )


@create("selection:bvr")
def create_selection_behavior(term):
    return Behavior(
        name="Selection",
        has_param=True,
    )


@create("store:bvr")
def create_default_store_behavior(term):
    return Behavior(
        name="Store",
        has_param=True,
    )


@create("display:bvr")
def create_display_behavior(term):
    return Behavior(
        name="Display",
        has_param=True,
    )


@create("pagination:bvr")
def create_pagination_behavior(term):
    return Behavior(
        name="Pagination",
        interface_name="IPagination",
        has_param=False,
    )


@create("x:x:bvr")
def create_custom_behavior(term):
    return Behavior(
        name=u0(parts_to_camel(term.parts)),
        has_param=False,
        is_skandha=False,
    )


@create("bvr")
def create_behavior(term):
    return Behavior(
        name=u0(kebab_to_camel(term.data)),
        has_param=False,
        is_skandha=False,
    )


rules = {
    "container": {
        (has, "drag-and-drop:bvr"): (
            #
            lambda container, bvr: create_forward(container, has, "hovering:bvr")
        ),
        (has, "filtering:bvr"): (
            #
            lambda container, bvr: create_forward(container, has, "display:bvr")
        ),
        (has, "insertion:bvr"): (
            #
            lambda container, bvr: create_forward(container, has, "display:bvr")
        ),
    }
}
