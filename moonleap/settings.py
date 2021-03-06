import os
from pathlib import Path

import ramda as R

from moonleap.utils import yaml2dict
from moonleap.utils.merge_into_config import merge_into_config

_settings = None


def load_settings(fn):
    global _settings

    if _settings is None:
        _settings = {}

        global_settings_fn = ".moonleap.config.yml"
        if os.path.exists(global_settings_fn):
            with open(global_settings_fn) as ifs:
                merge_into_config(_settings, yaml2dict(ifs.read()))

        if not os.path.exists(fn):
            raise Exception(f"Settings file not found: {fn}")
        with open(fn) as ifs:
            merge_into_config(_settings, yaml2dict(ifs.read()))

        override_fn = Path(fn).with_suffix(".override.yml")
        if os.path.exists(override_fn):
            with open(override_fn) as ifs:
                merge_into_config(_settings, yaml2dict(ifs.read()))

        _settings["references"] = R.pipe(
            R.always(_settings.setdefault("references", {})),
            R.to_pairs,
            R.map(lambda x: (x[0], x[1][:-1] if x[1].endswith("/") else x[1])),
            R.from_pairs,
        )(None)

    return _settings


def get_settings():
    global _settings

    if _settings is None:
        raise Exception("No settings file has been loaded")

    return _settings


def get_tweaks():
    return get_settings().get("tweaks", {})
