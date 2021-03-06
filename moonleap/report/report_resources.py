import os
from pathlib import Path

import markdown
from moonleap.parser.term import term_to_word, verb_to_word
from moonleap.render.template_renderer import _render
from moonleap.resource.rel import fuzzy_match
from moonleap.session import get_session


def _fn(resource, report_dir):
    id = resource.id
    report_basename = id + ".html"
    return os.path.join(report_dir, report_basename)


def _get_relations(res, is_inv):
    return [
        (rel, other_res)
        for rel, other_res in res._relations
        if rel.is_inv == is_inv
        # below we check if the rel is not in the private rels of the parent
        and (
            # first case (not is_inv): res is the parent and other_res is the child
            (not is_inv and not _match_rel_to_rels(rel, res.doc_meta.private_rels))
            # second case (is_inv): the opposite
            or (
                is_inv
                and not _match_rel_to_rels(rel.inv(), other_res.doc_meta.private_rels)
            )
        )
    ]


def _match_rel_to_rels(rel, other_rels):
    for other_rel in other_rels:
        if fuzzy_match(rel, other_rel):
            return True
    return False


def report_resources(blocks, session):
    get_session().report("Creating report...")

    report_dir = ".moonleap/report"
    index_fn = os.path.abspath(os.path.join(report_dir, "index.html"))

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    for block in blocks:
        resource_by_term = [x for x in block.get_resource_by_term() if x[2]]
        for term, resource, is_owner in resource_by_term:
            if hasattr(resource.__class__, "doc_meta"):
                resource.doc_meta.add(resource.__class__.doc_meta)
            report_fn = _fn(resource, report_dir)
            with open(report_fn, "w") as ofs:
                ofs.write(create_report(resource, term, session.settings, index_fn))

    with open(index_fn, "w") as ofs:
        ofs.write(create_index(blocks, session.unmatched_rels, session.settings))


def create_report(resource, term, settings, index_fn):
    default_template_fn = Path(__file__).parent / "templates" / "resource.md.j2"
    props = {
        prop_name: getattr(resource, prop_name) for prop_name in resource.doc_meta.props
    }
    child_relations = [
        (rel, res) for (rel, res) in _get_relations(resource, is_inv=False) if rel.subj
    ]
    parent_relations = [
        (rel, res) for (rel, res) in _get_relations(resource, is_inv=True) if rel.subj
    ]
    body = _render(
        default_template_fn,
        resource,
        term=term,
        settings=settings,
        props=props,
        child_relations=child_relations,
        parent_relations=parent_relations,
        index_fn=index_fn,
    )
    return (
        "<html><body>"
        + f"""{markdown.markdown(body, extensions=['tables'])}"""
        + "</body></html>"
    )


def create_index(blocks, unmatched_rels, settings):
    def to_rel_str(rel):
        subj = term_to_word(rel.subj)
        obj = term_to_word(rel.obj)
        return f"{subj} {verb_to_word(rel.verb)} {obj}"

    template_fn = Path(__file__).parent / "templates" / "index.md.j2"

    resource_by_term = []
    root_block = blocks[0]
    for block in root_block.get_blocks(include_children=True):
        resource_by_term += block.get_resource_by_term()

    unmatched_rel_strs = [
        to_rel_str(rel) for rel in unmatched_rels if rel.subj and rel.obj
    ]
    body = _render(
        template_fn,
        None,
        settings=settings,
        resource_by_term=[x for x in resource_by_term if x[0]],
        unmatched_rel_strs=unmatched_rel_strs,
    )
    return (
        "<html><body>"
        + f"""{markdown.markdown(body, extensions=['tables'])}"""
        + "</body></html>"
    )
