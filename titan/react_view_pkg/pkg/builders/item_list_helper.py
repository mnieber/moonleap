from moonleap import kebab_to_camel
from moonleap.blocks.term.__init__ import word_to_term


class ItemListHelper:
    def __init__(self, widget_spec):
        self.widget_spec = widget_spec
        self._working_item_name = None

    @property
    def working_item_name(self):
        if not self._working_item_name:
            self._get_data()

        return self._working_item_name

    def _get_data(self):
        if pipeline_data := self.widget_spec.get_pipeline_data("items", recurse=True):
            if term := word_to_term(pipeline_data[-1]):
                self._working_item_name = kebab_to_camel(term.data)

    def item_list_data_path(self):
        if pipeline := self.widget_spec.get_pipeline_by_name("items", recurse=True):
            named_item_list = pipeline.resources[-1]
            return pipeline.data_path(obj=named_item_list)
        return None

    def maybe_add_item_pipeline_to_spec_extension(self, source_term_str, extension):
        pipelines = extension.setdefault("__pipelines__", {})

        if not self.widget_spec.get_pipeline_by_name("item", recurse=True):
            item_name = self.working_item_name
            if not item_name:
                if named_prop := self._get_named_prop():
                    item_name = named_prop.typ.item.item_name

            if not item_name:
                return False

            pipelines["item"] = [source_term_str, f"{item_name}+{item_name}:item"]

        return True

    def maybe_add_items_pipeline_to_spec_extension(self, extension):
        pipelines = extension.setdefault("__pipelines__", {})
        if not self.widget_spec.get_pipeline_by_name("items", recurse=True):
            if named_prop := self._get_named_prop():
                pipelines["items"] = ["component:props", str(named_prop.meta.term)]
            else:
                return False
        return True

    def _get_named_prop(self):
        named_props = self.widget_spec.root.get_named_props(
            lambda x: x.meta.term.tag == "item~list"
        )
        if len(named_props) != 1:
            return None
        return named_props[0]
