from dataclasses import dataclass

from moonleap_tools.tool import Tool


@dataclass
class ItemType(Tool):
    name: str
