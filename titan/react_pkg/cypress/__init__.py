import moonleap.resource.props as P
from moonleap import extend, rule, tags
from moonleap.verbs import has
from titan.project_pkg.service import Tool
from titan.react_pkg.reactapp import ReactApp


class Cypress(Tool):
    pass


@tags(["cypress"])
def create_cypress(term, block):
    cypress = Cypress(name="cypress")
    return cypress


@rule("react-app", has, "cypress")
def react_app_uses_cypress(react_app, cypress):
    react_app.utils_module.add_template_dir(__file__, "templates_utils")
    react_app.utils_module.use_packages(["cookies"])


@extend(Cypress)
class ExtendCypress:
    pass


@extend(ReactApp)
class ExtendReactApp:
    cypress = P.child(has, "cypress")