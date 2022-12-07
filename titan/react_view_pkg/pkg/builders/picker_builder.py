from moonleap.utils.fp import extend_uniq
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_builder_mixin import BvrsBuilderMixin

from .picker_builder_tpl import picker_div_tpl, picker_handler_tpl, picker_imports_tpl


class PickerBuilder(BvrsBuilderMixin, Builder):
    def __init__(self, widget_spec):
        Builder.__init__(self, widget_spec)
        BvrsBuilderMixin.__init__(self)
        if self.bvrs_has_selection and not self.bvrs_has_highlight:
            raise Exception("Picker with selection must also have highlight")
        if not self.bvrs_has_highlight:
            raise Exception("Picker requires highlight")

    def build(self):
        self._add_packages()
        self._add_default_props()
        self._add_lines()

    def _add_lines(self):
        context = {**self.bvrs_context(), "item": self.bvrs_item_name}

        # Add preamble
        handler_code = self.render_str(
            picker_handler_tpl, context, "picker_builder_handler.j2"
        )
        self.add_preamble_lines([handler_code])

        # Add imports
        self.add_import_lines([picker_imports_tpl])

        # Add div
        div = self.render_str(picker_div_tpl, context, "picker_builder_div.j2")
        self.add_lines([div])

    def _add_default_props(self):
        extend_uniq(self.output.default_props, self.bvrs_default_props())

    def _add_packages(self):
        packages = self.output.react_packages_by_module_name.setdefault("utils", [])
        extend_uniq(packages, ["ValuePicker"])
