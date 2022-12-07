from moonleap.utils.fp import append_uniq, extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin

from .list_view_builder_tpl import (
    lvi_body_div_attrs_tpl,
    lvi_body_div_styles_tpl,
    lvi_imports_tpl,
    lvi_instance_props_tpl,
    lvi_instance_tpl,
    lvi_preamble_tpl,
)


def lvi_spec(lvi_name):
    return {
        f"ListViewItem with {lvi_name}": "pass",
    }


def lvi_component_spec(lvi_name):
    return {
        f"LviComponent with {lvi_name} as ListViewItem, Bar[p-2]": {
            "LeftSlot with LviFields": "pass",
            "RightSlot with LviButtons": "pass",
        },
    }


class ListViewBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def get_spec_extension(self, places):
        lvi_name = lvi_name = (
            self.get_value_by_name("lvi-name") or self._get_default_lvi_name()
        )
        result = {}
        if "ListViewItem" not in places:
            result.update(lvi_spec(lvi_name))
        if "LviComponent" not in places:
            result.update(lvi_component_spec(lvi_name))
        return result

    def _get_default_lvi_name(self):
        default_lvi_name = self.widget_spec.root.widget_name
        if "-:" in default_lvi_name:
            default_lvi_name = default_lvi_name.replace("-:", "-") + "-item:view"
        else:
            pos = default_lvi_name.find(":")
            default_lvi_name = default_lvi_name[:pos] + "-item:view"
        return default_lvi_name

    def build(self):
        self._add_default_props()
        self._add_lines()

    def _add_lines(self):
        context = self._get_context()

        # Add imports
        self.add_import_lines(
            [self.render_str(lvi_imports_tpl, context, "liv__imports.j2")]
        )

        # Add preamble
        if True:
            builder_output = _get_lvi_instance_div(
                self.widget_spec,
                div_attrs=self.render_str(
                    lvi_instance_props_tpl, context, "lvi_instance_props.j2"
                ),
                key=f"{self.bvrs_item_name}.id",
            )
            context["child_widget_div"] = builder_output.div
            preamble_str = self.render_str(lvi_preamble_tpl, context, "lvi_preamble.j2")
            self.add_preamble_lines([preamble_str])

            # Add the rest of the builder_output that we haven't used so far
            # (especially the import_lines)
            builder_output.clear_div_lines()
            self.output.add(builder_output)

        # Add instance
        instance_str = self.render_str(lvi_instance_tpl, context, "lvi_instance.j2")
        self.add_lines([instance_str])

    def update_child_widget_spec(self, child_widget_spec):
        if child_widget_spec.place == "LviComponent":
            context = {
                **self.bvrs_context(),
                "item_name": self.bvrs_item_name,
                "component_name": child_widget_spec.widget_class_name,
            }

            # HACK: enforce that item is derived from self.bvrs_item_name
            child_widget_spec.values["item"] = f"+{self.bvrs_item_name}:item"

            append_uniq(
                child_widget_spec.div_styles,
                self.render_str(
                    lvi_body_div_styles_tpl, context, "lvi_body_div_styles.j2"
                ),
            )
            append_uniq(
                child_widget_spec.div_attrs,
                self.render_str(
                    lvi_body_div_attrs_tpl, context, "lvi_body_div_attrs.j2"
                ),
            )

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "items_expr": self.item_list_data_path(),
            "component_name": self.widget_spec.widget_class_name,
        }

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())


def _get_lvi_instance_div(widget_spec, div_attrs, key):
    # This returns the div that is used in the ListView.
    # Don't confuse this with the div that is used in the ListViewItem.
    from titan.react_view_pkg.pkg.get_builders import get_builder

    child_widget_spec = widget_spec.find_child_with_place("ListViewItem")
    memo = child_widget_spec.create_memo()
    child_widget_spec.div_key = key
    append_uniq(widget_spec.div_attrs, div_attrs)
    builder = get_builder(child_widget_spec)
    builder.build()
    child_widget_spec.restore_memo(memo)

    return builder.output
