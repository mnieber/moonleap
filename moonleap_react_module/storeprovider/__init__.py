from dataclasses import dataclass

import moonleap.resource.props as P
from moonleap import MemFun, StoreOutputPaths, extend, render_templates, rule
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react_module.appmodule import AppModule


@dataclass
class StoreProvider(Component):
    pass


@rule("app:module")
def app_module_created(app_module):
    store_provider = StoreProvider(name="StoreProvider", import_path="src/app")
    store_provider.output_path = app_module.output_path
    app_module.store_provider = store_provider
    app_module.service.add_tool(store_provider)


@extend(AppModule)
class ExtendAppModule:
    store_provider = P.child(has, "store-provider")


@extend(StoreProvider)
class ExtendStoreProvider(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    app_module = P.parent(AppModule, has, "store-provider")
