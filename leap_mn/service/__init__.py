import moonleap.props as props
from leap_mn.pipdependency import PipDependency, PipDependencyDev
from leap_mn.pkgdependency import PkgDependency, PkgDependencyDev, list_of_packages
from leap_mn.srcdir import SrcDir
from moonleap import Resource, output_path_from, tags


class Service(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["service"])
def create_service(term, block):
    return [Service(term.data)]


def meta():
    from leap_mn.project import Project

    return {
        Service: dict(
            output_dir=lambda x: str(output_path_from("project")(x) / x.name),
            props={
                "pip_dependencies": list_of_packages(PipDependency),
                "pip_dependencies_dev": list_of_packages(PipDependencyDev),
                "pkg_dependencies": list_of_packages(PkgDependency),
                "pkg_dependencies_dev": list_of_packages(PkgDependencyDev),
                "src_dir": props.child_of_type(SrcDir),
                "project": props.parent_of_type(Project),
            },
        )
    }
