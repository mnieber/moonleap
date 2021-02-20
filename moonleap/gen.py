import os
import sys

import moonleap_dodo
import moonleap_project
import moonleap_react
import moonleap_react_module
import moonleap_react_view
import moonleap_tools

from moonleap import create_resources, get_blocks, render_resources

moonleap_dodo.install_all()
moonleap_project.install_all()
moonleap_tools.install_all()
moonleap_react.install_all()
moonleap_react_module.install_all()
moonleap_react_view.install_all()


def main(gen_file):
    with open(gen_file) as ifs:
        raw_markdown = ifs.read()

    blocks = get_blocks(raw_markdown)
    create_resources(blocks)

    render_resources(blocks, output_root_dir="output")


def report(x):
    print(x)


if __name__ == "__main__":
    gen_file = "genspec.md"
    if not os.path.exists(gen_file):
        report("Genspec file not found: " + gen_file)
        sys.exit(1)

    main(gen_file)
