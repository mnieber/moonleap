import typing as T
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering

from moonleap.parser.term import word_to_term
from moonleap.resource.rel import Rel
from moonleap.verbs import is_created_as


class Priorities(Enum):
    DEFAULT = 1
    TWEAK = 100


@total_ordering
@dataclass
class Rule:
    rel: Rel
    f: T.Callable
    priority: int = 1
    fltr_subj: T.Optional[T.Callable] = None
    fltr_obj: T.Optional[T.Callable] = None

    def __lt__(self, other):
        return self.priority > other.priority


def rule(
    subj_term, verb=None, obj_term=None, fltr_subj=None, fltr_obj=None, priority=1
):
    if verb is None or obj_term is None:
        if verb is not None or obj_term is not None:
            raise Exception("Either define both verb and obj_term or neither")
        verb = is_created_as
        obj_term = subj_term

    def wrapped(f):
        rel = Rel(
            subj=word_to_term(subj_term, default_to_tag=True),
            verb=verb,
            obj=word_to_term(obj_term, default_to_tag=True),
        )
        f.moonleap_rule = Rule(
            rel, f, fltr_subj=fltr_subj, fltr_obj=fltr_obj, priority=priority
        )
        return f

    return wrapped


def tags(tags):
    def wrapped(f):
        f.moonleap_create_rule_by_tag = {}
        for tag in tags:
            f.moonleap_create_rule_by_tag[tag] = f

        return f

    return wrapped


_add_function_by_resource_type = {}


def add(resource, child_resource):
    f = _add_function_by_resource_type.get(child_resource.__class__)
    if not f:
        raise Exception(f"No add rule is registered for {child_resource.__class__}")
    f(resource, child_resource)


def register_add(resource_type):
    def wrapped(f):
        _add_function_by_resource_type[resource_type] = f
        return f

    return wrapped


def extend(resource_type):
    def wrapped(props):
        setattr(props, "moonleap_extends_resource_type", resource_type)
        return props

    return wrapped
