import typing as T
from dataclasses import dataclass, field

import ramda as R


@dataclass
class WidgetSpec:
    widget_base_type: str
    child_widget_specs: T.List["WidgetSpec"] = field(repr=False, default_factory=list)
    styles: T.List[str] = field(repr=False, default_factory=list)
    widget_type: T.Optional[str] = None
    module_name: T.Optional[str] = None
    place: T.Optional[str] = None
    values: T.Dict[str, str] = field(default_factory=dict)

    @property
    def is_component(self):
        return self.widget_type and ":" in self.widget_type

    @property
    def is_component_def(self):
        return (
            self.is_component
            and self.widget_base_type
            and self.widget_base_type != self.widget_type
        )

    def find_child_with_place(self, place):
        return R.head(x for x in self.child_widget_specs if x.place == place)

    def remove_child_with_place(self, place):
        widget_spec = self.find_child_with_place(place)
        if widget_spec:
            self.child_widget_specs.remove(widget_spec)
