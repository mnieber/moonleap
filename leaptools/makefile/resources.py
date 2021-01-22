from dataclasses import dataclass

from leaptools.tool import Tool
from moonleap import Resource


@dataclass
class Makefile(Tool):
    pass


@dataclass
class MakefileRule(Resource):
    text: str