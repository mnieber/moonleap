import os

import ramda as R
from moonleap.typespec.get_member_field_spec import get_member_field_spec
from moonleap.utils.inflect import plural
from titan.api_pkg.itemlist.resources import ItemList
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.get_chain import (
    ExtractItemFromItem,
    ExtractItemListFromItem,
    TakeHighlightedElmFromState,
    TakeItemFromQuery,
    TakeItemFromState,
    TakeItemListFromQuery,
    TakeItemListFromState,
    get_chain_to,
)
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)


def create_router_configs(self, named_component):
    result = []

    if self.state:
        router_config = create_component_router_config(
            self,
            named_component=named_component,
            wraps=True,
            url=get_component_base_url(self, ""),
        )
        result.append(router_config)

    return result


def _start_pos(chain):
    for pos in reversed(range(len(chain))):
        elm = chain[pos]
        if isinstance(
            elm,
            (
                TakeItemListFromState,
                TakeItemFromState,
                TakeHighlightedElmFromState,
            ),
        ):
            return pos
    return 0


def _get_default_input_props(chain):
    result = []
    for elm in chain:
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            result += [elm.obj]
    return result


def _expression(chain, query_name):
    result = ""
    result_rs = None
    for elm_idx in range(len(chain)):
        elm = chain[elm_idx]
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            postfix = "?" if elm_idx < len(chain) - 1 else ""
            result = f"props.{elm.obj.ts_var}{postfix}" + result
        elif isinstance(elm, (TakeItemFromQuery,)):
            result = f"R.values({query_name}.data?.{elm.obj.item_name} ?? {{}})"
            result_rs = f"{query_name}.status"
        elif isinstance(elm, (TakeItemListFromQuery,)):
            items_name = plural(elm.obj.item_name)
            result = f"R.values({query_name}.data?.{items_name} ?? {{}})"
            result_rs = f"{query_name}.status"
        elif isinstance(elm, (ExtractItemFromItem)):
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = f"{query_name}.data?[{result}.{member}]"
        elif isinstance(elm, (ExtractItemListFromItem)):
            items_name = plural(elm.obj.item_name)
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = (
                f"R.reject(R.isNil)"
                + f"(lookUp({result}.{member} ?? [], "
                + f"{query_name}.data?.{items_name} ?? {{}}))"
            )
    return result, result_rs


def get_context(state_provider):
    _ = lambda: None
    _.state = state_provider.state

    _.chain_by_id = {}
    _.short_chain_by_id = {}
    for target in list(_.state.items_provided) + list(_.state.item_lists_provided):
        chain = get_chain_to(target, _.state)
        _.chain_by_id[target.id] = chain
        _.short_chain_by_id[target.id] = chain[_start_pos(chain) : len(chain)]

    _.default_input_props = []
    for chain in R.values(_.short_chain_by_id):
        for default_input_prop in _get_default_input_props(chain):
            if default_input_prop not in _.default_input_props:
                _.default_input_props.append(default_input_prop)

    _.query_names = set()
    for chain in R.values(_.chain_by_id):
        _.query_names.add(chain[0].subj.name)

    _.mutation_names = set()
    for target in list(_.state.item_lists_provided):
        for bvr in _.state.bvrs_by_item_name[target.item_name]:
            if bvr.name == "deletion" and target.deleter_mutations:
                _.mutation_names.add(target.deleter_mutations[0].name)

    _.facet_names_by_item_name = dict()
    for item_name, bvrs in _.state.bvrs_by_item_name.items():
        _.facet_names_by_item_name[item_name] = [x.name for x in bvrs]

    class Sections:
        def default_input_props_imports(self):
            result = []
            for x in _.default_input_props:
                item = x.item if isinstance(x, ItemList) else x
                result.append(
                    f"import {{ {item.ts_type} }} from '{item.item_type.ts_type_import_path}';"
                )
            return os.linesep.join(result)

        def get_state_input_values(self):
            result = []
            for short_chain, chain in R.zip(
                R.values(_.short_chain_by_id), R.values(_.chain_by_id)
            ):
                query_name = chain[0].subj.name
                provided = chain[-1].obj.ts_var
                value, value_rs = _expression(short_chain, query_name)
                result.append(f"{provided}: {value},")
                if value_rs:
                    result.append(f"{provided}RS: {value_rs},")
            return os.linesep.join(result)

        def set_state_input_values(self):
            result = []
            tab = " " * 8
            for chain in _.R.values(_.short_chain_by_id):
                target = chain[-1].obj
                if isinstance(target, ItemList):
                    result.append(
                        f"{tab}state.inputs.{target.ts_var} = inputs.{target.ts_var};"
                    )
            return os.linesep.join(result)

        def default_props(self):
            result = ""

            if _.state:
                result = ""

                if _.state.behaviors:
                    result = f"      {_.state.name}State: () => state,\n"

                for target in list(_.state.items_provided) + list(
                    _.state.item_lists_provided
                ):
                    items_name = plural(target.item_name)
                    chain = _.chain_by_id[target.id]
                    short_chain = _.short_chain_by_id[target.id]
                    query_name = chain[0].subj.name
                    bvrs = _.state.bvrs_by_item_name.get(target.item_name, [])

                    if bvrs and isinstance(target, ItemList):
                        result += f"      {items_name}: () => state.outputs.{items_name}Display,\n"
                        result += f"      {items_name}RS: () => {query_name}.status,\n"

                        for bvr in bvrs:
                            result += bvr.sections.default_props(_.state)
                    else:
                        prop_name = (
                            items_name
                            if isinstance(target, ItemList)
                            else target.item_name
                        )
                        value, value_rs = _expression(short_chain, query_name)
                        result += f"      {prop_name}: () => {value},\n"
                        result += f"      {prop_name}RS: () => {value_rs},\n"
            return result

    return dict(sections=Sections(), _=_)
