from dataclasses import dataclass

from moonleap import RenderMixin, Resource, get_session


@dataclass
class Project(RenderMixin, Resource):
    name: str
    kebab_name: str

    @property
    def opt_dir_fn(self):
        return get_session().get_tweak_or(
            "/opt/" + self.kebab_name, ["project", "opt_dir_fn"]
        )
