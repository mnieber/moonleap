from moonleap.utils.case import sn


def get_helpers(_):
    class Helpers:
        def get_data(self):
            result = []
            for django_model in _.module.django_models:
                item_list = django_model.item_list
                type_spec = django_model.type_spec
                data = dict(
                    type_spec=type_spec,
                    create_inline_model=self.get_create_inline_model(type_spec),
                    inline_model_fields=self.get_inline_model_fields(type_spec),
                    excluded_model_fields=self.get_excluded_model_fields(type_spec),
                    has_sortable_inlines=bool(self.get_sortable_inlines(type_spec)),
                    autocomplete_fields=self.get_autocomplete_fields(type_spec),
                    search_by=type_spec.admin_search_by,
                )
                result.append((item_list, data))
            return result

        def get_create_inline_model(self, type_spec):
            return bool(
                [
                    x
                    for x in type_spec.get_field_specs(["fk"])
                    if x.is_reverse_of_related_set
                    and x.is_reverse_of_related_set.admin_inline
                ]
            )

        def get_inline_model_fields(self, type_spec):
            return [
                x for x in type_spec.get_field_specs(["relatedSet"]) if x.admin_inline
            ]

        def get_excluded_model_fields(self, type_spec):
            return [x for x in type_spec.get_field_specs() if not x.admin]

        def get_autocomplete_fields(self, type_spec):
            return [
                sn(x.name)
                for x in type_spec.get_field_specs(["relatedSet"])
                if (not x.through or x.through == "+")
                and x.target_type_spec.admin_search_by
            ]

        def get_sortable_inlines(self, type_spec):
            return [
                x
                for x in self.get_inline_model_fields(type_spec)
                if x.target_type_spec.is_sorted
            ]

    return Helpers()