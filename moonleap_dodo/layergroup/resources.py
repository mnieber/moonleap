from dataclasses import dataclass

from moonleap import Resource


@dataclass
class LayerGroup(Resource):
    name: str
