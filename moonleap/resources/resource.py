import typing as T
from dataclasses import dataclass, field

from jdoc.moonleap.block import Block
from moonleap.resources.rel_selector import RelSelector
from moonleap.spec.term import Term
from moonleap.utils.case import kebab_to_camel
from moonleap.utils.get_id import get_id


@dataclass
class ResourceMetaData:
    term: Term
    block: Block
    base_tags: T.List[str]


@dataclass
class Resource:
    id: str = field(default_factory=get_id, init=False, repr=False)
    _relations: T.List[T.Tuple["Rel", "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )
    _inv_relations: T.List[T.Tuple["Rel", "Resource"]] = field(
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

    @property
    def kebab_data(self):
        return self.meta.term.data

    @property
    def camel_data(self):
        return kebab_to_camel(self.meta.term.data)
