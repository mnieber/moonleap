import re

from moonleap.utils.fp import append_uniq
from moonleap.utils.quote import quote
from moonleap.utils.split_non_empty import split_non_empty
from titan.types_pkg.pkg.load_type_specs.split_raw_key import split_symbols


def get_widget_attrs(key, parts):
    attrs = dict(styles=[], values={}, widget_base_type=None)

    parts_with = key.split(" with ")
    if len(parts_with) == 2:
        attrs["place"] = parts_with[0]
        key = parts_with[1]

    if key == "children":
        widget_base_type = "Children"
        widget_type = "Children"
    else:
        parts_as = key.split(" as ")
        widget_base_type = parts_as[-1]
        widget_type = parts_as[0] if len(parts_as) == 2 else None

        if ":" in widget_base_type and not widget_type:
            widget_type, widget_base_type = widget_base_type, widget_type

        if widget_type:
            parts_module = widget_type.split(".")
            if len(parts_module) > 1:
                widget_type = parts_module[-1]
                if len(parts_module) > 1:
                    attrs["module_name"] = parts_module[0]

            attrs["widget_type"] = widget_type

    if widget_base_type:
        attrs["widget_base_type"], symbols = split_symbols(widget_base_type)

        for symbol in split_non_empty(symbols, ".") + parts:
            if _is_style(symbol):
                append_uniq(attrs["styles"], quote(symbol))
            else:
                parts_eq = symbol.split("=")
                if len(parts_eq) == 2:
                    attrs["values"][parts_eq[0]] = parts_eq[1]
                else:
                    raise Exception(f"Invalid symbol: {symbol}")

    return attrs


style_patterns = [
    r"text-(.+)-([0-9]+)",
    r"bg-(.+)-([0-9]+)",
    r"p-([0-9]+)",
    r"px-([0-9]+)",
    r"py-([0-9]+)",
    r"m-([0-9]+)",
    r"mx-([0-9]+)",
    r"my-([0-9]+)",
    r"rounded",
    r"rounded-(.+)",
]


def _is_style(symbol):
    for style_pattern in style_patterns:
        if re.fullmatch(style_pattern, symbol):
            return True
    return False
