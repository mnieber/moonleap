from moonleap.utils.queue import Queue
from titan.react_view_pkg.pkg.get_builder import get_builder


def get_helpers(_):
    class Helpers:
        view = _.component
        widget_spec = _.component.widget_spec
        components = []
        css_classes = []
        div = None
        has_children = False

        def __init__(self):
            self.div, self.components, self.css_classes = self._get_div(
                self.widget_spec
            )
            self.has_children = self._has_children()

        def _get_div(self, widget_spec, level=0):
            builder = get_builder(widget_spec, None, level)
            div, components, css_classes = builder.get_div()
            return div, components, css_classes

        def _has_children(self):
            q = Queue(lambda x: x, [self.widget_spec])
            for widget_spec in q:
                if widget_spec.widget_base_type == "Children":
                    return True
                q.extend(widget_spec.child_widget_specs)
            return False

    return Helpers()
