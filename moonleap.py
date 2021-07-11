import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import ramda as R
from plumbum import local

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
from moonleap.report.create_expected_dir import create_expected_dir
from moonleap.session import Session
from moonleap.settings import get_settings, load_settings

moonleap_dodo.install_all()
moonleap_project.install_all()
moonleap_project_and_dodo.install_all()
moonleap_tools.install_all()
moonleap_react.install_all()
moonleap_react_module.install_all()
moonleap_react_view.install_all()
moonleap_react_state.install_all()
moonleap_django.install_all()


def gen(spec_file, session):
    with open(spec_file) as ifs:
        raw_markdown = ifs.read()

    blocks = get_blocks(raw_markdown)

    create_resources(blocks, session)
    render_resources(blocks, session)
    report_resources(blocks, session)


def diff(spec_file):
    expected_dir = "./expected"
    create_expected_dir(expected_dir)
    diff_tool = R.path_or("diff", ["bin", "diff_tool"])(get_settings())
    if diff_tool == "meld":
        local["meld"]("./output", expected_dir)


def report(x):
    print(x)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("action", choices=["gen", "diff"])
    args = parser.parse_args()

    if not os.path.exists(args.spec):
        report("Genspec file not found: " + args.spec)
        sys.exit(1)

    session = Session(
        load_settings(Path(args.spec).with_suffix(".yml")),
        output_root_dir="output",
    )

    if args.action == "gen":
        gen(args.spec, session)

    if args.action == "diff":
        diff(args.spec)
