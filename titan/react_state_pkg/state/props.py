import bisect
import os

import ramda as R
from moonleap import u0
from moonleap.utils.inflect import plural
from titan.react_pkg.pkg.ml_get import ml_react_app
from titan.react_pkg.pkg.ts_var import ts_type, ts_type_import_path
from titan.react_state_pkg.stateprovider.props import get_items_selected_from_url


def _find_module_that_provides_item_list(react_app, item_name):
    for module in react_app.modules:
        for store in module.stores:
            for item_list in store.item_lists_stored:
                if item_list.item_name == item_name:
                    return module
    return None


def bvrs_by_item_name(self):
    result = dict()
    for bvr in self.behaviors:
        bvrs = result.setdefault(bvr.item_name, [])
        pos = bisect.bisect_left(R.map(R.prop("name"))(bvrs), bvr.name)
        result[bvr.item_name].insert(pos, bvr)
    for item_list in self.item_lists_provided:
        result.setdefault(item_list.item_name, [])
    return result


def store_by_item_name(self):
    result = {}
    stores = []
    for x in ml_react_app(self).modules:
        stores.extend(x.stores)

    for item_name in bvrs_by_item_name(self).keys():
        for store in stores:
            if [x for x in store.item_lists_stored if x.item_name == item_name]:
                result[item_name] = store
                break
    return result


def type_import_path(self, item_name):
    module = _find_module_that_provides_item_list(ml_react_app(self), item_name)
    if module:
        return f"{module.module_path}/types"
    return None


def get_context(state):
    _ = lambda: None
    _.selected_items = get_items_selected_from_url(state.state_provider)

    class Sections:
        def constructor(self):
            indent = "  "
            result = []

            for item_name, bvrs in state.bvrs_by_item_name.items():
                result += [f"{plural(item_name)} = {{"]
                for bvr in bvrs:
                    result += [bvr.sections.constructor()]
                result += [r"};"]

            return os.linesep.join([(indent + x) for x in result])

        def import_item_types(self):
            result = []
            for item in _.selected_items:
                result.append(
                    f"import {{ {ts_type(item)} }} from '{ts_type_import_path(item)}';"
                )
            return os.linesep.join(result)

        def callbacks(self):
            indent = "  "
            result = []

            for item_name, bvrs in state.bvrs_by_item_name.items():
                redRoses = plural(item_name)

                body = []
                for bvr in bvrs:
                    body += [bvr.sections.callbacks(state.behaviors)]

                result += [f"_set{u0(redRoses)}Callbacks(props: PropsT) {{"]

                if body:
                    if [bvr for bvr in state.behaviors if bvr.name == "selection"]:
                        result += [f"  const inputs = this.inputs;"]
                    result += [f"  const ctr = this.{redRoses};"]
                    result += body

                result += [r"}", ""]

            return os.linesep.join([(indent + x) for x in result])

        def declare_policies(self, item_name):
            indent = "    "
            items = plural(item_name)
            result = [
                f"const Inputs_items = [Inputs, '{items}', this] as CMT;",
                f"const Outputs_display = [Outputs, '{items}Display', this] as CMT;",  # noqa: E501
            ]

            return os.linesep.join([(indent + x) for x in result])

        def policies(self):
            facet_names = [x.name for x in state.behaviors]
            indent = "      "
            result = []

            if "filtering" not in facet_names:
                result += [
                    r"Skandha.mapDataToFacet(Outputs_display, getm(Inputs_items)),",
                ]

            return os.linesep.join([(indent + x) for x in result])

    return dict(sections=Sections(), _=_)
