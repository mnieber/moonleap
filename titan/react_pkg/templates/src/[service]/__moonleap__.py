from moonleap import append_uniq, u0
from titan.react_pkg.behavior.resources import is_exposed_bvr


def get_helpers(_):
    class Helpers:
        provided_states = list()
        bvrs = list()
        skandha_bvrs = list()
        item_names = list()
        provided_data = dict()

        def __init__(self):
            for module in _.react_app.modules:
                for component in module.components:
                    if component.meta.term.tag == "state~provider":
                        state = component.state
                        self._add_state(state)

        def _add_state(self, state):
            self.provided_states.append(state)
            for container in state.containers:
                bvrs = [x for x in container.bvrs if is_exposed_bvr(x)]
                if container.item_name:
                    append_uniq(self.item_names, container.item_name)

                if container.item_name or bvrs:
                    data = self.provided_data.setdefault(container.name, {})
                    data["item_list"] = container.item_list
                    data["item"] = (
                        container.item_list.item
                        if container.highlight_bvr
                        else container.item
                    )
                    data["bvrs"] = data.setdefault("bvrs", [])
                    for bvr in bvrs:
                        if not [x for x in data["bvrs"] if x.name == bvr.name]:
                            data["bvrs"].append(bvr)

                for bvr in bvrs:
                    append_uniq(self.bvrs, bvr)
                    if bvr.is_skandha:
                        append_uniq(self.skandha_bvrs, bvr)

        def section_names(self):
            result = ["dpsStates"]
            for key in self.provided_data.keys():
                result.append(f"dps{ u0(key) }")
            return sorted(result)

    return Helpers()


def get_contexts(_):
    return [
        dict(service=service, react_app=service.react_app)
        for service in _.project.services
        if service.has_react_app
    ]


def get_meta_data_by_fn(_, __):
    return {
        ".": {
            "name": f"../{_.service.name}",
        }
    }
