from pathlib import Path

import ramda as R
from plumbum import local


def _diff_tool_name_and_exe(settings):
    diff_tool_name = settings.get("diff_tool", "diff")
    return diff_tool_name, R.path_or(diff_tool_name, ["bin", diff_tool_name, "exe"])(
        settings
    )


def _diff(session, from_dir, to_dir, sudo=False):
    diff_tool_name, diff_tool_exe = _diff_tool_name_and_exe(session.settings)
    if diff_tool_name == "meld":
        args = [diff_tool_exe, from_dir, to_dir]
    else:
        session.report(f"Unknown diff tool: {diff_tool_name}")
        return

    if sudo:
        args.insert(0, "sudo")
    local[args[0]](*args[1:])


def diff(session, sudo=False):
    _diff(session, ".moonleap/output", session.expected_dir, sudo)


def _same_file(stat_lhs, stat_rhs):
    return (
        stat_lhs.st_mtime == stat_rhs.st_mtime and stat_lhs.st_size == stat_rhs.st_size
    )


def create_symlinks(session):
    ref_dir = Path(session.expected_dir)

    for fn in Path(".moonleap/output").rglob("*"):
        if not fn.is_dir() and not fn.is_symlink():
            ref_fn = (ref_dir / fn.relative_to(".moonleap/output")).absolute()
            if ref_fn.exists() and _same_file(fn.stat(), ref_fn.stat()):
                fn.unlink()
                fn.symlink_to(ref_fn)
