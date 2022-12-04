from titan.react_view_pkg.pkg.builder import Builder


class ComponentBuilder(Builder):
    def build(self):
        attrs = []
        component = self.widget_spec.component
        for pipeline in component.pipelines:
            if pipeline.root_props:
                named_input = pipeline.elements[0].obj
                required_prop_name = named_input.name or named_input.typ.ts_var
                # The required prop must be supplied by some parent component
                data_path = self.parent_builder.get_data_path(named_input)
                attrs += [f"{required_prop_name}={{{data_path}}}"]

        attrs_str = " ".join(attrs)
        key = self.widget_spec.div_key
        key_attr = f"key={{{key}}}" if key else ""
        self.add_lines([f"<{self.output.widget_class_name} {key_attr} {attrs_str}/>"])
