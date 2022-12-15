from moonleap import Tpls
from moonleap.parser.term import word_to_term
from moonleap.utils import chop0
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin
from titan.widgets_pkg.pkg.widget_spec_pipeline import WsPipeline


class ArrayBuilder(Builder, BvrsBuilderMixin):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)

    def update_widget_spec(self):
        term_str = f"+{self.bvrs_item_name}:item"
        term = word_to_term(term_str)
        self.widget_spec.values["item"] = term_str
        self.widget_spec.pipelines.append(
            WsPipeline(term=term, term_data_path=self.bvrs_item_name)
        )

    def build(self):
        term = self.named_item_list_term
        item_name = term.data
        const_name = self._get_const_name()

        child_widget_div = self.output.graft(
            _get_child_widget_output(self.widget_spec, item_name)
        )
        context = {
            "const_name": const_name,
            "items_expr": self.item_list_data_path(),
            "item_name": item_name,
            "child_widget_div": child_widget_div,
        }

        self.add(
            preamble_lines=[tpls.render("preamble_tpl", context)],
            lines=[tpls.render("instance_tpl", context)],
        )

    def _get_const_name(self):
        const_name = self.widget_spec.widget_name
        if not const_name:
            raise Exception("ArrayBuilder requires a widget name")
        return const_name


def _get_child_widget_output(widget_spec, item_name):
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Child")
    with child_widget_spec.memo():
        child_widget_spec.values["item"] = item_name
        child_widget_spec.div.key = f"{item_name}.id"
        return build(child_widget_spec)


preamble_tpl = chop0(
    """
const {{ const_name }} = {{ items_expr }}.map(({{ item_name }}) => {
  {{ child_widget_div }}
});
"""
)

instance_tpl = chop0(
    """
{ {{ const_name }} }
"""
)

tpls = Tpls("array_builder", preamble_tpl=preamble_tpl, instance_tpl=instance_tpl)
