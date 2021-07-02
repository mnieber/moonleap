import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import moonleap_django
import moonleap_dodo
import moonleap_project
import moonleap_project_and_dodo
import moonleap_react
import moonleap_react_module
import moonleap_react_state
import moonleap_react_view
import moonleap_tools
from moonleap import create_resources, get_blocks, render_resources, report_resources
from moonleap.render.settings import load_settings
from moonleap.session import Session

moonleap_dodo.install_all()
moonleap_project.install_all()
moonleap_project_and_dodo.install_all()
moonleap_tools.install_all()
moonleap_react.install_all()
moonleap_react_module.install_all()
moonleap_react_view.install_all()
moonleap_react_state.install_all()
moonleap_django.install_all()


def main(gen_file):
    session = Session(
        load_settings(Path(gen_file).with_suffix(".yml")), output_root_dir="output"
    )

    with open(gen_file) as ifs:
        raw_markdown = ifs.read()

    blocks = get_blocks(raw_markdown)

    create_resources(blocks, session)
    render_resources(blocks, session)
    report_resources(blocks, session)


def report(x):
    print(x)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("spec_file")
    args = parser.parse_args()

    if not os.path.exists(args.spec_file):
        report("Genspec file not found: " + args.spec_file)
        sys.exit(1)

    main(args.spec_file)
