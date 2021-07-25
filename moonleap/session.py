from pathlib import Path

from moonleap.context_manager import ContextManager
from moonleap.settings import load_settings

_session = None


class Session:
    def __init__(self, spec_dir, settings_fn, output_root_dir):
        self.spec_dir = spec_dir
        self.settings_fn = settings_fn
        self.settings = None
        self.context_manager = ContextManager()
        self.output_root_dir = output_root_dir
        self.expected_dir = ".moonleap/expected"

    def load_settings(self):
        settings_fn = Path(self.spec_dir) / self.settings_fn
        if not settings_fn.exists():
            raise Exception(f"Settings file not found: {settings_fn}")
        self.settings = load_settings(settings_fn)
        self.settings["spec_dir"] = self.spec_dir
        self.context_manager.import_packages(
            self.settings.get("packages_by_context_name", {})
        )

    def report(self, x):
        print(x)

    def get_tweaks(self):
        if not self.settings:
            raise Exception("No settings loaded")
        return self.settings.get("tweaks", {})


def set_session(session):
    global _session

    if _session:
        raise Exception("There already is a session")
    _session = session


def get_session():
    if not _session:
        raise Exception("There is no session")
    return _session
