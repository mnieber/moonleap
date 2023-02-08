from moonleap import append_uniq
from titan.react_view_pkg.stateprovider.get_container_data import (
    delete_items_data,
    order_items_data,
    save_item_data,
)


def get_helpers(_):
    class Helpers:
        states = _.state_provider.states
        widget_spec = _.state_provider.widget_spec
        mutations = []

        def __init__(self):
            self.mutations = self._get_mutations()
            self.type_specs_to_import = self._type_specs_to_import()

        def delete_items_data(self, container):
            return delete_items_data(container)

        def order_items_data(self, container):
            return order_items_data(container)

        def save_item_data(self, container):
            return save_item_data(container)

        def _get_mutations(self):
            mutations = self.widget_spec.mutations
            for state in self.states:
                for container in state.containers:
                    if delete_items_mutation := container.delete_items_mutation:
                        append_uniq(mutations, delete_items_mutation)
                    if delete_item_mutation := container.delete_item_mutation:
                        append_uniq(mutations, delete_item_mutation)
                    if save_item_mutation := container.save_item_mutation:
                        append_uniq(mutations, save_item_mutation)
                    if order_items_mutation := container.order_items_mutation:
                        append_uniq(mutations, order_items_mutation)
            return mutations

        def _type_specs_to_import(self):
            types = []
            for mutation in self.mutations:
                for field in mutation.api_spec.get_inputs(
                    ["fk", "relatedSet", "uuid", "uuid[]"]
                ):
                    append_uniq(types, field.target_type_spec)
            return types

    return Helpers()
