import os

from moonleap import load_yaml
from titan.types_pkg.typeregistry import get_type_reg
from typespec.get_api_spec import get_api_spec


def load_api_specs(api_reg, spec_dir):
    fn = os.path.join(spec_dir, "api.yaml")
    if os.path.exists(fn):
        get_all_api_specs(api_reg, "client", load_yaml(fn))


def get_all_api_specs(api_reg, host, root_api_spec_dict):
    for key, api_spec_dict in root_api_spec_dict.items():
        get_api_spec(api_reg, host, key, api_spec_dict, get_type_reg().type_names)