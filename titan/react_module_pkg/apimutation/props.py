import os
from pathlib import Path

import ramda as R
from moonleap import render_templates
from titan.api_pkg.pkg.graphql_args import graphql_args
from titan.api_pkg.typeregistry import TypeRegistry
from titan.react_module_pkg.apiquery.graphql_body import graphql_body
from titan.react_module_pkg.apiquery.props import define_schema_field
from titan.react_pkg.pkg.field_spec_to_ts_type import field_spec_to_ts_type
from titan.react_pkg.pkg.ts_var import ts_form_type, ts_type_import_path


def get_context(mutation, api_module):
    _ = lambda: None
    _.api_module = api_module
    _.type_reg = TypeRegistry(api_module.graphql_api)
    _.mutation = mutation
    _.input_field_specs = mutation.inputs_type_spec.field_specs
    _.form_input_field_specs = [
        x for x in _.input_field_specs if x.field_type == "form"
    ]
    _.output_schema_name = mutation.name + "Outputs"
    _.fk_output_field_specs = mutation.outputs_type_spec.get_field_specs(
        ["relatedSet", "fk"]
    )

    class Sections:
        def schema_imports(self):
            result = []
            for field_spec in _.fk_output_field_specs:
                fk_item_name = field_spec.target
                result.append(f"import {{ {fk_item_name} }} from 'src/api/schema';")

            return os.linesep.join(result)

        def ts_type_imports(self):
            result = []
            for field_spec in _.form_input_field_specs:
                item_name = field_spec.target
                item = _.type_reg.get_item_by_name(item_name)
                result.append(
                    f"import {{ {ts_form_type(item)} }} from '{ts_type_import_path(item)}';"
                )
            return os.linesep.join(result)

        def mutation_output_schema_fields(self):
            result = []
            for field_spec in _.fk_output_field_specs:
                result.append(define_schema_field(field_spec, _.output_schema_name))
            return ("," + os.linesep).join(result)

        def ts_mutation_args(self):
            return ", ".join(
                R.map(
                    lambda field_spec: f"{field_spec.name}: "
                    + f"{field_spec_to_ts_type(field_spec, fk_as_str=False)}",
                    _.input_field_specs,
                )
            )

        def ts_mutation_graphql_args(self, before):
            return graphql_args(_.input_field_specs, before)

        def ts_mutation_graphql_body(self):
            return graphql_body(_.mutation.outputs_type_spec, recurse=False)

        def ts_mutation_graphql_variables(self):
            tab = " " * 6
            return tab + ("," + os.linesep + tab).join(
                [field_spec.name for field_spec in _.input_field_specs]
            )

    return dict(sections=Sections(), _=_)


def render_mutation_endpoint(api_module, mutation, write_file, render_template):
    template_path = Path(__file__).parent / "templates"
    render_templates(template_path, get_context=lambda x: get_context(x, api_module))(
        mutation, write_file, render_template, output_path=api_module.merged_output_path
    )