from dataclasses import dataclass

from moonleap import Resource


@dataclass
class ItemType(Resource):
    name_camel: str
    name_snake: str