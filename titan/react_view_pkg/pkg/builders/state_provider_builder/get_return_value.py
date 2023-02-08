from moonleap import l0
from moonleap.utils.inflect import plural


def get_return_value(state_provider, state, data, hint=None):
    widget_spec = state_provider.widget_spec

    if data in state_provider.named_items_provided:
        named_item = data
        data_path = widget_spec.get_data_path(named_item)
        maybe_expr = widget_spec.maybe_expression(named_item)
        item_name = named_item.typ.item_name
        return f"cache.{item_name})" if maybe_expr else data_path

    if data in state_provider.named_item_lists_provided:
        named_item_list = data
        data_path = widget_spec.get_data_path(named_item_list)
        maybe_expr = widget_spec.maybe_expression(named_item_list)
        items_name = plural(named_item_list.typ.item_name)
        return f"cache.{items_name}" if maybe_expr else data_path

    if data in state.containers and hint == "items":
        container = data
        named_item_list = container.named_item_list
        assert named_item_list
        maybe_expr = widget_spec.maybe_expression(named_item_list)
        items_name = plural(container.item.item_name)
        data_path = f"{l0(state.name)}.{container.name}.data.{items_name}" + (
            "Display"
            if (container.get_bvr("filtering") or container.get_bvr("insertion"))
            else ""
        )
        return f"cache.{items_name}" if maybe_expr else data_path

    if data in state.containers and hint == "highlighted_item":
        container = data
        named_item_list = container.named_item_list
        assert named_item_list
        maybe_expr = widget_spec.maybe_expression(named_item_list)
        item_name = container.item.item_name
        data_path = f"{l0(state.name)}.{container.name}.highlight.item"
        return f"cache.{item_name}" if maybe_expr else data_path
