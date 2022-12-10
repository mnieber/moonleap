from moonleap.utils.fp import append_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin

from .list_view_item_builder_tpl import tpls


class ListViewItemBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def build(self):
        context = self._get_context()

        self.add(
            import_lines=[tpls.render("lvi_imports_tpl", context)],
            props_lines=[tpls.render("lvi_props_tpl", context)],
            scss_lines=[tpls.render("lvi_scss_tpl", context)],
        )

    def update_widget_spec(self):
        context = self._get_context()

        if not self.named_item_term:
            self.widget_spec.values["item"] = f"+{self.bvrs_item_name}:item"

        append_uniq(
            self.widget_spec.div_styles,
            tpls.render("lvi_div_styles_tpl", context),
        )
        append_uniq(
            self.widget_spec.div_attrs,
            tpls.render("lvi_div_attrs_tpl", context),
        )

    def _get_context(self):
        return {
            **self.bvrs_context(),
            "item_name": self.bvrs_item_name,
            "component_name": self.widget_spec.widget_class_name,
            "uikit": True or self.use_uikit,
        }
