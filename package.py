# coding: utf-8
name = "lumaNukeGizmos"
version = "0.0.3"
requires = [
    "nuke",
]
# note : this version has been created due to viewer causing problem in aces configuration OC_PLTG in Luma merge

def commands():
    env.NUKE_PATH.append("{root}")  # noqa
    env.NUKE_GIZMO_PATH.append("{root}/Gizmos")  # noqa
