import ramda as R
from moonleap import get_session
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_view_pkg.router import RouterConfig
from titan.react_view_pkg.router.resources import reduce_router_configs


def _wraps(panel):
    return panel and panel.wraps_children


def _get_route_params(self):
    return R.path_or(
        [],
        [
            "services",
            self.module.react_app.service.name,
            "react_app",
            "components",
            self.name,
            "route_params",
        ],
    )(get_session().get_tweaks())


def create_router_configs(self):
    base_url = get_component_base_url(self, "")
    url = "/".join(
        ([base_url] if base_url else [])
        + [":" + x for x in _get_route_params(self) if x is not None]
    )
    router_config = RouterConfig(
        component=self,
        url=url,
        wraps=_wraps(self.top_panel)
        or _wraps(self.middle_panel)
        or _wraps(self.bottom_panel)
        or _wraps(self.left_panel)
        or _wraps(self.right_panel),
    )
    result = reduce_router_configs([router_config])
    return result