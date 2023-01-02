from pathlib import Path

from moonleap.blocks.builder.build_blocks import build_blocks
from moonleap.blocks.parser.expand_markdown import expand_markdown
from moonleap.blocks.parser.get_blocks import get_blocks
from moonleap.post_process import post_process_output_files
from moonleap.render.render_mixin import get_root_resource, render_resource
from moonleap.report.report_resources import report_resources
from moonleap.session import trace


def generate_code(session, file_writer, post_process_all_files):
    expanded_markdown = expand_markdown(
        session.spec_fn, output_fn=Path(".moonleap") / "spec.md"
    )

    trace("Parsing...")
    blocks = get_blocks(expanded_markdown)
    build_blocks(blocks)

    try:
        trace("Rendering...")
        trace("Rendering root resource", 1)
        root_resource = get_root_resource()
        render_resource(
            root_resource,
            write_file=file_writer.write_file,
            output_path="",
            context=dict(has_flag=root_resource.has_flag),
        )

        file_writer.write_merged_files()
        for warning in file_writer.warnings:
            trace(warning)
    finally:
        file_writer.write_snapshot()

        trace("Post processing...")
        post_process_output_files(
            file_writer.all_output_filenames
            if post_process_all_files
            else file_writer.output_filenames,
            session.get_post_process_settings(),
            session.get_bin_settings(),
        )

    trace("Creating report...")
    report_resources(blocks)
