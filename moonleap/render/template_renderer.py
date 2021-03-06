import os
from pathlib import Path

from jinja2 import Template
from moonleap.render.merge import get_file_merger
from moonleap.render.template_env import template_env
from moonleap.render.transforms import post_transforms


class TemplateRenderer:
    def __init__(self):
        self.filenames = []

    def render(self, resource, settings, template_fn, fn):
        content = (
            _render(template_fn, resource, settings=settings)
            if template_fn.suffix == ".j2"
            else _get_file_content(template_fn)
        )

        if fn in self.filenames:
            content, warnings = _merge(fn, content)
            for w in warnings:
                print(w)
        else:
            self.filenames.append(fn)

        with open(fn, "w") as ofs:
            ofs.write(content)

        return fn


def _render(template_fn, resource, **kwargs):
    template = template_env.get_template(str(template_fn))
    content = template.render(res=resource, **kwargs)

    lines = content.split(os.linesep)
    for post_transform in post_transforms:
        lines = post_transform(lines)
    content = os.linesep.join(lines)
    return content


def _get_file_content(template_fn):
    with open(template_fn) as ifs:
        content = ifs.read()
    return content


def _merge(fn, content):
    warnings = []

    file_merger = get_file_merger(fn)
    if file_merger:
        with open(fn) as ifs:
            lhs_content = ifs.read()
            content = file_merger.merge(lhs_content, content)
    else:
        warnings.append(f"Warning: writing twice to {fn}")

    return content, warnings


def _resolve_output_fn(templates_path, resource, template_fn):
    if str(template_fn) == ".":
        return template_fn

    meta_filename = str(templates_path / template_fn) + ".fn"
    name = (
        (
            template_env.get_template(meta_filename)
            .render(res=resource)
            .split(os.linesep)[0]
        )
        if Path(meta_filename).exists()
        else Template(template_fn.name).render(res=resource)
    )

    if name.endswith(".j2"):
        name = name[:-3]

    return _resolve_output_fn(templates_path, resource, template_fn.parent) / name


def _get_output_fn(output_root_dir, output_subdir, template_fn):
    return (Path(output_root_dir) / output_subdir / template_fn).resolve()


def render_templates(root_filename, location="templates"):
    def render(resource, settings, output_root_dir, template_renderer):
        location_path = Path(root_filename).parent / (
            location(resource) if callable(location) else location
        )
        if location_path.is_dir():
            templates_path = location_path
            template_paths = templates_path.glob("**/*")
        else:
            templates_path = location_path.parent
            template_paths = [location_path]

        output_filenames = []
        for template_fn in template_paths:
            if template_fn.suffix == ".fn":
                continue
            if not template_fn.is_dir():
                output_fn = _get_output_fn(
                    output_root_dir,
                    resource.merged_output_path,
                    _resolve_output_fn(
                        templates_path,
                        resource,
                        template_fn.relative_to(templates_path),
                    ),
                )

                output_fn.parent.mkdir(parents=True, exist_ok=True)
                output_filenames.append(
                    template_renderer.render(resource, settings, template_fn, output_fn)
                )
        return output_filenames

    return render
