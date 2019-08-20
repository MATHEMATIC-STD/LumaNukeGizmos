# coding: utf-8
name = "lumaNukeGizmos"
version = "0.0.0"
requires = [
    "nuke",
]


def commands():
    env.NUKE_PATH.append("{root}")  # noqa
    env.NUKE_GIZMO_PATH.append("{root}/Gizmos")  # noqa
