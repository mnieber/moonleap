from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class FormView(Component):
    item_name: str
