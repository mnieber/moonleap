import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule, tags
from moonleap.verbs import has, with_
from moonleap_tools.pipdependency import PipRequirement

from . import layer_configs, opt_paths
from .resources import Pytest, PytestHtml


@tags(["pytest"])
def create_pytest(term, block):
    pytest = Pytest(name="pytest")

    add(pytest, PipRequirement(["pytest"], is_dev=True))
    add(pytest, layer_configs.get_pytest_options(pytest))

    return pytest


@tags(["pytest-html"])
def create_pytest_html(term, block):
    pytest_html = PytestHtml(name="pytest-html")

    add(pytest_html, PipRequirement(["pytest-html"], is_dev=True))
    add(pytest_html, layer_configs.get_pytest_html_options(pytest_html))
    add(pytest_html, opt_paths.pytest_html_opt_path)
    add(pytest_html, opt_paths.pytest_html_asset_path)

    return pytest_html


@rule("service", has, "pytest")
def service_has_pytest_html(service, pytest):
    if pytest.pytest_html:
        return create_forward(service, has, ":tool", pytest.pytest_html)


def meta():
    from moonleap_project.service import Service

    @extend(Pytest)
    class ExtendPytest:
        pytest_html = P.child(with_, "pytest-html")
        service = P.parent(Service, has)

    return [ExtendPytest]
