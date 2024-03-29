import typing as T
from collections import defaultdict
from dataclasses import dataclass, field

from moonleap import Resource, u0
from moonleap.spec_parser.get_meta import get_meta
from moonleap.utils.case import l0
from titan.typespec.type_spec import TypeSpec


@dataclass
class Item(Resource):
    item_name: str
    item_list: "ItemList" = field(repr=False)
    type_spec: TypeSpec = field(repr=False)


@dataclass
class ItemList(Resource):
    item_name: str
    item: Item = field(repr=False)
    type_spec: "TypeSpec" = field(repr=False)


@dataclass
class TypeRegistry(Resource):
    def __post_init__(self):
        self._type_spec_by_type_name: T.Dict[str, "TypeSpec"] = {}
        self.parents_by_type_name = defaultdict(list)
        self._item_by_item_name = dict()
        self._item_list_by_item_name = dict()

    def setdefault(self, type_name, default_value):
        assert type_name and type_name[0] == type_name[0].upper()

        if self.has(type_name):
            return self.get(type_name)

        self._type_spec_by_type_name[type_name] = default_value
        return default_value

    def has(self, type_name):
        assert type_name and type_name[0] == type_name[0].upper()

        return type_name in self._type_spec_by_type_name

    def get(self, type_name, default=None) -> TypeSpec:
        assert type_name and type_name[0] == type_name[0].upper()

        type_spec = self._type_spec_by_type_name.get(type_name, None)
        if type_spec is not None:
            return type_spec

        return default

    def get_item(self, item_name):
        if item_name not in self._item_by_item_name:
            self._create_item_and_item_list(item_name)
        return self._item_by_item_name[item_name]

    def get_item_list(self, item_name):
        if item_name not in self._item_list_by_item_name:
            self._create_item_and_item_list(item_name)
        return self._item_list_by_item_name[item_name]

    def _create_item_and_item_list(self, item_name):
        type_spec = self.get(u0(item_name), default=None)
        if not type_spec:
            raise Exception(f"Cannot create item. Unknown type-spec {u0(item_name)}")
        item = Item(item_name=item_name, type_spec=type_spec, item_list=None)  # type: ignore
        item.meta = get_meta(f"{item_name}:item")
        item_list = ItemList(item_name=item_name, type_spec=type_spec, item=item)
        item_list.meta = get_meta(f"{item_name}:item~list")
        item.item_list = item_list
        self._item_list_by_item_name[item_name] = item_list
        self._item_by_item_name[item_name] = item

    def type_specs(self) -> T.List[TypeSpec]:
        return list(self._type_spec_by_type_name.values())

    @property
    def items(self) -> T.List[Item]:
        return [
            self.get_item(l0(type_spec.type_name))
            for type_spec in self.type_specs()
            if not type_spec.is_form
        ]

    def register_parent_child(self, parent_type_name, child_type_name):
        self.parents_by_type_name[child_type_name].append(parent_type_name)

    @property
    def type_names(self):
        return self._type_spec_by_type_name.keys()
