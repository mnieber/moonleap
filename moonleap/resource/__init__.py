import random
import typing as T
import uuid
from dataclasses import dataclass, field

from moonleap.parser.block import Block
from moonleap.parser.term import Term
from moonleap.resource.rel import Rel
from moonleap.resource.slctrs import RelSelector

# Use a fixed seed for the id generator
rd = random.Random()
rd.seed(0)


def get_id():
    return uuid.UUID(int=rd.getrandbits(128)).hex


@dataclass
class ResourceMetaData:
    term: Term
    block: Block
    base_tags: T.List[str]


@dataclass
class Resource:
    id: str = field(default_factory=get_id, init=False, repr=False)
    _relations: T.List[T.Tuple[Rel, "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )
    _inv_relations: T.List[T.Tuple[Rel, "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )
    meta: T.Optional[ResourceMetaData] = field(
        default_factory=lambda: None, init=False, repr=False
    )

    def __repr__(self):
        return self.__class__.__name__

    def get_relations(self):
        return self._relations

    def get_inv_relations(self):
        return self._inv_relations

    def has_relation(self, rel, resource):
        return resource in RelSelector(rel).select_from(self)

    def add_relation(self, relation, obj_res):
        if not self.has_relation(relation, obj_res):
            self._relations.append((relation, obj_res))
            obj_res._inv_relations.append((relation, self))
