from dataclasses import dataclass

from moonleap import Resource
from moonleap.utils.inflect import plural


@dataclass
class ItemList(Resource):
    item_name: str

    @property
    def plural_item_name(self):
        return plural(self.item_name)
